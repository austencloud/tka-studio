/**
 * Word-cards models exports
 *
 * Selective exports to avoid conflicts
 */

// Import types needed for interfaces defined in this file
import type { SequenceData } from "$shared/domain";
import type {
  PageOrientation,
  WordCardPaperSize,
} from "../types/PageLayoutTypes";
import type { PageDimensions } from "./PageLayout";

export * from "./PageLayoutConstants";

// From WordCard.ts (primary source for WordCardExportResult)
export * from "./WordCard";
export type { WordCardExportResult } from "./WordCard";

// From WordCardExport.ts (exclude conflicting types)
export type {
  BatchExportProgress,
  BatchOperationConfig,
  ExportMetrics,
  WordCardDimensions,
  WordCardMetadata as WordCardExportMetadata,
} from "./WordCardExport";

// From PageLayout.ts (primary source for LayoutCalculationResult) - exclude Page to avoid conflict
export type {
  DPIConfig,
  DPIConfiguration,
  GridConfig,
  LayoutCalculationResult,
  LayoutValidationResult,
  Margins,
  PageDimensions,
  LayoutCalculationRequest as PageLayoutCalculationRequest,
  PageLayoutConfig,
  PageCreationOptions as PageLayoutCreationOptions,
  GridCalculationOptions as PageLayoutGridCalculationOptions,
  PrintConfig,
  Rectangle,
} from "./PageLayout";

// From PageLayoutTypes.ts
export type { WordCardPaperSize } from "../types/PageLayoutTypes";

// Additional commonly needed types for services
export interface MeasurementUnit {
  name: string;
  pointsPerUnit: number;
  displayName?: string;
}

export interface PageMargins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

export interface PaperSpecification {
  name: WordCardPaperSize;
  dimensions: PageDimensions; // in points (1/72 inch)
  displayName: string;
  description: string;
}

export interface GridCalculationOptions {
  minCardsPerPage: number;
  maxCardsPerPage: number;
  preferSquareLayout: boolean;
  prioritizeCardSize: boolean;
  allowPartialLastPage: boolean;
  minCardSize?: { width: number; height: number };
  maxCardSize?: { width: number; height: number };
  preferredAspectRatio?: number;
  padding?: number;
}

export interface LayoutCalculationRequest {
  sequences: unknown[];
  paperSize: string;
  orientation: PageOrientation;
  margins: PageMargins;
  preferredCardsPerPage?: number;
  cardAspectRatio?: number;
  sequenceCount?: number;
}

export interface PageCreationOptions {
  layout: unknown;
  sequences: unknown[];
  startPageNumber: number;
  enableEmptyPages?: boolean;
  emptyPageMessage?: string;
}

export interface WordCardGridConfig {
  rows: number;
  columns: number;
  cardWidth: number;
  cardHeight: number;
  spacing: number;
}

export interface SequenceStatistics {
  totalSequences: number;
  averageLength: number;
  complexityDistribution: Record<string, number>;
  totalBeats?: number;
  blankBeats?: number;
  filledBeats?: number;
  totalDuration?: number;
  averageBeatDuration?: number;
  hasStartPosition?: boolean;
  reversalCount?: {
    blue: number;
    red: number;
  };
}

export interface Page {
  id: string;
  sequences: SequenceData[];
  pageNumber: number;
  layout?: unknown;
  paperSize?: string;
  orientation?: string;
  margins?: PageMargins;
}

export interface LayoutValidationError {
  code: string;
  message: string;
  severity: "error" | "warning";
  field?: string;
}

export interface LayoutValidationWarning {
  code: string;
  message: string;
  severity: "warning";
  suggestion?: string;
}

export interface WordCardMetadata {
  title?: string;
  description?: string;
  tags?: string[];
  difficulty?: number;
  author?: string;
  backgroundColor?: string;
  beatNumbers?: boolean;
  timestamp?: boolean;
}

// Use DPIConfig from PageLayout.ts (not word-card-models.ts) to match service expectations
