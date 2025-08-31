/**
 * Beat Fallback Rendering Service Interfaces
 *
 * Service contracts for fallback beat rendering when primary rendering fails.
 */

import type { BeatData } from "$domain";

// ============================================================================
// DATA CONTRACTS
// ============================================================================

export interface FallbackRenderOptions {
  showErrorMessage: boolean;
  errorMessageText?: string;
  backgroundColor?: string;
  textColor?: string;
  fontSize?: number;
}

export interface FallbackRenderResult {
  success: boolean;
  canvas?: HTMLCanvasElement;
  error?: string;
}

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IBeatFallbackRenderer {
  /**
   * Render a fallback representation of a beat
   */
  renderFallback(
    beat: BeatData,
    canvas: HTMLCanvasElement,
    options?: FallbackRenderOptions
  ): Promise<FallbackRenderResult>;

  /**
   * Check if fallback rendering is needed
   */
  shouldUseFallback(beat: BeatData): boolean;

  /**
   * Get default fallback options
   */
  getDefaultOptions(): FallbackRenderOptions;

  /**
   * Clear fallback cache
   */
  clearCache(): void;

  /**
   * Create an empty beat placeholder
   */
  createEmptyBeat(options: EmptyBeatOptions): Promise<HTMLCanvasElement>;

  /**
   * Create an error beat display
   */
  createErrorBeat(options: ErrorBeatOptions): Promise<HTMLCanvasElement>;

  /**
   * Create a default start position beat
   */
  createDefaultStartPosition(): Promise<HTMLCanvasElement>;
}

// Missing data types
export interface EmptyBeatOptions {
  showPlaceholder: boolean;
  placeholderText?: string;
}

export interface ErrorBeatOptions {
  showError: boolean;
  errorMessage?: string;
  size?: { width: number; height: number };
}
