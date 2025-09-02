/**
 * Sequence Card Batch Processing Service
 *
 * Handles batch processing operations for sequence cards.
 * Single responsibility: Efficient batch processing with memory management.
 */

import { injectable } from "inversify";
import type {
  BatchExportProgress,
  BatchOperationConfig,
  ISequenceCardBatchProcessingService,
  SequenceCardExportResult,
} from "../../contracts/sequence-card-export-interfaces";

@injectable()
export class SequenceCardBatchProcessingService
  implements ISequenceCardBatchProcessingService
{
  private cancellationRequested = false;
  private readonly memoryThresholdBytes: number;

  constructor() {
    // Default to 500MB memory threshold
    this.memoryThresholdBytes = 500 * 1024 * 1024;
  }

  /**
   * Process sequence cards in optimized batches
   */
  async processBatch<T>(
    items: T[],
    config: BatchOperationConfig,
    processor: (item: T, index: number) => Promise<SequenceCardExportResult>,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<SequenceCardExportResult[]> {
    this.cancellationRequested = false;
    const results: SequenceCardExportResult[] = [];
    const startTime = new Date();

    try {
      console.log(`🚀 Starting batch processing of ${items.length} items`);

      const optimalBatchSize = this.calculateOptimalBatchSize(
        items.length,
        this.estimateAverageItemSize(),
        this.getAvailableMemory()
      );

      const actualBatchSize = Math.min(config.batchSize, optimalBatchSize);
      console.log(
        `📊 Using batch size: ${actualBatchSize} (requested: ${config.batchSize}, optimal: ${optimalBatchSize})`
      );

      // Process items in batches
      for (let i = 0; i < items.length; i += actualBatchSize) {
        if (this.cancellationRequested) {
          console.log("🛑 Batch processing cancelled");
          break;
        }

        const batchStart = i;
        const batchEnd = Math.min(i + actualBatchSize, items.length);
        const batchItems = items.slice(batchStart, batchEnd);

        console.log(
          `📦 Processing batch ${Math.floor(i / actualBatchSize) + 1} (items ${batchStart + 1}-${batchEnd})`
        );

        // Process current batch
        const batchResults = await this.processBatchChunk(
          batchItems,
          batchStart,
          processor,
          (itemProgress) => {
            if (onProgress && config.enableProgressReporting) {
              const overallProgress: BatchExportProgress = {
                current: batchStart + itemProgress + 1,
                total: items.length,
                percentage:
                  ((batchStart + itemProgress + 1) / items.length) * 100,
                message: `Processing item ${batchStart + itemProgress + 1} of ${items.length}`,
                stage: "processing",
                errorCount: results.filter((r) => !r.success).length,
                warningCount: 0,
                startTime,
              };
              onProgress(overallProgress);
            }
          }
        );

        results.push(...batchResults);

        // Memory management between batches
        if (i + actualBatchSize < items.length) {
          await this.performMemoryCleanup();

          // Check memory pressure
          const memoryUsage = this.getMemoryUsage();
          if (memoryUsage.used > memoryUsage.threshold) {
            console.warn(
              "⚠️ High memory usage detected, forcing garbage collection"
            );
            await this.forceGarbageCollection();
          }
        }
      }

      const successCount = results.filter((r) => r.success).length;
      const failureCount = results.filter((r) => !r.success).length;

      console.log(
        `✅ Batch processing complete: ${successCount} success, ${failureCount} failures`
      );

      // Final progress update
      if (onProgress && config.enableProgressReporting) {
        const finalProgress: BatchExportProgress = {
          current: items.length,
          total: items.length,
          percentage: 100,
          message: `Completed: ${successCount} success, ${failureCount} failures`,
          stage: "finalizing",
          errorCount: failureCount,
          warningCount: 0,
          startTime,
        };
        onProgress(finalProgress);
      }

      return results;
    } catch (error) {
      console.error("❌ Batch processing failed:", error);
      throw error;
    }
  }

  /**
   * Calculate optimal batch size based on memory constraints
   */
  calculateOptimalBatchSize(
    itemCount: number,
    averageItemSize: number,
    availableMemory: number
  ): number {
    // Reserve 50% of available memory for batch processing
    const usableMemory = availableMemory * 0.5;

    // Calculate how many items we can process safely
    const optimalBatchSize = Math.floor(usableMemory / averageItemSize);

    // Ensure minimum batch size of 1 and maximum of 50
    const clampedBatchSize = Math.max(1, Math.min(optimalBatchSize, 50));

    console.log(`📊 Optimal batch size calculation:
      - Items: ${itemCount}
      - Avg item size: ${this.formatBytes(averageItemSize)}
      - Available memory: ${this.formatBytes(availableMemory)}
      - Usable memory: ${this.formatBytes(usableMemory)}
      - Optimal batch size: ${clampedBatchSize}`);

    return clampedBatchSize;
  }

  /**
   * Monitor memory usage during batch processing
   */
  getMemoryUsage(): {
    used: number;
    available: number;
    threshold: number;
  } {
    // Try to get actual memory usage if available (Chrome DevTools)
    if ("performance" in window && "memory" in window.performance) {
      const memory = (
        window.performance as unknown as {
          memory: { usedJSHeapSize: number; jsHeapSizeLimit: number };
        }
      ).memory;
      return {
        used: memory.usedJSHeapSize || 0,
        available: memory.jsHeapSizeLimit || this.memoryThresholdBytes,
        threshold: this.memoryThresholdBytes,
      };
    }

    // Fallback estimation
    return {
      used: 0, // Can't determine actual usage
      available: this.memoryThresholdBytes,
      threshold: this.memoryThresholdBytes,
    };
  }

  /**
   * Request cancellation of current batch
   */
  requestCancellation(): void {
    this.cancellationRequested = true;
    console.log("🛑 Batch cancellation requested");
  }

  /**
   * Check if cancellation was requested
   */
  isCancellationRequested(): boolean {
    return this.cancellationRequested;
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private async processBatchChunk<T>(
    batchItems: T[],
    startIndex: number,
    processor: (item: T, index: number) => Promise<SequenceCardExportResult>,
    onItemProgress?: (itemIndex: number) => void
  ): Promise<SequenceCardExportResult[]> {
    const results: SequenceCardExportResult[] = [];

    for (let i = 0; i < batchItems.length; i++) {
      if (this.cancellationRequested) {
        break;
      }

      try {
        const item = batchItems[i];
        const globalIndex = startIndex + i;

        const result = await processor(item, globalIndex);
        results.push(result);

        if (onItemProgress) {
          onItemProgress(i);
        }
      } catch (error) {
        console.error(`❌ Failed to process item ${startIndex + i}:`, error);
        results.push({
          sequenceId: `item-${startIndex + i}`,
          success: false,
          error: error instanceof Error ? error : new Error(String(error)),
        });
      }
    }

    return results;
  }

  private estimateAverageItemSize(): number {
    // Conservative estimate: 2MB per sequence card image
    return 2 * 1024 * 1024;
  }

  private getAvailableMemory(): number {
    // Try to get actual available memory
    if ("performance" in window && "memory" in window.performance) {
      const memory = (
        window.performance as unknown as {
          memory: { usedJSHeapSize: number; jsHeapSizeLimit: number };
        }
      ).memory;
      return (
        (memory.jsHeapSizeLimit || this.memoryThresholdBytes) -
        (memory.usedJSHeapSize || 0)
      );
    }

    // Fallback to conservative estimate
    return this.memoryThresholdBytes;
  }

  private async performMemoryCleanup(): Promise<void> {
    // Small delay to allow browser to process pending operations
    await new Promise((resolve) => setTimeout(resolve, 10));

    // Clear any temporary objects that might be in scope
    if (global && typeof global.gc === "function") {
      global.gc();
    }
  }

  private async forceGarbageCollection(): Promise<void> {
    // Force garbage collection if available (Chrome DevTools)
    if (
      "gc" in window &&
      typeof (window as { gc?: () => void }).gc === "function"
    ) {
      (window as { gc: () => void }).gc();
      console.log("🗑️ Forced garbage collection");
    }

    // Additional cleanup delay
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  private formatBytes(bytes: number): string {
    const sizes = ["Bytes", "KB", "MB", "GB"];
    if (bytes === 0) return "0 Bytes";
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + " " + sizes[i];
  }
}
