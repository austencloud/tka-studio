/**
 * Arrow Rendering Service (Refactored)
 *
 * Orchestrates arrow rendering using focused microservices.
 *
 */

import type { MotionColor } from "$shared";
import type { IArrowPathResolver, IArrowSvgLoader, IArrowSvgParser, ISvgColorTransformer } from "$shared";
import {  } from "$shared";
import {
  createMotionData,
  GridLocation,
  MotionType,
  Orientation,
  RotationDirection,
  type ArrowPlacementData,
  type ArrowPosition,
  type MotionData,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";

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

  loadArrowSvg(
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
  constructor(
    @inject(TYPES.IArrowPathResolver) private pathResolver: IArrowPathResolver,
    @inject(TYPES.IArrowSvgParser) private svgParser: IArrowSvgParser,
    @inject(TYPES.IArrowSvgColorTransformer)
    private colorTransformer: ISvgColorTransformer,
    @inject(TYPES.IArrowSvgLoader) private svgLoader: IArrowSvgLoader
  ) {}

  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   * Simple implementation without positioning service dependency
   */
  async renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void> {
    // Handle undefined motionData by creating a default one with the provided color
    const safeMotionData: MotionData =
      motionData ||
      createMotionData({
        color: color,
        motionType: MotionType.STATIC,
        rotationDirection: RotationDirection.NO_ROTATION,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.NORTH,
        turns: 0,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        isVisible: true,
      });

    try {
      // Get the correct arrow SVG path
      const arrowSvgPath = this.pathResolver.getArrowSvgPath(safeMotionData);

      // Load the arrow SVG
      const response = await fetch(arrowSvgPath);
      if (!response.ok) {
        throw new Error(`Failed to load arrow SVG: ${response.status}`);
      }

      const svgContent = await response.text();

      // Create arrow group with metadata
      const arrowGroup = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "g"
      );
      arrowGroup.setAttribute("class", `arrow-${color}`);
      arrowGroup.setAttribute("data-color", color);
      arrowGroup.setAttribute("data-position", `${position.x},${position.y}`);
      arrowGroup.setAttribute("data-rotation", position.rotation.toString());

      // Apply position and rotation transform
      const transform = `translate(${position.x}, ${position.y}) rotate(${position.rotation})`;
      arrowGroup.setAttribute("transform", transform);

      // Parse and insert the SVG content
      const parser = new DOMParser();

      // Apply color transformation
      const coloredSvg = this.colorTransformer.applyColorToSvg(
        svgContent,
        color
      );
      arrowGroup.innerHTML = coloredSvg;

      // Add to parent SVG
      svg.appendChild(arrowGroup);
    } catch (error) {
      console.error("Failed to render arrow:", error);
      throw error;
    }
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
   * Load arrow SVG data - delegates to SvgLoader
   */
  async loadArrowSvg(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }> {
    // Delegate to the existing SvgLoader which handles the real SVG loading
    const svgData = await this.svgLoader.loadArrowSvg(arrowData, motionData);

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
