/**
 * Construct Tab State - Sub-tab State
 *
 * Manages state specific to the Construct sub-tab functionality.
 * Handles start position selection, option picking, and construct-specific UI state.
 *
 * ✅ All construct-specific runes ($state, $derived, $effect) live here
 * ✅ Pure reactive wrappers - no business logic
 * ✅ Services injected via parameters
 * ✅ Component-scoped state (not global singleton)
 */

import { GridMode } from "$lib/domain";
import type { IBuildTabService } from "$lib/services/interfaces/IBuildTabService";
import type { IStartPositionService } from "$lib/services/interfaces/IStartPositionService";
import type { PictographData } from "$lib/domain/PictographData";

/**
 * Creates construct tab state for construct-specific concerns
 *
 * @param buildTabService - Injected build tab service for business logic
 * @param startPositionService - Injected start position service
 * @returns Reactive state object with getters and state mutations
 */
export function createConstructTabState(
  buildTabService: IBuildTabService,
  startPositionService: IStartPositionService
) {
  // ============================================================================
  // REACTIVE STATE (Construct-specific)
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioning = $state(false);
  let showStartPositionPicker = $state(true);
  let selectedStartPosition = $state<PictographData | null>(null);

  // Sub-states (construct-specific)
  const startPositionStateService =
    createStartPositionPickerState(startPositionService);

  // ============================================================================
  // DERIVED STATE (Construct-specific derived state)
  // ============================================================================

  const hasError = $derived(error !== null);
  const canSelectOptions = $derived(selectedStartPosition !== null);
  const shouldShowStartPositionPicker = $derived(() => showStartPositionPicker);

  // ============================================================================
  // EFFECTS (Construct-specific effects)
  // ============================================================================

  // Load start positions when construct tab is initialized - using onMount to prevent infinite loops
  let startPositionsLoaded = $state(false);
  let coordinationSetup = $state(false);

  // Initialize construct tab - called from component onMount
  function initializeConstructTab() {
    if (!startPositionsLoaded) {
      console.log("🚀 Loading start positions...");
      startPositionStateService.loadStartPositions(GridMode.DIAMOND);
      startPositionsLoaded = true;
      console.log("✅ Start positions loaded flag set");
    }

    if (!coordinationSetup) {
      console.log("🚀 Initializing build tab service...");
      buildTabService.initialize();
      coordinationSetup = true;
      console.log("✅ Coordination setup flag set");
    }
  }

  // ============================================================================
  // STATE MUTATIONS (Construct-specific state updates)
  // ============================================================================

  function setLoading(loading: boolean) {
    isLoading = loading;
  }

  function setTransitioning(transitioning: boolean) {
    isTransitioning = transitioning;
  }

  function setError(errorMessage: string | null) {
    error = errorMessage;
  }

  function clearError() {
    error = null;
  }

  function setShowStartPositionPicker(show: boolean) {
    showStartPositionPicker = show;
  }

  function setSelectedStartPosition(position: PictographData | null) {
    selectedStartPosition = position;
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
      return isTransitioning;
    },
    get hasError() {
      return hasError;
    },
    get canSelectOptions() {
      return canSelectOptions;
    },
    get showStartPositionPicker() {
      return showStartPositionPicker;
    },
    get shouldShowStartPositionPicker() {
      return shouldShowStartPositionPicker;
    },
    get selectedStartPosition() {
      return selectedStartPosition;
    },

    // Sub-states
    get startPositionStateService() {
      return startPositionStateService;
    },

    // State mutations
    setLoading,
    setTransitioning,
    setError,
    clearError,
    setShowStartPositionPicker,
    setSelectedStartPosition,

    // Initialization
    initializeConstructTab,
  };
}

// Import required state factories
import { createStartPositionPickerState } from "./start-position-state.svelte";
