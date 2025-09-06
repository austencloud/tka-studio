/**
 * Build Tab State - Master Tab State
 *
 * Manages shared state for the Build tab (master tab).
 * Handles concerns that are shared across all sub-tabs (Construct, Generate, Edit, Export).
 *
 * ✅ All runes ($state, $derived, $effect) live here
 * ✅ Pure reactive wrappers - no business logic
 * ✅ Services injected via parameters
 * ✅ Component-scoped state (not global singleton)
 */

// Import required state factories
import type { ActiveBuildTab } from "$shared/domain";
// import type { ISequenceService } from "../services/contracts";
// import { createSequenceState } from "./workbench/sequence-state.svelte";

/**
 * Creates master build tab state for shared concerns
 *
 * @param sequenceService - Injected sequence service
 * @returns Reactive state object with getters and state mutations
 */
export function createBuildTabState(sequenceService: any) {
  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioningSubTab = $state(false);
  let activeSubTab = $state<ActiveBuildTab>("construct"); // Which sub-tab is active

  // Shared sub-states
  // const sequenceState = createSequenceState({ sequenceService });

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const hasError = $derived(error !== null);
  const hasSequence = $derived(false); // sequenceState.currentSequence !== null

  // ============================================================================
  // STATE MUTATIONS
  // ============================================================================

  function setLoading(loading: boolean) {
    isLoading = loading;
  }

  function setTransitioningSubTab(transitioning: boolean) {
    isTransitioningSubTab = transitioning;
  }

  function setError(errorMessage: string | null) {
    error = errorMessage;
  }

  function clearError() {
    error = null;
  }

  function setActiveRightPanel(panel: ActiveBuildTab) {
    activeSubTab = panel;
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // Readonly state access
    get isLoading() {
      return isLoading;
    },
    get error() {
      return error;
    },
    get isTransitioning() {
      return isTransitioningSubTab;
    },
    get hasError() {
      return hasError;
    },
    get hasSequence() {
      return hasSequence;
    },
    get activeSubTab() {
      return activeSubTab;
    },

    // Sub-states
    get sequenceState() {
      return null; // sequenceState
    },

    // State mutations
    setLoading,
    setTransitioning: setTransitioningSubTab,
    setError,
    clearError,
    setActiveRightPanel,
  };
}
