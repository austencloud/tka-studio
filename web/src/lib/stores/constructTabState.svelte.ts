/**
 * Legacy Compatibility Wrapper for ConstructTabState
 *
 * This file provides backward compatibility for components that still import
 * from the old stores location. It re-exports the new factory-based state.
 */

// Re-export types
export type {
  ActiveRightPanel,
  GridMode,
} from "$lib/state/construct-tab-state.svelte";

// For legacy compatibility, create a simple global state instance
// This is a temporary solution during migration
import { createConstructTabState } from "$lib/state/construct-tab-state.svelte";

// Create a mock sequence state for legacy compatibility
const mockSequenceState = {
  currentSequence: null,
};

// Create global instance for legacy compatibility
const legacyConstructTabState = createConstructTabState(mockSequenceState);

// Export individual functions for legacy compatibility
export const state = {
  get activeRightPanel() {
    return legacyConstructTabState.activeRightPanel;
  },
  get gridMode() {
    return legacyConstructTabState.gridMode;
  },
  get isTransitioning() {
    return legacyConstructTabState.isTransitioning;
  },
  get isSubTabTransitionActive() {
    return legacyConstructTabState.isSubTabTransitionActive;
  },
  get currentSubTabTransition() {
    return legacyConstructTabState.currentSubTabTransition;
  },
  get errorMessage() {
    return legacyConstructTabState.errorMessage;
  },
  get shouldShowStartPositionPicker() {
    return legacyConstructTabState.shouldShowStartPositionPicker;
  },

  // Setters for legacy compatibility
  set activeRightPanel(value) {
    legacyConstructTabState.setActiveRightPanel(value);
  },
  set gridMode(value) {
    legacyConstructTabState.setGridMode(value);
  },
  set isTransitioning(value) {
    legacyConstructTabState.setTransitioning(value);
  },
  set isSubTabTransitionActive(value) {
    /* No-op for legacy compatibility */
  },
  set currentSubTabTransition(value) {
    /* No-op for legacy compatibility */
  },
  set errorMessage(value) {
    value
      ? legacyConstructTabState.setError(value)
      : legacyConstructTabState.clearError();
  },
};

export const setActiveRightPanel = legacyConstructTabState.setActiveRightPanel;
export const setGridMode = legacyConstructTabState.setGridMode;
export const setError = legacyConstructTabState.setError;
export const clearError = legacyConstructTabState.clearError;
export const updateShouldShowStartPositionPicker =
  legacyConstructTabState.updateShouldShowStartPositionPicker;
export const getCurrentSequence = legacyConstructTabState.getCurrentSequence;
export const getHasError = legacyConstructTabState.getHasError;
export const getIsInBuildMode = legacyConstructTabState.getIsInBuildMode;
