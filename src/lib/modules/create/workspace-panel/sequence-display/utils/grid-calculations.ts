/**
 * Grid Calculation Utilities
 *
 * Pure functions for calculating grid layout dimensions and positions.
 * These are NOT reactive - they take inputs and return outputs.
 * The component's $derived will call these with reactive values.
 */

import type { IDeviceDetector } from "$shared";
import {
  getBeatFrameLayout,
  getMaxColumnsForBeatCount,
} from "../domain/models/beat-frame-layouts";

export interface GridLayout {
  rows: number;
  columns: number;
  totalColumns: number;
  cellSize: number;
  maxColumns: number;
}

export interface GridSizingConfig {
  minCellSize?: number;
  maxCellSize?: number;
  widthPaddingRatio?: number;
  heightPaddingRatio?: number;
  heightSizingRowThreshold?: number;
  columnBreakpoint?: number;
  isSideBySideLayout?: boolean;
}

const DEFAULT_SIZING: Required<GridSizingConfig> = {
  minCellSize: 50,
  maxCellSize: 200,
  widthPaddingRatio: 0.95,
  heightPaddingRatio: 0.95, // Increased from 0.9 to 1.0 to maximize cell size and fill available vertical space
  heightSizingRowThreshold: 4,
  columnBreakpoint: 650,
  isSideBySideLayout: false,
};

/**
 * Calculate responsive grid layout
 */
export function calculateGridLayout(
  beatCount: number,
  containerWidth: number,
  containerHeight: number,
  deviceDetector: IDeviceDetector | null,
  config: GridSizingConfig = {}
): GridLayout {
  const sizing = { ...DEFAULT_SIZING, ...config };

  // Determine if we should use wide layout based on container width and layout mode
  // Side-by-side layout: ALWAYS use narrow layout (ignore width)
  // Top-and-bottom layout: Use width to determine narrow vs wide
  const useWideLayout =
    !sizing.isSideBySideLayout && containerWidth >= sizing.columnBreakpoint;

  // Get optimal layout from desktop-aligned configuration
  const optimalLayout = getBeatFrameLayout(beatCount, useWideLayout);

  // Determine max columns based on layout mode and optimal layout
  // Side-by-side layout: Always 4 columns max (ignores container width)
  // Top-and-bottom layout: Width-based (4 or 8 columns depending on width)
  const maxColumns = getMaxColumnsForBeatCount(
    beatCount,
    sizing.isSideBySideLayout,
    containerWidth
  );

  // Calculate actual columns based on beat count and max columns
  // For small beat counts, use the optimal count; for larger counts, respect max columns
  const columns = Math.min(beatCount, maxColumns);
  const rows = Math.ceil(beatCount / columns);
  const totalColumns = columns + 1; // +1 for start position

  // Calculate responsive cell size considering both width and height
  let cellSize = 160; // Default

  if (containerWidth > 0 && containerHeight > 0) {
    // Use padding ratio to leave space around grid
    const maxCellWidth =
      (containerWidth * sizing.widthPaddingRatio) / totalColumns;

    // For grids with threshold rows or fewer, consider height to prevent clipping
    // For larger grids, prioritize width since scrolling is inevitable
    if (rows <= sizing.heightSizingRowThreshold) {
      // Use padding ratio for height
      const maxCellHeight =
        (containerHeight * sizing.heightPaddingRatio) / rows;
      // Use the smaller dimension to ensure the entire grid fits
      cellSize = Math.max(
        sizing.minCellSize,
        Math.min(
          sizing.maxCellSize,
          Math.floor(Math.min(maxCellWidth, maxCellHeight))
        )
      );
    } else {
      // For larger grids, prioritize width-based sizing
      cellSize = Math.max(
        sizing.minCellSize,
        Math.min(sizing.maxCellSize, Math.floor(maxCellWidth))
      );
    }
  }

  return {
    rows,
    columns,
    totalColumns,
    cellSize,
    maxColumns,
  };
}

/**
 * Calculate grid position (row, column) for beat index
 */
export function calculateBeatPosition(
  beatIndex: number,
  columns: number
): { row: number; column: number } {
  const row = Math.floor(beatIndex / columns) + 1;
  const column = (beatIndex % columns) + 2; // +2 because start position is column 1
  return { row, column };
}
