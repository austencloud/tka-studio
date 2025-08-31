/**
 * Sequence Card Export Service Inteexport interface BatchExportProgress extends ProgressInfo {
 * Clean, focused service contracts for sequence card image generation.
 * Follows single responsibility principle and TKA DI patterns.
 */
// ============================================================================
// CORE TYPES
// ============================================================================
import type { ProgressInfo } from "$domain/sequence-card";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface SequenceCardDimensions {
  width: number;
  height: number;
  scale?: number; // Device pixel ratio multiplier
}

export interface SequenceCardMetadata {
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

export interface BatchExportProgress extends ProgressInfo {
  stage:
    | "initializing"
    | "processing"
    | "rendering"
    | "exporting"
    | "finalizing";
}

export interface SequenceCardExportResult {
  sequenceId: string;
  success: boolean;
  blob?: Blob;
  error?: Error;
  metrics?: ExportMetrics;
}
