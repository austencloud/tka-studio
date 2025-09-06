import type { BeatData, SequenceData } from "$shared/domain";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
// import type { BeatRenderOptions } from "../../../../export/domain";
import type { ICanvasManagementService, ISVGToCanvasConverterService } from "../../../../export/services/contracts";
import type { IBeatFallbackRenderer } from "../../contracts";

// Temporary type definition
interface BeatRenderOptions {
  addBeatNumbers: boolean;
  redVisible: boolean;
  blueVisible: boolean;
  combinedGrids: boolean;
  beatScale: number;
}

@injectable()
export class BeatRenderingService {
  constructor(
    @inject(TYPES.ISVGToCanvasConverterService)
    private svgToCanvasConverter: ISVGToCanvasConverterService,
    @inject(TYPES.IBeatFallbackRenderer)
    private fallbackService: IBeatFallbackRenderer,
    @inject(TYPES.ICanvasManagementService)
    private canvasManager: ICanvasManagementService
  ) {}

  /**
   * Render a single beat to canvas
   * Orchestrates the rendering process using microservices
   */
  async renderBeatToCanvas(
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement> {
    if (!beatData) {
      throw new Error("Beat data is required for rendering");
    }

    if (size <= 0) {
      throw new Error(`Invalid size: ${size}`);
    }

    try {
      // Create canvas
      const canvas = this.canvasManager.createCanvas(size, size);
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        throw new Error("Failed to get 2D context from canvas");
      }

      // Clear canvas with white background
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, size, size);

      // Handle empty/error beats using fallback service
      if (beatData.isBlank || !beatData.pictographData) {
        const fallbackCanvas = await this.fallbackService.createEmptyBeat({
          showPlaceholder: true,
          placeholderText: "Empty Beat",
        });

        // Copy fallback to our canvas
        ctx.drawImage(fallbackCanvas, 0, 0);
        this.canvasManager.disposeCanvas(fallbackCanvas);

        return canvas;
      }

      // Generate SVG for the beat
      const svgString = await this.generateSVGString(beatData, size, options);
      if (!svgString) {
        // Use fallback for failed SVG generation
        const fallbackCanvas = await this.fallbackService.createErrorBeat({
          showError: true,
          errorMessage: "Failed to generate SVG",
          size: { width: size, height: size },
        });

        ctx.drawImage(fallbackCanvas, 0, 0);
        this.canvasManager.disposeCanvas(fallbackCanvas);

        return canvas;
      }

      // Convert SVG to canvas using microservice
      const convertedCanvas =
        await this.svgToCanvasConverter.convertSVGStringToCanvas(svgString, {
          width: size,
          height: size,
          preserveAspectRatio: true,
          backgroundColor: "white",
        });

      // Copy converted canvas to our canvas
      ctx.drawImage(convertedCanvas, 0, 0);

      // Apply grid overlays using grid service (if needed)
      // Note: Grid rendering would be controlled by other options

      // Apply post-processing
      this.applyPostProcessing(ctx, beatData, size, options);

      return canvas;
    } catch (error) {
      throw new Error(
        `Failed to render beat to canvas: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Render start position to canvas
   */
  async renderStartPositionToCanvas(
    sequence: SequenceData,
    _size: number,
    _options: BeatRenderOptions
  ): Promise<HTMLCanvasElement> {
    if (!sequence) {
      throw new Error("Sequence data is required for start position rendering");
    }

    try {
      // Use fallback service for consistent start position rendering
      return await this.fallbackService.createDefaultStartPosition();
    } catch (error) {
      throw new Error(
        `Failed to render start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Render multiple beats in batch
   */
  async renderBeatsToCanvases(
    beats: BeatData[],
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!beats || beats.length === 0) {
      return [];
    }

    try {
      // Process beats in parallel for better performance
      const promises = beats.map((beat) =>
        this.renderBeatToCanvas(beat, size, options)
      );

      return await Promise.all(promises);
    } catch (error) {
      throw new Error(
        `Batch rendering failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Apply visibility settings to rendered beat
   */
  applyVisibilitySettings(
    canvas: HTMLCanvasElement,
    options: BeatRenderOptions
  ): HTMLCanvasElement {
    if (options.redVisible && options.blueVisible) {
      return canvas; // Both visible - no changes needed
    }

    // Create new canvas for filtered result
    const filteredCanvas = this.canvasManager.createCanvas(
      canvas.width,
      canvas.height
    );
    const filteredCtx = filteredCanvas.getContext("2d");
    if (!filteredCtx) {
      throw new Error("Failed to get 2D context from filtered canvas");
    }

    // Draw original canvas
    filteredCtx.drawImage(canvas, 0, 0);

    // Apply visibility filters
    this.applyColorFilters(filteredCtx, canvas.width, canvas.height, options);

    // Dispose original canvas
    this.canvasManager.disposeCanvas(canvas);

    return filteredCanvas;
  }

  /**
   * Generate SVG string for a beat
   */
  private async generateSVGString(
    beatData: BeatData,
    _size: number,
    _options: BeatRenderOptions
  ): Promise<string | null> {
    try {
      // TODO: Implement proper SVG generation using pictograph service
      // For now, return null to trigger fallback rendering
      console.warn("SVG generation not yet implemented for beat:", beatData.id);
      return null;
    } catch (error) {
      console.warn("Failed to generate SVG string:", error);
      return null;
    }
  }

  /**
   * Apply post-processing effects (simplified)
   */
  private applyPostProcessing(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): void {
    // Apply combined grids if enabled
    if (options.combinedGrids) {
      // TODO: Implement combined grids - requires canvas, not context
      console.warn("Combined grids not yet implemented");
    }

    // Apply beat number if enabled
    if (options.addBeatNumbers && beatData.beatNumber > 0) {
      this.drawBeatNumber(ctx, beatData.beatNumber, size);
    }
  }

  /**
   * Apply color filters for visibility settings
   */
  private applyColorFilters(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    options: BeatRenderOptions
  ): void {
    if (!options.redVisible || !options.blueVisible) {
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        // Simple color filtering logic
        if (!options.redVisible && r > g && r > b) {
          data[i + 3] = 0; // Make red elements transparent
        }
        if (!options.blueVisible && b > r && b > g) {
          data[i + 3] = 0; // Make blue elements transparent
        }
      }

      ctx.putImageData(imageData, 0, 0);
    }
  }

  /**
   * Draw beat number (lightweight implementation)
   */
  private drawBeatNumber(
    ctx: CanvasRenderingContext2D,
    beatNumber: number,
    size: number
  ): void {
    ctx.fillStyle = "#4b5563";
    ctx.font = `bold ${size * 0.15}px Arial, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(beatNumber.toString(), size / 2, size * 0.05);
  }

  /**
   * Cleanup method
   */
  dispose(): void {
    // Canvas management handled by CanvasManagementService
    // Nothing to clean up here
  }
}
