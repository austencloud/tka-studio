/**
 * StartPositionState.svelte.ts - Simple state layer for start positions
 * Follows TKA architecture: Service → State → Component
 */

import { GridMode } from "$domain";
import type { PictographData } from "$domain/core/pictograph/PictographData";
import type { IStartPositionService } from "$lib/services/contracts/application/IStartPositionService";

/**
 * Simple state service that syncs with StartPositionService
 * Avoids over-engineering by directly reflecting service state
 */
export function createStartPositionPickerState(
  startPositionService: IStartPositionService
) {
  // Create reactive state that syncs with service
  let startPositionPictographs = $state(startPositionService.startPositions);
  let selectedStartPos = $state(startPositionService.selectedPosition);
  let isLoading = $state(startPositionService.isLoading);
  let loadingError = $state(!!startPositionService.error);

  // Sync with service changes via events
  if (typeof window !== "undefined") {
    const handleServiceChange = () => {
      startPositionPictographs = startPositionService.startPositions;
      selectedStartPos = startPositionService.selectedPosition;
      isLoading = startPositionService.isLoading;
      loadingError = !!startPositionService.error;
    };

    window.addEventListener(
      "startPositionServiceStateChange",
      handleServiceChange
    );
  }

  /**
   * Load start positions - delegates to service
   */
  async function loadStartPositions(gridMode: GridMode = GridMode.DIAMOND) {
    await startPositionService.getDefaultStartPositions(gridMode);
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
  };
}
