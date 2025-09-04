/**
 * Ar/**
 * Arrow Positioning Service
 *
 * Handles positioning and rendering arrows in SVG containers.
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type {
  ArrowPlacementData,
  ArrowPosition,
  MotionColor,
  MotionData,
  PictographData,
} from "$domain";
import type {
  IArrowPathResolutionService,
  IArrowPositioningService,
  ISvgColorTransformer,
} from "$services";
import { injectable } from "inversify";

@injectable()
export class ArrowPositioningService implements IArrowPositioningService {
  constructor(
    private pathResolver: IArrowPathResolutionService,
    private colorTransformer: ISvgColorTransformer
  ) {}
  calculatePosition(
    _arrowData: ArrowPlacementData,
    _motionData: MotionData,
    _pictographData: PictographData
  ): Promise<{ x: number; y: number; rotation: number }> {
    throw new Error("Method not implemented.");
  }
  shouldMirror(
    _arrowData: ArrowPlacementData,
    _motionData: MotionData,
    _pictographData: PictographData
  ): boolean {
    throw new Error("Method not implemented.");
  }

  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  async renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void> {
    // Use the provided color and position parameters
    const arrowPosition = {
      x: position.x,
      y: position.y,
      rotation: position.rotation,
    };

    try {
      // Get the correct arrow SVG path
      const arrowSvgPath = this.pathResolver.getArrowSvgPath(motionData);

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
      arrowGroup.setAttribute(
        "class",
        `arrow-${color} sophisticated-positioning`
      );
      arrowGroup.setAttribute("data-color", color);
      arrowGroup.setAttribute(
        "data-position",
        `${arrowPosition.x},${arrowPosition.y}`
      );
      arrowGroup.setAttribute(
        "data-rotation",
        arrowPosition.rotation.toString()
      );

      // Apply sophisticated position and rotation transform
      const transform = `translate(${arrowPosition.x}, ${arrowPosition.y}) rotate(${arrowPosition.rotation})`;
      arrowGroup.setAttribute("transform", transform);

      // Parse and insert the SVG content
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgContent, "image/svg+xml");
      const svgElement = svgDoc.documentElement as unknown as SVGElement;

      // Apply color transformation
      this.colorTransformer.applyArrowColorTransformation(svgElement, color);

      // Import the SVG content into the arrow group
      const importedSvg = document.importNode(svgElement, true);
      arrowGroup.appendChild(importedSvg);

      svg.appendChild(arrowGroup);
    } catch (error) {
      console.error(`❌ Error loading arrow SVG for ${color}:`, error);
      throw error; // No fallback - proper error handling required
    }
  }
}
