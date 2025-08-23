/**
 * Simple Beat Fallback Service
 * Just handles the basic cases without overengineering
 */

import type {
  EmptyBeatOptions,
  ErrorBeatOptions,
  IBeatFallbackRenderingService,
} from "../../interfaces/beat-fallback-interfaces";

export class BeatFallbackRenderingService
  implements IBeatFallbackRenderingService
{
  /**
   * Create error beat canvas - just a simple red X
   */
  createErrorBeat(options: ErrorBeatOptions): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    canvas.width = options.size;
    canvas.height = options.size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    // White background
    ctx.fillStyle = options.backgroundColor || "white";
    ctx.fillRect(0, 0, options.size, options.size);

    // Simple red X
    ctx.strokeStyle = "#dc3545";
    ctx.lineWidth = 3;
    const margin = options.size * 0.3;
    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(options.size - margin, options.size - margin);
    ctx.moveTo(options.size - margin, margin);
    ctx.lineTo(margin, options.size - margin);
    ctx.stroke();

    return canvas;
  }

  /**
   * Create empty beat canvas - just white
   */
  createEmptyBeat(options: EmptyBeatOptions): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    canvas.width = options.size;
    canvas.height = options.size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    // Just white background
    ctx.fillStyle = options.backgroundColor || "white";
    ctx.fillRect(0, 0, options.size, options.size);

    return canvas;
  }

  /**
   * Create default start position - just white canvas
   */
  createDefaultStartPosition(
    size: number,
    backgroundColor = "white"
  ): HTMLCanvasElement {
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;

    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, size, size);

    return canvas;
  }

  // Stub implementations for interface compatibility
  createLoadingBeat(): HTMLCanvasElement {
    throw new Error("Loading beats not implemented - use simple fallback");
  }

  createErrorBeatSVG(): string {
    throw new Error("SVG error beats not implemented - use canvas version");
  }

  createEmptyBeatSVG(): string {
    throw new Error("SVG empty beats not implemented - use canvas version");
  }

  validateFallbackOptions(): boolean {
    return true; // Always valid for simple implementation
  }
}
