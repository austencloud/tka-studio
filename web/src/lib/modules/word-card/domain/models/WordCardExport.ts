/**
 * Word Card Export Service Inteexport interface BatchExportProgress extends ProgressInfo {
 * Clean, focused service contracts for word card image generation.
 * Follows single responsibility principle and TKA DI patterns.
 */
// ============================================================================
// CORE TYPES
// ============================================================================

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface WordCardDimensions {
  width: number;
  height: number;
  scale?: number; // Device pixel ratio multiplier
}

export interface WordCardMetadata {
  title?: string;
  author?: string;
  beatNumbers?: boolean;
  timestamp?: boolean;
  backgroundColor?: string;
}

export interface BatchOperationConfig {
  batchSize: number;
  memoryThreshold: number; // MB
  enableProgressReporting: boolean;
  enableCancellation: boolean;
}

export interface ExportMetrics {
  processingTime: number;
  fileSize: number;
  resolution: { width: number; height: number };
  memoryUsage?: number;
}

export interface BatchExportProgress {
  // ProgressInfo already includes all the properties we need:
  // current, total, percentage, message, stage, startTime, errorCount, warningCount
  // We can add additional properties specific to batch export if needed
  current: number;
  total: number;
  percentage: number;
  message: string;
  stage?: string;
  startTime?: Date;
  errorCount?: number;
  warningCount?: number;
  batchId?: string;
  itemsProcessed?: number;
}

export interface WordCardExportResult {
  sequenceId: string;
  success: boolean;
  blob?: Blob;
  error?: Error;
  metrics?: ExportMetrics;
}
