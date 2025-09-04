/**
 * TKA Image Export Core Domain Types
 *
 * Core domain models for the TKA image export system.
 * Contains the main configuration types and fundamental data structures.
 */

// ============================================================================
// EXPORT OPTIONS AND CONFIGURATION
// ============================================================================

export interface SequenceExportOptions {
  // Core export settings (match desktop defaults)
  includeStartPosition: boolean;
  addBeatNumbers: boolean;
  addReversalSymbols: boolean;
  addUserInfo: boolean;
  addWord: boolean;
  combinedGrids: boolean;
  addDifficultyLevel: boolean;

  // Scaling and sizing
  beatScale: number;
  beatSize: number;
  margin: number;

  // Visibility settings
  redVisible: boolean;
  blueVisible: boolean;

  // User information
  userName: string;
  exportDate: string;
  notes: string;

  // Output format
  format: "PNG" | "JPEG" | "WebP";
  quality: number; // 0-1 for JPEG
  scale: number;
  width?: number;
  height?: number;
  backgroundColor?: string;
}



export interface BeatRenderOptions {
  addBeatNumbers: boolean;
  redVisible: boolean;
  blueVisible: boolean;
  combinedGrids: boolean;
  beatScale: number;
}

export interface TextRenderOptions {
  margin: number;
  beatScale: number;
  additionalHeightTop?: number;
  additionalHeightBottom?: number;
}

export interface CompositionOptions extends SequenceExportOptions {
  layout: [number, number]; // [columns, rows]
  additionalHeightTop: number;
  additionalHeightBottom: number;
}

export interface UserInfo {
  userName: string;
  notes: string;
  exportDate: string;
}

export interface LayoutData {
  columns: number;
  rows: number;
  beatSize: number;
  includeStartPosition: boolean;
  additionalHeightTop: number;
  additionalHeightBottom: number;
}

// ============================================================================
// EXPORT PROGRESS AND RESULTS
// ============================================================================

export interface ExportProgress {
  stage: "validation" | "rendering" | "composition" | "export" | "complete";
  progress: number; // 0-100
  message: string;
  currentBeat?: number;
  totalBeats?: number;
}

export interface ExportError extends Error {
  stage: string;
  details?: unknown;
}

export interface MemoryEstimate {
  estimatedMB: number;
  safe: boolean;
}

export interface SequenceExportResult {
  success: boolean;
  blob?: Blob;
  filename: string;
  error?: ExportError;
  metadata: {
    format: string;
    size: number;
    dimensions: { width: number; height: number };
    beatCount: number;
    processingTime: number;
  };
}

// ============================================================================
// RENDERING CONFIGURATION
// ============================================================================

export interface SequenceRenderQualitySettings {
  antialiasing: boolean;
  smoothScaling: boolean;
  highResolution: boolean;
  textQuality: "low" | "medium" | "high";
}

export interface LayoutConstraints {
  maxColumns: number;
  maxRows: number;
  minBeatSize: number;
  maxBeatSize: number;
  aspectRatio?: number;
}

// ============================================================================
// SERVICE INTERFACE SYMBOLS
// ============================================================================

export const ITKAImageExportServiceInterface = Symbol.for(
  "ITKAImageExportService"
);
