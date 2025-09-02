/**
 * Sequence Card Export Orchestrator
 *
 * Main orchestrator for sequence card export operations.
 * Single responsibility: Coordinate focused services for export workflow.
 */

// Domain types
import type {
  BatchExportProgress,
  BatchOperationConfig,
  SequenceCardDimensions,
  SequenceCardExportResult,
  SequenceCardMetadata,
  SequenceData,
} from "$domain";

// Behavioral contracts
import type {
  ISequenceCardBatchProcessingService,
  ISequenceCardCacheService,
  ISequenceCardExportOrchestrator,
  ISequenceCardExportProgressTracker,
  ISequenceCardImageConversionService,
  ISequenceCardImageGenerationService,
} from "../../contracts/sequence-card-export-interfaces";

export class SequenceCardExportOrchestrator
  implements ISequenceCardExportOrchestrator
{
  private currentOperationId: string | null = null;

  constructor(
    private readonly imageGenerationService: ISequenceCardImageGenerationService,
    private readonly imageConversionService: ISequenceCardImageConversionService,
    private readonly batchProcessingService: ISequenceCardBatchProcessingService,
    private readonly progressTracker: ISequenceCardExportProgressTracker,
    private readonly cacheService: ISequenceCardCacheService
  ) {}

  /**
   * Export single sequence card
   */
  async exportSequenceCard(
    sequence: SequenceData,
    dimensions: SequenceCardDimensions,
    _metadata?: SequenceCardMetadata
  ): Promise<SequenceCardExportResult> {
    const startTime = performance.now();
    const sequenceId = sequence.id || sequence.name || "unknown";

    try {
      console.log(`🚀 Starting export for sequence: ${sequenceId}`);

      // Check cache first
      const cachedBlob = await this.cacheService.retrieveImage(sequenceId);
      if (cachedBlob) {
        console.log(`🎯 Cache hit for sequence: ${sequenceId}`);
        return {
          sequenceId,
          success: true,
          blob: cachedBlob,
          metrics: {
            processingTime: performance.now() - startTime,
            fileSize: cachedBlob.size,
            resolution: dimensions,
          },
        };
      }

      // Generate image
      const canvas = await this.imageGenerationService.generateSequenceImage(
        sequence,
        dimensions
      );

      // Convert to blob
      const blob = await this.imageConversionService.canvasToBlob(
        canvas,
        "PNG",
        0.95
      );

      // Cache the result
      await this.cacheService.storeImage(sequenceId, blob);

      const result: SequenceCardExportResult = {
        sequenceId,
        success: true,
        blob,
        metrics: {
          processingTime: performance.now() - startTime,
          fileSize: blob.size,
          resolution: dimensions,
        },
      };

      console.log(`✅ Successfully exported sequence: ${sequenceId}`);
      return result;
    } catch (error) {
      console.error(`❌ Failed to export sequence ${sequenceId}:`, error);

      return {
        sequenceId,
        success: false,
        error: error instanceof Error ? error : new Error(String(error)),
      };
    }
  }

  /**
   * Export multiple sequence cards in batch
   */
  async exportBatch(
    sequences: SequenceData[],
    dimensions: SequenceCardDimensions,
    config: BatchOperationConfig,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<SequenceCardExportResult[]> {
    const operationId = this.generateOperationId();
    this.currentOperationId = operationId;

    try {
      console.log(`🚀 Starting batch export of ${sequences.length} sequences`);

      // Start progress tracking
      this.progressTracker.startOperation(operationId, sequences.length);

      // Subscribe to internal progress updates
      const unsubscribe = this.progressTracker.onProgress(
        operationId,
        (progress) => {
          if (onProgress) {
            onProgress(progress);
          }
        }
      );

      // Process batch using batch service
      const results = await this.batchProcessingService.processBatch(
        sequences,
        config,
        async (sequence, _index) => {
          return await this.exportSequenceCard(sequence, dimensions);
        },
        (progress) => {
          // Update progress tracker
          this.progressTracker.updateProgress(
            operationId,
            progress.current,
            progress.message,
            progress.stage
          );
        }
      );

      // Complete operation
      this.progressTracker.completeOperation(operationId);
      unsubscribe();

      const successCount = results.filter((r) => r.success).length;
      const failureCount = results.filter((r) => !r.success).length;

      console.log(
        `✅ Batch export complete: ${successCount} success, ${failureCount} failures`
      );
      return results;
    } catch (error) {
      console.error("❌ Batch export failed:", error);

      this.progressTracker.addError(
        operationId,
        error instanceof Error ? error : new Error(String(error))
      );
      this.progressTracker.completeOperation(operationId);

      throw error;
    } finally {
      this.currentOperationId = null;
    }
  }

  /**
   * Cancel current batch operation
   */
  cancelBatch(): void {
    if (this.currentOperationId) {
      console.log("🛑 Cancelling current batch operation");
      this.batchProcessingService.requestCancellation();
    } else {
      console.warn("⚠️ No active batch operation to cancel");
    }
  }

  /**
   * Get current operation status
   */
  getOperationStatus(): {
    isActive: boolean;
    currentOperation?: string;
    progress?: BatchExportProgress;
  } {
    if (!this.currentOperationId) {
      return { isActive: false };
    }

    const progress = this.progressTracker.getProgress(this.currentOperationId);

    return {
      isActive: true,
      currentOperation: this.currentOperationId,
      progress: progress || undefined,
    };
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private generateOperationId(): string {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 8);
    return `export-${timestamp}-${random}`;
  }
}
