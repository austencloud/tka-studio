/**
 * Sequence Service Interfaces
 *
 * Interfaces for sequence management, creation, updates, and domain logic.
 * This includes both service contracts and related data structures.
 *
 * Also includes page layout services for printable word card creation.
 */

import type { Page } from "@sveltejs/kit";
import type { SequenceData, ValidationResult } from "../../../../../shared/domain";
import type { DPIConfiguration, GridCalculationOptions, LayoutCalculationRequest, LayoutCalculationResult, LayoutValidationResult, PageCreationOptions, PageDimensions, PageLayoutConfig, PageMargins, PageOrientation, Rectangle, WordCardGridConfig, WordCardPaperSize } from "../../../../word-card";
import type { BeatData, DeleteConfirmationData, DeleteResult, SequenceCreateRequest } from "../../domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISequenceService {
  createSequence(request: SequenceCreateRequest): Promise<SequenceData>;
  updateBeat(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void>;
  getSequence(id: string): Promise<SequenceData | null>;
  getAllSequences(): Promise<SequenceData[]>;
}

export interface ISequenceDeletionService {
  deleteSequence(sequenceId: string): Promise<void>;
  removeBeat(sequenceId: string, beatIndex: number): Promise<SequenceData>;
  clearSequenceBeats(sequenceId: string): Promise<SequenceData>;
  removeBeats(sequenceId: string, beatIndices: number[]): Promise<SequenceData>;
  removeBeatAndFollowing(
    sequenceId: string,
    startIndex: number
  ): Promise<SequenceData>;
}


export interface ISequenceImportService {
  importFromPNG(id: string): Promise<SequenceData | null>;
  convertPngMetadata(id: string, metadata: unknown[]): Promise<SequenceData>;
}

export interface IWorkbenchDeleteService {
  /** Prepare deletion data for confirmation dialog */
  prepareDeleteConfirmation(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteConfirmationData>;

  /** Delete sequence and handle cleanup */
  deleteSequence(
    sequenceId: string,
    allSequences: SequenceData[]
  ): Promise<DeleteResult>;

  /** Fix variation numbers after deletion */
  fixVariationNumbers(
    deletedSequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;

  /** Check if sequence can be safely deleted */
  canDeleteSequence(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<boolean>;

  /** Get sequences that would be affected by deletion */
  getAffectedSequences(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;
}

export interface ISequenceDomainService {
  validateCreateRequest(request: SequenceCreateRequest): ValidationResult;
  createSequence(request: SequenceCreateRequest): SequenceData;
  updateBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData: BeatData
  ): SequenceData;
  calculateSequenceWord(sequence: SequenceData): string;
}

export interface IPersistenceService {
  saveSequence(sequence: SequenceData): Promise<void>;
  loadSequence(id: string): Promise<SequenceData | null>;
  loadAllSequences(): Promise<SequenceData[]>;
  deleteSequence(id: string): Promise<void>;
}

export interface IPrintablePageLayoutService {
  /**
   * Calculate page dimensions for a given paper size and orientation
   */
  calculatePageDimensions(
    paperSize: WordCardPaperSize,
    orientation: PageOrientation
  ): PageDimensions;

  /**
   * Calculate margins for a given paper size
   */
  calculateMargins(paperSize: WordCardPaperSize): PageMargins;

  /**
   * Calculate the content area (page dimensions minus margins)
   */
  calculateContentArea(
    pageSize: PageDimensions,
    margins: PageMargins
  ): Rectangle;

  /**
   * Calculate optimal grid configuration for given constraints
   */
  calculateOptimalGrid(
    cardAspectRatio: number,
    contentArea: Rectangle,
    options?: Partial<GridCalculationOptions>
  ): WordCardGridConfig;

  /**
   * Get page size in pixels for screen display
   */
  getPageSizeInPixels(
    paperSize: WordCardPaperSize,
    orientation: PageOrientation,
    dpi?: number
  ): PageDimensions;

  /**
   * Perform layout calculation for given requirements
   */
  calculateLayout(request: LayoutCalculationRequest): LayoutCalculationResult;

  /**
   * Validate a layout configuration
   */
  validateLayout(config: PageLayoutConfig): LayoutValidationResult;

  /**
   * Get DPI configuration for screen and print
   */
  getDPIConfiguration(): DPIConfiguration;

  /**
   * Convert measurements between different units
   */
  convertMeasurement(value: number, fromUnit: string, toUnit: string): number;
}

export interface IPageFactoryService {
  /**
   * Create pages from sequences using the given layout configuration
   */
  createPages(sequences: SequenceData[], options: PageCreationOptions): Page[];

  /**
   * Create a single empty page with optional message
   */
  createEmptyPage(
    pageNumber: number,
    layout: PageLayoutConfig,
    message?: string
  ): Page;

  /**
   * Calculate how many pages are needed for given sequences and layout
   */
  calculatePagesNeeded(sequenceCount: number, sequencesPerPage: number): number;

  /**
   * Distribute sequences across pages optimally
   */
  distributeSequences(
    sequences: SequenceData[],
    sequencesPerPage: number
  ): SequenceData[][];

  /**
   * Generate page numbering for a set of pages
   */
  generatePageNumbers(pageCount: number, startNumber?: number): number[];

  /**
   * Validate page creation options
   */
  validatePageOptions(options: PageCreationOptions): LayoutValidationResult;

  /**
   * Get optimal cards per page for given layout constraints
   */
  getOptimalCardsPerPage(
    contentArea: Rectangle,
    cardAspectRatio: number,
    options?: Partial<GridCalculationOptions>
  ): number;
}

export interface IWordCardExportIntegrationService {
  /**
   * Export all visible printable pages as image files
   */
  exportPrintablePagesAsImages(
    options?: {
      format?: "PNG" | "JPEG" | "WebP";
      quality?: number;
      scale?: number;
      filenamePrefix?: string;
    },
    onProgress?: (current: number, total: number, message: string) => void
  ): Promise<{ successCount: number; failureCount: number; errors: Error[] }>;

  /**
   * Export selected pages by their indices
   */
  exportSelectedPages(
    pageIndices: number[],
    options?: {
      format?: "PNG" | "JPEG" | "WebP";
      quality?: number;
      scale?: number;
      filenamePrefix?: string;
    },
    onProgress?: (current: number, total: number, message: string) => void
  ): Promise<{ successCount: number; failureCount: number; errors: Error[] }>;

  /**
   * Get printable page elements from the DOM
   */
  getPrintablePageElements(): HTMLElement[];

  /**
   * Validate that export is possible (pages exist, browser supports export)
   */
  validateExportCapability(): {
    canExport: boolean;
    pageCount: number;
    issues: string[];
  };

  /**
   * Cancel any ongoing export operation
   */
  cancelExport(): void;

  /**
   * Get default export options
   */
  getDefaultExportOptions(): {
    format: "PNG" | "JPEG" | "WebP";
    quality: number;
    scale: number;
    filenamePrefix: string;
  };
}
