/**
 * TKA Image Export Rendering Interfaces
 *
 * Service contracts for beat rendering, image composition, canvas management,
 * and visual effects in the TKA image export system.
 */

import type {
  BeatData,
  BeatRenderOptions,
  CompositionOptions,
  ImageExportOptions,
  LayoutData,
  SequenceData,
  TextRenderOptions,
  UserInfo,
} from "$domain";

// ============================================================================
// RENDERING SERVICES
// ============================================================================

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
    options: ImageExportOptions
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

// ============================================================================
// SERVICE INTERFACE SYMBOLS
// ============================================================================

export const IBeatRenderingServiceInterface = Symbol.for(
  "IBeatRenderingService"
);
export const ITextRenderingServiceInterface = Symbol.for(
  "ITextRenderingService"
);
export const IImageCompositionServiceInterface = Symbol.for(
  "IImageCompositionService"
);
export const ICanvasManagementServiceInterface = Symbol.for(
  "ICanvasManagementService"
);
export const IGridOverlayServiceInterface = Symbol.for("IGridOverlayService");
export const IReversalDetectionServiceInterface = Symbol.for(
  "IReversalDetectionService"
);
export const IFontManagementServiceInterface = Symbol.for(
  "IFontManagementService"
);
