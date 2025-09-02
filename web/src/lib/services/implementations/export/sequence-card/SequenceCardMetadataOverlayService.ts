/**
 * Sequence Card Metadata Overlay Service
 *
 * Handles adding metadata overlays to sequence card SVGs.
 * Single responsibility: Adding titles, beat numbers, and styling.
 */

import type { SequenceData } from "$domain";
import { injectable } from "inversify";
// Domain types
import type { SequenceCardDimensions, SequenceCardMetadata } from "$domain";

// Behavioral contracts
import type { ISequenceCardMetadataOverlayService } from "../../../contracts/sequence-card-export-interfaces";

@injectable()
export class SequenceCardMetadataOverlayService
  implements ISequenceCardMetadataOverlayService
{
  private readonly titleHeight = 40;
  private readonly titlePadding = 10;
  private readonly beatNumberSize = 14;
  private readonly defaultBackgroundColor = "#ffffff";

  /**
   * Add metadata overlays to SVG
   */
  async addMetadataOverlays(
    svg: string,
    sequence: SequenceData,
    metadata: SequenceCardMetadata,
    dimensions: SequenceCardDimensions
  ): Promise<string> {
    try {
      console.log(`🏷️ Adding metadata overlays for sequence: ${sequence.name}`);

      let modifiedSVG = svg;

      // Add background and borders first
      if (metadata.backgroundColor) {
        modifiedSVG = this.addBackgroundAndBorders(
          modifiedSVG,
          dimensions,
          metadata.backgroundColor
        );
      }

      // Add title if requested
      if (metadata.title || sequence.name) {
        const title = metadata.title || sequence.name || "Untitled Sequence";
        const titleOverlay = this.generateTitleOverlay(title, dimensions);
        modifiedSVG = this.insertBeforeClosingTag(
          modifiedSVG,
          titleOverlay,
          "</svg>"
        );
      }

      // Add beat numbers if requested
      if (metadata.beatNumbers) {
        const beatCount = sequence.beats?.length || 0;
        if (beatCount > 0) {
          const layout = this.extractLayoutFromSVG(modifiedSVG, beatCount);
          const beatNumberOverlays = this.generateBeatNumberOverlays(
            beatCount,
            layout
          );

          for (const overlay of beatNumberOverlays) {
            modifiedSVG = this.insertBeforeClosingTag(
              modifiedSVG,
              overlay,
              "</svg>"
            );
          }
        }
      }

      // Add timestamp if requested
      if (metadata.timestamp) {
        const timestampOverlay = this.generateTimestampOverlay(dimensions);
        modifiedSVG = this.insertBeforeClosingTag(
          modifiedSVG,
          timestampOverlay,
          "</svg>"
        );
      }

      // Add author if requested and available
      if (metadata.author || sequence.metadata?.author) {
        const author = metadata.author || (sequence.metadata?.author as string);
        if (author) {
          const authorOverlay = this.generateAuthorOverlay(author, dimensions);
          modifiedSVG = this.insertBeforeClosingTag(
            modifiedSVG,
            authorOverlay,
            "</svg>"
          );
        }
      }

      console.log("✅ Successfully added metadata overlays");
      return modifiedSVG;
    } catch (error) {
      console.error("❌ Failed to add metadata overlays:", error);
      // Return original SVG if overlay addition fails
      return svg;
    }
  }

  /**
   * Generate title overlay
   */
  generateTitleOverlay(
    title: string,
    dimensions: SequenceCardDimensions
  ): string {
    const centerX = dimensions.width / 2;
    const titleY = this.titlePadding + this.titleHeight / 2;

    // Escape XML special characters in title
    const escapedTitle = this.escapeXMLChars(title);

    return `
      <!-- Title Background -->
      <rect 
        x="0" 
        y="0" 
        width="${dimensions.width}" 
        height="${this.titleHeight}" 
        fill="rgba(0, 0, 0, 0.05)" 
        stroke="none"
      />
      
      <!-- Title Text -->
      <text 
        x="${centerX}" 
        y="${titleY}" 
        text-anchor="middle" 
        dominant-baseline="central"
        font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" 
        font-size="18" 
        font-weight="600" 
        fill="#333333"
        letter-spacing="0.5px"
      >
        ${escapedTitle}
      </text>`;
  }

  /**
   * Generate beat number overlays
   */
  generateBeatNumberOverlays(
    beatCount: number,
    layout: {
      rows: number;
      columns: number;
      beatWidth: number;
      beatHeight: number;
    }
  ): string[] {
    const overlays: string[] = [];
    const padding = 20; // Same as layout padding

    for (let i = 0; i < beatCount; i++) {
      const row = Math.floor(i / layout.columns);
      const col = i % layout.columns;

      // Calculate position (accounting for title and layout padding)
      const x = padding + col * (layout.beatWidth + 8) + 5; // 8 = spacing, 5 = number offset
      const y = this.titleHeight + padding + row * (layout.beatHeight + 8) + 15; // 15 = number offset

      const beatNumber = i + 1;

      overlays.push(`
        <!-- Beat Number ${beatNumber} Background -->
        <circle 
          cx="${x + 8}" 
          cy="${y}" 
          r="10" 
          fill="rgba(0, 0, 0, 0.7)" 
          stroke="rgba(255, 255, 255, 0.8)" 
          stroke-width="1"
        />
        
        <!-- Beat Number ${beatNumber} Text -->
        <text 
          x="${x + 8}" 
          y="${y}" 
          text-anchor="middle" 
          dominant-baseline="central"
          font-family="system-ui, sans-serif" 
          font-size="${this.beatNumberSize}" 
          font-weight="bold" 
          fill="white"
        >
          ${beatNumber}
        </text>`);
    }

    return overlays;
  }

  /**
   * Add background and borders
   */
  addBackgroundAndBorders(
    svg: string,
    dimensions: SequenceCardDimensions,
    backgroundColor?: string
  ): string {
    const bgColor = backgroundColor || this.defaultBackgroundColor;

    // Insert background right after opening SVG tag
    const backgroundRect = `
      <!-- Card Background -->
      <rect 
        width="100%" 
        height="100%" 
        fill="${bgColor}" 
        stroke="#e0e0e0" 
        stroke-width="2" 
        rx="8" 
        ry="8"
      />`;

    return this.insertAfterOpeningTag(svg, backgroundRect, "<svg");
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private generateTimestampOverlay(dimensions: SequenceCardDimensions): string {
    const now = new Date();
    const timestamp = now.toLocaleDateString() + " " + now.toLocaleTimeString();
    const escapedTimestamp = this.escapeXMLChars(timestamp);

    return `
      <!-- Timestamp -->
      <text 
        x="${dimensions.width - 10}" 
        y="${dimensions.height - 10}" 
        text-anchor="end" 
        font-family="system-ui, sans-serif" 
        font-size="10" 
        fill="#666666"
        opacity="0.7"
      >
        ${escapedTimestamp}
      </text>`;
  }

  private generateAuthorOverlay(
    author: string,
    dimensions: SequenceCardDimensions
  ): string {
    const escapedAuthor = this.escapeXMLChars(author);

    return `
      <!-- Author -->
      <text 
        x="10" 
        y="${dimensions.height - 10}" 
        text-anchor="start" 
        font-family="system-ui, sans-serif" 
        font-size="12" 
        fill="#666666"
        font-style="italic"
      >
        by ${escapedAuthor}
      </text>`;
  }

  private extractLayoutFromSVG(
    svg: string,
    beatCount: number
  ): { rows: number; columns: number; beatWidth: number; beatHeight: number } {
    // Try to extract layout info from SVG comments or calculate fallback

    // Look for layout comments (if added by composition service)
    const layoutMatch = svg.match(/<!-- Layout: (\d+)x(\d+), (\d+)x(\d+) -->/);

    if (layoutMatch) {
      return {
        rows: parseInt(layoutMatch[1]),
        columns: parseInt(layoutMatch[2]),
        beatWidth: parseInt(layoutMatch[3]),
        beatHeight: parseInt(layoutMatch[4]),
      };
    }

    // Fallback: estimate based on beat count
    const columns = Math.min(beatCount, 4);
    const rows = Math.ceil(beatCount / columns);

    return {
      rows,
      columns,
      beatWidth: 120, // Reasonable default
      beatHeight: 120,
    };
  }

  private escapeXMLChars(text: string): string {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  private insertAfterOpeningTag(
    svg: string,
    content: string,
    tagStart: string
  ): string {
    const tagEndIndex = svg.indexOf(">", svg.indexOf(tagStart));
    if (tagEndIndex === -1) {
      console.warn("Could not find opening SVG tag");
      return svg;
    }

    return (
      svg.substring(0, tagEndIndex + 1) +
      content +
      svg.substring(tagEndIndex + 1)
    );
  }

  private insertBeforeClosingTag(
    svg: string,
    content: string,
    closingTag: string
  ): string {
    const lastIndex = svg.lastIndexOf(closingTag);
    if (lastIndex === -1) {
      console.warn(`Could not find closing tag: ${closingTag}`);
      return svg + content;
    }

    return (
      svg.substring(0, lastIndex) + content + "\n" + svg.substring(lastIndex)
    );
  }
}
