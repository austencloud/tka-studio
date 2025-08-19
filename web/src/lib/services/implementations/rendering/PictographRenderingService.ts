/**
 * Pictograph Rendering Service - Microservices Orchestrator
 *
 * Orchestrates rendering using specialized microservices.
 * Refactored from monolithic service to microservices architecture.
 */

import type { BeatData, PictographData } from "$lib/domain";
import { GridMode, MotionColor } from "$lib/domain";

import type {
  IArrowRenderingService,
  IDataTransformationService,
  IGridRenderingService,
  IOverlayRenderingService,
  IPictographRenderingService,
  ISvgUtilityService,
} from "../../interfaces/pictograph-interfaces";
import type { IArrowPositioningOrchestrator } from "../../positioning/core-services";
import type { IPropRenderingService } from "../../interfaces/positioning-interfaces";

export class PictographRenderingService implements IPictographRenderingService {
  constructor(
    private arrowPositioning: IArrowPositioningOrchestrator,
    private propRendering: IPropRenderingService,
    private svgUtility: ISvgUtilityService,
    private gridRendering: IGridRenderingService,
    private arrowRendering: IArrowRenderingService,
    private overlayRendering: IOverlayRenderingService,
    private dataTransformation: IDataTransformationService
  ) {
    // PictographRenderingService initialized with microservices
  }

  /**
   * Render a pictograph from pictograph data
   */
  async renderPictograph(data: PictographData): Promise<SVGElement> {
    try {
      // 1. Create base SVG
      const svg = this.svgUtility.createBaseSVG();

      // 2. Render grid
      const gridMode: GridMode = data.gridData?.gridMode ?? GridMode.DIAMOND;
      await this.gridRendering.renderGrid(svg, gridMode);

      // 3. Calculate arrow positions using sophisticated positioning orchestrator
      const updatedPictographData =
        await this.arrowPositioning.calculateAllArrowPositions(data);

      // 4. Render arrows with sophisticated calculated positions
      for (const [color, arrowData] of Object.entries(
        updatedPictographData.arrows
      )) {
        if (arrowData.isVisible) {
          const position = {
            x: arrowData.position_x,
            y: arrowData.position_y,
            rotation: arrowData.rotation_angle,
          };
          const motionData = data.motions?.[color as MotionColor];
          await this.arrowRendering.renderArrowAtPosition(
            svg,
            color as MotionColor,
            position,
            motionData
          );
        }
      }

      // 5. Render props (handled by existing prop service)
      await this.renderProps(svg, data);

      // 6. Render overlays
      await this.overlayRendering.renderOverlays(svg, data);

      // 7. Add metadata
      this.overlayRendering.renderIdLabel(svg, data);
      // Create arrow positions map for debug info
      const arrowPositions = new Map<
        string,
        { x: number; y: number; rotation: number }
      >();
      for (const [color, arrowData] of Object.entries(
        updatedPictographData.arrows
      )) {
        if (arrowData.isVisible) {
          arrowPositions.set(color, {
            x: arrowData.position_x,
            y: arrowData.position_y,
            rotation: arrowData.rotation_angle,
          });
        }
      }
      this.overlayRendering.renderDebugInfo(svg, data, arrowPositions);

      return svg;
    } catch (error) {
      console.error("❌ Error rendering pictograph:", error);
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error";
      return this.svgUtility.createErrorSVG(errorMessage);
    }
  }

  /**
   * Render a beat as a pictograph
   */
  async renderBeat(beat: BeatData): Promise<SVGElement> {
    // Convert beat data to pictograph data using transformation service
    const pictographData = this.dataTransformation.beatToPictographData(beat);
    return await this.renderPictograph(pictographData);
  }

  /**
   * Render props for both colors
   * DISABLED: Props are now rendered by Prop.svelte components to avoid duplicates
   */
  private async renderProps(
    _svg: SVGElement,
    _data: PictographData
  ): Promise<void> {
    // Props are now handled by Pictograph.svelte -> Prop.svelte components
    // This service-level rendering is disabled to prevent duplicate CIRCLE_PROP elements
    return;
  }
}
