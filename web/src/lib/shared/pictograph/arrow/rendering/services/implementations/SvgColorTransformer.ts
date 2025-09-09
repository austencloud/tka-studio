/**
 * SVG Color Transformation Service
 *
 * Applies color transformations to SVG content.
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type { ISvgColorTransformer } from "$shared";
import { MotionColor } from "$shared";

export class SvgColorTransformer implements ISvgColorTransformer {
  private readonly colorMap = new Map([
    [MotionColor.BLUE, "#2E3192"],
    [MotionColor.RED, "#ED1C24"],
  ]);

  private readonly modernColorMap = new Map([
    [MotionColor.BLUE, { fill: "#3b82f6", stroke: "#1d4ed8" }],
    [MotionColor.RED, { fill: "#ef4444", stroke: "#dc2626" }],
  ]);

  /**
   * Apply color transformation to SVG content (extracted from Arrow.svelte)
   */
  applyColorToSvg(svgText: string, color: MotionColor): string {
    const targetColor = this.colorMap.get(color) || "#2E3192";

    // Use regex replacement to change fill colors directly
    let coloredSvg = svgText.replace(
      /fill="#[0-9A-Fa-f]{6}"/g,
      `fill="${targetColor}"`
    );
    coloredSvg = coloredSvg.replace(
      /fill:\s*#[0-9A-Fa-f]{6}/g,
      `fill:${targetColor}`
    );

    // Remove the centerPoint circle entirely to prevent unwanted visual elements
    coloredSvg = coloredSvg.replace(
      /<circle[^>]*id="centerPoint"[^>]*\/?>/,
      ""
    );

    return coloredSvg;
  }

  /**
   * Apply color transformation to arrow SVG element
   */
  applyArrowColorTransformation(
    svgElement: SVGElement,
    color: MotionColor
  ): void {
    const colors = this.getColorsForMotionColor(color);

    // Find all path elements and apply color
    const paths = svgElement.querySelectorAll("path");

    paths.forEach((path) => {
      path.setAttribute("fill", colors.fill);
      path.setAttribute("stroke", colors.stroke);
      path.setAttribute("stroke-width", "1");
    });
  }

  /**
   * Get fill and stroke colors for a given motion color
   */
  getColorsForMotionColor(color: MotionColor): {
    fill: string;
    stroke: string;
  } {
    return (
      this.modernColorMap.get(color) || { fill: "#3b82f6", stroke: "#1d4ed8" }
    );
  }
}
