/**
 * Canvas Renderer for animation visualization
 * Based on the exact implementation from standalone_animator.html
 */

import { GridLocation } from "$shared";
import { injectable } from "inversify";
import { LOCATION_ANGLES, PI } from "../../domain/math-constants";
import type { PropState } from "../../domain/types/PropState";
import type { ICanvasRenderer } from "../contracts/ICanvasRenderer";

// Constants from standalone_animator.html
// Using "strict" hand point offset (actual hand position, further from center)
// From gridCoordinates.ts: n_diamond_hand_point_strict at (475, 325.0) = 150px from center
const GRID_HALFWAY_POINT_OFFSET = 150;

/**
 * Convert angle (radians) to nearest GridLocation for human-readable logging
 */
function angleToGridLocation(angle: number): string {
  // Normalize angle to [0, 2π)
  let normalized = angle % (2 * PI);
  if (normalized < 0) normalized += 2 * PI;

  // Find closest grid location
  let closestLoc = GridLocation.EAST;
  let minDiff = Infinity;

  for (const [loc, locAngle] of Object.entries(LOCATION_ANGLES)) {
    let diff = Math.abs(normalized - locAngle);
    // Handle wrap-around (e.g., comparing 0° and 350°)
    if (diff > PI) diff = 2 * PI - diff;

    if (diff < minDiff) {
      minDiff = diff;
      closestLoc = loc as GridLocation;
    }
  }

  return closestLoc.toUpperCase();
}

@injectable()
export class CanvasRenderer implements ICanvasRenderer {
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
    bluePropViewBoxDimensions: { width: number; height: number } = {
      width: 252.8,
      height: 77.8,
    },
    redPropViewBoxDimensions: { width: number; height: number } = {
      width: 252.8,
      height: 77.8,
    }
  ): void {
    // Rendering logging removed - too noisy, use beat transition logging instead

    // Clear canvas exactly as in standalone
    ctx.clearRect(0, 0, canvasSize, canvasSize);

    // Draw white background (required for GIF export)
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvasSize, canvasSize);

    // Draw grid exactly as in standalone
    this.drawGrid(ctx, canvasSize, gridVisible, gridImage);

    // Draw props with their viewBox dimensions
    if (blueStaffImage) {
      this.drawStaff(
        ctx,
        canvasSize,
        blueProp,
        blueStaffImage,
        bluePropViewBoxDimensions
      );
    }

    if (redStaffImage) {
      this.drawStaff(
        ctx,
        canvasSize,
        redProp,
        redStaffImage,
        redPropViewBoxDimensions
      );
    }
  }

  /**
   * Render a letter glyph onto the canvas at the standard position
   * This is called separately during GIF export to overlay the glyph
   */
  renderLetterToCanvas(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    letterImage: HTMLImageElement,
    letterViewBoxDimensions: { width: number; height: number }
  ): void {
    this.drawLetter(ctx, canvasSize, letterImage, letterViewBoxDimensions);
  }

  /**
   * Draw grid exactly as in standalone_animator.html
   */
  private drawGrid(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    gridVisible: boolean,
    gridImage: HTMLImageElement | null
  ): void {
    if (!gridVisible || !gridImage) return;
    ctx.drawImage(gridImage, 0, 0, canvasSize, canvasSize);
  }

  /**
   * Draw prop with proper aspect ratio preservation
   * The prop's length (height in viewBox) is constrained to fit between center and outer point,
   * and the width is scaled proportionally to preserve the aspect ratio.
   *
   * For dash motions, uses pre-calculated Cartesian x,y coordinates for straight-line movement.
   * For other motions, calculates position from angle using polar coordinates.
   */
  private drawStaff(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    propState: PropState,
    staffImage: HTMLImageElement,
    viewBoxDimensions: { width: number; height: number }
  ): void {
    if (!propState) return;

    // Calculate position
    const centerX = canvasSize / 2;
    const centerY = canvasSize / 2;
    const inwardFactor = 0.95;
    const gridScaleFactor = canvasSize / 950; // 950 is the viewBox size
    const scaledHalfwayRadius = GRID_HALFWAY_POINT_OFFSET * gridScaleFactor;

    // Use pre-calculated x,y if provided (dash motions), otherwise calculate from angle
    let x: number, y: number;
    const staffAngle = ((propState.staffRotationAngle * 180) / Math.PI).toFixed(
      0
    );
    if (propState.x !== undefined && propState.y !== undefined) {
      // Dash motion: use Cartesian coordinates directly (already in unit circle space)
      x = centerX + propState.x * scaledHalfwayRadius * inwardFactor;
      y = centerY + propState.y * scaledHalfwayRadius * inwardFactor;
    } else {
      // Regular motion: calculate from angle using polar coordinates
      x =
        centerX +
        Math.cos(propState.centerPathAngle) *
          scaledHalfwayRadius *
          inwardFactor;
      y =
        centerY +
        Math.sin(propState.centerPathAngle) *
          scaledHalfwayRadius *
          inwardFactor;
    }

    // Scale the prop dimensions from viewBox coordinate space to canvas pixels
    // This preserves the aspect ratio of the prop
    const propWidth = viewBoxDimensions.width * gridScaleFactor;
    const propHeight = viewBoxDimensions.height * gridScaleFactor;

    // Calculate center point from viewBox dimensions
    const propCenterX = viewBoxDimensions.width / 2;
    const propCenterY = viewBoxDimensions.height / 2;

    // Draw the prop
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(propState.staffRotationAngle);
    ctx.drawImage(
      staffImage,
      -propCenterX * gridScaleFactor,
      -propCenterY * gridScaleFactor,
      propWidth,
      propHeight
    );
    ctx.restore();
  }

  /**
   * Draw letter glyph in the bottom-left area of the canvas
   * Position matches the SVG overlay positioning: x=50, y=800 in 950px viewBox
   */
  private drawLetter(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    letterImage: HTMLImageElement,
    letterViewBoxDimensions: { width: number; height: number }
  ): void {
    if (!letterImage) return;

    const gridScaleFactor = canvasSize / 950; // 950 is the viewBox size

    // Position matches TKAGlyph.svelte defaults: x=50, y=800 in 950px viewBox
    const x = 50 * gridScaleFactor;
    const y = 800 * gridScaleFactor;

    // Scale letter to match canvas size relative to 950px viewBox (same as props and grid)
    // All SVGs are designed relative to the 950×950 viewBox, so we use gridScaleFactor consistently
    const scaledWidth = letterViewBoxDimensions.width * gridScaleFactor;
    const scaledHeight = letterViewBoxDimensions.height * gridScaleFactor;

    ctx.drawImage(letterImage, x, y, scaledWidth, scaledHeight);
  }
}
