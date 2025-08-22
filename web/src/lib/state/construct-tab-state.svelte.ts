/**
 * ConstructTab State Factory - Component-Scoped State for Svelte 5 Runes
 *
 * Creates component-scoped state management for ConstructTab component.
 * Takes sequence state as dependency instead of importing global state.
 */

import type { SequenceData } from "$lib/domain";

import { GridMode } from "$lib/domain";

export type ActiveRightPanel = "build" | "generate" | "edit" | "export";

// Type for sequence state dependency
interface SequenceStateType {
  currentSequence: SequenceData | null;
}

// ============================================================================
// FACTORY FUNCTION
// ============================================================================

export function createConstructTabState(sequenceState: SequenceStateType) {
  // ============================================================================
  // COMPONENT-SCOPED STATE
  // ============================================================================

  const state = $state({
    // Main tab state
    activeRightPanel: "build" as ActiveRightPanel,
    gridMode: GridMode.DIAMOND as GridMode,

    // Transition and loading states
    isTransitioning: false,
    isSubTabTransitionActive: false,
    currentSubTabTransition: null as string | null,

    // Error handling
    errorMessage: null as string | null,
  });

  // ============================================================================
  // STATE MANAGEMENT FUNCTIONS
  // ============================================================================

  // REACTIVE: Automatically update shouldShowStartPositionPicker when sequence changes
  const shouldShowStartPositionPicker = $derived(() => {
    const sequence = sequenceState.currentSequence;

    // Show start position picker if:
    // 1. No sequence exists, OR
    // 2. Sequence exists but has no start position set
    const shouldShow = !sequence || !sequence.startingPositionBeat;

    console.log(
      `🎯 [CONSTRUCT-TAB-STATE] Start position picker: ${shouldShow ? "SHOW" : "HIDE"}`,
      {
        sequenceExists: !!sequence,
        sequenceId: sequence?.id,
        hasStartPosition: !!sequence?.startingPositionBeat,
        startPositionId: sequence?.startingPositionBeat?.pictographData?.id,
        beatCount: sequence?.beats?.length || 0,
        shouldShow,
      }
    );

    return shouldShow;
  });

  // Method to manually trigger update (for backward compatibility)
  function updateShouldShowStartPositionPicker() {
    // This is now handled automatically by the derived state above
    // But we keep this method for any components that might call it
  }

  // State management functions
  function setActiveRightPanel(panel: ActiveRightPanel) {
    state.activeRightPanel = panel;
  }

  function setGridMode(mode: GridMode) {
    state.gridMode = mode;
  }

  function setTransitioning(isTransitioning: boolean) {
    state.isTransitioning = isTransitioning;
  }

  function setSubTabTransition(
    isActive: boolean,
    transitionId: string | null = null
  ) {
    state.isSubTabTransitionActive = isActive;
    state.currentSubTabTransition = transitionId;
  }

  function setError(message: string | null) {
    state.errorMessage = message;
  }

  function clearError() {
    state.errorMessage = null;
  }

  // ============================================================================
  // DERIVED STATE GETTERS
  // ============================================================================

  function getCurrentSequence() {
    return sequenceState.currentSequence;
  }

  function getHasError() {
    return state.errorMessage !== null;
  }

  function getIsInBuildMode() {
    return state.activeRightPanel === "build";
  }

  function getIsInGenerateMode() {
    return state.activeRightPanel === "generate";
  }

  function getIsInEditMode() {
    return state.activeRightPanel === "edit";
  }

  function getIsInExportMode() {
    return state.activeRightPanel === "export";
  }

  // shouldShowStartPositionPicker is now automatically reactive via $derived

  // ============================================================================
  // RETURN STATE OBJECT
  // ============================================================================

  return {
    // State access (reactive)
    get activeRightPanel() {
      return state.activeRightPanel;
    },
    get gridMode() {
      return state.gridMode;
    },
    get isTransitioning() {
      return state.isTransitioning;
    },
    get isSubTabTransitionActive() {
      return state.isSubTabTransitionActive;
    },
    get currentSubTabTransition() {
      return state.currentSubTabTransition;
    },
    get errorMessage() {
      return state.errorMessage;
    },
    get shouldShowStartPositionPicker() {
      return shouldShowStartPositionPicker;
    },

    // Actions
    updateShouldShowStartPositionPicker,
    setActiveRightPanel,
    setGridMode,
    setTransitioning,
    setSubTabTransition,
    setError,
    clearError,

    // Getters
    getCurrentSequence,
    getHasError,
    getIsInBuildMode,
    getIsInGenerateMode,
    getIsInEditMode,
    getIsInExportMode,
  };
}
