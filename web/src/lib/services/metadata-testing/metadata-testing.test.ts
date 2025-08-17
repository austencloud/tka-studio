/**
 * Metadata Testing Services Test Suite
 *
 * Comprehensive tests for the refactored metadata testing services.
 * Validates that the clean architecture maintains all functionality.
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  SequenceDiscoveryService,
  MetadataExtractionService,
  MetadataAnalysisService,
  BatchAnalysisService,
  MetadataTestingStateManager,
  createMetadataTestingStateManager,
  defaultMetadataTestingConfig,
} from "./index";
import type {
  ThumbnailFile,
  MetadataAnalysisResult,
} from "$lib/domain/metadata-testing/types";

// Mock data
const mockThumbnailFile: ThumbnailFile = {
  name: "ABC.png",
  path: "/path/to/ABC.png",
  word: "ABC",
};

const mockMetadata = [
  {
    beat_number: 1,
    letter: "A",
    author: "Test Author",
    level: 3,
    sequence_start_position: "front",
    blue_attributes: { motion_type: "contact" },
    red_attributes: { motion_type: "roll" },
  },
  {
    beat_number: 2,
    letter: "B",
    blue_attributes: { motion_type: "isolation" },
    red_attributes: { motion_type: "plane_bend" },
  },
];

// Mock PNG metadata extractor at the top level
vi.mock("$lib/utils/png-metadata-extractor", () => ({
  PngMetadataExtractor: {
    extractMetadata: vi.fn().mockResolvedValue([
      {
        beat_number: 1,
        letter: "A",
        author: "Test Author",
        level: 3,
        sequence_start_position: "front",
        blue_attributes: { motion_type: "contact" },
        red_attributes: { motion_type: "roll" },
      },
      {
        beat_number: 2,
        letter: "B",
        blue_attributes: { motion_type: "isolation" },
        red_attributes: { motion_type: "plane_bend" },
      },
    ]),
  },
}));

describe("SequenceDiscoveryService", () => {
  let discoveryService: SequenceDiscoveryService;

  beforeEach(() => {
    discoveryService = new SequenceDiscoveryService();
  });

  it("should create service instance", () => {
    expect(discoveryService).toBeInstanceOf(SequenceDiscoveryService);
  });

  it("should implement ISequenceDiscoveryService interface", () => {
    expect(typeof discoveryService.discoverSequences).toBe("function");
    expect(typeof discoveryService.validateSequenceFile).toBe("function");
  });

  it("should have known sequences configured", async () => {
    // This tests that the service has configuration
    const result = await discoveryService.validateSequenceFile("ABC.png");
    expect(typeof result).toBe("boolean");
  });
});

describe("MetadataExtractionService", () => {
  let extractionService: MetadataExtractionService;

  beforeEach(() => {
    extractionService = new MetadataExtractionService();
  });

  it("should create service instance", () => {
    expect(extractionService).toBeInstanceOf(MetadataExtractionService);
  });

  it("should implement IMetadataExtractionService interface", () => {
    expect(typeof extractionService.extractMetadata).toBe("function");
    expect(typeof extractionService.extractMetadataFromFile).toBe("function");
    expect(typeof extractionService.extractRawMetadata).toBe("function");
  });
});

describe("MetadataAnalysisService", () => {
  let analysisService: MetadataAnalysisService;

  beforeEach(() => {
    analysisService = new MetadataAnalysisService();
  });

  it("should create service instance", () => {
    expect(analysisService).toBeInstanceOf(MetadataAnalysisService);
  });

  it("should implement IMetadataAnalysisService interface", () => {
    expect(typeof analysisService.analyzeMetadata).toBe("function");
    expect(typeof analysisService.validateMotionTypes).toBe("function");
    expect(typeof analysisService.calculateHealthScore).toBe("function");
  });

  it("should analyze metadata and return MetadataAnalysisResult", () => {
    const result = analysisService.analyzeMetadata(mockMetadata, "ABC");

    expect(result).toHaveProperty("sequenceName", "ABC");
    expect(result).toHaveProperty("stats");
    expect(result).toHaveProperty("issues");
    expect(result.stats).toHaveProperty("healthScore");
    expect(typeof result.stats.healthScore).toBe("number");
    expect(result.stats.healthScore).toBeGreaterThanOrEqual(0);
    expect(result.stats.healthScore).toBeLessThanOrEqual(100);
  });

  it("should handle empty metadata gracefully", () => {
    const result = analysisService.analyzeMetadata([], "EMPTY");

    expect(result.sequenceName).toBe("EMPTY");
    expect(result.stats.totalBeats).toBe(0);
    expect(result.stats.healthScore).toBe(0);
  });

  it("should validate motion types correctly", () => {
    const invalidTypes = analysisService.validateMotionTypes([
      {
        beat_number: 1,
        blue_attributes: { motion_type: "invalid_motion" },
      },
    ]);

    expect(invalidTypes).toHaveLength(1);
    expect(invalidTypes[0]).toHaveProperty("beat", 1);
    expect(invalidTypes[0]).toHaveProperty("prop", "blue");
    expect(invalidTypes[0]).toHaveProperty("type", "invalid_motion");
  });

  it("should calculate health score correctly", () => {
    const mockStats = {
      totalBeats: 10,
      sequenceLength: 10,
      realBeatsCount: 10,
      startPositionCount: 1,
      hasAuthor: true,
      authorName: "Test",
      authorMissing: false,
      authorInconsistent: false,
      hasLevel: true,
      level: 3,
      levelMissing: false,
      levelInconsistent: false,
      levelZero: false,
      hasStartPosition: true,
      startPositionMissing: false,
      startPositionInconsistent: false,
      startPositionValue: "front",
      missingBeatNumbers: [],
      missingLetters: [],
      missingMotionData: [],
      invalidMotionTypes: [],
      duplicateBeats: [],
      invalidBeatStructure: [],
      missingRequiredFields: [],
      hasErrors: false,
      hasWarnings: false,
      errorCount: 0,
      warningCount: 0,
      healthScore: 0,
    };

    const score = analysisService.calculateHealthScore(mockStats);
    expect(score).toBeGreaterThan(90); // Should be high for good data
  });
});

describe("BatchAnalysisService", () => {
  let batchService: BatchAnalysisService;
  let extractionService: MetadataExtractionService;
  let analysisService: MetadataAnalysisService;

  beforeEach(() => {
    extractionService = new MetadataExtractionService();
    analysisService = new MetadataAnalysisService();
    batchService = new BatchAnalysisService(extractionService, analysisService);
  });

  it("should create service instance", () => {
    expect(batchService).toBeInstanceOf(BatchAnalysisService);
  });

  it("should track analysis state", () => {
    expect(batchService.isRunning()).toBe(false);
    expect(batchService.getCurrentAnalysisId()).toBe("");
  });

  it("should export results to CSV format", () => {
    const mockBatchResult = {
      analysisId: "test-id",
      totalSequences: 1,
      successfulAnalyses: 1,
      failedAnalyses: 0,
      results: [
        {
          sequenceName: "ABC",
          stats: {
            healthScore: 95,
            hasErrors: false,
            hasWarnings: false,
            totalBeats: 10,
            authorName: "Test Author",
            level: 3,
            startPositionValue: "front",
          },
          issues: { errors: {}, warnings: {} },
        },
      ] as MetadataAnalysisResult[],
      errors: [],
      duration: 1000,
      summary: {
        averageHealthScore: 95,
        totalErrors: 0,
        totalWarnings: 0,
        commonIssues: [],
        healthDistribution: { excellent: 1, good: 0, fair: 0, poor: 0 },
      },
      timestamp: new Date().toISOString(),
    };

    const csv = batchService.exportToCsv(mockBatchResult);
    expect(csv).toContain("Sequence Name");
    expect(csv).toContain("Health Score");
    expect(csv).toContain("ABC");
    expect(csv).toContain("95.00");
  });

  it("should export results to JSON format", () => {
    const mockBatchResult = {
      analysisId: "test-id",
      totalSequences: 1,
      successfulAnalyses: 1,
      failedAnalyses: 0,
      results: [],
      errors: [],
      duration: 1000,
      summary: {
        averageHealthScore: 0,
        totalErrors: 0,
        totalWarnings: 0,
        commonIssues: [],
        healthDistribution: { excellent: 0, good: 0, fair: 0, poor: 0 },
      },
      timestamp: new Date().toISOString(),
    };

    const json = batchService.exportToJson(mockBatchResult);
    const parsed = JSON.parse(json);
    expect(parsed).toHaveProperty("analysisId", "test-id");
    expect(parsed).toHaveProperty("totalSequences", 1);
  });
});

describe("MetadataTestingStateManager", () => {
  let stateManager: MetadataTestingStateManager;

  beforeEach(() => {
    stateManager = new MetadataTestingStateManager();
  });

  it("should create state manager instance", () => {
    expect(stateManager).toBeInstanceOf(MetadataTestingStateManager);
  });

  it("should have initial state", () => {
    const state = stateManager.state;

    expect(state.thumbnails).toEqual([]);
    expect(state.filteredThumbnails).toEqual([]);
    expect(state.selectedThumbnails).toEqual([]);
    expect(state.analysisResults).toEqual([]);
    expect(state.batchResults).toBeNull();
    expect(state.currentAnalysis).toBeNull();
    expect(state.isDiscovering).toBe(false);
    expect(state.isAnalyzing).toBe(false);
    expect(state.analysisProgress).toBe(0);
    expect(state.currentAnalysisFile).toBe("");
  });

  it("should handle thumbnail selection", () => {
    const mockThumbnail = mockThumbnailFile;

    stateManager.selectThumbnail(mockThumbnail);
    let state = stateManager.state;
    expect(state.selectedThumbnails).toContain(mockThumbnail);

    stateManager.selectThumbnail(mockThumbnail); // Deselect
    state = stateManager.state;
    expect(state.selectedThumbnails).not.toContain(mockThumbnail);
  });

  it("should handle search filtering", () => {
    stateManager.setSearchQuery("ABC");
    const state = stateManager.state;
    expect(state.searchQuery).toBe("ABC");
  });

  it("should handle filter settings", () => {
    stateManager.setErrorFilter(true);
    stateManager.setWarningFilter(true);
    stateManager.setHealthScoreFilter(50, 90);

    const state = stateManager.state;
    expect(state.showOnlyErrors).toBe(true);
    expect(state.showOnlyWarnings).toBe(true);
    expect(state.healthScoreFilter).toEqual({ min: 50, max: 90 });
  });

  it("should clear data appropriately", () => {
    stateManager.clearResults();
    let state = stateManager.state;
    expect(state.analysisResults).toEqual([]);
    expect(state.batchResults).toBeNull();

    stateManager.clearAll();
    state = stateManager.state;
    expect(state.thumbnails).toEqual([]);
    expect(state.selectedThumbnails).toEqual([]);
    expect(state.searchQuery).toBe("");
  });
});

describe("Factory Functions", () => {
  it("should create state manager via factory", () => {
    const stateManager = createMetadataTestingStateManager();
    expect(stateManager).toBeInstanceOf(MetadataTestingStateManager);
  });
});

describe("Configuration", () => {
  it("should have valid default configuration", () => {
    expect(defaultMetadataTestingConfig).toHaveProperty("validMotionTypes");
    expect(defaultMetadataTestingConfig).toHaveProperty("requiredFields");
    expect(defaultMetadataTestingConfig).toHaveProperty("healthScoreWeights");

    expect(Array.isArray(defaultMetadataTestingConfig.validMotionTypes)).toBe(
      true
    );
    expect(
      defaultMetadataTestingConfig.validMotionTypes.length
    ).toBeGreaterThan(0);

    expect(Array.isArray(defaultMetadataTestingConfig.requiredFields)).toBe(
      true
    );
    expect(defaultMetadataTestingConfig.requiredFields).toContain("letter");
    expect(defaultMetadataTestingConfig.requiredFields).toContain(
      "beat_number"
    );

    const weights = defaultMetadataTestingConfig.healthScoreWeights;
    const totalWeight =
      weights.authorWeight +
      weights.levelWeight +
      weights.startPositionWeight +
      weights.beatIntegrityWeight +
      weights.motionDataWeight;
    expect(totalWeight).toBeCloseTo(1.0, 2);
  });
});

describe("Integration Tests", () => {
  it("should work end-to-end with mocked data", () => {
    const analysisService = new MetadataAnalysisService();

    // Test the analysis pipeline
    const analysisResult = analysisService.analyzeMetadata(mockMetadata, "ABC");

    expect(analysisResult.sequenceName).toBe("ABC");
    expect(analysisResult.stats.totalBeats).toBe(1); // Only 1 real beat (the second one), first has start position
    expect(analysisResult.stats.hasAuthor).toBe(true);
    expect(analysisResult.stats.hasLevel).toBe(true);
    expect(analysisResult.stats.hasStartPosition).toBe(true);
    expect(analysisResult.stats.healthScore).toBeGreaterThan(0);
  });
});
