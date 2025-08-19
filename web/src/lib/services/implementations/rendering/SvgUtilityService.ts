/**
 * SVG Utility Service
 *
 * Handles basic SVG creation and utility functions.
 * Extracted from PictographRenderingService.
 */

import type { ISvgConfiguration } from "./SvgConfiguration";

export interface ISvgUtilityService {
  createBaseSVG(): SVGElement;
  createErrorSVG(errorMessage?: string): SVGElement;
}

export class SvgUtilityService implements ISvgUtilityService {
  constructor(private config: ISvgConfiguration) {}

  /**
   * Create base SVG element
   */
  createBaseSVG(): SVGElement {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", this.config.SVG_SIZE.toString());
    svg.setAttribute("height", this.config.SVG_SIZE.toString());
    svg.setAttribute(
      "viewBox",
      `0 0 ${this.config.SVG_SIZE} ${this.config.SVG_SIZE}`
    );
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");

    // Add background
    const background = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "rect"
    );
    background.setAttribute("width", "100%");
    background.setAttribute("height", "100%");
    background.setAttribute("fill", "#ffffff");
    svg.appendChild(background);

    return svg;
  }

  /**
   * Create error SVG with detailed error information
   */
  createErrorSVG(errorMessage?: string): SVGElement {
    const svg = this.createBaseSVG();

    const errorText = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    errorText.setAttribute("x", this.config.CENTER_X.toString());
    errorText.setAttribute("y", this.config.CENTER_Y.toString());
    errorText.setAttribute("text-anchor", "middle");
    errorText.setAttribute("fill", "#dc2626");
    errorText.setAttribute("font-weight", "bold");
    errorText.textContent = "Rendering Error";

    if (errorMessage) {
      const detailText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      detailText.setAttribute("x", this.config.CENTER_X.toString());
      detailText.setAttribute("y", (this.config.CENTER_Y + 20).toString());
      detailText.setAttribute("text-anchor", "middle");
      detailText.setAttribute("fill", "#dc2626");
      detailText.setAttribute("font-size", "12");
      detailText.textContent =
        errorMessage.substring(0, 50) + (errorMessage.length > 50 ? "..." : "");
      svg.appendChild(detailText);
    }

    svg.appendChild(errorText);
    return svg;
  }
}
