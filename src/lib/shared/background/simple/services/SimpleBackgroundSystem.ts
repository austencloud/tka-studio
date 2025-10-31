/**
 * Simple Background System
 *
 * Implements IBackgroundSystem for static backgrounds (solid colors and gradients).
 * No animation - just renders a static background.
 */

import type {
  AccessibilitySettings,
  Dimensions,
  IBackgroundSystem,
  QualityLevel,
} from "$shared";

export interface SimpleBackgroundConfig {
  type: "solid" | "gradient";
  color?: string; // For solid backgrounds
  colors?: string[]; // For gradient backgrounds (2-4 colors)
  direction?: number; // Gradient angle in degrees (0-360)
}

export class SimpleBackgroundSystem implements IBackgroundSystem {
  private config: SimpleBackgroundConfig;

  constructor(config: SimpleBackgroundConfig) {
    this.config = config;
  }

  /**
   * Initialize the background system (no-op for simple backgrounds)
   */
  initialize(_dimensions: Dimensions, _quality: QualityLevel): void {
    // No initialization needed for static backgrounds
  }

  /**
   * Update the background system (no-op for simple backgrounds)
   */
  update(_dimensions: Dimensions, _frameMultiplier?: number): void {
    // No animation updates needed for static backgrounds
  }

  /**
   * Draw the background to the canvas
   */
  draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    // Clear the entire canvas first to remove any previous background elements
    ctx.clearRect(0, 0, dimensions.width, dimensions.height);

    if (this.config.type === "solid") {
      this.drawSolidColor(ctx, dimensions);
    } else {
      this.drawGradient(ctx, dimensions);
    }
  }

  /**
   * Draw a solid color background
   */
  private drawSolidColor(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    ctx.fillStyle = this.config.color || "#1a1a2e";
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  /**
   * Draw a linear gradient background
   */
  private drawGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    const colors = this.config.colors || ["#667eea", "#764ba2"];
    const direction = this.config.direction || 135;

    // Convert angle to radians
    const angleRad = (direction * Math.PI) / 180;

    // Calculate gradient start and end points based on angle
    const centerX = dimensions.width / 2;
    const centerY = dimensions.height / 2;
    const maxDist = Math.sqrt(centerX * centerX + centerY * centerY);

    const x0 = centerX - Math.cos(angleRad) * maxDist;
    const y0 = centerY - Math.sin(angleRad) * maxDist;
    const x1 = centerX + Math.cos(angleRad) * maxDist;
    const y1 = centerY + Math.sin(angleRad) * maxDist;

    // Create gradient
    const gradient = ctx.createLinearGradient(x0, y0, x1, y1);

    // Add color stops
    const numColors = colors.length;
    colors.forEach((color, index) => {
      const stop = index / (numColors - 1);
      gradient.addColorStop(stop, color);
    });

    // Fill with gradient
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  /**
   * Set the quality level (no-op for simple backgrounds)
   */
  setQuality(_quality: QualityLevel): void {
    // Quality doesn't affect static backgrounds
  }

  /**
   * Clean up resources (no-op for simple backgrounds)
   */
  cleanup(): void {
    // No resources to clean up
  }

  /**
   * Handle resize events (no-op for simple backgrounds)
   */
  handleResize?(_oldDimensions: Dimensions, _newDimensions: Dimensions): void {
    // No resize handling needed for static backgrounds
  }

  /**
   * Set accessibility settings (no-op for simple backgrounds)
   */
  setAccessibility?(_settings: AccessibilitySettings): void {
    // Accessibility doesn't affect static backgrounds
  }

  /**
   * Update the background configuration
   */
  updateConfig(config: Partial<SimpleBackgroundConfig>): void {
    this.config = { ...this.config, ...config };
  }
}
