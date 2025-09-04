import type {
  PageOrientation,
  SequenceData,
  WordCardPaperSize,
} from "$shared/domain";

// Type alias for backward compatibility

export interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

export interface LayoutValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export interface Rectangle {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface GridConfig {
  rows: number;
  columns: number;
  cardWidth: number;
  cardHeight: number;
  spacing: number;
}

export interface LayoutCalculationRequest {
  paperSize: WordCardPaperSize;
  orientation: PageOrientation;
  cardCount: number;
  cardAspectRatio: number;
}

export interface LayoutCalculationResult {
  isOptimal: boolean;
  gridConfig: GridConfig;
  pageConfig: PageLayoutConfig;
  utilization: number;
}

// DPIConfig moved to line 197 to avoid duplicates

// Duplicate interface removed - using the complete definition below

/**
 * Page Layout Models
 *
 * Interface definitions for printable page layout functionality including page dimensions,
 * paper sizes, margins, grid calculations, and print specifications.
 */

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

export interface WordCardGridConfig {
  rows: number;
  columns: number;
  spacing: number;
  cardWidth: number;
  cardHeight: number;
}

export interface Page {
  id: string;
  sequences: SequenceData[];
  layout: WordCardGridConfig;
  pageNumber: number;
  paperSize: WordCardPaperSize;
  orientation: PageOrientation;
  margins: PageMargins;
}

// ============================================================================
// PAPER SPECIFICATIONS
// ============================================================================

export interface PaperSpecification {
  name: WordCardPaperSize;
  dimensions: PageDimensions; // in points (1/72 inch)
  displayName: string;
  description: string;
}

export interface PrintConfig {
  paperSize: WordCardPaperSize;
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
  paperSize: WordCardPaperSize;
  orientation: PageOrientation;
  margins: PageMargins;
  cardAspectRatio: number;
  sequenceCount: number;
  preferredCardsPerPage?: number;
}

export interface WordCardLayoutCalculationResult {
  gridConfig: WordCardGridConfig;
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
  printConfig: PrintConfig;
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

export interface DPIConfig {
  screenDPI: number;
  printDPI: number;
  scaleFactor: number;
}

// Type alias for backward compatibility with services expecting DPIConfiguration
export type DPIConfiguration = DPIConfig;

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
// Duplicate simplified types removed — using the core, fully-defined interfaces above.

// ============================================================================
// GRID LAYOUT INTERFACES
// ============================================================================

export interface GridLayout {
  columns: number;
  rows: number;
  cardWidth: number;
  cardHeight: number;
  spacing: number;
  totalWidth: number;
  totalHeight: number;
}

export interface LayoutRecommendation {
  layout: GridLayout;
  score: number;
  description: string;
  pros: string[];
  cons: string[];
}
