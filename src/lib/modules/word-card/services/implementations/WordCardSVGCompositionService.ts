/**
 * Word Card SVG Composition Service
 *
 * Handles SVG layout composition for word cards.
 * Single responsibility: Arranging beat SVGs into card layouts.
 */

import { injectable } from "inversify";
// Domain types
// import type { WordCardDimensions } from "$wordcard/domain";

// Temporary interface definition
interface WordCardDimensions {
  width: number;
  height: number;
  scale?: number;
}

// Behavioral contracts

interface BeatLayout {
  rows: number;
  columns: number;
  beatWidth: number;
  beatHeight: number;
  spacing: { x: number; y: number };
}

@injectable()
export class WordCardSVGCompositionService {
  private readonly minBeatSize = 80; // Minimum beat size in pixels
  private readonly maxBeatSize = 200; // Maximum beat size in pixels
  private readonly minSpacing = 8; // Minimum spacing between beats
  private readonly padding = 20; // Padding around the card

  /**
   * Create SVG layout for sequence beats
   */
  async createSequenceLayout(
    beatSVGs: string[],
    dimensions: WordCardDimensions
  ): Promise<string> {
    try {
      if (beatSVGs.length === 0) {
        throw new Error("No beat SVGs provided");
      }

      console.log(`🎨 Creating SVG layout for ${beatSVGs.length} beats`);

      // Calculate optimal layout
      const layout = this.calculateBeatLayout(beatSVGs.length, dimensions);

      // Create container SVG
      const containerSVG = this.createContainerSVG(dimensions);

      // Add beats to layout
      const beatsGroup = this.createBeatsGroup(beatSVGs, layout);

      // Combine into final SVG
      const finalSVG = this.combineSVGElements(containerSVG, beatsGroup);

      console.log(
        `✅ Created SVG layout: ${layout.rows}x${layout.columns} grid`
      );
      return finalSVG;
    } catch (error) {
      console.error("❌ Failed to create SVG layout:", error);
      throw new Error(`SVG layout creation failed: ${error}`);
    }
  }

  /**
   * Calculate optimal beat arrangement
   */
  calculateBeatLayout(
    beatCount: number,
    dimensions: WordCardDimensions
  ): BeatLayout {
    try {
      // Calculate available space (minus padding)
      const availableWidth = dimensions.width - this.padding * 2;
      const availableHeight = dimensions.height - this.padding * 2;

      // Find optimal grid arrangement
      const gridOptions = this.generateGridOptions(beatCount);
      const bestOption = this.selectBestGridOption(
        gridOptions,
        availableWidth,
        availableHeight
      );

      const layout: BeatLayout = {
        rows: bestOption.rows,
        columns: bestOption.columns,
        beatWidth: bestOption.beatWidth,
        beatHeight: bestOption.beatHeight,
        spacing: {
          x: bestOption.spacingX,
          y: bestOption.spacingY,
        },
      };

      console.log(`📊 Calculated beat layout:`, layout);
      return layout;
    } catch (error) {
      console.error("❌ Failed to calculate beat layout:", error);
      // Fallback to simple single-row layout
      return this.createFallbackLayout(beatCount, dimensions);
    }
  }

  /**
   * Apply responsive sizing based on beat count
   */
  calculateResponsiveDimensions(
    beatCount: number,
    maxDimensions: WordCardDimensions
  ): WordCardDimensions {
    try {
      // Determine aspect ratio based on beat count
      const aspectRatio = this.calculateOptimalAspectRatio(beatCount);

      // Calculate dimensions that fit within max bounds
      let width = maxDimensions.width;
      let height = maxDimensions.height;

      // Adjust to maintain aspect ratio
      if (width / height > aspectRatio) {
        width = height * aspectRatio;
      } else {
        height = width / aspectRatio;
      }

      // Ensure minimum dimensions
      const minWidth = Math.max(200, this.minBeatSize * 2 + this.padding * 2);
      const minHeight = Math.max(150, this.minBeatSize + this.padding * 2);

      width = Math.max(width, minWidth);
      height = Math.max(height, minHeight);

      const responsiveDimensions: WordCardDimensions = {
        width: Math.round(width),
        height: Math.round(height),
        ...(maxDimensions.scale !== undefined && {
          scale: maxDimensions.scale,
        }),
      };

      console.log(
        `📱 Responsive dimensions for ${beatCount} beats:`,
        responsiveDimensions
      );
      return responsiveDimensions;
    } catch (error) {
      console.error("❌ Failed to calculate responsive dimensions:", error);
      return maxDimensions; // Fallback to max dimensions
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private generateGridOptions(beatCount: number): Array<{
    rows: number;
    columns: number;
    efficiency: number;
  }> {
    const options: Array<{
      rows: number;
      columns: number;
      efficiency: number;
    }> = [];

    // Generate reasonable grid combinations
    for (let cols = 1; cols <= Math.min(beatCount, 6); cols++) {
      const rows = Math.ceil(beatCount / cols);
      const totalCells = rows * cols;
      const efficiency = beatCount / totalCells;

      options.push({ rows, columns: cols, efficiency });
    }

    // Sort by efficiency (less wasted space is better)
    return options.sort((a, b) => b.efficiency - a.efficiency);
  }

  private selectBestGridOption(
    gridOptions: Array<{ rows: number; columns: number; efficiency: number }>,
    availableWidth: number,
    availableHeight: number
  ): {
    rows: number;
    columns: number;
    beatWidth: number;
    beatHeight: number;
    spacingX: number;
    spacingY: number;
  } {
    for (const option of gridOptions) {
      // Calculate beat size for this grid option
      const spacingX = this.minSpacing;
      const spacingY = this.minSpacing;

      const beatWidth =
        (availableWidth - spacingX * (option.columns - 1)) / option.columns;
      const beatHeight =
        (availableHeight - spacingY * (option.rows - 1)) / option.rows;

      // Check if beat size is within acceptable range
      if (
        beatWidth >= this.minBeatSize &&
        beatHeight >= this.minBeatSize &&
        beatWidth <= this.maxBeatSize &&
        beatHeight <= this.maxBeatSize
      ) {
        return {
          ...option,
          beatWidth: Math.floor(beatWidth),
          beatHeight: Math.floor(beatHeight),
          spacingX,
          spacingY,
        };
      }
    }

    // If no option fits well, use the most efficient one with scaled-down beats
    const bestOption = gridOptions[0]!;
    const maxBeatWidth =
      (availableWidth - this.minSpacing * (bestOption.columns - 1)) /
      bestOption.columns;
    const maxBeatHeight =
      (availableHeight - this.minSpacing * (bestOption.rows - 1)) /
      bestOption.rows;

    return {
      rows: bestOption.rows,
      columns: bestOption.columns,
      beatWidth: Math.max(this.minBeatSize, Math.floor(maxBeatWidth)),
      beatHeight: Math.max(this.minBeatSize, Math.floor(maxBeatHeight)),
      spacingX: this.minSpacing,
      spacingY: this.minSpacing,
    };
  }

  private createFallbackLayout(
    beatCount: number,
    dimensions: WordCardDimensions
  ): BeatLayout {
    const availableWidth = dimensions.width - this.padding * 2;
    const availableHeight = dimensions.height - this.padding * 2;

    // Simple single-row layout
    const beatWidth = Math.min(
      (availableWidth - this.minSpacing * (beatCount - 1)) / beatCount,
      this.maxBeatSize
    );

    return {
      rows: 1,
      columns: beatCount,
      beatWidth: Math.max(this.minBeatSize, Math.floor(beatWidth)),
      beatHeight: Math.max(this.minBeatSize, Math.floor(availableHeight)),
      spacing: { x: this.minSpacing, y: this.minSpacing },
    };
  }

  private calculateOptimalAspectRatio(beatCount: number): number {
    // Common aspect ratios based on beat count
    if (beatCount <= 3) return 16 / 9; // Wide for few beats
    if (beatCount <= 6) return 4 / 3; // Standard for medium counts
    if (beatCount <= 12) return 1 / 1; // Square for many beats
    return 3 / 4; // Tall for lots of beats
  }

  private createContainerSVG(dimensions: WordCardDimensions): string {
    return `<svg width="${dimensions.width}" height="${dimensions.height}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${dimensions.width} ${dimensions.height}">`;
  }

  private createBeatsGroup(beatSVGs: string[], layout: BeatLayout): string {
    let beatsGroup = `<g id="beats-group" transform="translate(${this.padding}, ${this.padding})">`;

    for (let i = 0; i < beatSVGs.length; i++) {
      const row = Math.floor(i / layout.columns);
      const col = i % layout.columns;

      const x = col * (layout.beatWidth + layout.spacing.x);
      const y = row * (layout.beatHeight + layout.spacing.y);

      // Extract SVG content (remove outer SVG tags)
      const svgContent = this.extractSVGContent(beatSVGs[i]!);

      beatsGroup += `
        <g transform="translate(${x}, ${y})">
          <svg x="0" y="0" width="${layout.beatWidth}" height="${layout.beatHeight}" viewBox="0 0 ${layout.beatWidth} ${layout.beatHeight}">
            ${svgContent}
          </svg>
        </g>`;
    }

    beatsGroup += "</g>";
    return beatsGroup;
  }

  private extractSVGContent(svgString: string): string {
    // Extract content between <svg> and </svg> tags
    const match = svgString.match(/<svg[^>]*>([\s\S]*?)<\/svg>/i);
    return match ? match[1]! : svgString;
  }

  private combineSVGElements(containerSVG: string, beatsGroup: string): string {
    return `${containerSVG}
      <!-- Background -->
      <rect width="100%" height="100%" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
      
      <!-- Beats -->
      ${beatsGroup}
    </svg>`;
  }
}
