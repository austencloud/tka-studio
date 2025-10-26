/**
 * Beat Frame Layout Configuration
 *
 * Defines the optimal grid layout (rows, columns) for different beat counts.
 * Based on desktop app configuration for consistent UX across platforms.
 *
 * Format: [rows, columns] for each beat count
 * These layouts are optimized for visual balance and readability.
 */

export interface BeatFrameLayout {
  rows: number;
  columns: number;
}

/**
 * Desktop-aligned beat frame layouts
 * Source: desktop/data/beat_frame_layouts.py
 * Format: Desktop stores as (rows, columns) tuples
 *
 * Key patterns:
 * - Small counts (1-4): Single column, expanding rows
 * - Medium counts (5-20): Multiple columns, typically 2-4 columns
 * - 12 beats: Special case - 4 columns x 3 rows for optimal viewing
 * - Large counts (21+): Expanding columns, typically 4 rows
 */
export const BEAT_FRAME_LAYOUTS: Record<number, BeatFrameLayout> = {
  0: { rows: 0, columns: 1 },      // Desktop: (0, 1)
  1: { rows: 1, columns: 1 },      // Desktop: (1, 1)
  2: { rows: 1, columns: 2 },      // Desktop: (2, 1) -> 1 row, 2 columns
  3: { rows: 1, columns: 3 },      // Desktop: (3, 1) -> 1 row, 3 columns
  4: { rows: 1, columns: 4 },      // Desktop: (4, 1) -> 1 row, 4 columns
  5: { rows: 2, columns: 3 },      // Desktop: (3, 2) -> 2 rows, 3 columns
  6: { rows: 2, columns: 3 },      // Desktop: (3, 2)
  7: { rows: 2, columns: 4 },      // Desktop: (4, 2) -> 2 rows, 4 columns
  8: { rows: 2, columns: 4 },      // Desktop: (4, 2)
  9: { rows: 3, columns: 3 },      // Desktop: (3, 3) -> 3 rows, 3 columns
  10: { rows: 2, columns: 5 },     // Desktop: (5, 2) -> 2 rows, 5 columns
  11: { rows: 4, columns: 3 },     // Desktop: (3, 4) -> 4 rows, 3 columns
  12: { rows: 4, columns: 3 },     // Desktop: (3, 4) -> 4 rows, 3 columns - KEY: 12 beats = 3 cols!
  13: { rows: 4, columns: 4 },     // Desktop: (4, 4) -> 4 rows, 4 columns
  14: { rows: 4, columns: 4 },     // Desktop: (4, 4)
  15: { rows: 4, columns: 4 },     // Desktop: (4, 4)
  16: { rows: 4, columns: 4 },     // Desktop: (4, 4)
  17: { rows: 4, columns: 5 },     // Desktop: (5, 4) -> 4 rows, 5 columns
  18: { rows: 4, columns: 5 },     // Desktop: (5, 4)
  19: { rows: 4, columns: 5 },     // Desktop: (5, 4)
  20: { rows: 4, columns: 5 },     // Desktop: (5, 4)
  21: { rows: 6, columns: 4 },     // Desktop: (4, 6) -> 6 rows, 4 columns
  22: { rows: 6, columns: 4 },     // Desktop: (4, 6)
  23: { rows: 6, columns: 4 },     // Desktop: (4, 6)
  24: { rows: 6, columns: 4 },     // Desktop: (4, 6)
  25: { rows: 7, columns: 4 },     // Desktop: (4, 7) -> 7 rows, 4 columns
  26: { rows: 7, columns: 4 },     // Desktop: (4, 7)
  27: { rows: 7, columns: 4 },     // Desktop: (4, 7)
  28: { rows: 7, columns: 4 },     // Desktop: (4, 7)
  29: { rows: 8, columns: 4 },     // Desktop: (4, 8) -> 8 rows, 4 columns
  30: { rows: 8, columns: 4 },     // Desktop: (4, 8)
  31: { rows: 8, columns: 4 },     // Desktop: (4, 8)
  32: { rows: 8, columns: 4 },     // Desktop: (4, 8)
  33: { rows: 9, columns: 4 },     // Desktop: (4, 9) -> 9 rows, 4 columns
  34: { rows: 9, columns: 4 },     // Desktop: (4, 9)
  35: { rows: 9, columns: 4 },     // Desktop: (4, 9)
  36: { rows: 9, columns: 4 },     // Desktop: (4, 9)
  37: { rows: 10, columns: 4 },    // Desktop: (4, 10) -> 10 rows, 4 columns
  38: { rows: 10, columns: 4 },    // Desktop: (4, 10)
  39: { rows: 10, columns: 4 },    // Desktop: (4, 10)
  40: { rows: 10, columns: 4 },    // Desktop: (4, 10)
  41: { rows: 11, columns: 4 },    // Desktop: (4, 11) -> 11 rows, 4 columns
  42: { rows: 11, columns: 4 },    // Desktop: (4, 11)
  43: { rows: 11, columns: 4 },    // Desktop: (4, 11)
  44: { rows: 11, columns: 4 },    // Desktop: (4, 11)
  45: { rows: 12, columns: 4 },    // Desktop: (4, 12) -> 12 rows, 4 columns
  46: { rows: 12, columns: 4 },    // Desktop: (4, 12)
  47: { rows: 12, columns: 4 },    // Desktop: (4, 12)
  48: { rows: 12, columns: 4 },    // Desktop: (4, 12)
  49: { rows: 13, columns: 4 },    // Desktop: (4, 13) -> 13 rows, 4 columns
  50: { rows: 13, columns: 4 },    // Desktop: (4, 13)
  51: { rows: 13, columns: 4 },    // Desktop: (4, 13)
  52: { rows: 13, columns: 4 },    // Desktop: (4, 13)
  53: { rows: 14, columns: 4 },    // Desktop: (4, 14) -> 14 rows, 4 columns
  54: { rows: 14, columns: 4 },    // Desktop: (4, 14)
  55: { rows: 14, columns: 4 },    // Desktop: (4, 14)
  56: { rows: 14, columns: 4 },    // Desktop: (4, 14)
  57: { rows: 15, columns: 4 },    // Desktop: (4, 15) -> 15 rows, 4 columns
  58: { rows: 15, columns: 4 },    // Desktop: (4, 15)
  59: { rows: 15, columns: 4 },    // Desktop: (4, 15)
  60: { rows: 15, columns: 4 },    // Desktop: (4, 15)
  61: { rows: 16, columns: 4 },    // Desktop: (4, 16) -> 16 rows, 4 columns
  62: { rows: 16, columns: 4 },    // Desktop: (4, 16)
  63: { rows: 16, columns: 4 },    // Desktop: (4, 16)
  64: { rows: 16, columns: 4 },    // Desktop: (4, 16)
};

/**
 * Get the optimal layout for a given beat count
 * Falls back to calculated layout for counts not in the table
 */
export function getBeatFrameLayout(beatCount: number): BeatFrameLayout {
  // Use predefined layout if available
  if (beatCount in BEAT_FRAME_LAYOUTS) {
    return BEAT_FRAME_LAYOUTS[beatCount];
  }

  // Fallback: Calculate layout for counts beyond table
  // Pattern for large counts: 4 rows, expanding columns
  const columns = Math.ceil(beatCount / 4);
  return { rows: 4, columns };
}

/**
 * Check if a beat count should use a narrow layout (fewer columns than default)
 * Useful for responsive adjustments
 */
export function shouldUseNarrowLayout(beatCount: number): boolean {
  const layout = getBeatFrameLayout(beatCount);
  return layout.columns <= 3;
}

/**
 * Get maximum columns for responsive layout calculations
 * Returns the column count that should be used for the given beat count,
 * respecting both the optimal layout and layout mode constraints
 */
export function getMaxColumnsForBeatCount(
  beatCount: number,
  isSideBySideLayout: boolean
): number {
  const optimalLayout = getBeatFrameLayout(beatCount);

  // In side-by-side layout, respect the optimal column count but cap at 4
  // In stacked layout, use optimal column count with higher cap at 8
  if (isSideBySideLayout) {
    return Math.min(optimalLayout.columns, 4);
  } else {
    return Math.min(optimalLayout.columns, 8);
  }
}
