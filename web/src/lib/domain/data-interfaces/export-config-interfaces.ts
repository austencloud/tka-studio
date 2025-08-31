/**
 * Export Configuration Interfaces
 *
 * Foundation types for export services - configuration options, results,
 * and progress types used across all export functionality.
 */

import type { ExportResult } from "$domain/sequence-card/SequenceCard";

// ============================================================================
// EXPORT CONFIGURATION TYPES
// ============================================================================

export interface ImageExportOptions {
  format: "PNG" | "JPEG" | "WebP";
  quality: number; // 0-1 for JPEG/WebP
  width?: number;
  height?: number;
  scale: number; // Device pixel ratio multiplier
  backgroundColor?: string;
}

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

// ExportResult is imported from domain layer via domain-types.ts
// Service layer extends it with additional service-specific properties
export interface ServiceExportResult extends ExportResult {
  sequenceId: string;
  filename: string;
  metrics: {
    processingTime: number;
    fileSize: number;
    resolution: { width: number; height: number };
  };
  metadata: {
    format: string;
    size: number;
    dimensions?: { width: number; height: number };
    processingTime: number;
  };
}

export interface BatchExportResult {
  success: boolean;
  results: ServiceExportResult[];
  totalProcessingTime: number;
  successCount: number;
  failureCount: number;
  totalPages?: number; // Optional for page-specific exports
  errors: Error[] | Array<{ sequenceId: string; error: Error }>; // Support both formats
}

export interface ExportProgress {
  current: number;
  total: number;
  currentItem: number;
  currentPage?: number; // Optional for page-specific progress
  totalItems: number;
  percentage: number;
  estimatedTimeRemaining: number;
  currentOperation: string;
  isComplete: boolean;
}
