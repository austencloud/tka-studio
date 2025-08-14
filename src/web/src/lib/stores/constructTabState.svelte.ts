/**
 * ConstructTab State Management
 *
 * Centralized state management for the ConstructTab component using Svelte 5 runes.
 * This manages all the reactive state that was previously scattered throughout
 * the massive ConstructTab component.
 */

import { state as sequenceState } from "../state/sequenceState.svelte";

export type ActiveRightPanel = "build" | "generate" | "edit" | "export";
export type GridMode = "diamond" | "box";

// ============================================================================
// CORE STATE
// ============================================================================

const state = $state({
  // Main tab state
  activeRightPanel: "build" as ActiveRightPanel,
  gridMode: "diamond" as GridMode,

  // Transition and loading states
  isTransitioning: false,
  isSubTabTransitionActive: false,
  currentSubTabTransition: null as string | null,

  // Error handling
  errorMessage: null as string | null,

  // Build tab conditional logic
  shouldShowStartPositionPicker: true,
});

// ============================================================================
// EXPORTS
// ============================================================================

// Export the state for direct reactive access
export { state };

// ============================================================================
// STATE MANAGEMENT FUNCTIONS
// ============================================================================

// Method to update shouldShowStartPositionPicker - called from components
export function updateShouldShowStartPositionPicker() {
  const sequence = sequenceState.currentSequence;

  // Show start position picker if:
  // 1. No sequence exists, OR
  // 2. Sequence exists but has no start position set
  const shouldShow = !sequence || !sequence.start_position;

  // Only log if the value actually changes to reduce noise
  if (state.shouldShowStartPositionPicker !== shouldShow) {
    console.log(
      `🎯 Start position picker: ${shouldShow ? "show" : "hide"} (has start_position: ${!!sequence?.start_position}, beats: ${sequence?.beats?.length || 0})`
    );
  }

  state.shouldShowStartPositionPicker = shouldShow;
}

// State management functions
export function setActiveRightPanel(panel: ActiveRightPanel) {
  state.activeRightPanel = panel;
}

export function setGridMode(mode: GridMode) {
  state.gridMode = mode;
}

export function setTransitioning(isTransitioning: boolean) {
  state.isTransitioning = isTransitioning;
}

export function setSubTabTransition(
  isActive: boolean,
  transitionId: string | null = null
) {
  state.isSubTabTransitionActive = isActive;
  state.currentSubTabTransition = transitionId;
}

export function setError(message: string | null) {
  state.errorMessage = message;
}

export function clearError() {
  state.errorMessage = null;
}

// ============================================================================
// DERIVED STATE GETTERS
// ============================================================================

export function getCurrentSequence() {
  return sequenceState.currentSequence;
}

export function getHasError() {
  return state.errorMessage !== null;
}

export function getIsInBuildMode() {
  return state.activeRightPanel === "build";
}

export function getIsInGenerateMode() {
  return state.activeRightPanel === "generate";
}

export function getIsInEditMode() {
  return state.activeRightPanel === "edit";
}

export function getIsInExportMode() {
  return state.activeRightPanel === "export";
}

// ============================================================================
// INITIALIZATION
// ============================================================================

// Initialize shouldShowStartPositionPicker based on current sequence
// Note: This is called during module initialization, but can be called again
// from components when needed
try {
  updateShouldShowStartPositionPicker();
} catch (error) {
  // Ignore errors during testing when mocks aren't ready
  console.warn("Failed to initialize shouldShowStartPositionPicker:", error);
}
