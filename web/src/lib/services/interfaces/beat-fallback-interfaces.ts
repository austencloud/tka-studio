/**
 * Simple Beat Fallback Service Interfaces
 * Just the basics without overengineering
 */

export interface EmptyBeatOptions {
  size: number;
  backgroundColor?: string;
}

export interface ErrorBeatOptions {
  size: number;
  backgroundColor?: string;
}

/**
 * Simple beat fallback rendering service
 */
export interface IBeatFallbackRenderingService {
  /**
   * Create error beat canvas - simple red X
   */
  createErrorBeat(options: ErrorBeatOptions): HTMLCanvasElement;

  /**
   * Create empty beat canvas - just white
   */
  createEmptyBeat(options: EmptyBeatOptions): HTMLCanvasElement;

  /**
   * Create default start position - just white canvas
   */
  createDefaultStartPosition(
    size: number,
    backgroundColor?: string
  ): HTMLCanvasElement;

  // Stub methods for interface compatibility (will throw if used)
  createLoadingBeat(): HTMLCanvasElement;
  createErrorBeatSVG(): string;
  createEmptyBeatSVG(): string;
  validateFallbackOptions(): boolean;
}
