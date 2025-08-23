/**
 * Simple Grid Service
 * Just loads the pre-existing SVG grid files instead of recreating them
 */

import { GridMode } from "$lib/domain/enums";

export class BeatGridService {
  private gridCache = new Map<string, string>();

  /**
   * Draw grid on canvas by loading the pre-existing SVG
   */
  async drawGrid(
    ctx: CanvasRenderingContext2D,
    gridMode: GridMode,
    options: { size: number; opacity?: number }
  ): Promise<void> {
    const svgString = await this.getGridSVG(gridMode);
    const img = await this.svgToImage(svgString, options.size);

    ctx.save();
    ctx.globalAlpha = options.opacity || 0.6;
    ctx.drawImage(img, 0, 0, options.size, options.size);
    ctx.restore();
  }

  /**
   * Get the SVG string for a grid mode
   */
  private async getGridSVG(gridMode: GridMode): Promise<string> {
    const filename =
      gridMode === GridMode.BOX ? "box_grid.svg" : "diamond_grid.svg";

    if (this.gridCache.has(filename)) {
      return this.gridCache.get(filename)!;
    }

    const response = await fetch(`/${filename}`);
    const svgString = await response.text();
    this.gridCache.set(filename, svgString);
    return svgString;
  }

  /**
   * Convert SVG string to image
   */
  private async svgToImage(
    svgString: string,
    _size: number
  ): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;

      const blob = new Blob([svgString], { type: "image/svg+xml" });
      img.src = URL.createObjectURL(blob);
    });
  }
}
