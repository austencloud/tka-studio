import type {
  PageOrientation,
  SequenceCardPaperSize,
  SequenceData,
} from "$domain";

// Type alias for backward compatibility
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

export interface PageLayoutConfig {
  paperSize: SequenceCardPaperSize;
  orientation: PageOrientation;
  margins: Margins;
  sequencesPerPage: number;
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

export interface GridCalculationOptions {
  minCardSize: number;
  maxCardSize: number;
  preferredAspectRatio: number;
  padding: number;
}

export interface GridConfig {
  rows: number;
  columns: number;
  cardWidth: number;
  cardHeight: number;
  spacing: number;
}

export interface LayoutCalculationRequest {
  paperSize: SequenceCardPaperSize;
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

export interface DPIConfiguration {
  screen: number;
  print: number;
}

export interface PageCreationOptions {
  layout: PageLayoutConfig;
  sequencesPerPage: number;
  includePageNumbers: boolean;
  includeHeaders: boolean;
}

export interface Page {
  pageNumber: number;
  sequences: SequenceData[];
  layout: PageLayoutConfig;
  isEmpty: boolean;
  message?: string;
}
