/**
 * Canvas Renderer Service Contract
 *
 * Handles rendering of animation visualization on canvas.
 */

import type { PropState } from "../../domain/types/PropState";

export interface ICanvasRenderer {
  /**
   * Render the complete animation scene
   * @param bluePropViewBoxDimensions - ViewBox dimensions from the blue prop SVG (default: staff 252.8 x 77.8)
   * @param redPropViewBoxDimensions - ViewBox dimensions from the red prop SVG (default: staff 252.8 x 77.8)
   */
  renderScene(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    gridVisible: boolean,
    gridImage: HTMLImageElement | null,
    blueStaffImage: HTMLImageElement | null,
    redStaffImage: HTMLImageElement | null,
    blueProp: PropState,
    redProp: PropState,
    bluePropViewBoxDimensions?: { width: number; height: number },
    redPropViewBoxDimensions?: { width: number; height: number }
  ): void;
}
