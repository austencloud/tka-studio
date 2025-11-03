/**
 * Create Module State - Master Tab State
 *
 * Manages shared state for the Create module.
 * Handles concerns that are shared across all tabs (Construct, Generate, Edit, Export).
 *
 * ✅ All runes ($state, $derived, $effect) live here
 * ✅ Pure reactive wrappers - no business logic
 * ✅ Services injected via parameters
 * ✅ Component-scoped state (not global singleton)
 */

// Import required state factories
import type { BuildModeId, BeatData, SequenceData } from "$shared";
import { resolve, TYPES } from "$shared";
import { navigationState } from "$shared/navigation/state/navigation-state.svelte";
import type { ISequencePersistenceService, ISequenceService } from "../services/contracts";
import type { ISequenceStatisticsService } from "../services/contracts/ISequenceStatisticsService";
import type { ISequenceTransformationService } from "../services/contracts/ISequenceTransformationService";
import type { ISequenceValidationService } from "../services/contracts/ISequenceValidationService";
import type { IUndoService, UndoMetadata } from "../services/contracts/IUndoService";
import { UndoOperationType } from "../services/contracts/IUndoService";
import { createSequenceState } from "./SequenceStateOrchestrator.svelte";
import { createHandPathCoordinator } from "./hand-path-coordinator.svelte";

/**
 * Navigation history entry for tracking panel navigation
 */
type NavigationHistoryEntry = {
  panel: BuildModeId;
  timestamp: number;
};

/**
 * Option selection history entry for tracking beat additions
 */
type OptionSelectionHistoryEntry = {
  beatIndex: number;
  beatData: BeatData;
  timestamp: number;
};

/**
 * Creates master Create Module State for shared concerns
 *
 * @param sequenceService - Injected sequence service
 * @param sequencePersistenceService - Injected persistence service
 * @returns Reactive state object with getters and state mutations
 */
export function createCreateModuleState(
  sequenceService: ISequenceService,
  sequencePersistenceService?: ISequencePersistenceService
) {
  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioningSection = $state(false);
  let activeSection = $state<BuildModeId | null>(null); // Start with null to prevent flicker during restoration
  let isPersistenceInitialized = $state(false); // Track if persistence has been loaded
  let isNavigatingBack = $state(false); // Track if currently in back navigation to prevent sync loops

  // Track the last content tab (Generate or Construct) before going to Animate
  let lastContentTab = $state<'generate' | 'construct'>('construct'); // Default to construct

  // Navigation history tracking
  let navigationHistory = $state<NavigationHistoryEntry[]>([]);
  const MAX_HISTORY = 10;

  // Option selection history tracking
  let optionSelectionHistory = $state<OptionSelectionHistoryEntry[]>([]);
  const MAX_OPTION_HISTORY = 50; // Allow tracking up to 50 option selections

  // Flag to prevent sync loop when updating from toggle
  let isUpdatingFromToggle = $state(false);

  // Undo service - professional undo/redo management
  const undoService = resolve<IUndoService>(TYPES.IUndoService);

  // Reactive wrapper for undo service state
  // We use a counter that increments on each change to trigger reactivity
  let undoChangeCounter = $state(0);

  // Subscribe to undo service changes (no $effect needed - this is called from component context)
  undoService.onChange(() => {
    undoChangeCounter++;
  });

  // Callback for showing start position picker (set by construct tab state)
  let showStartPositionPickerCallback: (() => void) | null = null;

  // Callback for triggering undo option animation (set by ToolPanel)
  let onUndoingOptionCallback: ((isUndoing: boolean) => void) | null = null;

  // Callback for confirming switch to Guided mode (returns promise resolving to boolean)
  let confirmGuidedSwitchCallback: (() => Promise<boolean>) | null = null;

  // Callback for clearing sequence completely (set by construct tab state)
  let clearSequenceCompletelyCallback: (() => Promise<void>) | null = null;

  // Shared sub-states
  const sequenceState = createSequenceState({
    sequenceService,
    sequencePersistenceService: sequencePersistenceService!,
    sequenceStatisticsService: resolve(TYPES.ISequenceStatisticsService) as ISequenceStatisticsService,
    sequenceTransformationService: resolve(TYPES.ISequenceTransformationService) as ISequenceTransformationService,
    sequenceValidationService: resolve(TYPES.ISequenceValidationService) as ISequenceValidationService,
  });

  // Hand Path Coordinator for gestural path building
  const handPathCoordinator = createHandPathCoordinator();

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const hasError = $derived(error !== null);
  const hasSequence = $derived(sequenceState.currentSequence !== null);
  const isSectionLoading = $derived(activeSection === null); // Loading state detection like main navigation
  const canGoBack = $derived(navigationHistory.length > 0);
  const hasOptionHistory = $derived(optionSelectionHistory.length > 0);

  // Tab accessibility - Edit and Export tabs require a start position to be selected
  const canAccessEditTab = $derived(sequenceState.hasStartPosition);
  const canAccessExportTab = $derived(sequenceState.hasStartPosition);

  // ============================================================================
  // STATE MUTATIONS
  // ============================================================================

  function setLoading(loading: boolean) {
    isLoading = loading;
  }

  function setTransitioningSection(transitioning: boolean) {
    isTransitioningSection = transitioning;
  }

  function setError(errorMessage: string | null) {
    error = errorMessage;
  }

  function clearError() {
    error = null;
  }

  async function setactiveToolPanel(panel: BuildModeId) {
    // Check if switching to Guided mode with existing sequence
    if (panel === 'guided' && sequenceState.currentSequence && sequenceState.currentSequence.beats.length > 0) {
      // Ask for confirmation via callback
      if (confirmGuidedSwitchCallback) {
        const confirmed = await confirmGuidedSwitchCallback();
        if (!confirmed) {
          // User cancelled - don't switch
          return;
        }
        // User confirmed - clear sequence before switching
        // Use the construct tab state's clearSequenceCompletely to ensure UI state is updated
        if (clearSequenceCompletelyCallback) {
          await clearSequenceCompletelyCallback();
        } else {
          // Fallback to direct sequence state clear if callback not available
          sequenceState.clearSequenceCompletely();
        }
      }
    }

    // Set flag to prevent sync loop
    isUpdatingFromToggle = true;
    setactiveToolPanelInternal(panel, true);
    // Also sync to navigation state directly
    navigationState.setCurrentSection(panel);
    // Reset flag after a microtask to allow sync effects to see the updated state
    setTimeout(() => {
      isUpdatingFromToggle = false;
    }, 0);
  }

  /**
   * Internal method to set active panel with optional history tracking
   * @param panel - The panel to activate
   * @param addToHistory - Whether to add this navigation to history
   */
  function setactiveToolPanelInternal(panel: BuildModeId, addToHistory: boolean = true) {
    console.log("🔄 createModuleState.setactiveToolPanelInternal called with:", { panel, currentActiveSection: activeSection });

    // Track the last content tab (generate or construct) BEFORE navigating away from it
    if ((activeSection === 'generate' || activeSection === 'construct') && activeSection !== panel) {
      lastContentTab = activeSection;
    }

    // Add to navigation history if it's different from current AND we should track history
    if (addToHistory && activeSection !== panel && activeSection !== null) {
      navigationHistory.push({
        panel: activeSection,
        timestamp: Date.now(),
      });

      // Keep only last MAX_HISTORY entries
      if (navigationHistory.length > MAX_HISTORY) {
        navigationHistory.shift();
      }
    }

    activeSection = panel;
    console.log("✅ createModuleState.activeSection updated to:", activeSection);
    // Save the active tab to persistence
    saveCurrentState();
  }

  function goBack() {
    if (navigationHistory.length > 0) {
      // Get the previous entry
      const previous = navigationHistory.pop();
      if (previous) {
        // Set flag to prevent sync loop
        isNavigatingBack = true;
        // Set without adding to history (using internal method)
        setactiveToolPanelInternal(previous.panel, false);
        // Reset flag after state settles
        setTimeout(() => {
          isNavigatingBack = false;
        }, 0);
      }
    }
  }

  // ============================================================================
  // OPTION SELECTION HISTORY MANAGEMENT
  // ============================================================================

  function addOptionToHistory(beatIndex: number, beatData: BeatData) {
    optionSelectionHistory.push({
      beatIndex,
      beatData,
      timestamp: Date.now(),
    });

    // Keep only last MAX_OPTION_HISTORY entries
    if (optionSelectionHistory.length > MAX_OPTION_HISTORY) {
      optionSelectionHistory.shift();
    }
  }

  function popLastOptionFromHistory(): OptionSelectionHistoryEntry | null {
    const lastEntry = optionSelectionHistory.pop();
    return lastEntry || null;
  }

  function clearOptionHistory() {
    optionSelectionHistory = [];
  }

  function rebuildOptionHistoryFromSequence() {
    if (!sequenceState.currentSequence) {
      return;
    }

    // Clear existing history
    optionSelectionHistory = [];

    // Build history from sequence beats (excluding start position at index 0)
    const beats = sequenceState.currentSequence.beats;
    for (let i = 1; i < beats.length; i++) {
      const beat = beats[i]!;
      optionSelectionHistory.push({
        beatIndex: i,
        beatData: beat,
        timestamp: Date.now() - (beats.length - i) * 1000, // Simulate chronological timestamps
      });
    }
  }

  // ============================================================================
  // UNDO HISTORY MANAGEMENT
  // ============================================================================

  /**
   * Push a snapshot of the current sequence state before a destructive operation
   * OPTIMIZED: Defers expensive deep copy to microtask to avoid blocking UI
   */
  function pushUndoSnapshot(
    type: 'REMOVE_BEATS' | 'CLEAR_SEQUENCE' | 'ADD_BEAT' | 'SELECT_START_POSITION',
    metadata?: UndoMetadata
  ) {
    // For start position selection, allow null sequence
    // For other operations, require a sequence
    if (!sequenceState.currentSequence && type !== 'SELECT_START_POSITION') {
      return;
    }

    // Map old type strings to new UndoOperationType enum
    const operationType = type === 'SELECT_START_POSITION' ? UndoOperationType.SELECT_START_POSITION :
                          type === 'ADD_BEAT' ? UndoOperationType.ADD_BEAT :
                          type === 'REMOVE_BEATS' ? UndoOperationType.REMOVE_BEATS :
                          UndoOperationType.CLEAR_SEQUENCE;

    // 🚀 PERFORMANCE OPTIMIZATION: Capture references immediately, defer deep copy
    // This prevents blocking the main thread during beat addition
    const currentSequenceRef = sequenceState.currentSequence;
    const selectedBeatNumberRef = sequenceState.selectedBeatNumber;
    const activeSectionRef = activeSection;
    const timestampRef = Date.now();

    // Defer the expensive deep copy operation to a microtask
    // This allows the UI to update immediately while we snapshot in the background
    queueMicrotask(() => {
      // Create a deep copy of the sequence to preserve state (if it exists)
      const sequenceCopy: SequenceData | null = currentSequenceRef ? {
        ...currentSequenceRef,
        beats: [...currentSequenceRef.beats.map(beat => ({ ...beat }))]
      } : null;

      // Create state snapshot
      const beforeState = {
        sequence: sequenceCopy,
        selectedBeatNumber: selectedBeatNumberRef,
        activeSection: activeSectionRef,
        shouldShowStartPositionPicker: type === 'SELECT_START_POSITION' ? true : false,
        timestamp: timestampRef
      };

      // Push to undo service
      undoService.pushUndo(operationType, beforeState, metadata);
    });
  }

  /**
   * Undo the last destructive operation with fade-out animation
   */
  function undo() {
    const lastEntry = undoService.undo();
    if (!lastEntry) {
      return false;
    }

    // Special handling for start position selection undo
    if (lastEntry.type === UndoOperationType.SELECT_START_POSITION) {
      // Clear the sequence completely
      sequenceState.clearSequenceCompletely();

      // Show the start position picker again (if callback is set)
      if (showStartPositionPickerCallback) {
        showStartPositionPickerCallback();
      }

      return true;
    }

    // Determine which beats need to be animated out
    const currentSequence = sequenceState.currentSequence;
    const restoredSequence = lastEntry.beforeState.sequence;

    if (currentSequence && restoredSequence) {
      const currentBeatCount = currentSequence.beats.length;
      const restoredBeatCount = restoredSequence.beats.length;

      // If beats are being removed, animate them out
      if (currentBeatCount > restoredBeatCount) {
        const beatsToRemove: number[] = [];

        // Collect indices of beats that will be removed
        for (let i = restoredBeatCount; i < currentBeatCount; i++) {
          beatsToRemove.push(i);
        }

        // Trigger fade-out animation for beats being removed
        sequenceState.animationState.startRemovingBeats(beatsToRemove);

        // Trigger option picker fade animation if callback is set
        if (onUndoingOptionCallback) {
          onUndoingOptionCallback(true);
        }

        // Wait for animation to complete, then restore sequence
        const fadeAnimationDuration = 250; // Match fadeOutDisintegrate animation
        setTimeout(() => {
          // Restore the sequence state
          sequenceState.setCurrentSequence(restoredSequence);

          // Clear animation state
          sequenceState.animationState.endRemovingBeats();

          // End option picker fade animation
          if (onUndoingOptionCallback) {
            onUndoingOptionCallback(false);
          }

          // Restore the selection
          if (lastEntry.beforeState.selectedBeatNumber !== null) {
            sequenceState.selectBeat(lastEntry.beforeState.selectedBeatNumber);
          } else {
            sequenceState.clearSelection();
          }

          // Restore the active tab
          if (lastEntry.beforeState.activeSection !== null) {
            setactiveToolPanelInternal(lastEntry.beforeState.activeSection, false);
          }
        }, fadeAnimationDuration);

        return true;
      }
    }

    // No animation needed - restore immediately
    sequenceState.setCurrentSequence(restoredSequence);

    // Restore the selection
    if (lastEntry.beforeState.selectedBeatNumber !== null) {
      sequenceState.selectBeat(lastEntry.beforeState.selectedBeatNumber);
    } else {
      sequenceState.clearSelection();
    }

    // Restore the active tab (important for clear sequence undo)
    if (lastEntry.beforeState.activeSection !== null) {
      setactiveToolPanelInternal(lastEntry.beforeState.activeSection, false);  // Don't add to navigation history
    }

    return true;
  }

  /**
   * Clear all undo history
   */
  function clearUndoHistory() {
    undoService.clearHistory();
  }

  /**
   * Set callback for showing start position picker (called by construct tab state)
   */
  function setShowStartPositionPickerCallback(callback: () => void) {
    showStartPositionPickerCallback = callback;
  }

  /**
   * Set callback for triggering undo option animation (called by ToolPanel)
   */
  function setOnUndoingOptionCallback(callback: (isUndoing: boolean) => void) {
    onUndoingOptionCallback = callback;
  }

  /**
   * Set callback for confirming switch to Guided mode (called by CreateModule)
   */
  function setConfirmGuidedSwitchCallback(callback: () => Promise<boolean>) {
    confirmGuidedSwitchCallback = callback;
  }

  /**
   * Set callback for clearing sequence completely (called by CreateModule)
   */
  function setClearSequenceCompletelyCallback(callback: () => Promise<void>) {
    clearSequenceCompletelyCallback = callback;
  }

  // ============================================================================
  // PERSISTENCE FUNCTIONS
  // ============================================================================

  async function initializeWithPersistence(): Promise<void> {
    try {
      // Initialize sequence state first
      await sequenceState.initializeWithPersistence();

      // Initialize hand path coordinator services
      handPathCoordinator.initializeServices();

      // Load saved Create Module State using the sequence persistence service
      if (sequencePersistenceService) {
        const savedState = await sequencePersistenceService.loadCurrentState();
        if (savedState?.activeBuildSection) {
          activeSection = savedState.activeBuildSection;
        } else {
          // Set default tab when no saved state is found
          activeSection = "construct";
        }
      } else {
        // Set default tab when no persistence service is available
        activeSection = "construct";
      }

      // Rebuild option history from persisted sequence
      rebuildOptionHistoryFromSequence();

      // Load undo history from undo service
      await undoService.loadHistory();

      isPersistenceInitialized = true;
    } catch (error) {
      console.error("❌ CreateModuleState: Failed to initialize persistence:", error);
      isPersistenceInitialized = true; // Still mark as initialized to prevent blocking
    }
  }

  async function saveCurrentState(): Promise<void> {
    if (!isPersistenceInitialized) return;

    try {
      if (activeSection) {
        await sequenceState.saveCurrentState(activeSection);
      }
    } catch (error) {
      console.error("❌ CreateModuleState: Failed to save current state:", error);
    }
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
      return isTransitioningSection;
    },
    get hasError() {
      return hasError;
    },
    get hasSequence() {
      return hasSequence;
    },
    get activeSection() {
      return activeSection;
    },
    get lastContentTab() {
      return lastContentTab;
    },
    get isPersistenceInitialized() {
      return isPersistenceInitialized;
    },
    get isSectionLoading() {
      return isSectionLoading;
    },
    get canGoBack() {
      return canGoBack;
    },
    get isNavigatingBack() {
      return isNavigatingBack;
    },
    get isUpdatingFromToggle() {
      return isUpdatingFromToggle;
    },
    get hasOptionHistory() {
      return hasOptionHistory;
    },
    get canUndo() {
      // Access counter to create reactive dependency
      // Just reading the variable creates the dependency
      void undoChangeCounter;
      return undoService.canUndo;
    },
    get canRedo() {
      // Access counter to create reactive dependency
      // Just reading the variable creates the dependency
      void undoChangeCounter;
      return undoService.canRedo;
    },
    get undoHistory() {
      return undoService.undoHistory;
    },
    get canAccessEditTab() {
      return canAccessEditTab;
    },
    get canAccessExportTab() {
      return canAccessExportTab;
    },
    get navigationHistory() {
      return navigationHistory;
    },

    // Sub-states
    get sequenceState() {
      return sequenceState;
    },
    get handPathCoordinator() {
      return handPathCoordinator;
    },

    // State mutations
    setLoading,
    setTransitioning: setTransitioningSection,
    setError,
    clearError,
    setactiveToolPanel,
    setactiveToolPanelInternal, // Internal method for sync effects
    goBack,

    // Option history management
    addOptionToHistory,
    popLastOptionFromHistory,
    clearOptionHistory,
    rebuildOptionHistoryFromSequence,

    // Undo history management
    pushUndoSnapshot,
    undo,
    clearUndoHistory,
    setShowStartPositionPickerCallback,
    setOnUndoingOptionCallback,
    setConfirmGuidedSwitchCallback,
    setClearSequenceCompletelyCallback,

    // Persistence functions
    initializeWithPersistence,
    saveCurrentState,
  };
}
