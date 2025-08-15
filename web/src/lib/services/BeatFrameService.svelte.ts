/**
 * Beat Frame Service (Runes-based) - Enhanced with Legacy Sizing Logic
 *
 * Manages beat frame layout and interactions for the Workbench.
 * Now supports responsive sizing based on container dimensions like the legacy app.
 */

import type { BeatData } from "../domain";
import { GridMode } from "../domain";

interface BeatFrameConfig {
  /** Number of columns allocated for BEATS (excludes the Start tile column) */
  columns: number;
  beatSize: number;
  gap: number;
  gridMode: GridMode;
  /** Whether to reserve the first column for the Start Position tile */
  hasStartTile: boolean;
}

interface ContainerDimensions {
  width: number;
  height: number;
  isFullscreen: boolean;
}

interface LayoutInfo {
  rows: number;
  columns: number;
  cellSize: number;
  totalWidth: number;
  totalHeight: number;
  shouldScroll: boolean;
}

class BeatFrameService {
  // Configuration state
  #config = $state<BeatFrameConfig>({
    columns: 4, // columns for beats only
    beatSize: 160, // Increased default fallback size from 120 to 160
    gap: 0, // Desktop parity: zero spacing between cells
    gridMode: GridMode.DIAMOND,
    hasStartTile: true,
  });

  // Container dimensions state
  #containerDimensions = $state<ContainerDimensions>({
    width: 0,
    height: 0,
    isFullscreen: false,
  });

  // Interaction state
  #hoveredBeatIndex = $state<number>(-1);
  #draggedBeatIndex = $state<number>(-1);

  // Beat count grid mapping from legacy (optimal layouts)
  private readonly beatCountGridMap: Record<number, [number, number]> = {
    1: [1, 1], // One beat + start position
    2: [1, 2],
    3: [1, 3],
    4: [1, 4],
    5: [2, 4],
    6: [2, 4],
    7: [2, 4],
    8: [2, 4],
    9: [3, 4],
    10: [3, 4],
    11: [3, 4],
    12: [3, 4],
    13: [4, 4],
    14: [4, 4],
    15: [4, 4],
    16: [4, 4],
    17: [5, 4],
    18: [5, 4],
    19: [5, 4],
    20: [5, 4],
    21: [6, 4],
    22: [6, 4],
    23: [6, 4],
    24: [6, 4],
    25: [7, 4],
    26: [7, 4],
    27: [7, 4],
    28: [7, 4],
    29: [8, 4],
    30: [8, 4],
    31: [8, 4],
    32: [8, 4],
  };

  // Derived state
  readonly config = $derived(this.#config);
  readonly hoveredBeatIndex = $derived(this.#hoveredBeatIndex);
  readonly draggedBeatIndex = $derived(this.#draggedBeatIndex);
  readonly containerDimensions = $derived(this.#containerDimensions);

  // Actions
  setConfig(updates: Partial<BeatFrameConfig>): void {
    this.#config = { ...this.#config, ...updates };
  }

  setContainerDimensions(
    width: number,
    height: number,
    isFullscreen = false
  ): void {
    // Only update if dimensions actually changed to prevent loops
    if (
      this.#containerDimensions.width === width &&
      this.#containerDimensions.height === height &&
      this.#containerDimensions.isFullscreen === isFullscreen
    ) {
      return; // No change, skip update
    }

    this.#containerDimensions = {
      width,
      height,
      isFullscreen,
    };

    // DEBUG: Log container dimension updates
    console.log("[MODERN] BeatFrameService container dimensions updated:", {
      width,
      height,
      isFullscreen,
      currentConfig: this.#config,
    });

    // Don't automatically recalculate here - let components trigger when needed
  }

  setHoveredBeat(index: number): void {
    this.#hoveredBeatIndex = index;
  }

  clearHoveredBeat(): void {
    this.#hoveredBeatIndex = -1;
  }

  setDraggedBeat(index: number): void {
    this.#draggedBeatIndex = index;
  }

  clearDraggedBeat(): void {
    this.#draggedBeatIndex = -1;
  }

  // Layout calculations with legacy logic
  private autoAdjustLayout(beatCount: number): [number, number] {
    // For empty sequence or only start position, use single column layout
    if (beatCount <= 0) return [1, 1];
    if (beatCount === 1) return [1, 1]; // Single beat + start position

    // Use predefined layouts for common beat counts
    if (beatCount <= 32 && this.beatCountGridMap[beatCount]) {
      return this.beatCountGridMap[beatCount];
    }

    // Default layout for larger sequences
    const cols = 4;
    const rows = Math.ceil(beatCount / cols);
    return [rows, cols];
  }

  /**
   * Calculate the optimal cell size for the beat frame grid (from legacy)
   */
  private calculateCellSize(
    beatCount: number,
    containerWidth: number,
    containerHeight: number,
    totalRows: number,
    totalCols: number,
    gap: number
  ): number {
    // Increased minimum cell size thresholds for better visibility
    const MIN_CELL_SIZE_FULLSCREEN = 140; // Increased from 100px
    const MIN_CELL_SIZE_NORMAL = 120; // Increased from 70px

    // Ensure we have valid dimensions
    if (
      containerWidth <= 0 ||
      containerHeight <= 0 ||
      totalRows <= 0 ||
      totalCols <= 0
    ) {
      return 140; // Increased default fallback size
    }

    // Detect if we're in fullscreen mode by checking container dimensions
    const isLikelyFullscreen =
      this.#containerDimensions.isFullscreen ||
      (containerWidth > 800 && containerHeight > 600);

    // Set the minimum cell size based on mode
    const minCellSize = isLikelyFullscreen
      ? MIN_CELL_SIZE_FULLSCREEN
      : MIN_CELL_SIZE_NORMAL;

    // Calculate total space needed for gaps
    const totalGapWidth = gap * (totalCols - 1);
    const totalGapHeight = gap * (totalRows - 1);

    // Reduced padding for more space utilization
    const horizontalPadding = beatCount === 0 ? containerWidth * 0.02 : 8; // Reduced from 0.05 and 10
    const verticalPadding = 16; // Reduced from 24
    const availableWidth = Math.max(
      0,
      containerWidth - totalGapWidth - horizontalPadding * 2
    );
    const availableHeight = Math.max(
      0,
      containerHeight - totalGapHeight - verticalPadding * 2
    );

    // Calculate cell size based on available space in both dimensions
    const cellWidthByContainer = Math.floor(availableWidth / totalCols);
    const cellHeightByContainer = Math.floor(availableHeight / totalRows);

    // Use the smaller dimension to maintain square cells and preserve aspect ratio
    const baseSize = Math.min(cellWidthByContainer, cellHeightByContainer);

    // Reduced scaling factor to preserve more size
    const scalingFactor = 0.98; // Reduced scaling from 0.92 to 0.98 (only 2% reduction)
    const scaledBaseSize = Math.floor(baseSize * scalingFactor);

    // For start position only, make it proportionally larger
    const cellSize = beatCount === 0 ? scaledBaseSize * 1.1 : scaledBaseSize;

    // Check if the calculated cell size is below the minimum threshold
    if (cellSize < minCellSize) {
      console.debug(
        "Cell size below minimum threshold, using minimum size instead:",
        {
          calculatedSize: cellSize,
          minCellSize,
          totalRows,
          totalCols,
          containerWidth,
          containerHeight,
        }
      );

      // Apply different constraints based on mode
      if (isLikelyFullscreen) {
        return Math.min(Math.max(minCellSize, MIN_CELL_SIZE_FULLSCREEN), 300); // Increased max from 200px to 300px
      } else {
        return Math.min(Math.max(minCellSize, MIN_CELL_SIZE_NORMAL), 250); // Increased max from 160px to 250px
      }
    }

    // Apply different constraints based on mode with increased maximums
    if (isLikelyFullscreen) {
      // In fullscreen, allow larger cells
      return Math.min(Math.max(cellSize, MIN_CELL_SIZE_FULLSCREEN), 300); // Increased max from 200px to 300px
    } else {
      // In normal mode, allow larger cells
      return Math.min(Math.max(cellSize, MIN_CELL_SIZE_NORMAL), 250); // Increased max from 160px to 250px
    }
  }

  /**
   * Update beat size based on current container dimensions
   */
  private updateBeatSizeFromContainer(beatCount = 0): void {
    if (
      this.#containerDimensions.width <= 0 ||
      this.#containerDimensions.height <= 0
    ) {
      return; // Wait for valid dimensions
    }

    const [rows, cols] = this.autoAdjustLayout(beatCount);
    const totalCols = cols + (this.#config.hasStartTile ? 1 : 0);

    const newCellSize = this.calculateCellSize(
      beatCount,
      this.#containerDimensions.width,
      this.#containerDimensions.height,
      rows,
      totalCols,
      this.#config.gap
    );

    // Update configuration with new size and layout
    this.#config = {
      ...this.#config,
      beatSize: newCellSize,
      columns: cols,
    };
  }

  private totalColumns(): number {
    return this.#config.columns + (this.#config.hasStartTile ? 1 : 0);
  }

  calculateBeatPosition(
    index: number,
    beatCount?: number
  ): { x: number; y: number } {
    // Use the optimal layout for this beat count
    const [, cols] = this.autoAdjustLayout(beatCount ?? index + 1);
    const columnsForBeats = Math.max(1, cols);
    const row = Math.floor(index / columnsForBeats);
    const col = (index % columnsForBeats) + (this.#config.hasStartTile ? 1 : 0);

    const step = this.#config.beatSize + this.#config.gap;
    return { x: col * step, y: row * step };
  }

  calculateFrameDimensions(beatCount: number): {
    width: number;
    height: number;
  } {
    const step = this.#config.beatSize + this.#config.gap;

    // If no beats, size to just the Start tile (desktop shows START only)
    if (beatCount <= 0) {
      const width = this.#config.hasStartTile ? this.#config.beatSize : 0;
      const height = this.#config.beatSize;
      return { width, height };
    }

    const [rows, cols] = this.autoAdjustLayout(beatCount);
    const totalCols = cols + (this.#config.hasStartTile ? 1 : 0);

    return {
      width: totalCols * step - this.#config.gap,
      height: rows * step - this.#config.gap,
    };
  }

  /**
   * Calculate comprehensive layout information including overflow detection (PURE)
   */
  calculateLayoutInfo(beatCount: number): LayoutInfo {
    // Get optimal layout without mutating state
    const [rows, cols] = this.autoAdjustLayout(beatCount);
    const totalCols = cols + (this.#config.hasStartTile ? 1 : 0);

    // Calculate optimal cell size without mutating state
    const optimalCellSize = this.calculateOptimalCellSize(
      beatCount,
      rows,
      totalCols
    );

    const step = optimalCellSize + this.#config.gap;
    const totalWidth = totalCols * step - this.#config.gap;
    const totalHeight = rows * step - this.#config.gap;

    // Check if content would overflow container
    const containerWidth = this.#containerDimensions.width;
    const containerHeight = this.#containerDimensions.height;

    const shouldScroll =
      (containerWidth > 0 && totalWidth > containerWidth) ||
      (containerHeight > 0 && totalHeight > containerHeight) ||
      optimalCellSize <=
        (this.#containerDimensions.isFullscreen ? 140 : 120) * 1.1; // Updated thresholds to match new minimums

    return {
      rows,
      columns: cols,
      cellSize: optimalCellSize,
      totalWidth,
      totalHeight,
      shouldScroll,
    };
  }

  /**
   * Calculate optimal cell size without mutating state (PURE)
   */
  private calculateOptimalCellSize(
    beatCount: number,
    rows: number,
    totalCols: number
  ): number {
    try {
      if (
        this.#containerDimensions.width <= 0 ||
        this.#containerDimensions.height <= 0
      ) {
        return this.#config.beatSize; // Return current size if no container dimensions
      }

      const result = this.calculateCellSize(
        beatCount,
        this.#containerDimensions.width,
        this.#containerDimensions.height,
        rows,
        totalCols,
        this.#config.gap
      );

      // Ensure result is a valid number
      return isNaN(result) || result <= 0 ? this.#config.beatSize : result;
    } catch (error) {
      console.warn("Error calculating optimal cell size:", error);
      return this.#config.beatSize;
    }
  }

  // Beat interaction helpers
  getBeatAtPosition(x: number, y: number, beatCount: number): number {
    const step = this.#config.beatSize + this.#config.gap;
    const colRaw = Math.floor(x / step);
    const row = Math.floor(y / step);

    // Ignore clicks on the Start tile column
    const startOffset = this.#config.hasStartTile ? 1 : 0;
    if (colRaw < startOffset) return -1;

    const col = colRaw - startOffset;
    const index = row * Math.max(1, this.#config.columns) + col;
    return index >= 0 && index < beatCount ? index : -1;
  }

  isBeatVisible(beat: BeatData): boolean {
    return !beat.is_blank || beat.pictograph_data != null;
  }

  getBeatDisplayText(beat: BeatData): string {
    if (beat.is_blank && !beat.pictograph_data) {
      // fallback: show beat number if available on metadata or domain type
      return (
        beat.beat_number ??
        (beat.metadata as Record<string, unknown>)?.beat_number ??
        ""
      ).toString();
    }
    const metadataLetter = (beat.metadata as Record<string, unknown>)?.letter;
    return (
      beat.pictograph_data?.letter ??
      (typeof metadataLetter === "string" ? metadataLetter : "") ??
      ""
    );
  }
}

// Singleton instance
export const beatFrameService = new BeatFrameService();
