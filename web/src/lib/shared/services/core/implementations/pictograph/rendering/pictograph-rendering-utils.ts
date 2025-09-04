/**
 * Pictograph Rendering Utilities
 *
 * Direct composition functions for rendering pictographs without orchestration service.
 * This replaces the PictographRenderingService with explicit composition.
 */

import type { MotionData, PictographData } from "$domain";
import { GridMode, MotionColor } from "$domain";
import type {
  IArrowPositioningOrchestrator,
  IArrowRenderer,
  IGridModeDeriver,
  IGridRenderingService,
  IOverlayRenderer,
  ISvgUtilityService,
} from "$services";
import { resolve, TYPES } from "$shared/inversify/container";

/**
 * Render a pictograph using direct composition of microservices
 */
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
      await arrowPositioning.calculateAllArrowPositions(data);

    // Render arrows
    if (updatedPictographData.motions) {
      for (const [color, motionData] of Object.entries(
        updatedPictographData.motions
      )) {
        const motion = motionData as MotionData;
        if (motion?.isVisible && motion.arrowPlacementData) {
          const position = {
            x: motion.arrowPlacementData.positionX,
            y: motion.arrowPlacementData.positionY,
            rotation: motion.arrowPlacementData.rotationAngle,
          };
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
    const arrowPositions = new Map<
      string,
      { x: number; y: number; rotation: number }
    >();
    if (updatedPictographData.motions) {
      for (const [color, motionData] of Object.entries(
        updatedPictographData.motions
      )) {
        const motion = motionData as MotionData;
        if (motion?.isVisible && motion.arrowPlacementData) {
          arrowPositions.set(color, {
            x: motion.arrowPlacementData.positionX,
            y: motion.arrowPlacementData.positionY,
            rotation: motion.arrowPlacementData.rotationAngle,
          });
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
