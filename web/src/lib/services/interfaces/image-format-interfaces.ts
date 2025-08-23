/**
 * Image Format Conversion Service Interfaces
 *
 * Service contracts for converting Canvas to various image formats.
 * Consolidates the canvas-to-blob/dataURL logic that was duplicated
 * across FileExportService, SequenceCardImageConversionService,
 * PageImageExportService, and others.
 */

export interface ImageFormatOptions {
  format: "PNG" | "JPEG" | "WEBP";
  quality: number; // 0-1, only used for JPEG/WEBP
  optimize: boolean;
}

export interface OptimizationSettings {
  useCase: "web" | "print" | "archive";
  maxFileSize?: number; // bytes
  preserveQuality?: boolean;
  compressionLevel?: number; // 0-9
}

export interface ConversionMetrics {
  originalSize: number; // bytes
  compressedSize: number; // bytes
  compressionRatio: number; // 0-1
  processingTime: number; // ms
  format: string;
  dimensions: { width: number; height: number };
}

export interface ConversionResult {
  success: boolean;
  blob?: Blob;
  dataURL?: string;
  error?: string;
  metrics: ConversionMetrics;
}

/**
 * Core image format conversion service
 * Replaces duplicate canvas-to-blob implementations
 */
export interface IImageFormatConverterService {
  /**
   * Convert Canvas to Blob
   * Consolidates logic from FileExportService, SequenceCardImageConversionService, etc.
   */
  canvasToBlob(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): Promise<Blob>;

  /**
   * Convert Canvas to Data URL
   * For immediate display in UI
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): string;

  /**
   * Batch convert multiple canvases
   * Optimized for sequence export
   */
  convertMultipleCanvasesToBlobs(
    canvases: HTMLCanvasElement[],
    options: ImageFormatOptions
  ): Promise<Blob[]>;

  /**
   * Optimize image for specific use case
   * Applies compression, resizing, and format selection
   */
  optimizeForUseCase(
    blob: Blob,
    optimization: OptimizationSettings
  ): Promise<Blob>;

  /**
   * Get optimal format for content type
   * Analyzes image and recommends best format
   */
  getOptimalFormat(canvas: HTMLCanvasElement): "PNG" | "JPEG" | "WEBP";

  /**
   * Validate format and quality settings
   */
  validateFormatOptions(options: ImageFormatOptions): boolean;

  /**
   * Get supported formats for current browser
   */
  getSupportedFormats(): string[];

  /**
   * Estimate file size before conversion
   */
  estimateFileSize(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): number;

  /**
   * Get conversion statistics
   */
  getConversionStats(): {
    totalConversions: number;
    totalBytesProcessed: number;
    averageCompressionRatio: number;
    formatUsage: Record<string, number>;
  };

  /**
   * Cleanup resources
   */
  cleanup(): void;
}
