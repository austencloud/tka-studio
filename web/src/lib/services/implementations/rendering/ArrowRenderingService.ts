/**
 * Arrow Rendering Service
 *
 * Handles arrow rendering with SVG assets, color transformation, and fallbacks.
 * Extracted from PictographRenderingService.
 */

import type { MotionData } from "$lib/domain";
import { MotionColor } from "$lib/domain/enums";
import type { ISvgConfiguration } from "./SvgConfiguration";

export interface ArrowPosition {
  x: number;
  y: number;
  rotation: number;
}

export interface IArrowRenderingService {
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;
}

export class ArrowRenderingService implements IArrowRenderingService {
  constructor(private config: ISvgConfiguration) {}

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
      const arrowSvgPath = this.getArrowSvgPath(motionData);

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
      this.applyArrowColorTransformation(svgElement, color);

      // Import the SVG content into the arrow group
      const importedSvg = document.importNode(svgElement, true);
      arrowGroup.appendChild(importedSvg);

      svg.appendChild(arrowGroup);
    } catch (error) {
      console.error(`❌ Error loading arrow SVG for ${color}:`, error);
      // Fallback to simple arrow
      this.renderFallbackArrow(svg, color, position);
    }
  }

  /**
   * Get the correct arrow SVG path based on motion data (like ArrowSvgManager)
   */
  private getArrowSvgPath(motionData: MotionData | undefined): string {
    if (!motionData) {
      return "/images/arrows/static/from_radial/static_0.svg";
    }
    const motionType = motionData.motionType;
    const turnsVal = motionData.turns;
    const startOri = motionData.startOrientation;
    if (motionType === "float") return "/images/arrows/float.svg";
    const radialPath = startOri === "in" ? "from_radial" : "from_nonradial";
    let turnsStr: string;
    if (turnsVal === "fl") {
      turnsStr = "fl";
    } else if (typeof turnsVal === "number") {
      turnsStr = turnsVal % 1 === 0 ? `${turnsVal}.0` : turnsVal.toString();
    } else {
      turnsStr = "0.0";
    }
    return `/images/arrows/${motionType}/${radialPath}/${motionType}_${turnsStr}.svg`;
  }

  /**
   * Apply color transformation to arrow SVG
   */
  private applyArrowColorTransformation(
    svgElement: SVGElement,
    color: MotionColor
  ): void {
    // Find all path elements and apply color
    const paths = svgElement.querySelectorAll("path");
    const fillColor = color === MotionColor.BLUE ? "#3b82f6" : "#ef4444";
    const strokeColor = color === MotionColor.BLUE ? "#1d4ed8" : "#dc2626";

    paths.forEach((path) => {
      path.setAttribute("fill", fillColor);
      path.setAttribute("stroke", strokeColor);
      path.setAttribute("stroke-width", "1");
    });
  }

  /**
   * Render fallback arrow if SVG loading fails
   */
  private renderFallbackArrow(
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
  private createEnhancedArrowPath(color: MotionColor): SVGElement {
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
