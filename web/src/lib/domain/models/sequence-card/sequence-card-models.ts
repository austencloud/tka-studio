/**
 * Page Layout Models
 *
 * Interface definitions for printable page layout functionality including page dimensions,
 * paper sizes, margins, grid calculations, and print specifications.
 */

import type {
  OptimizationGoal,
  PageOrientation,
  SequenceCardPaperSize,
} from "../../types/PageLayoutTypes";
import type { SequenceData } from "../core/sequence/SequenceData";

// ============================================================================
// CORE PAGE LAYOUT INTERFACES
// ============================================================================

export interface PageDimensions {
  width: number;
  height: number;
}

export interface PageMargins {
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
  margins: PageMargins;
}

// ============================================================================
// PAPER SPECIFICATIONS
// ============================================================================

export interface PaperSpecification {
  name: SequenceCardPaperSize;
  dimensions: PageDimensions; // in points (1/72 inch)
  displayName: string;
  description: string;
}

export interface PrintConfiguration {
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: PageMargins;
  dpi: number;
  enablePageNumbers: boolean;
  enableHeader: boolean;
  enableFooter: boolean;
  headerText?: string;
  footerText?: string;
}

// ============================================================================
// LAYOUT CALCULATION INTERFACES
// ============================================================================

export interface LayoutCalculationRequest {
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: PageMargins;
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
// MEASUREMENT AND CONVERSION INTERFACES
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
// VALIDATION INTERFACES
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
// OPTIMIZATION INTERFACES
// ============================================================================

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
// Duplicate simplified types removed — using the core, fully-defined interfaces above.
