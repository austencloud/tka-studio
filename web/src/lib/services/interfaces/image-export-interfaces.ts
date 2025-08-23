/**
 * TKA Image Export Service Interfaces
 *
 * Service contracts for the TKA image export system, providing pixel-perfect
 * compatibility with the desktop application's image export functionality.
 *
 * This system converts TKA sequences into high-quality images for sharing,
 * printing, and archival purposes.
 */

import type { BeatData, SequenceData } from "./domain-types";

// ============================================================================
// EXPORT OPTIONS AND CONFIGURATION
// ============================================================================

export interface TKAImageExportOptions {
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
  format: "PNG" | "JPEG";
  quality: number; // 0-1 for JPEG
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

export interface CompositionOptions extends TKAImageExportOptions {
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
// MAIN IMAGE EXPORT SERVICES
// ============================================================================

/**
 * Main orchestrator for TKA image export operations
 * Equivalent to desktop ImageExportManager
 */
export interface ITKAImageExportService {
  /**
   * Export a complete sequence as an image blob
   */
  exportSequenceImage(
    sequence: SequenceData,
    options?: Partial<TKAImageExportOptions>
  ): Promise<Blob>;

  /**
   * Generate a preview image (smaller scale for UI)
   */
  generatePreview(
    sequence: SequenceData,
    options?: Partial<TKAImageExportOptions>
  ): Promise<string>; // Returns data URL

  /**
   * Export and download image file directly
   */
  exportAndDownload(
    sequence: SequenceData,
    filename?: string,
    options?: Partial<TKAImageExportOptions>
  ): Promise<void>;

  /**
   * Export multiple sequences as a batch
   */
  batchExport(
    sequences: SequenceData[],
    options?: Partial<TKAImageExportOptions>,
    progressCallback?: (current: number, total: number) => void
  ): Promise<void>;

  /**
   * Validate sequence and options before export
   */
  validateExport(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { valid: boolean; errors: string[] };

  /**
   * Get default export options
   */
  getDefaultOptions(): TKAImageExportOptions;
}

/**
 * Layout calculation service for grid positioning
 * Equivalent to desktop ImageExportLayoutHandler
 */
export interface ILayoutCalculationService {
  /**
   * Calculate optimal layout for given beat count
   * Returns [columns, rows] matching desktop layout tables
   */
  calculateLayout(
    beatCount: number,
    includeStartPosition: boolean
  ): [number, number];

  /**
   * Calculate image dimensions for layout
   * Returns [width, height] in pixels
   */
  calculateImageDimensions(
    layout: [number, number],
    additionalHeight: number,
    beatScale?: number
  ): [number, number];

  /**
   * Get layout for current beat frame (compatibility method)
   */
  getCurrentBeatFrameLayout(beatCount: number): [number, number];

  /**
   * Validate layout parameters
   */
  validateLayout(beatCount: number, includeStartPosition: boolean): boolean;
}

/**
 * Beat rendering service for individual beat conversion
 * Equivalent to desktop BeatDrawer and ImageExportBeatFactory
 */
export interface IBeatRenderingService {
  /**
   * Render a single beat to canvas
   */
  renderBeatToCanvas(
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Render start position to canvas
   */
  renderStartPositionToCanvas(
    sequence: SequenceData,
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Batch render multiple beats
   */
  renderBeatsToCanvases(
    beats: BeatData[],
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement[]>;

  /**
   * Apply visibility settings to rendered beat
   */
  applyVisibilitySettings(
    canvas: HTMLCanvasElement,
    options: BeatRenderOptions
  ): HTMLCanvasElement;
}

/**
 * Text rendering service for titles, user info, and overlays
 * Equivalent to desktop WordDrawer, UserInfoDrawer, DifficultyLevelDrawer
 */
export interface ITextRenderingService {
  /**
   * Render sequence word/title text
   */
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions
  ): void;

  /**
   * Render user information (name, date, notes)
   */
  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void;

  /**
   * Render difficulty level badge
   */
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void;

  /**
   * Calculate text dimensions for layout planning
   */
  measureText(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight?: string
  ): { width: number; height: number };

  /**
   * Apply custom kerning to text
   */
  renderTextWithKerning(
    ctx: CanvasRenderingContext2D,
    text: string,
    x: number,
    y: number,
    kerning: number
  ): void;
}

/**
 * Image composition service for assembling final images
 * Equivalent to desktop ImageCreator
 */
export interface IImageCompositionService {
  /**
   * Compose complete sequence image from rendered beats
   */
  composeSequenceImage(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Compose image from pre-rendered canvases
   */
  composeFromCanvases(
    beatCanvases: HTMLCanvasElement[],
    startPositionCanvas: HTMLCanvasElement | null,
    layoutData: LayoutData,
    options: CompositionOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Apply background and borders
   */
  applyBackground(
    canvas: HTMLCanvasElement,
    backgroundColor?: string
  ): HTMLCanvasElement;

  /**
   * Optimize canvas for export
   */
  optimizeForExport(canvas: HTMLCanvasElement): HTMLCanvasElement;
}

/**
 * File export service for browser downloads
 * Equivalent to desktop ImageSaver
 */
export interface IFileExportService {
  /**
   * Export canvas as blob
   */
  canvasToBlob(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG",
    quality?: number
  ): Promise<Blob>;

  /**
   * Convert canvas to data URL for immediate display
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG",
    quality?: number
  ): string;

  /**
   * Download blob as file
   */
  downloadBlob(blob: Blob, filename: string): Promise<void>;

  /**
   * Generate versioned filename
   */
  generateVersionedFilename(
    word: string,
    format: string,
    timestamp?: Date
  ): string;

  /**
   * Validate filename
   */
  validateFilename(filename: string): boolean;

  /**
   * Get supported export formats
   */
  getSupportedFormats(): string[];
}

// ============================================================================
// SPECIALIZED SERVICES
// ============================================================================

/**
 * Dimension calculation service
 * Equivalent to desktop HeightDeterminer
 */
export interface IDimensionCalculationService {
  /**
   * Determine additional heights for text areas
   * Returns [topHeight, bottomHeight]
   */
  determineAdditionalHeights(
    options: TKAImageExportOptions,
    beatCount: number,
    beatScale: number
  ): [number, number];

  /**
   * Calculate beat size with scaling
   */
  calculateScaledBeatSize(baseSize: number, scale: number): number;

  /**
   * Calculate margin with scaling
   */
  calculateScaledMargin(baseMargin: number, scale: number): number;

  /**
   * Validate dimension parameters
   */
  validateDimensions(
    beatCount: number,
    beatScale: number,
    options: TKAImageExportOptions
  ): boolean;
}

/**
 * Grid overlay service for combined grid mode
 * Equivalent to desktop CombinedGridHandler
 */
export interface IGridOverlayService {
  /**
   * Apply combined grids to beat canvas
   */
  applyCombinedGrids(
    canvas: HTMLCanvasElement,
    currentGridMode: string
  ): HTMLCanvasElement;

  /**
   * Draw grid overlay on canvas
   */
  drawGridOverlay(
    ctx: CanvasRenderingContext2D,
    gridMode: string,
    size: number,
    opacity?: number
  ): void;

  /**
   * Get opposite grid mode
   */
  getOppositeGridMode(currentMode: string): string;

  /**
   * Validate grid modes
   */
  validateGridMode(gridMode: string): boolean;
}

/**
 * Reversal detection and processing service
 * Equivalent to desktop BeatReversalProcessor
 */
export interface IReversalDetectionService {
  /**
   * Process reversals for sequence
   */
  processReversals(sequence: SequenceData, beats: BeatData[]): BeatData[];

  /**
   * Detect reversal for single beat
   */
  detectReversal(
    previousBeats: BeatData[],
    currentBeat: BeatData
  ): { blueReversal: boolean; redReversal: boolean };

  /**
   * Apply reversal symbols to beat
   */
  applyReversalSymbols(
    beatData: BeatData,
    reversalInfo: { blueReversal: boolean; redReversal: boolean }
  ): BeatData;
}

/**
 * Font and typography management service
 * Equivalent to desktop FontMarginHelper
 */
export interface IFontManagementService {
  /**
   * Adjust font size and margin based on beat count
   */
  adjustFontAndMargin(
    baseFontSize: number,
    baseMargin: number,
    beatCount: number,
    beatScale: number
  ): { fontSize: number; margin: number };

  /**
   * Load and validate fonts
   */
  loadFonts(): Promise<void>;

  /**
   * Get font family for element type
   */
  getFontFamily(elementType: "word" | "userInfo" | "difficulty"): string;

  /**
   * Calculate font scaling for responsive text
   */
  calculateFontScaling(
    text: string,
    maxWidth: number,
    maxHeight: number,
    baseFontSize: number
  ): number;
}

/**
 * Canvas management and optimization service
 */
export interface ICanvasManagementService {
  /**
   * Create optimized canvas
   */
  createCanvas(width: number, height: number): HTMLCanvasElement;

  /**
   * Clone canvas
   */
  cloneCanvas(source: HTMLCanvasElement): HTMLCanvasElement;

  /**
   * Dispose canvas resources
   */
  disposeCanvas(canvas: HTMLCanvasElement): void;

  /**
   * Get canvas memory usage
   */
  getMemoryUsage(): number;

  /**
   * Clear canvas cache
   */
  clearCache(): void;
}

// ============================================================================
// SETTINGS AND PERSISTENCE
// ============================================================================

/**
 * Export settings management service
 */
export interface IExportSettingsService {
  /**
   * Get current export settings
   */
  getCurrentSettings(): TKAImageExportOptions;

  /**
   * Update export settings
   */
  updateSettings(settings: Partial<TKAImageExportOptions>): Promise<void>;

  /**
   * Reset to default settings
   */
  resetToDefaults(): Promise<void>;

  /**
   * Save settings preset
   */
  savePreset(name: string, settings: TKAImageExportOptions): Promise<void>;

  /**
   * Load settings preset
   */
  loadPreset(name: string): Promise<TKAImageExportOptions | null>;

  /**
   * Get available presets
   */
  getPresets(): Promise<string[]>;

  /**
   * Validate settings
   */
  validateSettings(settings: TKAImageExportOptions): boolean;
}

// ============================================================================
// UTILITY TYPES
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

export interface ExportResult {
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

export interface RenderQualitySettings {
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

// Define unique symbols for DI container registration
export const ITKAImageExportServiceInterface = Symbol.for(
  "ITKAImageExportService"
);
export const ILayoutCalculationServiceInterface = Symbol.for(
  "ILayoutCalculationService"
);
export const IBeatRenderingServiceInterface = Symbol.for(
  "IBeatRenderingService"
);
export const ITextRenderingServiceInterface = Symbol.for(
  "ITextRenderingService"
);

// Text rendering component interface symbols
export const IWordTextRendererInterface = Symbol.for("IWordTextRenderer");
export const IUserInfoRendererInterface = Symbol.for("IUserInfoRenderer");
export const IDifficultyBadgeRendererInterface = Symbol.for("IDifficultyBadgeRenderer");
export const ITextRenderingUtilsInterface = Symbol.for("ITextRenderingUtils");

export const IImageCompositionServiceInterface = Symbol.for(
  "IImageCompositionService"
);
export const IFileExportServiceInterface = Symbol.for("IFileExportService");
export const IDimensionCalculationServiceInterface = Symbol.for(
  "IDimensionCalculationService"
);
export const IGridOverlayServiceInterface = Symbol.for("IGridOverlayService");
export const IReversalDetectionServiceInterface = Symbol.for(
  "IReversalDetectionService"
);
export const IFontManagementServiceInterface = Symbol.for(
  "IFontManagementService"
);
export const ICanvasManagementServiceInterface = Symbol.for(
  "ICanvasManagementService"
);
export const IExportSettingsServiceInterface = Symbol.for(
  "IExportSettingsService"
);
