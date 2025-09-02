/**
 * Sequence Card Image Generation Service
 *
 * Handles generation of sequence card images from sequence data.
 * Single responsibility: Converting sequence data to images via SVG composition.
 */

// Domain types
import type { BeatData, SequenceCardDimensions, SequenceData } from "$domain";

// Behavioral contracts
import type {
  ISequenceCardImageGenerationService,
  ISequenceCardMetadataOverlayService,
  ISequenceCardSVGCompositionService,
} from "../../../contracts/sequence-card-export-interfaces";

import { injectable } from "inversify";
import { renderPictograph } from "../../pictograph-rendering-utils";

@injectable()
export class SequenceCardImageGenerationService
  implements ISequenceCardImageGenerationService
{
  constructor(
    private readonly svgCompositionService: ISequenceCardSVGCompositionService,
    private readonly metadataService: ISequenceCardMetadataOverlayService
  ) {}

  /**
   * Generate image for a single sequence
   */
  async generateSequenceImage(
    sequence: SequenceData,
    dimensions: SequenceCardDimensions
  ): Promise<HTMLCanvasElement> {
    try {
      console.log(`🎨 Generating image for sequence: ${sequence.name}`);

      // Validate sequence data
      if (!this.validateSequenceData(sequence)) {
        throw new Error("Invalid sequence data provided");
      }

      // Step 1: Generate SVG for each beat
      console.log(`📊 Rendering ${sequence.beats.length} beats...`);
      const beatSVGs = await this.renderBeats([...sequence.beats]);

      // Step 2: Compose beats into sequence layout
      console.log("🔧 Composing sequence layout...");
      const sequenceSVG = await this.svgCompositionService.createSequenceLayout(
        beatSVGs,
        dimensions
      );

      // Step 3: Add metadata overlays
      console.log("🏷️ Adding metadata overlays...");
      const finalSVG = await this.metadataService.addMetadataOverlays(
        sequenceSVG,
        sequence,
        {
          title: sequence.name,
          author: sequence.metadata?.author as string,
          beatNumbers: true,
          timestamp: false,
          backgroundColor: "#ffffff",
        },
        dimensions
      );

      // Step 4: Convert SVG to Canvas
      console.log("🖼️ Converting SVG to canvas...");
      const canvas = await this.svgToCanvas(finalSVG, dimensions);

      console.log(
        `✅ Successfully generated image for sequence: ${sequence.name}`
      );
      return canvas;
    } catch (error) {
      console.error(
        `❌ Failed to generate image for sequence ${sequence.name}:`,
        error
      );

      // Return fallback canvas with error message
      return this.createErrorCanvas(
        `Failed to generate image: ${error instanceof Error ? error.message : "Unknown error"}`,
        dimensions
      );
    }
  }

  /**
   * Validate sequence data for image generation
   */
  validateSequenceData(sequence: SequenceData): boolean {
    try {
      // Check basic structure
      if (!sequence) {
        console.error("❌ Sequence data is null or undefined");
        return false;
      }

      if (!sequence.beats || !Array.isArray(sequence.beats)) {
        console.error("❌ Sequence beats is not an array");
        return false;
      }

      if (sequence.beats.length === 0) {
        console.error("❌ Sequence has no beats");
        return false;
      }

      // Check each beat has required data
      for (let i = 0; i < sequence.beats.length; i++) {
        const beat = sequence.beats[i];
        if (!beat) {
          console.error(`❌ Beat ${i} is null or undefined`);
          return false;
        }

        // Basic beat validation - adjust based on your BeatData structure
        if (!beat.blue || !beat.red) {
          console.error(`❌ Beat ${i} missing required motion data`);
          return false;
        }
      }

      console.log(
        `✅ Sequence validation passed: ${sequence.beats.length} beats`
      );
      return true;
    } catch (error) {
      console.error("❌ Sequence validation failed:", error);
      return false;
    }
  }

  /**
   * Get recommended dimensions for sequence
   */
  getRecommendedDimensions(beatCount: number): SequenceCardDimensions {
    try {
      // Base dimensions
      let width = 800;
      let height = 600;

      // Adjust based on beat count
      if (beatCount <= 3) {
        // Wide format for few beats
        width = 900;
        height = 400;
      } else if (beatCount <= 6) {
        // Standard format
        width = 800;
        height = 600;
      } else if (beatCount <= 12) {
        // Square format for many beats
        width = 800;
        height = 800;
      } else {
        // Tall format for lots of beats
        width = 600;
        height = 1000;
      }

      const dimensions: SequenceCardDimensions = {
        width,
        height,
        scale: 1,
      };

      console.log(
        `📏 Recommended dimensions for ${beatCount} beats:`,
        dimensions
      );
      return dimensions;
    } catch (error) {
      console.error("❌ Failed to calculate recommended dimensions:", error);

      // Fallback dimensions
      return {
        width: 800,
        height: 600,
        scale: 1,
      };
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private async renderBeats(beats: BeatData[]): Promise<string[]> {
    const beatSVGs: string[] = [];

    for (let i = 0; i < beats.length; i++) {
      try {
        const beat = beats[i];
        console.log(`🎯 Rendering beat ${i + 1}/${beats.length}`);

        // Check if pictograph data exists
        if (!beat.pictographData) {
          console.warn(
            `⚠️ Beat ${i + 1} has no pictograph data, using fallback`
          );
          const fallbackSVG = this.createFallbackBeatSVG(i + 1);
          beatSVGs.push(fallbackSVG);
          continue;
        }

        // Use direct composition utility to render the beat
        const pictographSVGElement = await renderPictograph(
          beat.pictographData
        );
        const beatSVG = this.svgElementToString(pictographSVGElement);
        beatSVGs.push(beatSVG);
      } catch (error) {
        console.error(`❌ Failed to render beat ${i + 1}:`, error);

        // Create fallback SVG for failed beat
        const fallbackSVG = this.createFallbackBeatSVG(i + 1);
        beatSVGs.push(fallbackSVG);
      }
    }

    return beatSVGs;
  }

  private async svgToCanvas(
    svgString: string,
    dimensions: SequenceCardDimensions
  ): Promise<HTMLCanvasElement> {
    return new Promise((resolve, reject) => {
      try {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        if (!ctx) {
          reject(new Error("Could not get 2D context"));
          return;
        }

        const scale = dimensions.scale || 1;
        canvas.width = dimensions.width * scale;
        canvas.height = dimensions.height * scale;

        // Create image from SVG
        const img = new Image();
        const svgBlob = new Blob([svgString], { type: "image/svg+xml" });
        const url = URL.createObjectURL(svgBlob);

        img.onload = () => {
          try {
            // High quality rendering
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";

            // Draw to canvas
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            URL.revokeObjectURL(url);
            resolve(canvas);
          } catch (error) {
            URL.revokeObjectURL(url);
            reject(new Error(`Failed to draw SVG to canvas: ${error}`));
          }
        };

        img.onerror = () => {
          URL.revokeObjectURL(url);
          reject(new Error("Failed to load SVG image"));
        };

        img.src = url;
      } catch (error) {
        reject(new Error(`SVG to Canvas conversion failed: ${error}`));
      }
    });
  }

  private svgElementToString(svgElement: SVGElement): string {
    try {
      // Create a temporary container
      const serializer = new XMLSerializer();
      return serializer.serializeToString(svgElement);
    } catch (error) {
      console.error("❌ Failed to serialize SVG element:", error);
      return this.createFallbackBeatSVG(0);
    }
  }

  private createFallbackBeatSVG(beatNumber: number): string {
    return `
      <svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f5f5f5" stroke="#ddd" stroke-width="2" rx="8"/>
        <text x="60" y="60" text-anchor="middle" dominant-baseline="central" 
              font-family="sans-serif" font-size="14" fill="#666">
          Beat ${beatNumber}
        </text>
        <text x="60" y="80" text-anchor="middle" dominant-baseline="central" 
              font-family="sans-serif" font-size="10" fill="#999">
          (Error)
        </text>
      </svg>`;
  }

  private createErrorCanvas(
    errorMessage: string,
    dimensions: SequenceCardDimensions
  ): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    if (!ctx) {
      return canvas;
    }

    canvas.width = dimensions.width;
    canvas.height = dimensions.height;

    // Draw error state
    ctx.fillStyle = "#f8f9fa";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Border
    ctx.strokeStyle = "#dee2e6";
    ctx.lineWidth = 2;
    ctx.strokeRect(1, 1, canvas.width - 2, canvas.height - 2);

    // Error icon (simple X)
    ctx.strokeStyle = "#dc3545";
    ctx.lineWidth = 4;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const size = 30;

    ctx.beginPath();
    ctx.moveTo(centerX - size, centerY - size);
    ctx.lineTo(centerX + size, centerY + size);
    ctx.moveTo(centerX + size, centerY - size);
    ctx.lineTo(centerX - size, centerY + size);
    ctx.stroke();

    // Error text
    ctx.fillStyle = "#6c757d";
    ctx.font = "16px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Generation Failed", centerX, centerY + 60);

    // Error message (truncated if too long)
    ctx.font = "12px system-ui, sans-serif";
    const truncatedMessage =
      errorMessage.length > 50
        ? errorMessage.substring(0, 47) + "..."
        : errorMessage;
    ctx.fillText(truncatedMessage, centerX, centerY + 80);

    return canvas;
  }
}
