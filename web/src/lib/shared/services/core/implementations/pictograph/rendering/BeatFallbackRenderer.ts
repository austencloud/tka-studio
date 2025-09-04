/**
 * Simple Beat Fallback Service
 * Just handles the basic cases without overengineering
 */

import type { BeatData } from "$domain";
import type {
  EmptyBeatOptions,
  ErrorBeatOptions,
  FallbackRenderOptions,
  FallbackRenderResult,
  IBeatFallbackRenderer,
} from "$services";
import { injectable } from "inversify";

@injectable()
export class BeatFallbackRenderer implements IBeatFallbackRenderer {
  /**
   * Create error beat canvas - just a simple red X
   */
  async createErrorBeat(options: ErrorBeatOptions): Promise<HTMLCanvasElement> {
    const canvas = document.createElement("canvas");
    const size = options.size?.width || options.size?.height || 100;
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    // White background
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, size, size);

    // Simple red X
    ctx.strokeStyle = "#dc3545";
    ctx.lineWidth = 3;
    const margin = size * 0.3;
    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(size - margin, size - margin);
    ctx.moveTo(size - margin, margin);
    ctx.lineTo(margin, size - margin);
    ctx.stroke();

    return canvas;
  }

  /**
   * Create empty beat canvas - just white
   */
  async createEmptyBeat(
    _options: EmptyBeatOptions
  ): Promise<HTMLCanvasElement> {
    const canvas = document.createElement("canvas");
    const size = 100; // Default size since EmptyBeatOptions doesn't have size in the interface
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    // Just white background
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, size, size);

    return canvas;
  }

  /**
   * Create default start position - just white canvas
   */
  async createDefaultStartPosition(): Promise<HTMLCanvasElement> {
    const canvas = document.createElement("canvas");
    const size = 100; // Default size
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, size, size);

    return canvas;
  }

  /**
   * Render a fallback representation of a beat
   */
  async renderFallback(
    beat: BeatData,
    canvas: HTMLCanvasElement,
    options?: FallbackRenderOptions
  ): Promise<FallbackRenderResult> {
    try {
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        return { success: false, error: "Failed to get canvas context" };
      }

      // Clear canvas
      ctx.fillStyle = options?.backgroundColor || "white";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Simple fallback rendering
      if (beat.isBlank) {
        // Just leave it white
      } else {
        // Draw a simple placeholder
        ctx.fillStyle = options?.textColor || "#666";
        ctx.font = `${options?.fontSize || 12}px Arial`;
        ctx.textAlign = "center";
        ctx.fillText("Beat", canvas.width / 2, canvas.height / 2);
      }

      return { success: true, canvas };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Check if fallback rendering is needed
   */
  shouldUseFallback(beat: BeatData): boolean {
    return beat.isBlank || !beat.pictographData;
  }

  /**
   * Get default fallback options
   */
  getDefaultOptions(): FallbackRenderOptions {
    return {
      showErrorMessage: true,
      backgroundColor: "white",
      textColor: "#666",
      fontSize: 12,
    };
  }

  /**
   * Clear fallback cache
   */
  clearCache(): void {
    // No cache to clear in this simple implementation
  }
}
