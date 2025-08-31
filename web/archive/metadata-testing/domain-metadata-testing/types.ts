// @ts-nocheck
/**
 * Metadata Testing Domain Types
 *
 * Domain types for metadata testing, analysis, and validation functionality.
 */

// ============================================================================
// CORE METADATA TYPES
// ============================================================================

export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
  level?: number;
  startPosition?: string;
  [key: string]: unknown;
}

export interface ThumbnailFile {
  name: string;
  path: string;
  size: number;
  lastModified: Date;
  metadata?: SequenceMetadata;
}

export interface SequenceFile {
  name: string;
  path: string;
  content: string;
  metadata: SequenceMetadata;
}

// ============================================================================
// ANALYSIS TYPES
// ============================================================================

export interface MetadataStats {
  totalBeats: number;
  sequenceLength: number;
  realBeatsCount: number;
  startPositionCount: number;
  hasAuthor: boolean;
  authorName: string | null;
  authorMissing: boolean;
  authorInconsistent: boolean;
  hasLevel: boolean;
  level: number | null;
  levelMissing: boolean;
  levelInconsistent: boolean;
  levelZero: boolean;
  hasStartPosition: boolean;
  startPositionMissing: boolean;
  startPositionInconsistent: boolean;
  startPositionValue: string | null;
  missingBeatNumbers: number[];
  missingLetters: number[];
  missingMotionData: number[];
  invalidMotionTypes: InvalidMotionType[];
  duplicateBeats: number[];
  invalidBeatStructure: number[];
  missingRequiredFields: string[];
  hasErrors: boolean;
  hasWarnings: boolean;
  errorCount: number;
  warningCount: number;
  healthScore: number;
}

export interface InvalidMotionType {
  beat: number;
  prop: string;
  type: string;
}

export interface MetadataValidationIssue {
  type: "error" | "warning";
  message: string;
  beat?: number;
  field?: string;
}

export interface MetadataAnalysisResult {
  sequenceName: string;
  stats: MetadataStats;
  issues: {
    errors: Record<string, string[]>;
    warnings: Record<string, string[]>;
  };
}

// ============================================================================
// BATCH ANALYSIS TYPES
// ============================================================================

export interface BatchAnalysisConfig {
  batchSize: number;
  delayMs: number;
  exportFormat: "json" | "csv";
}

export interface BatchAnalysisResult {
  totalFiles: number;
  processedFiles: number;
  successCount: number;
  errorCount: number;
  results: MetadataAnalysisResult[];
  errors: Array<{ file: string; error: string }>;
  processingTime: number;
}

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================

export interface MetadataTestingConfig {
  validMotionTypes: string[];
  requiredFields: string[];
  healthScoreWeights: {
    authorWeight: number;
    levelWeight: number;
    startPositionWeight: number;
    beatIntegrityWeight: number;
    motionDataWeight: number;
  };
}

