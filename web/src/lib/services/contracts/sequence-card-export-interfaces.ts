/**
 * Sequence Card Export Service Interfaces
 * Clean, focused service contracts for sequence card image generation.
 * Follows single responsibility principle and TKA DI patterns.
 */
// ============================================================================
// CORE TYPES
// ============================================================================
import type { ExportOptions, SequenceData } from "$domain";
import type {
  BatchExportProgress,
  BatchOperationConfig,
  SequenceCardDimensions,
  SequenceCardExportResult,
  SequenceCardMetadata,
} from "$domain/data-interfaces/sequence-card-export-interfaces-data";

// Re-export the imported types so other services can use them
export type {
  BatchExportProgress,
  BatchOperationConfig,
  SequenceCardDimensions,
  SequenceCardExportResult,
  SequenceCardMetadata,
} from "$domain/data-interfaces/sequence-card-export-interfaces-data";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISequenceCardExportOrchestrator {
  /**
   * Export single sequence card
   */
  exportSequenceCard(
    sequence: SequenceData,
    dimensions: SequenceCardDimensions,
    metadata?: SequenceCardMetadata
  ): Promise<SequenceCardExportResult>;

  /**
   * Export multiple sequence cards in batch
   */
  exportBatch(
    sequences: SequenceData[],
    dimensions: SequenceCardDimensions,
    config: BatchOperationConfig,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<SequenceCardExportResult[]>;

  /**
   * Cancel current batch operation
   */
  cancelBatch(): void;

  /**
   * Get current operation status
   */
  getOperationStatus(): {
    isActive: boolean;
    currentOperation?: string;
    progress?: BatchExportProgress;
  };
}

export interface ISequenceCardImageGenerationService {
  /**
   * Generate image for a single sequence
   */
  generateSequenceImage(
    sequence: SequenceData,
    dimensions: SequenceCardDimensions
  ): Promise<HTMLCanvasElement>;

  /**
   * Validate sequence data for image generation
   */
  validateSequenceData(sequence: SequenceData): boolean;

  /**
   * Get recommended dimensions for sequence
   */
  getRecommendedDimensions(beatCount: number): SequenceCardDimensions;
}

export interface ISequenceCardSVGCompositionService {
  /**
   * Create SVG layout for sequence beats
   */
  createSequenceLayout(
    beatSVGs: string[],
    dimensions: SequenceCardDimensions
  ): Promise<string>;

  /**
   * Calculate optimal beat arrangement
   */
  calculateBeatLayout(
    beatCount: number,
    dimensions: SequenceCardDimensions
  ): {
    rows: number;
    columns: number;
    beatWidth: number;
    beatHeight: number;
    spacing: { x: number; y: number };
  };

  /**
   * Apply responsive sizing based on beat count
   */
  calculateResponsiveDimensions(
    beatCount: number,
    maxDimensions: SequenceCardDimensions
  ): SequenceCardDimensions;
}

export interface ISequenceCardMetadataOverlayService {
  /**
   * Add metadata overlays to SVG
   */
  addMetadataOverlays(
    svg: string,
    sequence: SequenceData,
    metadata: SequenceCardMetadata,
    dimensions: SequenceCardDimensions
  ): Promise<string>;

  /**
   * Generate title overlay
   */
  generateTitleOverlay(
    title: string,
    dimensions: SequenceCardDimensions
  ): string;

  /**
   * Generate beat number overlays
   */
  generateBeatNumberOverlays(
    beatCount: number,
    layout: {
      rows: number;
      columns: number;
      beatWidth: number;
      beatHeight: number;
    }
  ): string[];

  /**
   * Add background and borders
   */
  addBackgroundAndBorders(
    svg: string,
    dimensions: SequenceCardDimensions,
    backgroundColor?: string
  ): string;
}

export interface ISequenceCardBatchProcessingService {
  /**
   * Process sequence cards in optimized batches
   */
  processBatch<T>(
    items: T[],
    config: BatchOperationConfig,
    processor: (item: T, index: number) => Promise<SequenceCardExportResult>,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<SequenceCardExportResult[]>;

  /**
   * Calculate optimal batch size based on memory constraints
   */
  calculateOptimalBatchSize(
    itemCount: number,
    averageItemSize: number,
    availableMemory: number
  ): number;

  /**
   * Monitor memory usage during batch processing
   */
  getMemoryUsage(): {
    used: number;
    available: number;
    threshold: number;
  };

  /**
   * Request cancellation of current batch
   */
  requestCancellation(): void;

  /**
   * Check if cancellation was requested
   */
  isCancellationRequested(): boolean;
}

export interface ISequenceCardImageConversionService {
  /**
   * Convert SVG string to Canvas
   */
  svgToCanvas(
    svgString: string,
    dimensions: SequenceCardDimensions
  ): Promise<HTMLCanvasElement>;

  /**
   * Convert Canvas to Blob
   */
  canvasToBlob(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG" | "WEBP",
    quality?: number
  ): Promise<Blob>;

  /**
   * Convert SVG directly to Blob (optimized pipeline)
   */
  svgToBlob(
    svgString: string,
    dimensions: SequenceCardDimensions,
    format: "PNG" | "JPEG" | "WEBP",
    quality?: number
  ): Promise<Blob>;

  /**
   * Optimize image for different use cases
   */
  optimizeImage(
    blob: Blob,
    useCase: "web" | "print" | "archive"
  ): Promise<Blob>;
}

export interface ISequenceCardExportProgressTracker {
  /**
   * Start tracking new operation
   */
  startOperation(operationId: string, totalSteps: number): void;

  /**
   * Update progress for current operation
   */
  updateProgress(
    operationId: string,
    current: number,
    message: string,
    stage: BatchExportProgress["stage"]
  ): void;

  /**
   * Add error to current operation
   */
  addError(operationId: string, error: Error): void;

  /**
   * Add warning to current operation
   */
  addWarning(operationId: string, warning: string): void;

  /**
   * Complete operation
   */
  completeOperation(operationId: string): void;

  /**
   * Get current progress
   */
  getProgress(operationId: string): BatchExportProgress | null;

  /**
   * Subscribe to progress updates
   */
  onProgress(
    operationId: string,
    callback: (progress: BatchExportProgress) => void
  ): () => void; // Returns unsubscribe function
}

export interface ISequenceCardCacheService {
  /**
   * Store image in cache
   */
  storeImage(
    sequenceId: string,
    imageBlob: Blob,
    options?: ExportOptions
  ): Promise<void>;

  /**
   * Retrieve image from cache
   */
  retrieveImage(
    sequenceId: string,
    options?: ExportOptions
  ): Promise<Blob | null>;

  /**
   * Store sequence data in cache
   */
  storeSequenceData(sequenceId: string, data: SequenceData): Promise<void>;

  /**
   * Retrieve sequence data from cache
   */
  retrieveSequenceData(sequenceId: string): Promise<SequenceData | null>;

  /**
   * Clear all cached data
   */
  clearCache(): Promise<void>;

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    entryCount: number;
    totalSize: number;
    hitRate: number;
    lastCleanup: Date;
  };

  /**
   * Cleanup expired cache entries
   */
  cleanup(): Promise<void>;
}

// Note: Import types directly from $domain/data-interfaces/sequence-card-export-interfaces-data
// instead of re-exporting them from service contracts
