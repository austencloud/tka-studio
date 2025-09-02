/**
 * Sequence Card Export Configuration Types
 *
 * Domain types for exporting sequence cards as images and PDF documents.
 * These types are specific to sequence card export functionality.
 */

// ============================================================================
// IMAGE EXPORT CONFIGURATION
// ============================================================================

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

export interface BatchExportOptions {
  batchSize: number;
  enableProgressReporting: boolean;
  memoryOptimization: boolean;
  filenameTemplate: string; // e.g., "sequence-cards-{pageNumber}.pdf"
  outputFormat: "individual" | "combined";
}

// ============================================================================
// EXPORT RESULT TYPES
// ============================================================================

import type { ExportResult } from "$domain";

// Extended result with additional service-level metadata
export interface ExportResultWithMetadata extends ExportResult {
  fileName?: string;
  mimeType?: string;
  warnings?: string[];
  // Note: metadata is inherited from ExportResult with proper structure
}

export interface BatchExportResult {
  success: boolean;
  results: ExportResultWithMetadata[];
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
export interface ServiceExportResult extends ExportResult {
  sequenceId: string;
  // Note: filename and metadata are inherited from ExportResult
  metrics: {
    processingTime: number;
    fileSize: number;
    resolution: { width: number; height: number };
  };
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
