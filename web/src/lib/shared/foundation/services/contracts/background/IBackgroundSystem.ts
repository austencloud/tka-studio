/**
 * Background System Interface
 *
 * Base interface for all background animation systems.
 * Defines the common contract that all background systems must implement.
 */

import type {
  AccessibilitySettings,
  Dimensions,
  QualityLevel,
} from "$shared/domain";

// Use the correct PerformanceMetrics from BackgroundTypes
import type { PerformanceMetrics } from "$shared/domain/ui/backgrounds/BackgroundTypes";

export interface IBackgroundSystem {
  /**
   * Initialize the background system with dimensions and quality
   */
  initialize(dimensions: Dimensions, quality: QualityLevel): void;

  /**
   * Update the background system animation state
   */
  update(dimensions: Dimensions): void;

  /**
   * Draw the background system to the canvas
   */
  draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void;

  /**
   * Set the quality level for the background system
   */
  setQuality(quality: QualityLevel): void;

  /**
   * Clean up resources used by the background system
   */
  cleanup(): void;

  /**
   * Handle resize events (optional)
   */
  handleResize?(oldDimensions: Dimensions, newDimensions: Dimensions): void;

  /**
   * Set accessibility settings (optional)
   */
  setAccessibility?(settings: AccessibilitySettings): void;

  /**
   * Get performance metrics (optional)
   */
  getMetrics?(): PerformanceMetrics;
}
