/**
 * Arrow Rendering Service (Refactored)
 *
 * Orchestrates arrow rendering using focused microservices.
 *
 */

import type { MotionData } from "$lib/domain";
import type { ArrowPlacementData } from "$lib/domain/ArrowPlacementData";
import { MotionColor } from "$lib/domain/enums";
import type { ISvgConfiguration } from "./SvgConfiguration";

// Import the microservices
import type {
  ArrowSvgData,
  IArrowPathResolutionService,
  IArrowPositioningService,
  ISvgColorTransformationService,
  ISvgLoadingService,
  ISvgParsingService,
} from "$lib/services/interfaces/pictograph-interfaces";
import type { ArrowPosition } from "$lib/services/positioning/types";
import {
  ArrowPathResolutionService,
  ArrowPositioningService,
  SvgColorTransformationService,
  SvgLoadingService,
  SvgParsingService,
} from "./arrow";

export interface IArrowRenderingService {
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

  // Method expected by DI container
  loadArrowSvgData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<ArrowSvgData>;
}

export class ArrowRenderingService implements IArrowRenderingService {
  private pathResolver: IArrowPathResolutionService;
  private svgParser: ISvgParsingService;
  private colorTransformer: ISvgColorTransformationService;
  private svgLoader: ISvgLoadingService;
  private positioningService: IArrowPositioningService;

  constructor(private config: ISvgConfiguration) {
    // Initialize microservices
    this.pathResolver = new ArrowPathResolutionService();
    this.svgParser = new SvgParsingService();
    this.colorTransformer = new SvgColorTransformationService();

    // Services that depend on other services
    this.svgLoader = new SvgLoadingService(
      this.pathResolver,
      this.svgParser,
      this.colorTransformer
    );

    this.positioningService = new ArrowPositioningService(
      this.pathResolver,
      this.colorTransformer
    );
  }

  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   * Delegates to ArrowPositioningService
   */
  async renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void> {
    return this.positioningService.renderArrowAtPosition(
      svg,
      color,
      position,
      motionData
    );
  }

  // Legacy methods for backward compatibility - delegate to microservices

  /**
   * Get arrow SVG path based on motion type and properties
   * Delegates to ArrowPathResolutionService
   */
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null {
    return this.pathResolver.getArrowPath(arrowData, motionData);
  }

  /**
   * Parse SVG to get proper dimensions and center point
   * Delegates to SvgParsingService
   */
  parseArrowSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    return this.svgParser.parseArrowSvg(svgText);
  }

  /**
   * Apply color transformation to SVG content
   * Delegates to SvgColorTransformationService
   */
  applyColorToSvg(svgText: string, color: MotionColor): string {
    return this.colorTransformer.applyColorToSvg(svgText, color);
  }

  /**
   * Load arrow placement data - delegates to SvgLoadingService
   */
  async loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }> {
    // Delegate to the existing SvgLoadingService which handles the real SVG loading
    const svgData = await this.svgLoader.loadArrowPlacementData(
      arrowData,
      motionData
    );

    // Convert ArrowSvgData format to the expected return format
    return {
      imageSrc: svgData.imageSrc,
      viewBox: svgData.viewBox,
      center: svgData.center,
    };
  }

  /**
   * Implementation of method expected by DI container
   * Delegates to SvgLoadingService
   */
  async loadArrowSvgData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<ArrowSvgData> {
    return this.svgLoader.loadArrowSvgData(arrowData, motionData);
  }
}
