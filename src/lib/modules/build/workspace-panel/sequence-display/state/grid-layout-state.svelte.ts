/**
 * Grid Layout State Factory
 *
 * Svelte 5 runes-based state management for responsive grid layout calculations.
 * Handles column count, row count, and cell sizing based on container dimensions.
 */

import type { IDeviceDetector } from "$shared";
import type {
  GridLayout,
  GridSizingConstraints,
} from "../domain/models/beat-grid-display-models";
import { DEFAULT_GRID_SIZING } from "../domain/models/beat-grid-display-models";

/**
 * Create grid layout state with responsive calculations
 */
export function createGridLayoutState(
  deviceDetector: IDeviceDetector | null,
  isSideBySideLayout: () => boolean = () => false
) {
  // Container dimensions (reactive)
  let containerWidth = $state(0);
  let containerHeight = $state(0);

  // Sizing constraints (can be configured)
  let sizingConstraints = $state<GridSizingConstraints>({
    ...DEFAULT_GRID_SIZING,
  } as GridSizingConstraints);

  /**
   * Calculate responsive grid layout
   */
  const gridLayout = $derived.by((): GridLayout => {
    // If no device detector or no container size, return defaults
    if (!deviceDetector || containerWidth === 0 || containerHeight === 0) {
      return {
        rows: 1,
        columns: 4,
        totalColumns: 5, // +1 for start position
        cellSize: 160,
        maxColumns: 4,
      };
    }

    const isDesktop = deviceDetector.isDesktop();

    // Determine max columns based on layout mode and container width
    // When in side-by-side layout (panels horizontal): Always use 4 columns
    // When in stacked layout (panels vertical): Use 650px threshold (8 or 4 columns)
    let maxColumns: number;
    if (isSideBySideLayout()) {
      // Side-by-side layout (desktop/landscape): Always 4 columns for better fit
      maxColumns = 4;
    } else {
      // Stacked layout (mobile/portrait): Use width-based threshold
      // 650px threshold matches OptionPicker behavior
      maxColumns = containerWidth >= 650 ? 8 : 4;
    }

    return {
      rows: 0, // Will be calculated when beat count is known
      columns: 0, // Will be calculated when beat count is known
      totalColumns: maxColumns + 1, // +1 for start position
      cellSize: 160, // Default, will be calculated
      maxColumns,
    };
  });

  /**
   * Calculate layout for specific beat count
   */
  function calculateLayoutForBeats(beatCount: number): GridLayout {
    const maxColumns = gridLayout.maxColumns;

    // Calculate actual columns based on beat count and max columns
    const columns = beatCount <= maxColumns ? beatCount : maxColumns;
    const rows = Math.ceil(beatCount / columns);
    const totalColumns = columns + 1; // +1 for start position

    // Calculate responsive cell size considering both width and height
    let cellSize = 160; // Default

    if (containerWidth > 0 && containerHeight > 0) {
      // Use padding ratios from constraints
      const maxCellWidth =
        (containerWidth * sizingConstraints.widthPaddingRatio) / totalColumns;

      // For grids with threshold rows or fewer, consider height
      // For larger grids, prioritize width since scrolling is inevitable
      if (rows <= sizingConstraints.heightSizingRowThreshold) {
        const maxCellHeight =
          (containerHeight * sizingConstraints.heightPaddingRatio) / rows;
        // Use the smaller dimension to ensure the entire grid fits
        cellSize = Math.max(
          sizingConstraints.minCellSize,
          Math.min(
            sizingConstraints.maxCellSize,
            Math.floor(Math.min(maxCellWidth, maxCellHeight))
          )
        );
      } else {
        // For larger grids, prioritize width-based sizing
        cellSize = Math.max(
          sizingConstraints.minCellSize,
          Math.min(sizingConstraints.maxCellSize, Math.floor(maxCellWidth))
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
  function calculateBeatPosition(
    beatIndex: number,
    layout: GridLayout
  ): { row: number; column: number } {
    const row = Math.floor(beatIndex / layout.columns) + 1;
    const column = (beatIndex % layout.columns) + 2; // +2 because start position is column 1
    return { row, column };
  }

  /**
   * Update container dimensions
   */
  function setContainerSize(width: number, height: number) {
    containerWidth = width;
    containerHeight = height;
  }

  /**
   * Update sizing constraints
   */
  function setSizingConstraints(constraints: Partial<GridSizingConstraints>) {
    sizingConstraints = { ...sizingConstraints, ...constraints };
  }

  return {
    // Getters for reactive state
    get containerWidth() {
      return containerWidth;
    },
    get containerHeight() {
      return containerHeight;
    },
    get gridLayout() {
      return gridLayout;
    },
    get sizingConstraints() {
      return sizingConstraints;
    },

    // Actions
    setContainerSize,
    setSizingConstraints,
    calculateLayoutForBeats,
    calculateBeatPosition,
  };
}

export type GridLayoutState = ReturnType<typeof createGridLayoutState>;
