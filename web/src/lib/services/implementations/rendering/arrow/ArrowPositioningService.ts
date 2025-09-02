/**
 * Ar/**
 * Arrow Positioning Service
 *
 * Handles positioning and rendering arrows in SVG containers.
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type { MotionData } from "$domain";
import { MotionColor } from "$domain";
import type {
  IArrowPositioningService,
  ISvgColorTransformer,
} from "$lib/services/contracts/pictograph-interfaces";
import type { IArrowPathResolutionService } from "$lib/services/contracts/positioning-interfaces";
import type { ArrowPosition } from "$lib/services/implementations/positioning/types";
import { injectable } from "inversify";

@injectable()
export class ArrowPositioningService implements IArrowPositioningService {
  constructor(
    private pathResolver: IArrowPathResolutionService,
    private colorTransformer: ISvgColorTransformer
  ) {}

  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  async renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void> {
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
      arrowGroup.setAttribute("data-position", `${position.x},${position.y}`);
      arrowGroup.setAttribute("data-rotation", position.rotation.toString());

      // Apply sophisticated position and rotation transform
      const transform = `translate(${position.x}, ${position.y}) rotate(${position.rotation})`;
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
