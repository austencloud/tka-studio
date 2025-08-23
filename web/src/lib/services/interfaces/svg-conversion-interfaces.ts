/**
 * SVG Conversion Service Interfaces
 *
 * Service contracts for converting SVG elements and strings to Canvas.
 * Consolidates the SVG-to-Canvas conversion logic that was duplicated
 * across 4+ different services in the image export system.
 */

export interface RenderQualitySettings {
  antialiasing: boolean;
  smoothScaling: boolean;
  imageSmoothingQuality: "low" | "medium" | "high";
  scale: number;
}

export interface SVGConversionOptions {
  width: number;
  height: number;
  backgroundColor?: string;
  quality?: RenderQualitySettings;
  preserveAspectRatio?: boolean;
}

export interface ConversionResult {
  success: boolean;
  canvas?: HTMLCanvasElement;
  error?: string;
  metadata: {
    originalWidth: number;
    originalHeight: number;
    finalWidth: number;
    finalHeight: number;
    conversionTime: number;
  };
}

/**
 * Core SVG to Canvas conversion service
 * Replaces duplicate implementations across the codebase
 */
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
