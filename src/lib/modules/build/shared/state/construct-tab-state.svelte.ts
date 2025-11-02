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

import type { PictographData } from "../../../../shared";
import { createHMRState } from "../../../../shared/utils/hmr-state-backup";
import { createSimplifiedStartPositionState } from "../../construct/start-position-picker/state/start-position-state.svelte";
import type { BeatData } from "../domain/models/BeatData";
import type { IBuildTabService, ISequencePersistenceService } from "../services/contracts";

/**
 * Creates construct tab state for construct-specific concerns
 *
 * @param buildTabService - Injected build tab service for business logic
 * @param sequenceState - Sequence state for updating workbench
 * @param sequencePersistenceService - Persistence service for state survival
 * @param buildTabState - Build tab state for accessing navigation history
 * @param navigationState - Navigation state for syncing tab navigation
 * @returns Reactive state object with getters and state mutations
 */
export function createConstructTabState(
  buildTabService: IBuildTabService,
  sequenceState?: any, // TODO: Type this properly
  sequencePersistenceService?: ISequencePersistenceService,
  buildTabState?: any, // TODO: Type this properly - for accessing lastContentTab
  navigationState?: any // TODO: Type this properly - for updating navigation
) {
  // ============================================================================
  // HMR STATE BACKUP
  // ============================================================================

  // Create HMR backup for critical state - temporarily disabled to debug effect_orphan error
  const hmrBackup = {
    initialValue: {
      showStartPositionPicker: null as boolean | null,
      selectedStartPosition: null as PictographData | null,
      isInitialized: false
    }
  };

  // ============================================================================
  // REACTIVE STATE (Construct-specific)
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioning = $state(false);
  let showStartPositionPicker = $state<boolean | null>(hmrBackup.initialValue.showStartPositionPicker);
  let selectedStartPosition = $state<PictographData | null>(hmrBackup.initialValue.selectedStartPosition);
  let isInitialized = $state(hmrBackup.initialValue.isInitialized);
  let isContinuousOnly = $state(false); // Filter state for option viewer

  // Sub-states (construct-specific)
  // Start position state service using proper simplified state
  const startPositionStateService = createSimplifiedStartPositionState();
  let unsubscribeStartPositionListener: (() => void) | null = null;

  // Event handler function for start position selection (reactive listener compatible)
  function handleStartPositionSelected(
    pictographData: PictographData | null,
    source: "user" | "sync" = "user"
  ) {
    if (!pictographData) {
      setSelectedStartPosition(null);
      if (sequenceState) {
        sequenceState.setSelectedStartPosition(null);
      }
      if (source === "user") {
        setShowStartPositionPicker(true);
      }
      return;
    }

    if (source === "user" && buildTabState && buildTabState.pushUndoSnapshot) {
      buildTabState.pushUndoSnapshot('SELECT_START_POSITION', {
        description: 'Select start position'
      });
    }

    setShowStartPositionPicker(false);
    setSelectedStartPosition(pictographData);

    if (sequenceState) {
      sequenceState.setSelectedStartPosition(pictographData);
    }

    if (source !== "user" || !sequenceState) {
      return;
    }

    console.log("?? ConstructTabState: Creating new sequence with start position");

    const beatData: BeatData = {
      ...pictographData,
      id: `beat-${Date.now()}`,
      beatNumber: 0,
      duration: 1000,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    };

    sequenceState.createSequence({
      name: `Sequence ${new Date().toLocaleTimeString()}`,
      length: 0
    }).then((newSequence: any) => {
      if (newSequence) {
        sequenceState.setCurrentSequence(newSequence);
        try {
          sequenceState.setStartPosition(beatData);
        } catch (error) {
          console.error("? ConstructTabState: Error setting start position:", error);
        }
      } else {
        console.error("? ConstructTabState: Failed to create new sequence");
      }
    }).catch((error: any) => {
      console.error("? ConstructTabState: Error creating sequence:", error);
    });
  }
  // ============================================================================
  // DERIVED STATE (Construct-specific derived state)
  // ============================================================================

  const hasError = $derived(error !== null);
  const canSelectOptions = $derived(selectedStartPosition !== null);
  const shouldShowStartPositionPicker = $derived(() => {
    // Don't return any state until initialization is complete
    if (!isInitialized) return null;
    return showStartPositionPicker;
  });
  const isPickerStateLoading = $derived(!isInitialized || showStartPositionPicker === null); // Loading state detection like main navigation

  // ============================================================================
  // EFFECTS (Construct-specific effects)
  // ============================================================================

  // NOTE: $effect has been removed from the factory function to prevent effect_orphan error
  // The sync logic is now handled in the initializeConstructTab function
  // This is necessary because factory functions called after async operations lose Svelte context

  // Load start positions when construct tab is initialized - using onMount to prevent infinite loops
  let startPositionsLoaded = $state(false);
  let coordinationSetup = $state(false);

  // Initialize construct tab - called from component onMount
  async function initializeConstructTab() {
    if (!startPositionsLoaded) {
      // Start positions are loaded automatically on state creation
      startPositionsLoaded = true;
    }

    if (!coordinationSetup) {
      buildTabService.initialize();
      coordinationSetup = true;
    }

    if (!unsubscribeStartPositionListener && startPositionStateService.onSelectedPositionChange) {
      unsubscribeStartPositionListener = startPositionStateService.onSelectedPositionChange((position, source) => {
        handleStartPositionSelected(position, source);
      });
    }


    // Register callback with build tab state for undo functionality
    if (buildTabState && buildTabState.setShowStartPositionPickerCallback) {
      buildTabState.setShowStartPositionPickerCallback(() => {
        setShowStartPositionPicker(true);
      });
    }

    // Initialize persistence and restore state if available
    if (sequencePersistenceService && sequenceState) {
      try {
        await sequenceState.initializeWithPersistence();

        // Check if we have a persisted state that should affect UI
        const savedState = await sequencePersistenceService.loadCurrentState();
        if (savedState && savedState.hasStartPosition) {
          setShowStartPositionPicker(false);
          setSelectedStartPosition(savedState.selectedStartPosition);
          if (savedState.selectedStartPosition) {
            startPositionStateService.setSelectedPosition(savedState.selectedStartPosition);
          }
        } else {
          // No saved state, set default to show start position picker
          setShowStartPositionPicker(true);
          startPositionStateService.clearSelectedPosition();
        }
      } catch (error) {
        console.error("❌ ConstructTabState: Failed to restore persisted state:", error);
        // On error, default to showing start position picker
        setShowStartPositionPicker(true);
        startPositionStateService.clearSelectedPosition();
      }
    } else {
      // No persistence service, default to showing start position picker
      setShowStartPositionPicker(true);
      startPositionStateService.clearSelectedPosition();
    }

    // Sync picker state with sequence state's hasStartPosition (replaces $effect)
    // This logic was moved from $effect to avoid effect_orphan error
    if (sequenceState) {
      if (sequenceState.hasStartPosition && showStartPositionPicker === true) {
        console.log("🔄 ConstructTabState: Syncing picker state - hiding start position picker (hasStartPosition: true)");
        setShowStartPositionPicker(false);
      } else if (!sequenceState.hasStartPosition && showStartPositionPicker === false) {
        console.log("🔄 ConstructTabState: Syncing picker state - showing start position picker (hasStartPosition: false)");
        setShowStartPositionPicker(true);
      }
    }

    // Mark as initialized after all setup is complete
    isInitialized = true;
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

  function setShowStartPositionPicker(show: boolean | null) {
    showStartPositionPicker = show;
  }

  function setSelectedStartPosition(position: PictographData | null) {
    selectedStartPosition = position;
  }

  function setContinuousOnly(continuous: boolean) {
    isContinuousOnly = continuous;
  }

  async function clearSequenceCompletely() {
    try {
      // Start UI transition and sequence clearing simultaneously for smooth UX
      setShowStartPositionPicker(true);
      setSelectedStartPosition(null);
      startPositionStateService.clearSelectedPosition();
      clearError();

      // Capture the target tab before clearing
      const shouldNavigate = buildTabState && buildTabState.activeSection === 'animate';
      const targetTab = shouldNavigate ? buildTabState.lastContentTab : null;

      if (shouldNavigate && targetTab) {
        console.log(`🎬 ConstructTabState: Will return to ${targetTab} after clearing from Animate tab`);
      }

      // Clear sequence state asynchronously
      if (sequenceState) {
        sequenceState.clearSequenceCompletely()
          .then(() => {
            // Navigate AFTER sequence is cleared to avoid state conflicts
            if (shouldNavigate && targetTab && buildTabState && navigationState) {
              console.log(`🎬 ConstructTabState: Navigating to ${targetTab} after clear`);
              buildTabState.setactiveToolPanel(targetTab);
              // CRITICAL: Also update navigation state to prevent guard from triggering
              navigationState.setCurrentSection(targetTab);
            }
          })
          .catch((error: unknown) => {
            console.error("❌ ConstructTabState: Failed to clear sequence state:", error);
            setError(error instanceof Error ? error.message : "Failed to clear sequence");
          });
      }
    } catch (error) {
      console.error("❌ ConstructTabState: Failed to initiate sequence clear:", error);
      setError(error instanceof Error ? error.message : "Failed to clear sequence");
    }
  }

  /**
   * Restore picker state after undo - shows option picker instead of start position picker
   * Called when undoing a clear sequence operation
   */
  function restorePickerStateAfterUndo() {
    setShowStartPositionPicker(false);
    console.log("⏪ ConstructTabState: Restored picker state to show option picker");
  }

  /**
   * Sync picker state with sequence state's hasStartPosition
   * This replaces the $effect that was causing effect_orphan error
   * Call this method whenever sequence state changes that might affect picker visibility
   */
  function syncPickerStateWithSequence() {
    if (!isInitialized || !sequenceState) return;

    // When sequence state has a start position, hide the start position picker
    if (sequenceState.hasStartPosition && showStartPositionPicker === true) {
      console.log("🔄 ConstructTabState: Syncing picker state - hiding start position picker (hasStartPosition: true)");
      setShowStartPositionPicker(false);
    }

    // When sequence state loses start position, show the start position picker
    if (!sequenceState.hasStartPosition && showStartPositionPicker === false) {
      console.log("🔄 ConstructTabState: Syncing picker state - showing start position picker (hasStartPosition: false)");
      setShowStartPositionPicker(true);
    }
  }

  // ============================================================================
  // DERIVED STATE - REMOVED
  // ============================================================================

  // CONSOLIDATION: Remove duplicate sequence data management
  // The SequenceState is now the single source of truth for all sequence data
  // Components should access sequence data directly through sequenceState

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
    get isPickerStateLoading() {
      return isPickerStateLoading;
    },
    get isInitialized() {
      return isInitialized;
    },
    get selectedStartPosition() {
      return selectedStartPosition;
    },
    get isContinuousOnly() {
      return isContinuousOnly;
    },
    // CONSOLIDATION: Direct access to sequence state - no duplicate data management
    get sequenceState() {
      return sequenceState;
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
    setContinuousOnly,
    clearSequenceCompletely,
    restorePickerStateAfterUndo,
    syncPickerStateWithSequence,

    // Event handlers
    handleStartPositionSelected,

    // Initialization
    initializeConstructTab,
  };
}

// ============================================================================
// HMR STATE PERSISTENCE EFFECT
// ============================================================================

/**
 * Add this effect to any component using ConstructTabState to enable HMR backup
 * IMPORTANT: This must be called from within a component's script context, not from
 * an async callback or after a setTimeout, to avoid effect_orphan errors
 *
 * Example usage in a component:
 * ```svelte
 * <script lang="ts">
 *   import { createConstructTabState, addHMRBackupEffect } from "../state";
 *
 *   let constructTabState = createConstructTabState(...);
 *
 *   // Call this directly in component script, NOT in onMount or async context
 *   addHMRBackupEffect(constructTabState);
 * </script>
 * ```
 */
export function addHMRBackupEffect(constructTabState: ReturnType<typeof createConstructTabState>) {
  // Auto-save critical state changes for HMR persistence
  $effect(() => {
    const stateToBackup = {
      showStartPositionPicker: constructTabState.showStartPositionPicker,
      selectedStartPosition: constructTabState.selectedStartPosition,
      isInitialized: constructTabState.isInitialized
    };

    // Only save if initialized to avoid saving empty initial state
    if (constructTabState.isInitialized) {
      const hmrBackup = createHMRState('construct-tab-state', stateToBackup);
      hmrBackup.saveState(stateToBackup);
    }
  });
}

// Import required state factories
