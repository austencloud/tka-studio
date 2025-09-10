/**
 * Prop SVG Loader Service
 *
 * Fast, direct SVG loading for props - mirrors arrow loading approach.
 * Bypasses SvgPreloadService for maximum performance.
 */

import { MotionColor, type MotionData, type PropPlacementData } from "$shared";
import { injectable } from "inversify";
import type { PropRenderData } from "../../domain/models/PropRenderData";
import type { IPropSvgLoader } from "../contracts/IPropSvgLoader";

@injectable()
export class PropSvgLoader implements IPropSvgLoader {
  /**
   * Load prop SVG data with color transformation - fast direct approach
   */
  async loadPropSvg(
    propData: PropPlacementData,
    motionData: MotionData
  ): Promise<PropRenderData> {
    try {
      // Get prop type and color
      const propType = motionData.propType || "staff";
      const color = motionData.color || MotionColor.BLUE;
      
      // Direct fetch - no service layers
      const path = `/images/props/${propType}.svg`;
      const originalSvgText = await this.fetchSvgContent(path);
      
      // Parse SVG for viewBox and center
      const { viewBox, center } = this.parsePropSvg(originalSvgText);
      
      // Apply color transformation
      const coloredSvgText = this.applyColorToSvg(originalSvgText, color);
      
      // Extract SVG content
      const svgContent = this.extractSvgContent(coloredSvgText);
      
      return {
        position: { x: propData.positionX, y: propData.positionY },
        rotation: propData.rotationAngle,
        svgData: {
          svgContent,
          viewBox,
          center,
        },
        loaded: true,
        error: null,
      };
    } catch (error) {
      console.error("❌ PropSvgLoader: Error loading prop SVG:", error);
      return {
        position: { x: 475, y: 475 },
        rotation: 0,
        svgData: null,
        loaded: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Fetch SVG content from a given path - direct fetch
   */
  async fetchSvgContent(path: string): Promise<string> {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch SVG: ${response.status}`);
    }
    return await response.text();
  }

  /**
   * Parse prop SVG to extract viewBox and center
   */
  private parsePropSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const svgElement = doc.querySelector("svg");

    if (!svgElement) {
      throw new Error("Invalid SVG: No SVG element found");
    }

    // Extract viewBox
    const viewBoxAttr = svgElement.getAttribute("viewBox");
    let width = 100, height = 100;
    
    if (viewBoxAttr) {
      const [, , w, h] = viewBoxAttr.split(" ").map(Number);
      width = w || 100;
      height = h || 100;
    }

    return {
      viewBox: { width, height },
      center: { x: width / 2, y: height / 2 },
    };
  }

  /**
   * Apply color transformation to SVG - sophisticated approach matching arrows
   * Simple and correct: props are blue by default, change to red when needed
   * Also makes CSS class names unique to prevent conflicts between different colored props
   */
  private applyColorToSvg(svgText: string, color: MotionColor): string {
    const colorMap: Record<MotionColor, string> = {
      [MotionColor.BLUE]: "#2E3192",
      [MotionColor.RED]: "#ED1C24",
    };

    const targetColor = colorMap[color] || colorMap[MotionColor.BLUE];

    // Replace fill colors in both attribute and CSS style formats
    let coloredSvg = svgText.replace(
      /fill="#[0-9A-Fa-f]{6}"/g,
      `fill="${targetColor}"`
    );
    coloredSvg = coloredSvg.replace(
      /fill:\s*#[0-9A-Fa-f]{6}/g,
      `fill:${targetColor}`
    );

    // Make CSS class names unique for each color to prevent conflicts
    // Replace .st0, .st1, etc. with .st0-blue, .st1-blue, etc.
    const colorSuffix = color.toLowerCase();
    coloredSvg = coloredSvg.replace(/\.st(\d+)/g, `.st$1-${colorSuffix}`);

    // Also update class references in elements
    coloredSvg = coloredSvg.replace(
      /class="st(\d+)"/g,
      `class="st$1-${colorSuffix}"`
    );

    // Remove the centerPoint circle entirely to prevent unwanted visual elements
    coloredSvg = coloredSvg.replace(
      /<circle[^>]*id="centerPoint"[^>]*\/?>/,
      ""
    );

    return coloredSvg;
  }

  /**
   * Extract SVG content (remove outer SVG wrapper)
   */
  private extractSvgContent(svgText: string): string {
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const svgElement = doc.querySelector("svg");

    if (!svgElement) {
      return svgText;
    }

    return svgElement.innerHTML;
  }
}
