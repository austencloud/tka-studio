/**
 * SVG Conversion Service Interfaces
 *
 * Service contracts for converting SVG elements and strings to Canvas.
 * Consolidates the SVG-to-Canvas conversion logic that was duplicated
 * across 4+ different services in the image export system.
 */

import type { RenderQualitySettings, SVGConversionOptions } from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISVGToCanvasConverterService {
  /**
   * Convert SVG string to Canvas
   * Consolidates logic from BeatRenderingService, SequenceCardImageGenerationService, etc.
   */
  convertSVGStringToCanvas(
    svgString: string,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Convert SVG element to Canvas
   * For when you already have an SVGElement instance
   */
  convertSVGElementToCanvas(
    svgElement: SVGElement,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement>;

  /**
   * Batch convert multiple SVG strings
   * Optimized for sequence rendering
   */
  convertMultipleSVGsToCanvases(
    svgStrings: string[],
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement[]>;

  /**
   * Set default quality settings for all conversions
   */
  setDefaultQuality(settings: RenderQualitySettings): void;

  /**
   * Get current quality settings
   */
  getQualitySettings(): RenderQualitySettings;

  /**
   * Validate SVG content before conversion
   */
  validateSVG(svgContent: string | SVGElement): boolean;

  /**
   * Get memory usage statistics
   */
  getMemoryUsage(): {
    activeConversions: number;
    totalMemoryUsed: number;
    peakMemoryUsed: number;
  };

  /**
   * Cleanup resources and cancel pending operations
   */
  cleanup(): void;
}

// ============================================================================
// RE-EXPORT TYPES FOR EXTERNAL USE
// ============================================================================

// REMOVED: Domain model re-exports. Import directly from $domain instead.
// Contracts should only contain service interface definitions.
