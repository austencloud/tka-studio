/**
 * Arrow Renderer Interface
 */

import type { ArrowPlacementData, ArrowPosition, MotionColor, MotionData } from "$shared";

export interface IArrowRenderer {
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;

  // Legacy methods for backward compatibility
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null;

  loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }>;

  parseArrowSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  };

  applyColorToSvg(svgText: string, color: MotionColor): string;
}
