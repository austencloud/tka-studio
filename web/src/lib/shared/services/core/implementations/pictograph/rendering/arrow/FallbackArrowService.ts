/**
 * Fallback Arrow Service
 *
 * Creates fallback arrows when SVG loading fails.
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type { ArrowPosition } from "$domain";
import { MotionColor } from "$domain";
import type { IFallbackArrowService } from "$services";
import { injectable } from "inversify";

@injectable()
export class FallbackArrowService implements IFallbackArrowService {
  /**
   * Render fallback arrow if SVG loading fails
   */
  renderFallbackArrow(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition
  ): void {
    // Create arrow group
    const arrowGroup = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "g"
    );
    arrowGroup.setAttribute("class", `arrow-${color} fallback`);
    arrowGroup.setAttribute(
      "transform",
      `translate(${position.x}, ${position.y}) rotate(${position.rotation})`
    );

    // Create simple arrow path
    const arrowPath = this.createEnhancedArrowPath(color);
    arrowGroup.appendChild(arrowPath);

    svg.appendChild(arrowGroup);
  }

  /**
   * Create enhanced arrow SVG path with sophisticated styling
   */
  createEnhancedArrowPath(color: MotionColor): SVGElement {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");

    // More sophisticated arrow shape
    path.setAttribute("d", "M 0,-25 L 15,0 L 0,25 L -8,15 L -8,-15 Z");
    path.setAttribute("fill", color);
    path.setAttribute("stroke", "#000000");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("opacity", "0.9");

    // Add sophisticated styling
    path.setAttribute("filter", "drop-shadow(1px 1px 2px rgba(0,0,0,0.3))");
    path.setAttribute("class", "sophisticated-arrow");

    return path;
  }
}
