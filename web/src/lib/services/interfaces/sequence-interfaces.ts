/**
 * Sequence Service Interfaces
 *
 * Interfaces for sequence management, creation, updates, and domain logic.
 * This includes both service contracts and related data structures.
 * 
 * Also includes page layout services for printable sequence card creation.
 */

import type { BeatData, SequenceData, ValidationResult } from "./domain-types";
import type { GridMode } from "./core-types";
import type {
  Page,
  PageDimensions,
  Margins,
  Rectangle,
  GridConfig,
  PaperSize,
  Orientation,
  PrintConfiguration,
  PageLayoutConfig,
  PageCreationOptions,
  LayoutCalculationRequest,
  LayoutCalculationResult,
  LayoutValidationResult,
  GridCalculationOptions,
  DPIConfiguration,
} from "../../domain/pageLayout";

// ============================================================================
// SEQUENCE REQUEST TYPES
// ============================================================================

export interface SequenceCreateRequest {
  name: string;
  length: number;
  gridMode?: GridMode;
  propType?: string;
}

// ============================================================================
// SEQUENCE SERVICE INTERFACES
// ============================================================================

/**
 * Main sequence service for CRUD operations and persistence
 */
export interface ISequenceService {
  createSequence(request: SequenceCreateRequest): Promise<SequenceData>;
  updateBeat(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void>;
  addBeat(sequenceId: string, beatData?: Partial<BeatData>): Promise<void>;
  setSequenceStartPosition(
    sequenceId: string,
    startPosition: BeatData
  ): Promise<void>;
  deleteSequence(id: string): Promise<void>;
  getSequence(id: string): Promise<SequenceData | null>;
  getAllSequences(): Promise<SequenceData[]>;
}

/**
 * Domain-specific sequence operations and business logic
 */
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

// ============================================================================
// PERSISTENCE SERVICE INTERFACE
// ============================================================================

/**
 * Data persistence abstraction for sequences
 */
export interface IPersistenceService {
  saveSequence(sequence: SequenceData): Promise<void>;
  loadSequence(id: string): Promise<SequenceData | null>;
  loadAllSequences(): Promise<SequenceData[]>;
  deleteSequence(id: string): Promise<void>;
}

// ============================================================================
// PAGE LAYOUT SERVICE INTERFACES
// ============================================================================

/**
 * Service for calculating page dimensions, margins, and grid layouts
 * for printable sequence card pages
 */
export interface IPrintablePageLayoutService {
  /**
   * Calculate page dimensions for a given paper size and orientation
   */
  calculatePageDimensions(paperSize: PaperSize, orientation: Orientation): PageDimensions;

  /**
   * Calculate margins for a given paper size
   */
  calculateMargins(paperSize: PaperSize): Margins;

  /**
   * Calculate the content area (page dimensions minus margins)
   */
  calculateContentArea(pageSize: PageDimensions, margins: Margins): Rectangle;

  /**
   * Calculate optimal grid configuration for given constraints
   */
  calculateOptimalGrid(
    cardAspectRatio: number,
    contentArea: Rectangle,
    options?: Partial<GridCalculationOptions>
  ): GridConfig;

  /**
   * Get page size in pixels for screen display
   */
  getPageSizeInPixels(
    paperSize: PaperSize,
    orientation: Orientation,
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
  convertMeasurement(
    value: number,
    fromUnit: string,
    toUnit: string
  ): number;
}

/**
 * Service for creating printable pages with sequence cards
 */
export interface IPageFactoryService {
  /**
   * Create pages from sequences using the given layout configuration
   */
  createPages(
    sequences: SequenceData[],
    options: PageCreationOptions
  ): Page[];

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
  calculatePagesNeeded(
    sequenceCount: number,
    sequencesPerPage: number
  ): number;

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
  generatePageNumbers(
    pageCount: number,
    startNumber?: number
  ): number[];

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

// ============================================================================
// SEQUENCE CARD EXPORT INTEGRATION SERVICE INTERFACE
// ============================================================================

/**
 * Service for integrating sequence card export functionality with the UI.
 * Bridges the gap between DOM elements and export services.
 */
export interface ISequenceCardExportIntegrationService {
  /**
   * Export all visible printable pages as image files
   */
  exportPrintablePagesAsImages(
    options?: {
      format?: 'PNG' | 'JPEG' | 'WebP';
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
      format?: 'PNG' | 'JPEG' | 'WebP';
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
    format: 'PNG' | 'JPEG' | 'WebP';
    quality: number;
    scale: number;
    filenamePrefix: string;
  };
}
