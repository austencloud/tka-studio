/**
 * Sequence Service Interfaces
 *
 * Interfaces for sequence management, creation, updates, and domain logic.
 * This includes both service contracts and related data structures.
 *
 * Also includes page layout services for printable sequence card creation.
 */
// ============================================================================
// IMPORTS
// ============================================================================
import type { GridMode, SequenceData } from "$domain";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface SequenceCreateRequest {
  name: string;
  length: number;
  gridMode?: GridMode;
  propType?: string;
}

export interface DeleteResult {
  success: boolean;
  deletedSequence: SequenceData | null;
  affectedSequences: SequenceData[];
  error?: string;
}

export interface DeleteConfirmationData {
  sequence: SequenceData;
  relatedSequences: SequenceData[];
  hasVariations: boolean;
  willFixVariationNumbers: boolean;
}

// Page layout types for printable sequence cards
export type PaperSize = "A4" | "Letter" | "Legal" | "Tabloid";
export type PageOrientation = "portrait" | "landscape";

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
  paperSize: PaperSize;
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
  paperSize: PaperSize;
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
