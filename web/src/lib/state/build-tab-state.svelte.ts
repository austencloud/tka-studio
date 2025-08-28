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
import type { ISequenceService } from "$lib/services/interfaces/sequence-interfaces";
import type { ActiveBuildSubTab } from "$lib/state/services/state-service-interfaces";
import { createSequenceState } from "./sequence-state.svelte";

/**
 * Creates master build tab state for shared concerns
 *
 * @param sequenceService - Injected sequence service
 * @returns Reactive state object with getters and state mutations
 */
export function createBuildTabState(sequenceService: ISequenceService) {
  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioningSubTab = $state(false);
  let activeSubTab = $state<ActiveBuildSubTab>("construct"); // Which sub-tab is active

  // Shared sub-states
  const sequenceState = createSequenceState(sequenceService);

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const hasError = $derived(error !== null);
  const hasSequence = $derived(sequenceState.currentSequence !== null);

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

  function setActiveRightPanel(panel: ActiveBuildSubTab) {
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
      return sequenceState;
    },

    // State mutations
    setLoading,
    setTransitioning: setTransitioningSubTab,
    setError,
    clearError,
    setActiveRightPanel,
  };
}
