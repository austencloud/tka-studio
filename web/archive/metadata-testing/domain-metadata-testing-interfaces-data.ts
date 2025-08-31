// @ts-nocheck
/**
 * Metadata Testing Interface Data Types
 *
 * Data structures used by metadata testing service interfaces.
 * These are pure data types with no business logic.
 */

// ============================================================================
// FILE DATA TYPES
// ============================================================================

export interface ThumbnailFile {
  name: string;
  path: string;
  size: number;
  lastModified: Date;
  metadata?: {
    word?: string;
    author?: string;
    difficulty?: number;
    tags?: string[];
  };
}

export interface SequenceFile {
  name: string;
  path: string;
  content: string;
  metadata: Record<string, unknown>;
  isValid: boolean;
}

// ============================================================================
// ANALYSIS DATA TYPES
// ============================================================================

export interface MetadataAnalysisResult {
  fileName: string;
  isValid: boolean;
  errors: string[];
  warnings: string[];
  extractedData: Record<string, unknown>;
  processingTime: number;
}

export interface BatchAnalysisResult {
  totalFiles: number;
  processedFiles: number;
  validFiles: number;
  invalidFiles: number;
  errors: string[];
  warnings: string[];
  results: MetadataAnalysisResult[];
  summary: {
    successRate: number;
    averageProcessingTime: number;
    commonErrors: string[];
    recommendations: string[];
  };
}

// ============================================================================
// TESTING DATA TYPES
// ============================================================================

export interface TestCase {
  id: string;
  name: string;
  description: string;
  inputData: unknown;
  expectedOutput: unknown;
  actualOutput?: unknown;
  status: "pending" | "running" | "passed" | "failed";
  duration?: number;
  error?: string;
}

export interface TestSuite {
  id: string;
  name: string;
  description: string;
  testCases: TestCase[];
  status: "pending" | "running" | "completed";
  results: {
    total: number;
    passed: number;
    failed: number;
    duration: number;
  };
}

// ============================================================================
// STATE DATA TYPES
// ============================================================================

export interface MetadataTestingState {
  isInitialized: boolean;
  isRunning: boolean;
  currentTest?: string;
  progress: number;
  results: BatchAnalysisResult | null;
  error: string | null;
  startTime?: Date;
  endTime?: Date;
}

export interface TestingConfiguration {
  maxConcurrentTests: number;
  timeoutMs: number;
  retryAttempts: number;
  outputFormat: "json" | "csv" | "html";
  includeWarnings: boolean;
}

