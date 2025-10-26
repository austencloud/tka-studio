/**
 * Simplified Start Position State
 *
 * Based on the working legacy implementation - simple and effective.
 * No over-engineering, just the core functionality needed.
 */

import { GridMode, resolve, type PictographData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { IStartPositionService } from "../services/contracts";

export function createSimplifiedStartPositionState() {
  // Lazy service resolution to avoid effect_orphan error
  let startPositionService: IStartPositionService | null = null;

  function getService(): IStartPositionService {
    if (!startPositionService) {
      startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
    }
    return startPositionService;
  }

  // Simple reactive state - just what we need
  let positions = $state<PictographData[]>([]);
  let allVariations = $state<PictographData[]>([]);
  let selectedPosition = $state<PictographData | null>(null);
  let currentGridMode = $state<GridMode>(GridMode.DIAMOND);

  // Load positions on initialization - always succeeds with hardcoded positions
  async function loadPositions() {
    // Use diamond mode by default (like legacy)
    positions = await getService().getStartPositions(GridMode.DIAMOND);
  }

  // Load all 16 start position variations for the current grid mode
  async function loadAllVariations(gridMode: GridMode = currentGridMode) {
    currentGridMode = gridMode;
    allVariations = await getService().getAllStartPositionVariations(gridMode);
  }

  // Select a position
  async function selectPosition(position: PictographData) {
    await getService().selectStartPosition(position);
    selectedPosition = position;
  }

  // Initialize on creation
  loadPositions();

  return {
    // State
    get positions() { return positions; },
    get allVariations() { return allVariations; },
    get selectedPosition() { return selectedPosition; },
    get currentGridMode() { return currentGridMode; },

    // Actions
    selectPosition,
    loadAllVariations
  };
}

export type SimplifiedStartPositionState = ReturnType<typeof createSimplifiedStartPositionState>;
