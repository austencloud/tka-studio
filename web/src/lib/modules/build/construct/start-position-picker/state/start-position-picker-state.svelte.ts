/**
 * StartPositionState.svelte.ts - Simple state layer for start positions
 * Follows TKA architecture: Service → State → Component
 */

import { GridMode, type PictographData } from "$shared";
import type { IStartPositionService } from "../services/contracts";

/**
 * Simple state service that syncs with StartPositionService
 * Avoids over-engineering by directly reflecting service state
 */
export function createStartPositionPickerState(
  startPositionService: IStartPositionService
) {
  // Create reactive state managed locally
  let startPositionPictographs = $state<PictographData[]>([]);
  let selectedStartPos = $state<PictographData | null>(null);
  let isLoading = $state(false);
  let loadingError = $state(false);

  // Load start positions when grid mode changes
  async function loadStartPositions(gridMode: GridMode) {
    try {
      isLoading = true;
      loadingError = false;
      startPositionPictographs = await startPositionService.getStartPositions(gridMode);
    } catch (error) {
      console.error("Error loading start positions:", error);
      loadingError = true;
      startPositionPictographs = [];
    } finally {
      isLoading = false;
    }
  }

  // Initialize with default grid mode
  if (typeof window !== "undefined") {
    loadStartPositions(GridMode.DIAMOND);
  }

  return {
    // Reactive state getters
    get startPositionPictographs() {
      return startPositionPictographs;
    },
    get selectedStartPos() {
      return selectedStartPos;
    },
    get isLoading() {
      return isLoading;
    },
    get loadingError() {
      return loadingError;
    },

    // Service delegation
    loadStartPositions,
    setSelectedStartPos: (pos: PictographData | null) => {
      selectedStartPos = pos;
    },
    selectStartPosition: async (position: PictographData) => {
      await startPositionService.selectStartPosition(position);
      selectedStartPos = position;
    },
  };
}
