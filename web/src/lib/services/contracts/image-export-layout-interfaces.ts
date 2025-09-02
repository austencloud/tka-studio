/**
 * TKA Image Export Layout Interfaces
 *
 * Service contracts for layout calculation, dimension management,
 * and positioning logic in the TKA image export system.
 */

import type { ImageExportOptions } from "$domain";

// ============================================================================
// LAYOUT AND DIMENSION SERVICES
// ============================================================================

/**
 * Layout calculation service for grid positioning
 * Equivalent to desktop ImageExportLayoutHandler
 */
export interface ILayoutCalculationService {
  /**
   * Calculate optimal layout for given beat count
   * Returns [columns, rows] matching desktop layout tables
   */
  calculateLayout(
    beatCount: number,
    includeStartPosition: boolean
  ): [number, number];

  /**
   * Calculate image dimensions for layout
   * Returns [width, height] in pixels
   */
  calculateImageDimensions(
    layout: [number, number],
    additionalHeight: number,
    beatScale?: number
  ): [number, number];

  /**
   * Get layout for current beat frame (compatibility method)
   */
  getCurrentBeatFrameLayout(beatCount: number): [number, number];

  /**
   * Validate layout parameters
   */
  validateLayout(beatCount: number, includeStartPosition: boolean): boolean;
}

/**
 * Dimension calculation service
 * Equivalent to desktop HeightDeterminer
 */
export interface IDimensionCalculationService {
  /**
   * Determine additional heights for text areas
   * Returns [topHeight, bottomHeight]
   */
  determineAdditionalHeights(
    options: ImageExportOptions,
    beatCount: number,
    beatScale: number
  ): [number, number];

  /**
   * Calculate beat size with scaling
   */
  calculateScaledBeatSize(baseSize: number, scale: number): number;

  /**
   * Calculate margin with scaling
   */
  calculateScaledMargin(baseMargin: number, scale: number): number;

  /**
   * Validate dimension parameters
   */
  validateDimensions(
    beatCount: number,
    beatScale: number,
    options: ImageExportOptions
  ): boolean;
}

// ============================================================================
// SERVICE INTERFACE SYMBOLS
// ============================================================================

export const ILayoutCalculationServiceInterface = Symbol.for(
  "ILayoutCalculationService"
);
export const IDimensionCalculationServiceInterface = Symbol.for(
  "IDimensionCalculationService"
);
