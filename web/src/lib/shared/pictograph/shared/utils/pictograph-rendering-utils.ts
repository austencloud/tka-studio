/**
 * Pictograph Rendering Utilities
 *
 * Direct composition functions for rendering pictographs without orchestration service.
 * This replaces the PictographRenderingService with explicit composition.
 */

import {
    GridMode,
    MotionColor,
    resolve,
    TYPES,
    type IArrowPositioningOrchestrator,
    type IGridModeDeriver,
    type MotionData,
    type PictographData,
} from "$shared";
import { Point } from "fabric";
import type { IOverlayRenderer } from "../../../../modules/animator/services/implementations/OverlayRenderer";
import type { ISvgUtilityService } from "../../../../modules/animator/services/implementations/SvgUtilityService";
import type { ArrowPosition } from "../../arrow";
import type { IArrowRenderer } from "../../arrow/rendering/services/contracts";
import type { IGridRenderingService } from "../../grid";


export async function renderPictograph(
  data: PictographData
): Promise<SVGElement> {
  try {
    // Resolve required services directly
    const svgUtility = resolve<ISvgUtilityService>(TYPES.ISvgUtilityService);
    const gridRendering = resolve<IGridRenderingService>(
      TYPES.IGridRenderingService
    );
    const arrowRendering = resolve<IArrowRenderer>(TYPES.IArrowRenderer);
    const overlayRendering = resolve<IOverlayRenderer>(TYPES.IOverlayRenderer);
    const gridModeService = resolve<IGridModeDeriver>(TYPES.IGridModeDeriver);

    // Get arrow positioning from InversifyJS container
    const arrowPositioning: IArrowPositioningOrchestrator = resolve(
      TYPES.IArrowPositioningOrchestrator
    );

    // Create base SVG
    const svg = svgUtility.createBaseSVG();

    // Determine grid mode
    const gridMode: GridMode =
      data.motions?.blue && data.motions?.red
        ? gridModeService.deriveGridMode(data.motions.blue, data.motions.red)
        : GridMode.DIAMOND;

    // Render grid
    await gridRendering.renderGrid(svg, gridMode);

    // Calculate arrow positions
    const updatedPictographData =
      await arrowPositioning.calculateAllArrowPoints(data);

    // Render arrows
    if (updatedPictographData.motions) {
      for (const [color, motionData] of Object.entries(
        updatedPictographData.motions
      )) {
        const motion = motionData as MotionData;
        if (motion?.isVisible && motion.arrowPlacementData) {
          const position = Object.assign(
            new Point(
              motion.arrowPlacementData.positionX,
              motion.arrowPlacementData.positionY
            ),
            { rotation: motion.arrowPlacementData.rotationAngle }
          );
          await arrowRendering.renderArrowAtPosition(
            svg,
            color as MotionColor,
            position,
            motion
          );
        }
      }
    }

    // Render overlays
    await overlayRendering.renderOverlays(svg, data);
    overlayRendering.renderIdLabel(svg, data);

    // Render debug info
    const arrowPositions = new Map<string, ArrowPosition>();
    if (updatedPictographData.motions) {
      for (const [color, motionData] of Object.entries(
        updatedPictographData.motions
      )) {
        const motion = motionData as MotionData;
        if (motion?.isVisible && motion.arrowPlacementData) {
          const arrowPosition = Object.assign(
            new Point(
              motion.arrowPlacementData.positionX,
              motion.arrowPlacementData.positionY
            ),
            { rotation: motion.arrowPlacementData.rotationAngle }
          );
          arrowPositions.set(color, arrowPosition);
        }
      }
    }
    overlayRendering.renderDebugInfo(svg, data, arrowPositions);

    return svg;
  } catch (error) {
    console.error("❌ Error rendering pictograph:", error);
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error";
    const svgUtility = resolve<ISvgUtilityService>(TYPES.ISvgUtilityService);
    return svgUtility.createErrorSVG(errorMessage);
  }
}

/**
 * Batch render multiple pictographs
 */
export async function renderPictographs(
  dataArray: PictographData[]
): Promise<SVGElement[]> {
  const promises = dataArray.map((data) => renderPictograph(data));
  return Promise.all(promises);
}
