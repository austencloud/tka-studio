/**
 * Word Card Export Config Types
 *
 * Domain types for exporting word cards as images and PDF documents.
 * These types are specific to word card export functionality.
 */

// ============================================================================
// IMAGE EXPORT CONFIGURATION
// ============================================================================

export interface WordCardExportOptions {
  format: "PNG" | "JPEG" | "WebP" | "PDF";
  quality: number; // 0-1 for JPEG/WebP
  width?: number;
  height?: number;
  scale: number; // Device pixel ratio multiplier
  backgroundColor?: string;
  includeMetadata?: boolean;
  filename?: string;
}

export interface ImageExportOptions {
  format: "PNG" | "JPEG" | "WebP";
  quality: number; // 0-1 for JPEG/WebP
  width?: number;
  height?: number;
  scale: number; // Device pixel ratio multiplier
  backgroundColor?: string;
}

// ============================================================================
// PDF EXPORT CONFIGURATION
// ============================================================================

export interface PDFExportOptions {
  orientation: "portrait" | "landscape";
  paperSize: "A4" | "Letter" | "Legal" | "Tabloid";
  margin: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
  enablePageNumbers: boolean;
  quality: "low" | "medium" | "high";
}

// ============================================================================
// BATCH EXPORT CONFIGURATION
// ============================================================================

export interface WordCardBatchExportOptions {
  batchSize: number;
  enableProgressReporting: boolean;
  memoryOptimization: boolean;
  filenameTemplate: string; // e.g., "word-cards-{pageNumber}.pdf"
  outputFormat: "individual" | "combined";
}

// ============================================================================
// EXPORT RESULT TYPES
// ============================================================================

// Extended result with additional service-level metadata
export interface WordCardExportResultWithMetadata extends WordCardExportResult {
  fileName?: string;
  mimeType?: string;
  warnings?: string[];
  // Note: metadata is inherited from WordCardExportResult with proper structure
}

export interface BatchExportResult {
  success: boolean;
  results: WordCardExportResultWithMetadata[];
  totalProcessingTime: number;
  successCount: number;
  failureCount: number;
  totalPages?: number; // Optional for page-specific exports
  errors: Error[] | Array<{ sequenceId: string; error: Error }>; // Support both formats
}

// Note: ExportProgress is now imported from build/image-export/core
// to avoid duplication across the domain

// ============================================================================
// ENHANCED EXPORT RESULT TYPES (from export-config-interfaces.ts)
// ============================================================================

// Extended service-level export result with additional metadata
export interface ServiceExportResult extends WordCardExportResult {
  conversionStartTime: number;
  // Note: filename and metadata are inherited from WordCardExportResult
}

// ============================================================================
// EXPORT PROGRESS TRACKING
// ============================================================================

export interface ExportProgressData {
  currentStep: number;
  totalSteps: number;
  stepDescription: string;
  percentComplete: number;
  estimatedTimeRemaining?: number;
  itemsProcessed: number;
  totalItems: number;
}

export interface ExportBatchProgress extends ExportProgressData {
  currentBatch: number;
  totalBatches: number;
  currentBatchSize: number;
  failedItems: number;
  skippedItems: number;
}

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

// BatchOperationConfig is now imported from shared domain

export interface ExportMetrics {
  processingTime: number;
  fileSize: number;
  resolution: { width: number; height: number };
  memoryUsage?: number;
}

// BatchExportProgress is now imported from shared domain

export interface WordCardExportResult {
  sequenceId: string;
  success: boolean;
  blob?: Blob;
  error?: Error;
  metrics?: ExportMetrics;
}

// ============================================================================
// PROGRESS TRACKING
// ============================================================================

export interface ProgressInfo {
  current: number;
  total: number;
  percentage: number;
  message?: string;
  stage?: string;
  startTime?: number;
  errorCount?: number;
  warningCount?: number;
}

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
  // Additional properties for service compatibility
  maxConcurrency: number;
  retryAttempts: number;
  timeoutMs: number;
}

export interface ExportMetrics {
  processingTime: number;
  fileSize: number;
  resolution: { width: number; height: number };
  memoryUsage?: number;
}

export interface BatchExportProgress extends ProgressInfo {
  // ProgressInfo already includes all the properties we need:
  // current, total, percentage, message, stage, startTime, errorCount, warningCount
  // We can add additional properties specific to batch export if needed
  batchId?: string;
  itemsProcessed?: number;
  // Additional properties for compatibility
  completed: number; // Alias for current
  currentItem?: string; // Alias for message
}

export interface WordCardExportResult {
  sequenceId: string;
  success: boolean;
  blob?: Blob;
  error?: Error;
  metrics?: ExportMetrics;
}
