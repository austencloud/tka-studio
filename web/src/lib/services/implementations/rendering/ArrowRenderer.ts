/**
 * Arrow Rendering Service (Refactored)
 *
 * Orchestrates arrow rendering using focused microservices.
 *
 */

import type { ISvgConfiguration } from "$contracts/pictograph-interfaces";
import type { ArrowPlacementData, MotionData } from "$domain";
import {
  createMotionData,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  RotationDirection,
} from "$domain";
import { inject, injectable } from "inversify";

// Import the microservices
import type {
  IArrowPathResolutionService,
  IArrowPositioningService,
  ISvgColorTransformer,
  ISvgLoader,
  ISvgParser,
} from "$contracts";
import type { ArrowPosition } from "$lib/services/implementations/positioning/types";
import { TYPES } from "../../inversify/types";
import {
  ArrowPathResolutionService,
  ArrowPositioningService,
  SvgColorTransformer,
  SvgLoader,
  SvgParser,
} from "./arrow";

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

@injectable()
export class ArrowRenderer implements IArrowRenderer {
  private pathResolver: IArrowPathResolutionService;
  private svgParser: ISvgParser;
  private colorTransformer: ISvgColorTransformer;
  private svgLoader: ISvgLoader;
  private positioningService: IArrowPositioningService;

  constructor(
    @inject(TYPES.ISvgConfiguration) private config: ISvgConfiguration
  ) {
    // Initialize microservices
    this.pathResolver = new ArrowPathResolutionService();
    this.svgParser = new SvgParser();
    this.colorTransformer = new SvgColorTransformer();

    // Services that depend on other services
    this.svgLoader = new SvgLoader(
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
    _color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void> {
    // Handle undefined motionData by creating a default one with the provided color
    const safeMotionData: MotionData =
      motionData ||
      createMotionData({
        color: _color,
        motionType: MotionType.STATIC,
        rotationDirection: RotationDirection.NO_ROTATION,
        startLocation: Location.NORTH,
        endLocation: Location.NORTH,
        turns: 0,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        isVisible: true,
      });

    return this.positioningService.renderArrowAtPosition(
      svg,
      position,
      safeMotionData
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
   * Delegates to SvgParser
   */
  parseArrowSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    const parsed = this.svgParser.parseArrowSvg(svgText);

    // Convert string viewBox to object format
    let viewBox = { width: 100, height: 100 };
    if (typeof parsed.viewBox === "string") {
      const [width, height] = parsed.viewBox.split(" ").map(Number);
      viewBox = { width: width || 100, height: height || 100 };
    } else if (parsed.viewBox) {
      viewBox = parsed.viewBox;
    }

    return {
      viewBox,
      center: parsed.center || { x: 50, y: 50 },
    };
  }

  /**
   * Apply color transformation to SVG content
   * Delegates to SvgColorTransformer
   */
  applyColorToSvg(svgText: string, color: MotionColor): string {
    return this.colorTransformer.applyColorToSvg(svgText, color);
  }

  /**
   * Load arrow placement data - delegates to SvgLoader
   */
  async loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }> {
    // Delegate to the existing SvgLoader which handles the real SVG loading
    const svgData = await this.svgLoader.loadArrowPlacementData(
      arrowData,
      motionData
    );

    // Convert ArrowSvgData format to the expected return format
    // Handle viewBox conversion from string to object
    let viewBox = { width: 100, height: 100 };
    if (typeof svgData.viewBox === "string") {
      const [width, height] = svgData.viewBox.split(" ").map(Number);
      viewBox = { width: width || 100, height: height || 100 };
    } else if (svgData.viewBox) {
      viewBox = svgData.viewBox;
    }

    return {
      imageSrc: svgData.imageSrc || "",
      viewBox,
      center: svgData.center || { x: 50, y: 50 },
    };
  }
}
