/**
 * Fallback Arrow Service Interface
 *
 * Provides fallback arrow rendering when main arrow services fail.
 * Part of the arrow domain's resilience strategy.
 */

import type { ArrowPosition, MotionColor } from "$shared";

export interface IFallbackArrowRenderer {
  /**
   * Render arrow using fallback positioning when main service fails
   */
  renderFallbackArrow(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition
  ): void;

  /**
   * Create enhanced arrow SVG path with sophisticated styling
   */
  createEnhancedArrowPath(color: MotionColor): SVGElement;
}
