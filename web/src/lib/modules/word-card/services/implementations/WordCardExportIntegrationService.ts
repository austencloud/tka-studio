/**
 * Word Card Export Integration Service Implementation
 *
 * Bridges the gap between UI components and export services.
 * Handles DOM element selection, export orchestration, and file downloads.
 */

// Domain types
import type { ImageExportOptions as SequenceExportOptions } from "$shared/domain";

// Behavioral contracts
import type {
  IPageImageExportService,
  IWordCardExportIntegrationService,
} from "$services";
import {
  downloadBlobBatch,
  generateTimestampedFilename,
  sanitizeFilename,
  supportsFileDownload,
} from "$shared/utils";
import { injectable } from "inversify";

@injectable()
export class WordCardExportIntegrationService
  implements IWordCardExportIntegrationService
{
  private isExporting = false;
  private abortController: AbortController | null = null;

  constructor(
    private readonly pageImageExportService: IPageImageExportService
  ) {}

  async exportPrintablePagesAsImages(
    options: {
      format?: "PNG" | "JPEG" | "WebP";
      quality?: number;
      scale?: number;
      filenamePrefix?: string;
    } = {},
    onProgress?: (current: number, total: number, message: string) => void
  ): Promise<{ successCount: number; failureCount: number; errors: Error[] }> {
    console.log("🖼️ Starting export of all printable pages as images");

    // Validate export capability
    const validation = this.validateExportCapability();
    if (!validation.canExport) {
      const error = new Error(
        `Export not possible: ${validation.issues.join(", ")}`
      );
      console.error("❌ Export validation failed:", error);
      return { successCount: 0, failureCount: 1, errors: [error] };
    }

    // Get page elements
    const pageElements = this.getPrintablePageElements();
    if (pageElements.length === 0) {
      const error = new Error("No printable page elements found in DOM");
      console.error("❌ No page elements found:", error);
      return { successCount: 0, failureCount: 1, errors: [error] };
    }

    console.log(`📄 Found ${pageElements.length} page elements to export`);

    try {
      this.isExporting = true;
      this.abortController = new AbortController();

      // Prepare export options
      const exportOptions = this.prepareImageExportOptions(options);
      console.log("⚙️ Export options prepared:", exportOptions);

      // Progress tracking
      const totalCount = pageElements.length;

      // Export pages to blobs
      onProgress?.(0, totalCount, "Starting page export...");
      const batchResult = await this.pageImageExportService.exportPagesAsImages(
        pageElements,
        exportOptions
      );

      console.log("📊 Batch export result:", batchResult);

      // Prepare download data
      const downloadData: Array<{ blob: Blob; filename: string }> = [];
      const errors: Error[] = batchResult.errors.map((err: any) =>
        err instanceof Error ? err : err.error
      );

      for (let i = 0; i < batchResult.results.length; i++) {
        const result = batchResult.results[i];

        if (result.success && result.data) {
          const pageNumber = i + 1;
          const filename = this.generatePageFilename(
            options.filenamePrefix || "sequence-cards",
            pageNumber,
            exportOptions.format,
            result.metadata?.dimensions as
              | { width: number; height: number }
              | undefined
          );

          downloadData.push({
            blob: result.data as Blob,
            filename,
          });
        } else if (result.error) {
          errors.push(new Error(result.error));
        }
      }

      console.log(`💾 Prepared ${downloadData.length} files for download`);

      // Download files
      if (downloadData.length > 0) {
        onProgress?.(
          totalCount,
          totalCount,
          `Downloading ${downloadData.length} files...`
        );

        const downloadResults = await downloadBlobBatch(downloadData, {
          delay: 200, // 200ms delay between downloads
        });

        // Check download results
        const failedDownloads = downloadResults.filter((r) => !r.success);
        if (failedDownloads.length > 0) {
          console.warn("⚠️ Some downloads failed:", failedDownloads);
          failedDownloads.forEach((result) => {
            if (result.error) {
              errors.push(result.error);
            }
          });
        }

        console.log(
          `✅ Successfully downloaded ${downloadData.length - failedDownloads.length} files`
        );
      }

      onProgress?.(
        totalCount,
        totalCount,
        `Export completed! ${batchResult.successCount} pages exported successfully.`
      );

      return {
        successCount: batchResult.successCount,
        failureCount: batchResult.failureCount,
        errors,
      };
    } catch (error) {
      console.error("❌ Export failed with error:", error);
      return {
        successCount: 0,
        failureCount: pageElements.length,
        errors: [error as Error],
      };
    } finally {
      this.isExporting = false;
      this.abortController = null;
    }
  }

  async exportSelectedPages(
    pageIndices: number[],
    options: {
      format?: "PNG" | "JPEG" | "WebP";
      quality?: number;
      scale?: number;
      filenamePrefix?: string;
    } = {},
    onProgress?: (current: number, total: number, message: string) => void
  ): Promise<{ successCount: number; failureCount: number; errors: Error[] }> {
    console.log("🎯 Starting export of selected pages:", pageIndices);

    // Get all page elements
    const allPageElements = this.getPrintablePageElements();

    // Filter to selected pages
    const selectedElements = pageIndices
      .filter((index) => index >= 0 && index < allPageElements.length)
      .map((index) => allPageElements[index]);

    if (selectedElements.length === 0) {
      const error = new Error(
        "No valid page elements found for selected indices"
      );
      console.error("❌ No valid selected elements:", error);
      return { successCount: 0, failureCount: 1, errors: [error] };
    }

    // For now, delegate to the full export method but with filtered elements
    // TODO: Could optimize this by modifying the export service to accept specific elements
    console.log(`📄 Exporting ${selectedElements.length} selected pages`);

    // This is a simplified implementation - in reality, we'd need to modify the export flow
    // For now, we'll export all and notify about the selected ones
    onProgress?.(
      0,
      selectedElements.length,
      "Note: Currently exports all pages (selection feature in development)"
    );

    return this.exportPrintablePagesAsImages(options, onProgress);
  }

  getPrintablePageElements(): HTMLElement[] {
    console.log("🔍 Searching for printable page elements in DOM");

    // Look for page elements with the expected data attribute or class
    const selectors = [
      "[data-page-id]",
      ".printable-page",
      ".page-wrapper .printable-page",
      ".pages-display .printable-page",
    ];

    let elements: HTMLElement[] = [];

    for (const selector of selectors) {
      const found = document.querySelectorAll(
        selector
      ) as NodeListOf<HTMLElement>;
      if (found.length > 0) {
        elements = Array.from(found);
        console.log(
          `✅ Found ${elements.length} page elements using selector: ${selector}`
        );
        break;
      }
    }

    if (elements.length === 0) {
      console.warn("⚠️ No printable page elements found with any selector");
      console.log("🔍 Available elements in DOM:");
      console.log(
        "- Elements with data-page-id:",
        document.querySelectorAll("[data-page-id]").length
      );
      console.log(
        "- Elements with class printable-page:",
        document.querySelectorAll(".printable-page").length
      );
    }

    return elements;
  }

  validateExportCapability(): {
    canExport: boolean;
    pageCount: number;
    issues: string[];
  } {
    const issues: string[] = [];

    // Check browser support
    if (!supportsFileDownload()) {
      issues.push("Browser does not support file downloads");
    }

    // Check for DOM elements
    const pageElements = this.getPrintablePageElements();
    const pageCount = pageElements.length;

    if (pageCount === 0) {
      issues.push("No printable page elements found in DOM");
    }

    // Check if already exporting
    if (this.isExporting) {
      issues.push("Export already in progress");
    }

    // Check for required services
    if (!this.pageImageExportService) {
      issues.push("Page image export service not available");
    }

    const canExport = issues.length === 0;

    console.log("🔍 Export capability validation:", {
      canExport,
      pageCount,
      issues,
    });

    return {
      canExport,
      pageCount,
      issues,
    };
  }

  cancelExport(): void {
    if (this.isExporting && this.abortController) {
      console.log("🛑 Cancelling export operation");
      this.abortController.abort();
      this.pageImageExportService.cancelExport();
      this.isExporting = false;
      this.abortController = null;
    }
  }

  getDefaultExportOptions(): {
    format: "PNG" | "JPEG" | "WebP";
    quality: number;
    scale: number;
    filenamePrefix: string;
  } {
    return {
      format: "PNG",
      quality: 0.95,
      scale: 2.0, // 2x for high quality
      filenamePrefix: "sequence-cards",
    };
  }

  // Private helper methods

  private prepareImageExportOptions(options: {
    format?: "PNG" | "JPEG" | "WebP";
    quality?: number;
    scale?: number;
    filenamePrefix?: string;
  }): SequenceExportOptions {
    const defaults = this.getDefaultExportOptions();

    return {
      ...defaults,
      ...options,
      // Override with specific values
      format: options.format || defaults.format,
      quality: options.quality ?? defaults.quality,
      scale: options.scale ?? defaults.scale,
    };
  }

  private generatePageFilename(
    prefix: string,
    pageNumber: number,
    format: string,
    dimensions?: { width: number; height: number }
  ): string {
    const sanitizedPrefix = sanitizeFilename(prefix);
    const pageNumStr = pageNumber.toString().padStart(3, "0");
    const extension = format.toLowerCase();

    // Include dimensions in filename for reference
    const dimensionStr = dimensions
      ? `_${dimensions.width}x${dimensions.height}`
      : "";

    return generateTimestampedFilename(
      `${sanitizedPrefix}_page_${pageNumStr}${dimensionStr}`,
      extension,
      false // Don't include time, just date
    );
  }
}
