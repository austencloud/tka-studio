/**
 * Word Card Export Service Interfaces
 * Clean, focused service contracts for word card image generation.
 * Follows single responsibility principle and TKA DI patterns.
 */
// ============================================================================
// CORE TYPES
// ============================================================================
import type { SequenceData } from "$shared/domain";
// import type {
//   BatchExportProgress,
//   BatchOperationConfig,
//   WordCardDimensions,
//   WordCardExportResult,
//   WordCardMetadata
// } from "../../../../word-card/domain";

// Temporary interface definitions
interface BatchExportProgress {
  completed: number;
  total: number;
  currentItem?: string;
  stage?: string;
}

interface BatchOperationConfig {
  batchSize: number;
  memoryThreshold: number;
  enableProgressReporting: boolean;
  enableCancellation: boolean;
}

interface WordCardDimensions {
  width: number;
  height: number;
}

interface WordCardExportResult {
  success: boolean;
  sequenceId: string;
  error?: Error;
}

interface WordCardMetadata {
  title?: string;
  author?: string;
  beatNumbers?: boolean;
  timestamp?: boolean;
  backgroundColor?: string;
}

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IWordCardExportOrchestrator {
  /**
   * Export single word card
   */
  exportWordCard(
    sequence: SequenceData,
    dimensions: WordCardDimensions,
    metadata?: WordCardMetadata
  ): Promise<WordCardExportResult>;

  /**
   * Export multiple sequence cards in batch
   */
  exportBatch(
    sequences: SequenceData[],
    dimensions: WordCardDimensions,
    config: BatchOperationConfig,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<WordCardExportResult[]>;

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

export interface IWordCardImageGenerationService {
  /**
   * Generate image for a single sequence
   */
  generateSequenceImage(
    sequence: SequenceData,
    dimensions: WordCardDimensions
  ): Promise<HTMLCanvasElement>;

  /**
   * Validate sequence data for image generation
   */
  validateSequenceData(sequence: SequenceData): boolean;

  /**
   * Get recommended dimensions for sequence
   */
  getRecommendedDimensions(beatCount: number): WordCardDimensions;
}

export interface IWordCardSVGCompositionService {
  /**
   * Create SVG layout for sequence beats
   */
  createSequenceLayout(
    beatSVGs: string[],
    dimensions: WordCardDimensions
  ): Promise<string>;

  /**
   * Calculate optimal beat arrangement
   */
  calculateBeatLayout(
    beatCount: number,
    dimensions: WordCardDimensions
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
    maxDimensions: WordCardDimensions
  ): WordCardDimensions;
}

export interface IWordCardMetadataOverlayService {
  /**
   * Add metadata overlays to SVG
   */
  addMetadataOverlays(
    svg: string,
    sequence: SequenceData,
    metadata: WordCardMetadata,
    dimensions: WordCardDimensions
  ): Promise<string>;

  /**
   * Generate title overlay
   */
  generateTitleOverlay(
    title: string,
    dimensions: WordCardDimensions
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
    dimensions: WordCardDimensions,
    backgroundColor?: string
  ): string;
}

export interface IWordCardBatchProcessingService {
  /**
   * Process sequence cards in optimized batches
   */
  processBatch<T>(
    items: T[],
    config: BatchOperationConfig,
    processor: (item: T, index: number) => Promise<WordCardExportResult>,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<WordCardExportResult[]>;

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

export interface IWordCardImageConversionService {
  /**
   * Convert SVG string to Canvas
   */
  svgToCanvas(
    svgString: string,
    dimensions: WordCardDimensions
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
    dimensions: WordCardDimensions,
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

export interface IWordCardExportProgressTracker {
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
