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

import type {
  IBeatRenderingService,
  IDimensionCalculationService,
  IImageCompositionService,
  ILayoutCalculationService,
} from "$contracts";
import type {
  CompositionOptions,
  ImageExportOptions,
  LayoutData,
  SequenceData,
} from "$domain";

import type {
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
  IUserInfoRenderer,
  IWordTextRenderer,
} from "$contracts";
import { inject, injectable } from "inversify";
import { TYPES } from "../../../inversify/types";

// Internal composition components
import { BeatGridPositioner } from "./BeatGridPositioner";
import { CanvasCreator } from "./CanvasCreator";
import { CompositionUtils } from "./CompositionTypes";
import { TextOverlayApplicator } from "./TextOverlayApplicator";

@injectable()
export class ImageCompositionService implements IImageCompositionService {
  // Internal composition components (not exposed via DI)
  private readonly canvasCreator: CanvasCreator;
  private readonly beatPositioner: BeatGridPositioner;
  private readonly textApplicator: TextOverlayApplicator;

  constructor(
    @inject(TYPES.ILayoutCalculationService)
    layoutService: ILayoutCalculationService,
    @inject(TYPES.IDimensionCalculationService)
    dimensionService: IDimensionCalculationService,
    @inject(TYPES.IBeatRenderingService) beatRenderer: IBeatRenderingService,
    @inject(TYPES.IWordTextRenderer) wordRenderer: IWordTextRenderer,
    @inject(TYPES.IUserInfoRenderer) userInfoRenderer: IUserInfoRenderer,
    @inject(TYPES.IDifficultyBadgeRenderer)
    difficultyRenderer: IDifficultyBadgeRenderer,
    @inject(TYPES.ITextRenderingUtils) textUtils: ITextRenderingUtils
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
  }

  /**
   * Compose complete sequence image from sequence data
   * Main entry point that orchestrates the entire composition process
   */
  async composeSequenceImage(
    sequence: SequenceData,
    options: ImageExportOptions
  ): Promise<HTMLCanvasElement> {
    if (!sequence) {
      throw new Error("Sequence data is required for composition");
    }

    try {
      // Step 1: Calculate layout and dimensions
      const layoutData = this.canvasCreator.calculateLayoutData(
        sequence,
        options
      );

      // Step 2: Create main canvas with calculated dimensions
      const mainCanvas = this.canvasCreator.createMainCanvas(
        layoutData,
        options
      );

      // Step 3: Render all beats to individual canvases
      const beatCanvases = await this.beatPositioner.renderAllBeats(
        sequence,
        layoutData,
        options
      );

      // Step 4: Render start position if needed
      const startPositionCanvas = options.includeStartPosition
        ? await this.beatPositioner.renderStartPosition(
            sequence,
            layoutData,
            options
          )
        : null;

      // Step 5: Compose final image
      await this.composeFromCanvases(
        beatCanvases,
        startPositionCanvas,
        layoutData,
        CompositionUtils.toCompositionOptions(options, layoutData)
      );

      // Step 6: Add text overlays
      this.textApplicator.addTextOverlays(
        mainCanvas,
        sequence,
        layoutData,
        options
      );

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
    this.beatPositioner.drawBeatsInGrid(
      ctx,
      beatCanvases,
      layoutData,
      options,
      startColumn
    );

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
   * Create composition preview (smaller scale)
   */
  async createPreview(
    sequence: SequenceData,
    options: ImageExportOptions,
    previewScale: number = 0.5
  ): Promise<HTMLCanvasElement> {
    const previewOptions = {
      ...options,
      beatScale: options.beatScale * previewScale,
    };

    return await this.composeSequenceImage(sequence, previewOptions);
  }
}
