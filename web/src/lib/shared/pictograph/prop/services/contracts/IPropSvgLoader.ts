/**
 * Prop SVG Loader Interface
 *
 * Fast, direct SVG loading for props - mirrors arrow loading approach
 */

import type { MotionData, PropPlacementData } from "$shared";
import type { PropRenderData } from "../../domain/models/PropRenderData";

export interface IPropSvgLoader {
  /**
   * Load prop SVG data with color transformation - fast direct approach
   */
  loadPropSvg(
    propData: PropPlacementData,
    motionData: MotionData
  ): Promise<PropRenderData>;

  /**
   * Fetch SVG content from a given path - direct fetch
   */
  fetchSvgContent(path: string): Promise<string>;
}
