/**
 * SVG Parsing Service
 *
 * Handles parsing SVG content to extract viewBox and center points.
 * Extracted from ArrowRenderingService to improve modularity and reusability.
 */

import type {
  ISvgParsingService,
  SVGDimensions,
} from "$lib/services/interfaces/pictograph-interfaces";

export class SvgParsingService implements ISvgParsingService {
  /**
   * Parse SVG to get proper dimensions and center point (extracted from Arrow.svelte)
   */
  parseArrowSvg(svgText: string): SVGDimensions {
    const doc = new DOMParser().parseFromString(svgText, "image/svg+xml");
    const svg = doc.documentElement;

    // Get viewBox dimensions
    const viewBoxValues = svg.getAttribute("viewBox")?.split(/\s+/) || [
      "0",
      "0",
      "100",
      "100",
    ];
    const viewBox = {
      width: parseFloat(viewBoxValues[2] || "100") || 100,
      height: parseFloat(viewBoxValues[3] || "100") || 100,
    };

    // Get center point from SVG
    let center = { x: viewBox.width / 2, y: viewBox.height / 2 };

    try {
      const centerElement = doc.getElementById("centerPoint");
      if (centerElement) {
        center = {
          x: parseFloat(centerElement.getAttribute("cx") || "0") || center.x,
          y: parseFloat(centerElement.getAttribute("cy") || "0") || center.y,
        };
      }
    } catch {
      // SVG center calculation failed, using default center
    }

    return { viewBox, center };
  }

  /**
   * Extract SVG content (everything inside the <svg> tags)
   */
  extractSvgContent(svgText: string): string {
    // Extract SVG content (everything inside the <svg> tags)
    // Arrows are already correctly sized for 950x950 coordinate system

    // Check if this is an empty/static SVG (self-closing or width="0")
    if (
      svgText.includes('width="0"') ||
      (svgText.includes("<svg") && svgText.includes("/>"))
    ) {
      // Static arrows are intentionally empty - return empty string
      return "";
    }

    const svgContentMatch = svgText.match(/<svg[^>]*>([\s\S]*)<\/svg>/);
    if (!svgContentMatch) {
      console.warn("Could not extract SVG content from non-static arrow");
      return svgText;
    }

    return svgContentMatch[1];
  }
}
