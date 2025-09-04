/**
 * Simple Beat Grid Service
 * Embeds SVG grid data directly - no file loading needed
 */

import {
  GridMode,
  type CombinedGridOptions,
  type GridDrawOptions,
  type GridValidationResult,
} from "$domain";
import type { IBeatGridService } from "$services";
import { injectable } from "inversify";

@injectable()
export class BeatGridService implements IBeatGridService {
  private gridImageCache = new Map<GridMode, HTMLImageElement>();

  // Embedded SVG data - copied directly from your static files
  private readonly BOX_GRID_SVG = `
    <svg viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg">
      <circle id="center_point" cx="475" cy="475" r="11.2"/>
      <circle id="ne_box_outer_point" cx="262.9" cy="262.9" r="17.7"/>
      <circle id="se_box_outer_point" cx="687.1" cy="262.9" r="17.7"/>
      <circle id="sw_box_outer_point" cx="687.1" cy="687.1" r="17.7"/>
      <circle id="nw_box_outer_point" cx="262.9" cy="687.1" r="17.7"/>
      <circle id="nw_box_hand_point" cx="373.8" cy="373.8" r="8"/>
      <circle id="ne_box_hand_point" cx="576.2" cy="373.8" r="8"/>
      <circle id="se_box_hand_point" cx="576.2" cy="576.2" r="8"/>
      <circle id="sw_box_hand_point" cx="373.8" cy="576.2" r="8"/>
    </svg>`;

  private readonly DIAMOND_GRID_SVG = `
    <svg viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg">
      <circle id="n_diamond_outer_point" cx="475" cy="175" r="25"/>
      <circle id="e_diamond_outer_point" cx="775" cy="475" r="25"/>
      <circle id="s_diamond_outer_point" cx="475" cy="775" r="25"/>
      <circle id="w_diamond_outer_point" cx="175" cy="475" r="25"/>
      <circle id="n_diamond_hand_point" cx="475" cy="331.9" r="8"/>
      <circle id="e_diamond_hand_point" cx="618.1" cy="475" r="8"/>
      <circle id="s_diamond_hand_point" cx="475" cy="618.1" r="8"/>
      <circle id="w_diamond_hand_point" cx="331.9" cy="475" r="8"/>
      <circle id="center_point" cx="475" cy="475" r="12"/>
    </svg>`;

  /**
   * Draw grid using embedded SVG data
   */
  drawGrid(
    ctx: CanvasRenderingContext2D,
    gridMode: GridMode,
    options: GridDrawOptions
  ): void {
    const img = this.getGridImage(gridMode);
    const size = options.size || 120; // Default size if not provided

    ctx.save();
    ctx.globalAlpha = options.opacity || 0.6;
    ctx.drawImage(img, 0, 0, size, size);
    ctx.restore();
  }

  /**
   * Apply combined grids
   */
  applyCombinedGrids(
    canvas: HTMLCanvasElement,
    options: CombinedGridOptions
  ): HTMLCanvasElement {
    const ctx = canvas.getContext("2d");
    if (!ctx) throw new Error("Could not get 2D context from canvas");

    // Draw primary grid
    this.drawGrid(ctx, options.primaryGridMode, {
      size: canvas.width,
      opacity: options.primaryOpacity || 0.6,
    });

    // Draw overlay grid if specified
    if (options.overlayGridMode) {
      this.drawGrid(ctx, options.overlayGridMode, {
        size: canvas.width,
        opacity: options.overlayOpacity || 0.3,
      });
    }

    return canvas;
  }

  /**
   * Get opposite grid mode
   */
  getOppositeGridMode(currentMode: GridMode): GridMode {
    return currentMode === GridMode.BOX ? GridMode.DIAMOND : GridMode.BOX;
  }

  /**
   * Determine grid mode from beat data
   */
  getGridModeForBeat(_beatData: unknown): GridMode {
    return GridMode.DIAMOND;
  }

  /**
   * Return embedded SVG string
   */
  createGridSVG(gridMode: GridMode): string {
    return gridMode === GridMode.BOX
      ? this.BOX_GRID_SVG
      : this.DIAMOND_GRID_SVG;
  }

  // Simple stubs for interface compatibility
  drawGridPoints(): void {}
  validateGridOptions(): GridValidationResult {
    return { isValid: true, errors: [], warnings: [] };
  }
  getGridMetrics() {
    return { spacing: 0, points: [], lines: [] };
  }
  getDefaultGridOptions(gridMode: GridMode): GridDrawOptions {
    return {
      size: 120,
      opacity: gridMode === GridMode.BOX ? 0.5 : 0.6,
      lineWidth: 1,
      strokeStyle: "#e0e0e0",
      padding: 10,
    };
  }
  areGridModesCompatible(primary: GridMode, overlay: GridMode): boolean {
    return primary !== overlay;
  }

  /**
   * Get cached grid image from embedded SVG
   */
  private getGridImage(gridMode: GridMode): HTMLImageElement {
    const cachedImage = this.gridImageCache.get(gridMode);
    if (cachedImage) {
      return cachedImage;
    }

    const svgString = this.createGridSVG(gridMode);
    const img = new Image();
    const blob = new Blob([svgString], { type: "image/svg+xml" });
    img.src = URL.createObjectURL(blob);

    this.gridImageCache.set(gridMode, img);
    return img;
  }
}
