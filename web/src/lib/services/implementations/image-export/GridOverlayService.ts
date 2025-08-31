/**
 * Grid Overlay Service
 *
 * Handles combined grid overlays for TKA image export. This service implements
 * the functionality equivalent to desktop CombinedGridHandler, allowing both
 * diamond and box grids to be displayed simultaneously.
 *
 * Critical: Must match desktop overlay opacity and positioning exactly.
 */

import { GridMode } from "$domain";
import { injectable } from "inversify";
import type { IGridOverlayService } from "../../contracts/image-export-interfaces";

@injectable()
export class GridOverlayService implements IGridOverlayService {
  // Grid constants
  private static readonly GRID_OPACITY = 1.0; // Desktop uses 100% opacity
  private static readonly GRID_COLOR = "#e5e7eb"; // Light gray
  private static readonly GRID_LINE_WIDTH = 1;

  /**
   * Apply combined grids to beat canvas
   * Matches desktop CombinedGridHandler.process_beat_for_combined_grids
   */
  applyCombinedGrids(
    canvas: HTMLCanvasElement,
    currentGridMode: GridMode
  ): HTMLCanvasElement {
    if (!this.validateGridMode(currentGridMode)) {
      throw new Error(`Invalid grid mode: ${currentGridMode}`);
    }

    // Create new canvas for combined result
    const combinedCanvas = document.createElement("canvas");
    combinedCanvas.width = canvas.width;
    combinedCanvas.height = canvas.height;

    const ctx = combinedCanvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from combined canvas");
    }

    // Step 1: Draw original canvas
    ctx.drawImage(canvas, 0, 0);

    // Step 2: Add opposite grid with full opacity (match desktop)
    const oppositeGridMode = this.getOppositeGridMode(currentGridMode);
    this.drawGridOverlay(
      ctx,
      oppositeGridMode,
      canvas.width,
      GridOverlayService.GRID_OPACITY
    );

    return combinedCanvas;
  }

  /**
   * Draw grid overlay on canvas
   * Implements both diamond and box grid patterns
   */
  drawGridOverlay(
    ctx: CanvasRenderingContext2D,
    gridMode: GridMode,
    size: number,
    opacity: number = 1.0
  ): void {
    if (!this.validateGridMode(gridMode)) {
      throw new Error(`Invalid grid mode: ${gridMode}`);
    }

    // Save current context state
    ctx.save();

    // Set grid drawing properties
    ctx.globalAlpha = opacity;
    ctx.strokeStyle = GridOverlayService.GRID_COLOR;
    ctx.lineWidth = GridOverlayService.GRID_LINE_WIDTH;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    if (gridMode === GridMode.DIAMOND) {
      this.drawDiamondGrid(ctx, size);
    } else if (gridMode === GridMode.BOX) {
      this.drawBoxGrid(ctx, size);
    }

    // Restore context state
    ctx.restore();
  }

  /**
   * Get opposite grid mode
   * Matches desktop logic exactly
   */
  getOppositeGridMode(currentMode: GridMode): GridMode {
    switch (currentMode) {
      case GridMode.DIAMOND:
        return GridMode.BOX;
      case GridMode.BOX:
        return GridMode.DIAMOND;
      default:
        throw new Error(`Unknown grid mode: ${currentMode}`);
    }
  }

  /**
   * Validate grid modes - only accepts proper GridMode enum
   */
  validateGridMode(gridMode: GridMode): boolean {
    const validModes = [GridMode.DIAMOND, GridMode.BOX];
    return validModes.includes(gridMode);
  }

  /**
   * Draw diamond grid pattern
   * Matches desktop diamond grid implementation
   */
  private drawDiamondGrid(ctx: CanvasRenderingContext2D, size: number): void {
    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size * 0.4; // Standard diamond size

    ctx.beginPath();

    // Draw diamond shape
    ctx.moveTo(centerX, centerY - radius); // Top point
    ctx.lineTo(centerX + radius, centerY); // Right point
    ctx.lineTo(centerX, centerY + radius); // Bottom point
    ctx.lineTo(centerX - radius, centerY); // Left point
    ctx.closePath();

    ctx.stroke();

    // Add grid lines inside diamond (optional enhancement)
    this.drawDiamondGridLines(ctx, centerX, centerY, radius);
  }

  /**
   * Draw box grid pattern
   * Matches desktop box grid implementation
   */
  private drawBoxGrid(ctx: CanvasRenderingContext2D, size: number): void {
    const margin = size * 0.1; // Standard box margin
    const boxSize = size - 2 * margin;

    // Draw main box
    ctx.strokeRect(margin, margin, boxSize, boxSize);

    // Add grid lines inside box (optional enhancement)
    this.drawBoxGridLines(ctx, margin, margin, boxSize);
  }

  /**
   * Draw internal grid lines for diamond
   */
  private drawDiamondGridLines(
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    radius: number
  ): void {
    // Lighter opacity for internal lines
    const originalAlpha = ctx.globalAlpha;
    ctx.globalAlpha = originalAlpha * 0.5;

    // Draw horizontal and vertical center lines
    ctx.beginPath();

    // Horizontal line
    ctx.moveTo(centerX - radius * 0.7, centerY);
    ctx.lineTo(centerX + radius * 0.7, centerY);

    // Vertical line
    ctx.moveTo(centerX, centerY - radius * 0.7);
    ctx.lineTo(centerX, centerY + radius * 0.7);

    ctx.stroke();

    // Restore original alpha
    ctx.globalAlpha = originalAlpha;
  }

  /**
   * Draw internal grid lines for box
   */
  private drawBoxGridLines(
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    size: number
  ): void {
    // Lighter opacity for internal lines
    const originalAlpha = ctx.globalAlpha;
    ctx.globalAlpha = originalAlpha * 0.5;

    ctx.beginPath();

    // Draw center cross
    const centerX = x + size / 2;
    const centerY = y + size / 2;

    // Horizontal line
    ctx.moveTo(x, centerY);
    ctx.lineTo(x + size, centerY);

    // Vertical line
    ctx.moveTo(centerX, y);
    ctx.lineTo(centerX, y + size);

    ctx.stroke();

    // Restore original alpha
    ctx.globalAlpha = originalAlpha;
  }

  /**
   * Create grid overlay as separate canvas
   * Useful for caching grid patterns
   */
  createGridCanvas(gridMode: GridMode, size: number): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from grid canvas");
    }

    // Fill with transparent background
    ctx.clearRect(0, 0, size, size);

    // Draw grid
    this.drawGridOverlay(ctx, gridMode, size);

    return canvas;
  }

  /**
   * Apply grid overlay with custom blend mode
   */
  applyGridWithBlendMode(
    canvas: HTMLCanvasElement,
    gridMode: GridMode,
    blendMode: GlobalCompositeOperation = "source-over"
  ): HTMLCanvasElement {
    const result = document.createElement("canvas");
    result.width = canvas.width;
    result.height = canvas.height;

    const ctx = result.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from result canvas");
    }

    // Draw original canvas
    ctx.drawImage(canvas, 0, 0);

    // Set blend mode and draw grid
    ctx.globalCompositeOperation = blendMode;
    this.drawGridOverlay(ctx, gridMode, canvas.width);

    // Reset blend mode
    ctx.globalCompositeOperation = "source-over";

    return result;
  }

  /**
   * Create combined grid overlay (both grids at once)
   */
  createCombinedGridOverlay(size: number): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context from canvas");
    }

    // Clear background
    ctx.clearRect(0, 0, size, size);

    // Draw both grids with reduced opacity
    ctx.globalAlpha = 0.7;
    this.drawGridOverlay(ctx, GridMode.DIAMOND, size);
    this.drawGridOverlay(ctx, GridMode.BOX, size);
    ctx.globalAlpha = 1.0;

    return canvas;
  }

  /**
   * Get recommended grid overlay settings
   */
  getRecommendedSettings(
    baseGridMode: GridMode,
    purpose: "export" | "preview" | "print"
  ): {
    overlayMode: GridMode;
    opacity: number;
    lineWidth: number;
    color: string;
  } {
    const overlayMode = this.getOppositeGridMode(baseGridMode);

    switch (purpose) {
      case "export":
        return {
          overlayMode,
          opacity: 1.0, // Full opacity for export (match desktop)
          lineWidth: 1,
          color: "#e5e7eb",
        };

      case "preview":
        return {
          overlayMode,
          opacity: 0.8, // Slightly transparent for preview
          lineWidth: 1,
          color: "#d1d5db",
        };

      case "print":
        return {
          overlayMode,
          opacity: 1.0, // Full opacity for print
          lineWidth: 2, // Thicker lines for print
          color: "#9ca3af",
        };

      default:
        throw new Error(`Unknown purpose: ${purpose}`);
    }
  }

  /**
   * Analyze grid contrast against background
   */
  analyzeGridContrast(
    _canvas: HTMLCanvasElement,
    _gridMode: string
  ): {
    averageContrast: number;
    minContrast: number;
    maxContrast: number;
    recommendation: "increase" | "decrease" | "optimal";
  } {
    // Create a test grid overlay
    // const testCanvas = this.createGridCanvas(gridMode, 100); // For future contrast analysis
    // const ctx = testCanvas.getContext("2d")!; // For future contrast analysis
    // const imageData = ctx.getImageData(0, 0, 100, 100); // For future contrast analysis

    // Simplified contrast analysis
    // In a full implementation, this would analyze actual pixel values
    const mockContrast = 0.7; // Placeholder value

    return {
      averageContrast: mockContrast,
      minContrast: mockContrast - 0.1,
      maxContrast: mockContrast + 0.1,
      recommendation: mockContrast > 0.6 ? "optimal" : "increase",
    };
  }

  /**
   * Debug method to test grid rendering
   */
  debugGridRendering(size: number = 200): {
    diamondGrid: HTMLCanvasElement;
    boxGrid: HTMLCanvasElement;
    combinedGrid: HTMLCanvasElement;
  } {
    return {
      diamondGrid: this.createGridCanvas(GridMode.DIAMOND, size),
      boxGrid: this.createGridCanvas(GridMode.BOX, size),
      combinedGrid: this.createCombinedGridOverlay(size),
    };
  }

  /**
   * Batch apply grid overlays to multiple canvases
   */
  batchApplyGrids(
    canvases: HTMLCanvasElement[],
    gridModes: GridMode[]
  ): HTMLCanvasElement[] {
    if (canvases.length !== gridModes.length) {
      throw new Error("Canvas count must match grid mode count");
    }

    return canvases.map((canvas, index) => {
      const gridMode = gridModes[index];
      return this.applyCombinedGrids(canvas, gridMode);
    });
  }

  /**
   * Get supported grid modes
   */
  getSupportedGridModes(): string[] {
    return [GridMode.DIAMOND, GridMode.BOX];
  }

  /**
   * REMOVED: normalizeGridMode is no longer needed with proper enum type safety
   * All methods now accept GridMode enum directly
   */
}
