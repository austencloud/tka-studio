/**
 * Page Layout Domain Types
 *
 * Type definitions for printable page layout functionality including page dimensions,
 * paper sizes, margins, grid calculations, and print specifications.
 *
 * These types support the creation of printable sequence card pages that match
 * desktop application functionality for physical printing.
 */

import type { SequenceData } from "../core/SequenceData";

// ============================================================================
// CORE PAGE LAYOUT TYPES
// ============================================================================

export interface PageDimensions {
  width: number;
  height: number;
}

export interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

export interface Rectangle {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface SequenceCardGridConfig {
  rows: number;
  columns: number;
  spacing: number;
  cardWidth: number;
  cardHeight: number;
}

export interface Page {
  id: string;
  sequences: SequenceData[];
  layout: SequenceCardGridConfig;
  pageNumber: number;
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: Margins;
}

// ============================================================================
// PAPER SPECIFICATIONS
// ============================================================================

export type SequenceCardPaperSize = "A4" | "Letter" | "Legal" | "Tabloid";
export type PageOrientation = "Portrait" | "Landscape";

export interface PaperSpecification {
  name: SequenceCardPaperSize;
  dimensions: PageDimensions; // in points (1/72 inch)
  displayName: string;
  description: string;
}

export interface PrintConfiguration {
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: Margins;
  dpi: number;
  enablePageNumbers: boolean;
  enableHeader: boolean;
  enableFooter: boolean;
  headerText?: string;
  footerText?: string;
}

// ============================================================================
// LAYOUT CALCULATION TYPES
// ============================================================================

export interface LayoutCalculationRequest {
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: Margins;
  cardAspectRatio: number;
  sequenceCount: number;
  preferredCardsPerPage?: number;
}

export interface LayoutCalculationResult {
  gridConfig: SequenceCardGridConfig;
  pagesNeeded: number;
  cardDimensions: PageDimensions;
  contentArea: Rectangle;
  utilization: number; // 0-1 representing how well the layout uses available space
  isOptimal: boolean;
}

export interface GridCalculationOptions {
  minCardsPerPage: number;
  maxCardsPerPage: number;
  preferSquareLayout: boolean;
  prioritizeCardSize: boolean;
  allowPartialLastPage: boolean;
}

// ============================================================================
// PAGE LAYOUT CONFIGURATION
// ============================================================================

export interface PageLayoutConfig {
  printConfiguration: PrintConfiguration;
  gridOptions: GridCalculationOptions;
  sequencesPerPage: number;
  enableOptimization: boolean;
}

export interface PageCreationOptions {
  layout: PageLayoutConfig;
  sequences: SequenceData[];
  startPageNumber: number;
  enableEmptyPages: boolean;
  emptyPageMessage?: string;
}

// ============================================================================
// MEASUREMENT AND CONVERSION TYPES
// ============================================================================

export interface DPIConfiguration {
  screenDPI: number;
  printDPI: number;
  scaleFactor: number;
}

export interface MeasurementUnit {
  name: string;
  pointsPerUnit: number; // 1 point = 1/72 inch
  displayName: string;
}

export interface ConversionResult {
  points: number;
  pixels: number;
  inches: number;
  millimeters: number;
}

// ============================================================================
// VALIDATION TYPES
// ============================================================================

export interface LayoutValidationResult {
  isValid: boolean;
  errors: LayoutValidationError[];
  warnings: LayoutValidationWarning[];
  suggestions: LayoutSuggestion[];
}

export interface LayoutValidationError {
  code: string;
  message: string;
  field?: string;
  severity: "error" | "warning" | "info";
}

export interface LayoutValidationWarning {
  code: string;
  message: string;
  suggestion?: string;
}

export interface LayoutSuggestion {
  type: "paper_size" | "orientation" | "grid" | "margins";
  description: string;
  suggestedValue: unknown;
  expectedImprovement: string;
}

// ============================================================================
// CONSTANTS
// ============================================================================

export const PAPER_SIZES: Record<SequenceCardPaperSize, PaperSpecification> = {
  A4: {
    name: "A4",
    dimensions: { width: 595, height: 842 }, // 210mm x 297mm at 72 DPI
    displayName: "A4",
    description: '210mm × 297mm (8.27" × 11.69")',
  },
  Letter: {
    name: "Letter",
    dimensions: { width: 612, height: 792 }, // 8.5" x 11" at 72 DPI
    displayName: "US Letter",
    description: '8.5" × 11" (216mm × 279mm)',
  },
  Legal: {
    name: "Legal",
    dimensions: { width: 612, height: 1008 }, // 8.5" x 14" at 72 DPI
    displayName: "US Legal",
    description: '8.5" × 14" (216mm × 356mm)',
  },
  Tabloid: {
    name: "Tabloid",
    dimensions: { width: 792, height: 1224 }, // 11" x 17" at 72 DPI
    displayName: "Tabloid",
    description: '11" × 17" (279mm × 432mm)',
  },
};

export const DEFAULT_MARGINS: Margins = {
  top: 36, // 0.5 inch
  right: 18, // 0.25 inch
  bottom: 36, // 0.5 inch
  left: 18, // 0.25 inch
};

export const DEFAULT_DPI_CONFIG: DPIConfiguration = {
  screenDPI: 96,
  printDPI: 300,
  scaleFactor: 96 / 72, // Convert points to pixels for screen display
};

export const MEASUREMENT_UNITS: Record<string, MeasurementUnit> = {
  points: { name: "points", pointsPerUnit: 1, displayName: "pt" },
  inches: { name: "inches", pointsPerUnit: 72, displayName: "in" },
  millimeters: {
    name: "millimeters",
    pointsPerUnit: 72 / 25.4,
    displayName: "mm",
  },
  centimeters: {
    name: "centimeters",
    pointsPerUnit: 72 / 2.54,
    displayName: "cm",
  },
};

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type SequenceCardLayoutMode = "optimal" | "fixed" | "custom";
export type OptimizationGoal =
  | "maximize_card_size"
  | "minimize_pages"
  | "balanced";

export interface LayoutOptimizationRequest {
  goal: OptimizationGoal;
  constraints: {
    minCardSize?: PageDimensions;
    maxPages?: number;
    preferredAspectRatio?: number;
  };
  weights: {
    cardSizeWeight: number;
    pageCountWeight: number;
    utilizationWeight: number;
  };
}

export interface LayoutOptimizationResult {
  recommendedConfig: PageLayoutConfig;
  alternativeConfigs: PageLayoutConfig[];
  optimizationScore: number;
  reasoning: string[];
}
