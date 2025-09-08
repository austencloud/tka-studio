/**
 * Overlay Rendering Service
 *
 * Handles overlay rendering including letter glyphs and metadata.
 * Extracted from PictographRenderingService.
 */

import type {
  ArrowPosition,
  ISvgConfig,
  Letter,
  PictographData,
} from "$shared";
import { getLetterImagePath, TYPES } from "$shared";
import { inject, injectable } from "inversify";

export interface IOverlayRenderer {
  renderOverlays(svg: SVGElement, data: PictographData): Promise<void>;
  renderIdLabel(svg: SVGElement, data: PictographData): void;
  renderDebugInfo(
    svg: SVGElement,
    data: PictographData,
    positions: Map<string, ArrowPosition>
  ): void;
}

@injectable()
export class OverlayRenderer implements IOverlayRenderer {
  constructor(@inject(TYPES.ISvgConfig) private config: ISvgConfig) {}

  /**
   * Render glyph overlays (letters now; VTG/elemental when data is available)
   */
  async renderOverlays(svg: SVGElement, data: PictographData): Promise<void> {
    try {
      if (data.letter) {
        await this.renderLetterGlyph(svg, data.letter);
      }
    } catch {
      // Overlay rendering skipped
    }
  }

  /**
   * Render letter glyph overlay
   */
  private async renderLetterGlyph(
    svg: SVGElement,
    letter: Letter
  ): Promise<void> {
    // Use comprehensive letter mapping with correct type-based paths
    const path = getLetterImagePath(letter);
    if (!path) return; // only render supported letters for now

    const res = await fetch(path);
    if (!res.ok) return;
    const content = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(content, "image/svg+xml");
    const el = doc.documentElement as unknown as SVGElement;

    // Create a group and insert first to measure natural size, then position bottom-left
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", "tka-letter");
    group.setAttribute("opacity", "0"); // hide during measurement
    const imported = document.importNode(el, true);
    group.appendChild(imported);
    svg.appendChild(group);

    // Measure bounding box after insertion
    let bbox: DOMRect;
    try {
      bbox = group.getBBox();
    } catch {
      // Fallback if getBBox fails
      bbox = new DOMRect(0, 0, 120, 80);
    }
    const letterHeight = bbox.height || 80;
    const x = Math.round(letterHeight / 1.5);
    const y = Math.round(this.config.SVG_SIZE - letterHeight * 1.7);
    group.setAttribute("transform", `translate(${x}, ${y})`);
    group.removeAttribute("opacity");
  }

  /**
   * Render ID label with enhanced metadata
   */
  renderIdLabel(svg: SVGElement, data: PictographData): void {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", this.config.CENTER_X.toString());
    text.setAttribute("y", (this.config.CENTER_Y + 130).toString());
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-family", "monospace");
    text.setAttribute("font-size", "11");
    text.setAttribute("fill", "#4b5563");
    text.textContent = `${data.id.slice(-8)} • Sophisticated Positioning`;
    svg.appendChild(text);
  }

  /**
   * Render debug information about positioning
   */
  renderDebugInfo(
    svg: SVGElement,
    data: PictographData,
    positions: Map<string, ArrowPosition>
  ): void {
    let yOffset = 15;

    for (const [color, position] of positions.entries()) {
      const debugText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      debugText.setAttribute("x", "10");
      debugText.setAttribute("y", yOffset.toString());
      debugText.setAttribute("font-family", "monospace");
      debugText.setAttribute("font-size", "10");
      debugText.setAttribute("fill", "#6b7280");
      debugText.textContent = `${color}: [${position.x.toFixed(1)}, ${position.y.toFixed(1)}] ∠${position.rotation.toFixed(0)}°`;
      svg.appendChild(debugText);
      yOffset += 12;
    }

    // Add letter info if present
    if (data.letter) {
      const letterText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      letterText.setAttribute("x", "10");
      letterText.setAttribute("y", yOffset.toString());
      letterText.setAttribute("font-family", "monospace");
      letterText.setAttribute("font-size", "10");
      letterText.setAttribute("fill", "#059669");
      letterText.setAttribute("font-weight", "bold");
      letterText.textContent = `Letter: ${data.letter}`;

      svg.appendChild(letterText);
    }
  }
}
