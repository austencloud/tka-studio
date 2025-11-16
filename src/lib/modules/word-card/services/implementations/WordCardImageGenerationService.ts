/**
 * Word Card Image Generation Service
 *
 * Handles generation of word card images from sequence data.
 * Single responsibility: Converting sequence data to images via SVG composition.
 */

// Domain types
import type { SequenceData, WordCardDimensions } from "$shared";

// Behavioral contracts
import type { IWordCardMetadataOverlayService, IWordCardSVGCompositionService } from "../contracts";
import {  } from "../contracts";
import type { IWordCardImageGenerationService } from "../contracts";

import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class WordCardImageGenerationService
  implements IWordCardImageGenerationService
{
  constructor(
    @inject(TYPES.IWordCardSVGCompositionService)
    private readonly svgCompositionService: IWordCardSVGCompositionService,
    @inject(TYPES.IWordCardMetadataOverlayService)
    private readonly metadataService: IWordCardMetadataOverlayService
  ) {}

  /**
   * Generate image for a single sequence
   */
  async generateSequenceImage(
    sequence: SequenceData,
    dimensions: WordCardDimensions
  ): Promise<HTMLCanvasElement> {
    try {
      // Validate sequence data
      if (!this.validateSequenceData(sequence)) {
        throw new Error("Invalid sequence data provided");
      }

      // Step 1: Compose sequence layout (includes beat rendering)
      const sequenceSVG = await this.svgCompositionService.composeSVG(
        sequence,
        dimensions
      );

      // Step 2: Convert SVG to Canvas
      const baseCanvas = await this.svgToCanvas(sequenceSVG, dimensions);

      // Step 3: Add metadata overlays
      const canvas = this.metadataService.addMetadataOverlay(
        baseCanvas,
        {
          title: sequence.name,
          author: sequence.metadata.author as string,
          beatNumbers: true,
          timestamp: false,
          backgroundColor: "#ffffff",
        },
        dimensions
      );

      return canvas;
    } catch (error) {
      console.error(
        `Failed to generate image for sequence ${sequence.name}:`,
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
   * Validate sequence data for image generation (from original word card implementation)
   */
  validateSequenceData(sequence: SequenceData): boolean {
    try {
      // Check basic structure
      if (!sequence) {
        console.error("Sequence data is null or undefined");
        return false;
      }

      if (!sequence.beats || !Array.isArray(sequence.beats)) {
        console.error("Sequence beats is not an array");
        return false;
      }

      if (sequence.beats.length === 0) {
        console.error("Sequence has no beats");
        return false;
      }

      // Check each beat has required data
      for (let i = 0; i < sequence.beats.length; i++) {
        const beat = sequence.beats[i];
        if (!beat) {
          console.error(`Beat ${i} is null or undefined`);
          return false;
        }

        // Basic beat validation - adjust based on your BeatData structure
        if (!beat.blue || !beat.red) {
          console.error(`Beat ${i} missing required motion data`);
          return false;
        }
      }

      return true;
    } catch (error) {
      console.error("Sequence validation failed:", error);
      return false;
    }
  }

  /**
   * Get recommended dimensions for sequence
   */
  getRecommendedDimensions(beatCount: number): WordCardDimensions {
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

      return {
        width,
        height,
        scale: 1,
      };
    } catch (error) {
      console.error("Failed to calculate recommended dimensions:", error);

      // Fallback dimensions
      return {
        width: 800,
        height: 600,
        scale: 1,
      };
    }
  }

  private async svgToCanvas(
    svgString: string,
    dimensions: WordCardDimensions
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

  private createErrorCanvas(
    errorMessage: string,
    dimensions: WordCardDimensions
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

  /**
   * Generate word card image (interface method)
   */
  async generateWordCardImage(
    sequence: SequenceData,
    dimensions: { width: number; height: number }
  ): Promise<HTMLCanvasElement> {
    const wordCardDimensions: WordCardDimensions = {
      width: dimensions.width,
      height: dimensions.height,
      scale: 1,
    };
    return this.generateSequenceImage(sequence, wordCardDimensions);
  }

  /**
   * Generate batch images using the original word card logic
   */
  async generateBatchImages(
    sequences: SequenceData[],
    dimensions: { width: number; height: number }
  ): Promise<Map<string, HTMLCanvasElement>> {
    const results = new Map<string, HTMLCanvasElement>();

    for (const sequence of sequences) {
      try {
        const canvas = await this.generateWordCardImage(sequence, dimensions);
        results.set(sequence.id, canvas);
      } catch (error) {
        console.error(
          `Failed to generate image for sequence ${sequence.name}:`,
          error
        );
        // Create error canvas for failed sequences using original logic
        const errorCanvas = this.createErrorCanvas(
          `Failed to generate: ${sequence.name} - ${error instanceof Error ? error.message : "Unknown error"}`,
          { width: dimensions.width, height: dimensions.height, scale: 1 }
        );
        results.set(sequence.id, errorCanvas);
      }
    }

    return results;
  }
}
