/**
 * Page Image Export Service Implementation
 *
 * Handles exporting page elements as images using html2canvas.
 * Supports PNG, JPEG, and WebP formats with quality and scaling options.
 */

// Html2Canvas interface for type safety
interface Html2CanvasFunction {
  (
    element: HTMLElement,
    options?: Html2CanvasOptions
  ): Promise<HTMLCanvasElement>;
}

interface Html2CanvasOptions {
  scale?: number;
  backgroundColor?: string;
  useCORS?: boolean;
  allowTaint?: boolean;
  width?: number;
  height?: number;
  removeContainer?: boolean;
  [key: string]: unknown; // Allow additional html2canvas options
}

interface WindowWithHtml2Canvas extends Window {
  html2canvas?: Html2CanvasFunction;
}

import type {
  IPageImageExportService,
  ImageExportOptions,
  ServiceExportResult,
  BatchExportResult,
  ExportProgress,
} from "../../interfaces/export-interfaces";

export class PageImageExportService implements IPageImageExportService {
  private abortController: AbortController | null = null;
  private currentProgress: ExportProgress | null = null;

  async exportPageAsImage(
    pageElement: HTMLElement,
    options: ImageExportOptions
  ): Promise<ServiceExportResult> {
    const startTime = performance.now();

    try {
      // Validate options
      const validation = this.validateExportOptions(options);
      if (!validation) {
        throw new Error(`Invalid export options`);
      }

      // Dynamic import of html2canvas (only load when needed)
      const html2canvas = await this.loadHtml2Canvas();

      // Prepare element for capture
      const preparedElement = this.prepareElementForCapture(pageElement);

      // Calculate dimensions
      const dimensions = this.calculateCaptureDimensions(
        preparedElement,
        options
      );

      // Capture the element
      const canvas = await html2canvas(preparedElement, {
        width: dimensions.width,
        height: dimensions.height,
        scale: options.scale,
        backgroundColor: options.backgroundColor || "#ffffff",
        useCORS: true,
        allowTaint: false,
        removeContainer: true,
        logging: false,
        // High quality rendering
        scrollX: 0,
        scrollY: 0,
        windowWidth: dimensions.width,
        windowHeight: dimensions.height,
      });

      // Convert canvas to blob
      const blob = await this.canvasToBlob(canvas, options);

      const processingTime = performance.now() - startTime;

      return {
        sequenceId: "page-export",
        success: true,
        blob,
        filename: this.generateFilename(options.format),
        metrics: {
          processingTime,
          fileSize: blob.size,
          resolution: { width: canvas.width, height: canvas.height },
        },
        metadata: {
          format: options.format,
          size: blob.size,
          dimensions: {
            width: canvas.width,
            height: canvas.height,
          },
          processingTime,
        },
      };
    } catch (error) {
      const processingTime = performance.now() - startTime;

      return {
        sequenceId: "page-export",
        success: false,
        filename: this.generateFilename(options.format),
        error: error as Error,
        metrics: {
          processingTime,
          fileSize: 0,
          resolution: { width: 0, height: 0 },
        },
        metadata: {
          format: options.format,
          size: 0,
          processingTime,
        },
      };
    }
  }

  async exportPagesAsImages(
    pageElements: HTMLElement[],
    options: ImageExportOptions,
    onProgress?: (progress: ExportProgress) => void
  ): Promise<BatchExportResult> {
    const startTime = performance.now();
    const results: ServiceExportResult[] = [];
    const errors: Error[] = [];
    let successCount = 0;
    let failureCount = 0;

    // Create abort controller for cancellation
    this.abortController = new AbortController();

    try {
      // Load html2canvas once for batch operation
      const html2canvas = await this.loadHtml2Canvas();

      for (let i = 0; i < pageElements.length; i++) {
        // Check for cancellation
        if (this.abortController.signal.aborted) {
          break;
        }

        // Update progress
        const progress: ExportProgress = {
          current: i + 1,
          total: pageElements.length,
          percentage: ((i + 1) / pageElements.length) * 100,
          currentPage: i + 1,
          currentOperation: `Exporting page ${i + 1} of ${pageElements.length}`,
          estimatedTimeRemaining: this.estimateTimeRemaining(
            i + 1,
            pageElements.length,
            performance.now() - startTime
          ),
        };

        this.currentProgress = progress;
        onProgress?.(progress);

        try {
          const result = await this.exportSinglePageWithCanvas(
            pageElements[i],
            html2canvas,
            options,
            i + 1
          );

          results.push(result);

          if (result.success) {
            successCount++;
          } else {
            failureCount++;
            if (result.error) {
              errors.push(result.error);
            }
          }
        } catch (error) {
          failureCount++;
          const err = error as Error;
          errors.push(err);

          results.push({
            sequenceId: `page-${i + 1}`,
            success: false,
            filename: this.generateFilename(options.format, i + 1),
            error: err,
            metrics: {
              processingTime: 0,
              fileSize: 0,
              resolution: { width: 0, height: 0 },
            },
            metadata: {
              format: options.format,
              size: 0,
              processingTime: 0,
            },
          });
        }

        // Brief pause to allow UI updates and prevent blocking
        await this.pauseForUI();
      }
    } catch (error) {
      errors.push(error as Error);
    } finally {
      this.abortController = null;
      this.currentProgress = null;
    }

    const totalProcessingTime = performance.now() - startTime;

    return {
      totalPages: pageElements.length,
      successCount,
      failureCount,
      results,
      totalProcessingTime,
      errors,
    };
  }

  calculateOptimalDimensions(
    pageElement: HTMLElement,
    targetDPI: number
  ): { width: number; height: number } {
    const rect = pageElement.getBoundingClientRect();
    const scaleFactor = targetDPI / 96; // 96 DPI is standard screen DPI

    return {
      width: Math.round(rect.width * scaleFactor),
      height: Math.round(rect.height * scaleFactor),
    };
  }

  validateExportOptions(options: ImageExportOptions): boolean {
    // Validate format
    if (!["PNG", "JPEG", "WebP"].includes(options.format)) {
      return false;
    }

    // Validate quality
    if (options.quality < 0 || options.quality > 1) {
      return false;
    }

    // Validate scale
    if (options.scale <= 0) {
      return false;
    }

    // Validate dimensions if provided
    if (options.width && options.width <= 0) {
      return false;
    }

    if (options.height && options.height <= 0) {
      return false;
    }

    return true;
  }

  getSupportedFormats(): string[] {
    return ["PNG", "JPEG", "WebP"];
  }

  getRecommendedSettings(
    useCase: "print" | "web" | "archive"
  ): ImageExportOptions {
    const baseOptions = {
      quality: 0.9,
      scale: 1.0,
      backgroundColor: "#ffffff",
    };

    switch (useCase) {
      case "print":
        return {
          ...baseOptions,
          format: "PNG" as const,
          scale: 2.0,
          quality: 1.0,
        };
      case "web":
        return {
          ...baseOptions,
          format: "JPEG" as const,
          scale: 1.0,
          quality: 0.8,
        };
      case "archive":
        return {
          ...baseOptions,
          format: "PNG" as const,
          scale: 1.5,
          quality: 1.0,
        };
      default:
        return {
          ...baseOptions,
          format: "PNG" as const,
        };
    }
  }

  // Cancel ongoing export
  cancelExport(): void {
    if (this.abortController) {
      this.abortController.abort();
    }
  }

  // Get current progress
  getCurrentProgress(): ExportProgress | null {
    return this.currentProgress;
  }

  // Private helper methods

  private async loadHtml2Canvas(): Promise<Html2CanvasFunction> {
    try {
      // Try to load from CDN
      if (
        typeof window !== "undefined" &&
        !(window as WindowWithHtml2Canvas).html2canvas
      ) {
        // Dynamically load html2canvas from CDN
        const script = document.createElement("script");
        script.src =
          "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";

        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
          document.head.appendChild(script);
        });
      }

      const html2canvas = (window as WindowWithHtml2Canvas).html2canvas;
      if (!html2canvas) {
        throw new Error("html2canvas failed to load");
      }

      return html2canvas;
    } catch (error) {
      throw new Error(
        "Failed to load html2canvas library. Check internet connection."
      );
    }
  }

  private prepareElementForCapture(element: HTMLElement): HTMLElement {
    // Clone the element to avoid modifying the original
    const clonedElement = element.cloneNode(true) as HTMLElement;

    // Apply capture-specific styles
    clonedElement.style.position = "static";
    clonedElement.style.transform = "none";
    clonedElement.style.margin = "0";
    clonedElement.style.padding = "0";

    // Ensure all images are loaded
    const images = clonedElement.querySelectorAll("img");
    images.forEach((img) => {
      if (!img.complete) {
        // Replace with placeholder if image not loaded
        img.src =
          "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwIiB5PSI1MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+SW1hZ2U8L3RleHQ+PC9zdmc+";
      }
    });

    return clonedElement;
  }

  private calculateCaptureDimensions(
    element: HTMLElement,
    options: ImageExportOptions
  ): { width: number; height: number } {
    const rect = element.getBoundingClientRect();

    if (options.width && options.height) {
      return { width: options.width, height: options.height };
    }

    if (options.width) {
      const aspectRatio = rect.height / rect.width;
      return { width: options.width, height: options.width * aspectRatio };
    }

    if (options.height) {
      const aspectRatio = rect.width / rect.height;
      return { width: options.height * aspectRatio, height: options.height };
    }

    return { width: rect.width, height: rect.height };
  }

  private async canvasToBlob(
    canvas: HTMLCanvasElement,
    options: ImageExportOptions
  ): Promise<Blob> {
    return new Promise((resolve, reject) => {
      const mimeType = this.getMimeType(options.format);
      const quality = options.format === "PNG" ? undefined : options.quality;

      canvas.toBlob(
        (blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error("Failed to create blob from canvas"));
          }
        },
        mimeType,
        quality
      );
    });
  }

  private getMimeType(format: string): string {
    switch (format) {
      case "PNG":
        return "image/png";
      case "JPEG":
        return "image/jpeg";
      case "WebP":
        return "image/webp";
      default:
        return "image/png";
    }
  }

  private generateFilename(format: string, pageNumber?: number): string {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, "-");
    const page = pageNumber ? `-page-${pageNumber}` : "";
    const ext = format.toLowerCase();
    return `sequence-cards${page}-${timestamp}.${ext}`;
  }

  private async exportSinglePageWithCanvas(
    pageElement: HTMLElement,
    html2canvas: Html2CanvasFunction,
    options: ImageExportOptions,
    pageNumber: number
  ): Promise<ServiceExportResult> {
    const startTime = performance.now();

    try {
      const preparedElement = this.prepareElementForCapture(pageElement);
      const dimensions = this.calculateCaptureDimensions(
        preparedElement,
        options
      );

      const canvas = await html2canvas(preparedElement, {
        width: dimensions.width,
        height: dimensions.height,
        scale: options.scale,
        backgroundColor: options.backgroundColor || "#ffffff",
        useCORS: true,
        allowTaint: false,
        removeContainer: true,
        logging: false,
        scrollX: 0,
        scrollY: 0,
        windowWidth: dimensions.width,
        windowHeight: dimensions.height,
      });

      const blob = await this.canvasToBlob(canvas, options);
      const processingTime = performance.now() - startTime;

      return {
        sequenceId: `page-${pageNumber}`,
        success: true,
        blob,
        filename: this.generateFilename(options.format, pageNumber),
        metrics: {
          processingTime,
          fileSize: blob.size,
          resolution: { width: canvas.width, height: canvas.height },
        },
        metadata: {
          format: options.format,
          size: blob.size,
          dimensions: {
            width: canvas.width,
            height: canvas.height,
          },
          processingTime,
        },
      };
    } catch (error) {
      const processingTime = performance.now() - startTime;

      return {
        sequenceId: `page-${pageNumber}`,
        success: false,
        filename: this.generateFilename(options.format, pageNumber),
        error: error as Error,
        metrics: {
          processingTime,
          fileSize: 0,
          resolution: { width: 0, height: 0 },
        },
        metadata: {
          format: options.format,
          size: 0,
          processingTime,
        },
      };
    }
  }

  private estimateTimeRemaining(
    current: number,
    total: number,
    elapsedTime: number
  ): number {
    if (current === 0) return 0;

    const averageTimePerItem = elapsedTime / current;
    const remainingItems = total - current;
    return remainingItems * averageTimePerItem;
  }

  private async pauseForUI(): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 10));
  }
}
