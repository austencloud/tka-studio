/**
 * Image Composition Service
 *
 * Main orchestrator for composing complete TKA sequence images. This service
 * combines rendered beats, text overlays, and background elements to create
 * the final export image. Equivalent to desktop ImageCreator.
 *
 * Critical: Maintains exact positioning and sizing compatibility with desktop.
 *
 * Architecture: Uses internal composition to delegate to specialized components
 * while maintaining the same public interface contracts.
 */

import type { SequenceData } from "../../interfaces/domain-types";
import type {
  CompositionOptions,
  IBeatRenderingService,
  IDimensionCalculationService,
  IImageCompositionService,
  ILayoutCalculationService,
  LayoutData,
  TKAImageExportOptions,
} from "../../interfaces/image-export-interfaces";

import type {
  IWordTextRenderer,
  IUserInfoRenderer,
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
} from "../../interfaces/text-rendering-interfaces";

// Internal composition components
import { CanvasCreator } from "./composition/internal/CanvasCreator";
import { BeatGridPositioner } from "./composition/internal/BeatGridPositioner";
import { TextOverlayApplicator } from "./composition/internal/TextOverlayApplicator";
import { CompositionValidator } from "./composition/internal/CompositionValidator";
import { CompositionUtils } from "./composition/internal/CompositionTypes";

export class ImageCompositionService implements IImageCompositionService {
  // Internal composition components (not exposed via DI)
  private readonly canvasCreator: CanvasCreator;
  private readonly beatPositioner: BeatGridPositioner;
  private readonly textApplicator: TextOverlayApplicator;
  private readonly validator: CompositionValidator;

  constructor(
    private layoutService: ILayoutCalculationService,
    private dimensionService: IDimensionCalculationService,
    private beatRenderer: IBeatRenderingService,
    private wordRenderer: IWordTextRenderer,
    private userInfoRenderer: IUserInfoRenderer,
    private difficultyRenderer: IDifficultyBadgeRenderer,
    private textUtils: ITextRenderingUtils
  ) {
    // Internal composition - these are not registered in DI container
    this.canvasCreator = new CanvasCreator(layoutService, dimensionService);
    this.beatPositioner = new BeatGridPositioner(beatRenderer);
    this.textApplicator = new TextOverlayApplicator(
      wordRenderer,
      userInfoRenderer,
      difficultyRenderer,
      textUtils
    );
    this.validator = new CompositionValidator(layoutService, dimensionService);
  }

  /**
   * Compose complete sequence image from sequence data
   * Main entry point that orchestrates the entire composition process
   */
  async composeSequenceImage(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): Promise<HTMLCanvasElement> {
    if (!sequence) {
      throw new Error("Sequence data is required for composition");
    }

    try {
      // Step 1: Calculate layout and dimensions
      const layoutData = this.canvasCreator.calculateLayoutData(sequence, options);

      // Step 2: Create main canvas with calculated dimensions
      const mainCanvas = this.canvasCreator.createMainCanvas(layoutData, options);

      // Step 3: Render all beats to individual canvases
      const beatCanvases = await this.beatPositioner.renderAllBeats(
        sequence,
        layoutData,
        options
      );

      // Step 4: Render start position if needed
      const startPositionCanvas = options.includeStartPosition
        ? await this.beatPositioner.renderStartPosition(sequence, layoutData, options)
        : null;

      // Step 5: Compose final image
      await this.composeFromCanvases(
        beatCanvases,
        startPositionCanvas,
        layoutData,
        CompositionUtils.toCompositionOptions(options, layoutData)
      );

      // Step 6: Add text overlays
      this.textApplicator.addTextOverlays(mainCanvas, sequence, layoutData, options);

      return mainCanvas;
    } catch (error) {
      throw new Error(
        `Image composition failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Compose image from pre-rendered canvases
   * Lower-level composition for when beats are already rendered
   */
  async composeFromCanvases(
    beatCanvases: HTMLCanvasElement[],
    startPositionCanvas: HTMLCanvasElement | null,
    layoutData: LayoutData,
    options: CompositionOptions
  ): Promise<HTMLCanvasElement> {
    // Create main canvas if not provided
    const mainCanvas = this.canvasCreator.createMainCanvas(layoutData, options);
    const ctx = mainCanvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from main canvas");
    }

    // Step 1: Fill background
    this.fillBackground(ctx, mainCanvas.width, mainCanvas.height);

    // Step 2: Position and draw start position
    let startColumn = 0;
    if (startPositionCanvas && options.includeStartPosition) {
      this.drawBeatCanvas(
        ctx,
        startPositionCanvas,
        0, // column 0
        0, // row 0
        layoutData,
        options
      );
      startColumn = 1;
    }

    // Step 3: Position and draw all beats in grid layout
    this.drawBeatsInGrid(ctx, beatCanvases, layoutData, options, startColumn);

    return mainCanvas;
  }

  /**
   * Apply background and borders
   * Matches desktop white background
   */
  applyBackground(
    canvas: HTMLCanvasElement,
    backgroundColor: string = "white"
  ): HTMLCanvasElement {
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from canvas");
    }
    this.fillBackground(ctx, canvas.width, canvas.height, backgroundColor);
    return canvas;
  }

  /**
   * Optimize canvas for export
   * Applies final optimizations before export
   */
  optimizeForExport(canvas: HTMLCanvasElement): HTMLCanvasElement {
    // For now, return as-is. In the future, could apply:
    // - Anti-aliasing improvements
    // - Color space conversions
    // - Compression optimizations
    return canvas;
  }

  /**
   * Calculate layout data for composition
   */
  private calculateLayoutData(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): LayoutData {
    const beatCount = sequence.beats.length;

    // Calculate layout using exact desktop algorithms
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );

    // Calculate additional heights for text areas
    const [additionalHeightTop, additionalHeightBottom] =
      this.dimensionService.determineAdditionalHeights(
        options,
        beatCount,
        options.beatScale
      );

    return {
      columns,
      rows,
      beatSize: Math.floor(options.beatSize * options.beatScale),
      includeStartPosition: options.includeStartPosition,
      additionalHeightTop,
      additionalHeightBottom,
    };
  }

  /**
   * Create main canvas with calculated dimensions
   */
  private createMainCanvas(
    layoutData: LayoutData,
    options: TKAImageExportOptions
  ): HTMLCanvasElement {
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;

    return canvas;
  }

  /**
   * Render all beats to individual canvases
   */
  private async renderAllBeats(
    sequence: SequenceData,
    layoutData: LayoutData,
    options: TKAImageExportOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!sequence.beats || sequence.beats.length === 0) {
      return [];
    }

    const beatRenderOptions = {
      addBeatNumbers: options.addBeatNumbers,
      redVisible: options.redVisible,
      blueVisible: options.blueVisible,
      combinedGrids: options.combinedGrids,
      beatScale: options.beatScale,
    };

    return await this.beatRenderer.renderBeatsToCanvases(
      [...sequence.beats],
      layoutData.beatSize,
      beatRenderOptions
    );
  }

  /**
   * Render start position canvas
   */
  private async renderStartPosition(
    sequence: SequenceData,
    layoutData: LayoutData,
    options: TKAImageExportOptions
  ): Promise<HTMLCanvasElement> {
    const beatRenderOptions = {
      addBeatNumbers: options.addBeatNumbers,
      redVisible: options.redVisible,
      blueVisible: options.blueVisible,
      combinedGrids: options.combinedGrids,
      beatScale: options.beatScale,
    };

    return await this.beatRenderer.renderStartPositionToCanvas(
      sequence,
      layoutData.beatSize,
      beatRenderOptions
    );
  }

  /**
   * Fill canvas background
   */
  private fillBackground(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    color: string = "white"
  ): void {
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, width, height);
  }

  /**
   * Draw a single beat canvas at grid position
   */
  private drawBeatCanvas(
    ctx: CanvasRenderingContext2D,
    beatCanvas: HTMLCanvasElement,
    column: number,
    row: number,
    layoutData: LayoutData,
    _options: CompositionOptions
  ): void {
    const x = column * layoutData.beatSize;
    const y = row * layoutData.beatSize + layoutData.additionalHeightTop;

    ctx.drawImage(beatCanvas, x, y);
  }

  /**
   * Draw all beats in grid layout
   * Matches desktop grid positioning exactly
   */
  private drawBeatsInGrid(
    ctx: CanvasRenderingContext2D,
    beatCanvases: HTMLCanvasElement[],
    layoutData: LayoutData,
    options: CompositionOptions,
    startColumn: number = 0
  ): void {
    let beatIndex = 0;

    // Iterate through grid positions (matches desktop logic)
    for (
      let row = 0;
      row < layoutData.rows && beatIndex < beatCanvases.length;
      row++
    ) {
      for (
        let col = startColumn;
        col < layoutData.columns && beatIndex < beatCanvases.length;
        col++
      ) {
        const beatCanvas = beatCanvases[beatIndex];
        this.drawBeatCanvas(ctx, beatCanvas, col, row, layoutData, options);
        beatIndex++;
      }
    }
  }

  /**
   * Add text overlays (word, user info, difficulty)
   */
  private addTextOverlays(
    canvas: HTMLCanvasElement,
    sequence: SequenceData,
    layoutData: LayoutData,
    options: TKAImageExportOptions
  ): void {
    const textOptions = {
      margin: Math.floor(options.margin * options.beatScale),
      beatScale: options.beatScale,
      additionalHeightTop: layoutData.additionalHeightTop,
      additionalHeightBottom: layoutData.additionalHeightBottom,
    };

    // Add word title if enabled
    if (options.addWord && sequence.word) {
      this.wordRenderer.render(canvas, sequence.word, textOptions);
    }

    // Add user info if enabled
    if (options.addUserInfo) {
      const userInfo = {
        userName: options.userName,
        notes: options.notes,
        exportDate: options.exportDate,
      };
      this.userInfoRenderer.render(canvas, userInfo, textOptions);
    }

    // Add difficulty level badge if enabled and available
    if (
      options.addDifficultyLevel &&
      sequence.level &&
      layoutData.additionalHeightTop > 0
    ) {
      const badgeSize = Math.floor(layoutData.additionalHeightTop * 0.75);
      const inset = Math.floor(layoutData.additionalHeightTop / 8);

      this.difficultyRenderer.render(
        canvas,
        sequence.level,
        [inset, inset],
        badgeSize
      );
    }
  }

  /**
   * Validate composition parameters
   */
  private validateCompositionParameters(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!sequence) {
      errors.push("Sequence data is required");
    }

    if (!options) {
      errors.push("Export options are required");
    }

    if (options && options.beatScale <= 0) {
      errors.push("Beat scale must be positive");
    }

    if (options && options.beatSize <= 0) {
      errors.push("Beat size must be positive");
    }

    if (sequence && sequence.beats && sequence.beats.length > 1000) {
      errors.push("Too many beats - maximum 1000 supported");
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Calculate memory usage estimate
   */
  estimateMemoryUsage(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { estimatedMB: number; safe: boolean } {
    const layoutData = this.calculateLayoutData(sequence, options);
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    // Estimate memory for main canvas + beat canvases
    const mainCanvasBytes = width * height * 4; // RGBA
    const beatCanvasBytes =
      sequence.beats.length * layoutData.beatSize * layoutData.beatSize * 4;
    const totalBytes = mainCanvasBytes + beatCanvasBytes;

    const estimatedMB = totalBytes / (1024 * 1024);
    const safe = estimatedMB < 100; // Conservative 100MB limit

    return { estimatedMB, safe };
  }

  /**
   * Create composition preview (smaller scale)
   */
  async createPreview(
    sequence: SequenceData,
    options: TKAImageExportOptions,
    previewScale: number = 0.5
  ): Promise<HTMLCanvasElement> {
    const previewOptions = {
      ...options,
      beatScale: options.beatScale * previewScale,
    };

    return await this.composeSequenceImage(sequence, previewOptions);
  }

  /**
   * Debug method to create test composition
   */
  async createTestComposition(): Promise<HTMLCanvasElement> {
    // Create minimal test sequence
    const testSequence: SequenceData = {
      id: "test",
      name: "Test Sequence",
      word: "TEST",
      beats: [
        {
          id: "beat1",
          beatNumber: 1,
          duration: 1,
          blueReversal: false,
          redReversal: false,
          isBlank: true,
          pictographData: null,
        },
      ],
      thumbnails: [],
      isFavorite: false,
      isCircular: false,
      tags: [],
      metadata: {},
      level: 3,
    };

    const testOptions: TKAImageExportOptions = {
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,
      beatScale: 1,
      beatSize: 144,
      margin: 50,
      redVisible: true,
      blueVisible: true,
      userName: "Test User",
      exportDate: "1-1-2024",
      notes: "Test composition",
      format: "PNG",
      quality: 1.0,
      addDifficultyLevel: true,
    };

    return await this.composeSequenceImage(testSequence, testOptions);
  }

  /**
   * Get composition statistics
   */
  getCompositionStats(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): {
    beatCount: number;
    layout: [number, number];
    dimensions: [number, number];
    memoryEstimate: number;
    textElements: string[];
  } {
    const beatCount = sequence.beats.length;
    const layout = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );
    const layoutData = this.calculateLayoutData(sequence, options);

    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;
    const dimensions = this.layoutService.calculateImageDimensions(
      layout,
      totalAdditionalHeight,
      options.beatScale
    );

    const { estimatedMB } = this.estimateMemoryUsage(sequence, options);

    const textElements: string[] = [];
    if (options.addWord && sequence.word) textElements.push("word");
    if (options.addUserInfo) textElements.push("userInfo");
    if (options.addDifficultyLevel && sequence.level)
      textElements.push("difficulty");

    return {
      beatCount,
      layout,
      dimensions,
      memoryEstimate: estimatedMB,
      textElements,
    };
  }
}
