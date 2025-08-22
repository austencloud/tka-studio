/**
 * Arrow Positioning Service Interface
 *
 * Handles positioning and rendering arrows in SVG containers.
 */

import type { MotionData } from "$lib/domain";
import { MotionColor } from "$lib/domain/enums";
import type { ArrowPosition } from "$lib/services/positioning/types";

export interface IArrowPositioningService {
  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;
}
