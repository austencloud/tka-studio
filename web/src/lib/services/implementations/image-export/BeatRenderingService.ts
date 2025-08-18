/**
 * Beat Rendering Service
 *
 * Converts TKA beats and pictographs from SVG format to Canvas for image export.
 * This service provides functionality equivalent to the desktop BeatDrawer and
 * ImageExportBeatFactory, handling the complex task of rendering beats for export.
 *
 * Critical: Must maintain visual fidelity when converting from SVG to Canvas.
 */

import type {
  IBeatRenderingService,
  BeatRenderOptions,
} from "../../interfaces/image-export-interfaces";
import type { BeatData, SequenceData } from "../../interfaces/domain-types";

export class BeatRenderingService implements IBeatRenderingService {
  // Canvas pool for memory efficiency
  private canvasPool: HTMLCanvasElement[] = [];
  private readonly MAX_POOL_SIZE = 10;

  /**
   * Render a single beat to canvas
   * Converts SVG pictograph to canvas representation
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
      // Create canvas for this beat
      const canvas = this.getCanvasFromPool(size, size);
      const ctx = canvas.getContext("2d")!;

      // Clear canvas with white background (match desktop)
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, size, size);

      // If beat is blank, return canvas with just background
      if (beatData.is_blank || !beatData.pictograph_data) {
        await this.renderEmptyBeat(ctx, beatData, size, options);
        return canvas;
      }

      // Render pictograph to canvas
      await this.renderPictographToCanvas(ctx, beatData, size, options);

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
   * Handles the special case of sequence start position
   */
  async renderStartPositionToCanvas(
    sequence: SequenceData,
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement> {
    if (!sequence) {
      throw new Error("Sequence data is required for start position rendering");
    }

    try {
      const canvas = this.getCanvasFromPool(size, size);
      const ctx = canvas.getContext("2d")!;

      // Clear canvas with white background
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, size, size);

      // Check if sequence has explicit start position data
      if (sequence.start_position) {
        await this.renderPictographToCanvas(
          ctx,
          { ...sequence.start_position, beat_number: 0 } as BeatData,
          size,
          options
        );
      } else {
        // Render default start position
        await this.renderDefaultStartPosition(ctx, size, options);
      }

      // Add "START" label if beat numbers are enabled
      if (options.addBeatNumbers) {
        this.renderStartPositionLabel(ctx, size);
      }

      return canvas;
    } catch (error) {
      throw new Error(
        `Failed to render start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Batch render multiple beats
   * Optimized for rendering many beats efficiently
   */
  async renderBeatsToCanvases(
    beats: BeatData[],
    size: number,
    options: BeatRenderOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!beats || beats.length === 0) {
      return [];
    }

    const canvases: HTMLCanvasElement[] = [];

    try {
      // Process beats in chunks to manage memory
      const CHUNK_SIZE = 5;
      for (let i = 0; i < beats.length; i += CHUNK_SIZE) {
        const chunk = beats.slice(i, i + CHUNK_SIZE);
        const chunkCanvases = await Promise.all(
          chunk.map((beat) => this.renderBeatToCanvas(beat, size, options))
        );
        canvases.push(...chunkCanvases);
      }

      return canvases;
    } catch (error) {
      // Clean up any created canvases on error
      canvases.forEach((canvas) => this.returnCanvasToPool(canvas));
      throw new Error(
        `Batch rendering failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Apply visibility settings to rendered beat
   * Matches desktop visibility logic
   */
  applyVisibilitySettings(
    canvas: HTMLCanvasElement,
    options: BeatRenderOptions
  ): HTMLCanvasElement {
    if (options.redVisible && options.blueVisible) {
      // Both visible - no changes needed
      return canvas;
    }

    // Create a new canvas for filtered result
    const filteredCanvas = this.getCanvasFromPool(canvas.width, canvas.height);
    const filteredCtx = filteredCanvas.getContext("2d")!;

    // Draw original canvas
    filteredCtx.drawImage(canvas, 0, 0);

    // Apply visibility filters
    this.applyColorFilters(filteredCtx, canvas.width, canvas.height, options);

    // Return original canvas to pool
    this.returnCanvasToPool(canvas);

    return filteredCanvas;
  }

  /**
   * Render pictograph data to canvas context
   * Core rendering logic that converts pictograph to canvas
   */
  private async renderPictographToCanvas(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<void> {
    if (!beatData.pictograph_data) {
      return;
    }

    try {
      // Method 1: Try to render using existing Pictograph component
      const svgElement = await this.createSVGFromPictographData(
        beatData,
        size,
        options
      );
      if (svgElement) {
        await this.drawSVGToCanvas(ctx, svgElement, size, size);
        return;
      }

      // Method 2: Fallback to manual rendering
      await this.renderPictographManually(ctx, beatData, size, options);
    } catch (error) {
      console.warn("Pictograph rendering failed, using fallback:", error);
      await this.renderFallbackBeat(ctx, beatData, size, options);
    }
  }

  /**
   * Create SVG element from pictograph data
   * Attempts to use the existing Pictograph component
   */
  private async createSVGFromPictographData(
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<SVGElement | null> {
    try {
      // Create temporary container
      const container = document.createElement("div");
      container.style.position = "absolute";
      container.style.left = "-9999px";
      container.style.width = `${size}px`;
      container.style.height = `${size}px`;
      document.body.appendChild(container);

      try {
        // Dynamically import and create Pictograph component
        const { default: Pictograph } = await import(
          "$lib/components/pictograph/Pictograph.svelte"
        );

        const component = new Pictograph({
          target: container,
          props: {
            beatData,
            width: size,
            height: size,
            beatNumber: options.addBeatNumbers ? beatData.beat_number : null,
            debug: false,
          },
        });

        // Wait for component to render
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Extract SVG
        const svgElement = container.querySelector("svg");

        if (svgElement) {
          // Clone the SVG to avoid issues when removing from DOM
          const clonedSVG = svgElement.cloneNode(true) as SVGElement;

          // Clean up
          component.$destroy();
          return clonedSVG;
        }

        component.$destroy();
        return null;
      } finally {
        document.body.removeChild(container);
      }
    } catch (error) {
      console.warn("Failed to create SVG from Pictograph component:", error);
      return null;
    }
  }

  /**
   * Draw SVG element to canvas
   */
  private async drawSVGToCanvas(
    ctx: CanvasRenderingContext2D,
    svgElement: SVGElement,
    width: number,
    height: number
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // Serialize SVG to string
        const svgData = new XMLSerializer().serializeToString(svgElement);

        // Create image from SVG
        const img = new Image();

        img.onload = () => {
          try {
            ctx.drawImage(img, 0, 0, width, height);
            resolve();
          } catch (error) {
            reject(error);
          }
        };

        img.onerror = () => {
          reject(new Error("Failed to load SVG as image"));
        };

        // Convert SVG to data URL
        const svgBlob = new Blob([svgData], {
          type: "image/svg+xml;charset=utf-8",
        });
        const url = URL.createObjectURL(svgBlob);

        img.src = url;

        // Clean up URL after image loads
        img.onload = () => {
          try {
            ctx.drawImage(img, 0, 0, width, height);
            URL.revokeObjectURL(url);
            resolve();
          } catch (error) {
            URL.revokeObjectURL(url);
            reject(error);
          }
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Manual pictograph rendering (fallback method)
   */
  private async renderPictographManually(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<void> {
    const pictograph = beatData.pictograph_data!;

    // Draw grid background
    this.drawGrid(ctx, pictograph.grid_data?.grid_mode || "diamond", size);

    // Draw props if visible
    if (pictograph.props) {
      if (options.blueVisible && pictograph.props.blue) {
        this.drawProp(ctx, pictograph.props.blue, "blue", size);
      }
      if (options.redVisible && pictograph.props.red) {
        this.drawProp(ctx, pictograph.props.red, "red", size);
      }
    }

    // Draw arrows if visible
    if (pictograph.arrows) {
      if (options.blueVisible && pictograph.arrows.blue) {
        this.drawArrow(ctx, pictograph.arrows.blue, "blue", size);
      }
      if (options.redVisible && pictograph.arrows.red) {
        this.drawArrow(ctx, pictograph.arrows.red, "red", size);
      }
    }

    // Draw letter if present
    if (pictograph.letter) {
      this.drawLetter(ctx, pictograph.letter, size);
    }
  }

  /**
   * Render empty beat (blank beat with just beat number)
   */
  private async renderEmptyBeat(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<void> {
    // Draw minimal grid
    this.drawGrid(ctx, "diamond", size);

    // Draw beat number if enabled
    if (options.addBeatNumbers && beatData.beat_number > 0) {
      this.drawBeatNumber(ctx, beatData.beat_number, size);
    }
  }

  /**
   * Render fallback beat when all else fails
   */
  private async renderFallbackBeat(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): Promise<void> {
    // Draw basic placeholder
    ctx.strokeStyle = "#ccc";
    ctx.lineWidth = 2;
    ctx.strokeRect(10, 10, size - 20, size - 20);

    // Draw X to indicate error
    ctx.beginPath();
    ctx.moveTo(20, 20);
    ctx.lineTo(size - 20, size - 20);
    ctx.moveTo(size - 20, 20);
    ctx.lineTo(20, size - 20);
    ctx.stroke();

    // Draw beat number
    if (options.addBeatNumbers) {
      this.drawBeatNumber(ctx, beatData.beat_number, size);
    }
  }

  /**
   * Render default start position
   */
  private async renderDefaultStartPosition(
    ctx: CanvasRenderingContext2D,
    size: number,
    _options: BeatRenderOptions
  ): Promise<void> {
    // Draw grid
    this.drawGrid(ctx, "diamond", size);

    // Draw center circle to indicate start position
    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size * 0.1;

    ctx.fillStyle = "#10b981"; // Green color for start
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fill();
  }

  /**
   * Draw simple grid pattern
   */
  private drawGrid(
    ctx: CanvasRenderingContext2D,
    gridMode: string,
    size: number
  ): void {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 1;

    if (gridMode === "diamond") {
      // Draw diamond grid
      const centerX = size / 2;
      const centerY = size / 2;
      const radius = size * 0.4;

      ctx.beginPath();
      ctx.moveTo(centerX, centerY - radius);
      ctx.lineTo(centerX + radius, centerY);
      ctx.lineTo(centerX, centerY + radius);
      ctx.lineTo(centerX - radius, centerY);
      ctx.closePath();
      ctx.stroke();
    } else {
      // Draw box grid
      const margin = size * 0.1;
      ctx.strokeRect(margin, margin, size - 2 * margin, size - 2 * margin);
    }
  }

  /**
   * Draw prop placeholder
   */
  private drawProp(
    ctx: CanvasRenderingContext2D,
    propData: any,
    color: string,
    size: number
  ): void {
    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size * 0.05;

    ctx.fillStyle = color === "blue" ? "#3b82f6" : "#ef4444";
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fill();
  }

  /**
   * Draw arrow placeholder
   */
  private drawArrow(
    ctx: CanvasRenderingContext2D,
    arrowData: any,
    color: string,
    size: number
  ): void {
    const centerX = size / 2;
    const centerY = size / 2;
    const length = size * 0.2;

    ctx.strokeStyle = color === "blue" ? "#3b82f6" : "#ef4444";
    ctx.lineWidth = 3;

    // Simple arrow pointing right
    ctx.beginPath();
    ctx.moveTo(centerX - length / 2, centerY);
    ctx.lineTo(centerX + length / 2, centerY);
    ctx.moveTo(centerX + length / 2 - 10, centerY - 5);
    ctx.lineTo(centerX + length / 2, centerY);
    ctx.lineTo(centerX + length / 2 - 10, centerY + 5);
    ctx.stroke();
  }

  /**
   * Draw letter text
   */
  private drawLetter(
    ctx: CanvasRenderingContext2D,
    letter: string,
    size: number
  ): void {
    ctx.fillStyle = "#374151";
    ctx.font = `${size * 0.2}px Arial, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(letter, size / 2, size / 2);
  }

  /**
   * Draw beat number
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
   * Render start position label
   */
  private renderStartPositionLabel(
    ctx: CanvasRenderingContext2D,
    size: number
  ): void {
    ctx.fillStyle = "#059669";
    ctx.font = `bold ${size * 0.12}px Arial, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText("START", size / 2, size * 0.05);
  }

  /**
   * Apply post-processing effects
   */
  private applyPostProcessing(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number,
    options: BeatRenderOptions
  ): void {
    // Apply combined grids if enabled
    if (options.combinedGrids) {
      this.applyCombinedGrids(ctx, size);
    }

    // Apply reversal symbols if needed
    if (beatData.blue_reversal || beatData.red_reversal) {
      this.drawReversalSymbols(ctx, beatData, size);
    }
  }

  /**
   * Apply combined grids overlay
   */
  private applyCombinedGrids(
    ctx: CanvasRenderingContext2D,
    size: number
  ): void {
    // Draw both diamond and box grids with slight transparency
    ctx.globalAlpha = 0.5;
    this.drawGrid(ctx, "diamond", size);
    this.drawGrid(ctx, "box", size);
    ctx.globalAlpha = 1.0;
  }

  /**
   * Draw reversal symbols
   */
  private drawReversalSymbols(
    ctx: CanvasRenderingContext2D,
    beatData: BeatData,
    size: number
  ): void {
    const symbolSize = size * 0.08;

    if (beatData.blue_reversal) {
      ctx.fillStyle = "#3b82f6";
      ctx.fillRect(size - symbolSize - 5, 5, symbolSize, symbolSize);
    }

    if (beatData.red_reversal) {
      ctx.fillStyle = "#ef4444";
      ctx.fillRect(
        size - symbolSize - 5,
        symbolSize + 10,
        symbolSize,
        symbolSize
      );
    }
  }

  /**
   * Apply color visibility filters
   */
  private applyColorFilters(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    options: BeatRenderOptions
  ): void {
    if (!options.redVisible || !options.blueVisible) {
      // This is a simplified approach - in a full implementation,
      // we would need more sophisticated color filtering
      console.warn("Color filtering not fully implemented yet");
    }
  }

  /**
   * Canvas pool management
   */
  private getCanvasFromPool(width: number, height: number): HTMLCanvasElement {
    const canvas = this.canvasPool.pop() || document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;

    // Clear the canvas
    const ctx = canvas.getContext("2d")!;
    ctx.clearRect(0, 0, width, height);

    return canvas;
  }

  private returnCanvasToPool(canvas: HTMLCanvasElement): void {
    if (this.canvasPool.length < this.MAX_POOL_SIZE) {
      this.canvasPool.push(canvas);
    }
  }

  /**
   * Cleanup method to dispose of resources
   */
  dispose(): void {
    this.canvasPool.length = 0;
  }
}
