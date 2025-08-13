/**
 * Canvas Renderer for animation visualization
 * Based on the exact implementation from standalone_animator.html
 */

import type { PropState } from "../../types/core.js";

// Constants from standalone_animator.html
const GRID_HALFWAY_POINT_OFFSET = 151.5;
const STAFF_VIEWBOX_WIDTH = 252.8;
const STAFF_VIEWBOX_HEIGHT = 77.8;
const STAFF_CENTER_X = 126.4;
const STAFF_CENTER_Y = 38.9;

export class CanvasRenderer {
  /**
   * Render the complete animation scene exactly as in standalone_animator.html
   */
  static renderScene(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    gridVisible: boolean,
    gridImage: HTMLImageElement | null,
    blueStaffImage: HTMLImageElement | null,
    redStaffImage: HTMLImageElement | null,
    blueProp: PropState,
    redProp: PropState,
  ): void {
    // Clear canvas exactly as in standalone
    ctx.clearRect(0, 0, canvasSize, canvasSize);

    // Draw grid exactly as in standalone
    this.drawGrid(ctx, canvasSize, gridVisible, gridImage);

    // Draw staffs exactly as in standalone
    if (blueStaffImage) {
      this.drawStaff(ctx, canvasSize, blueProp, blueStaffImage);
    }

    if (redStaffImage) {
      this.drawStaff(ctx, canvasSize, redProp, redStaffImage);
    }
  }

  /**
   * Draw grid exactly as in standalone_animator.html
   */
  private static drawGrid(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    gridVisible: boolean,
    gridImage: HTMLImageElement | null,
  ): void {
    if (!gridVisible || !gridImage) return;
    ctx.drawImage(gridImage, 0, 0, canvasSize, canvasSize);
  }

  /**
   * Draw staff exactly as in standalone_animator.html
   */
  private static drawStaff(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    propState: PropState,
    staffImage: HTMLImageElement,
  ): void {
    if (!propState) return;

    // Calculate position exactly as in standalone
    const centerX = canvasSize / 2;
    const centerY = canvasSize / 2;
    const inwardFactor = 0.95;
    const gridScaleFactor = canvasSize / 950; // 950 is the viewBox size from standalone
    const scaledHalfwayRadius = GRID_HALFWAY_POINT_OFFSET * gridScaleFactor;

    const x =
      centerX +
      Math.cos(propState.centerPathAngle) * scaledHalfwayRadius * inwardFactor;
    const y =
      centerY +
      Math.sin(propState.centerPathAngle) * scaledHalfwayRadius * inwardFactor;

    const staffWidth = STAFF_VIEWBOX_WIDTH * gridScaleFactor;
    const staffHeight = STAFF_VIEWBOX_HEIGHT * gridScaleFactor;

    // 🔧 [RENDER DEBUG] Log rendering values
    console.log("🔧 [RENDER DEBUG] Drawing staff:", {
      canvasSize: canvasSize,
      centerX: centerX,
      centerY: centerY,
      gridScaleFactor: gridScaleFactor,
      scaledHalfwayRadius: scaledHalfwayRadius,
      inwardFactor: inwardFactor,
      centerPathAngle: propState.centerPathAngle,
      centerPathAngleDegrees: (
        (propState.centerPathAngle * 180) /
        Math.PI
      ).toFixed(1),
      staffRotationAngle: propState.staffRotationAngle,
      staffRotationAngleDegrees: (
        (propState.staffRotationAngle * 180) /
        Math.PI
      ).toFixed(1),
      calculatedX: x,
      calculatedY: y,
      propStateX: propState.x,
      propStateY: propState.y,
    });

    // Draw exactly as in standalone
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(propState.staffRotationAngle);
    ctx.drawImage(
      staffImage,
      -STAFF_CENTER_X * gridScaleFactor,
      -STAFF_CENTER_Y * gridScaleFactor,
      staffWidth,
      staffHeight,
    );
    ctx.restore();
  }
}
