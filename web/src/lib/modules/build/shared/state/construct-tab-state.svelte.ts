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

import { GridMode, type BeatData, type PictographData } from "$shared";
import type { IBuildTabService } from "../services/contracts";

/**
 * Creates construct tab state for construct-specific concerns
 *
 * @param buildTabService - Injected build tab service for business logic
 * @param sequenceState - Sequence state for updating workbench
 * @returns Reactive state object with getters and state mutations
 */
export function createConstructTabState(
  buildTabService: IBuildTabService,
  sequenceState?: any // TODO: Type this properly
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
  // Start position state service (placeholder for now)
  const startPositionStateService = {} as any;

  // Set up event listener for start position selection using effect
  $effect(() => {
    console.log("🔧 ConstructTabState: Setting up event listener for start-position-selected");
    if (typeof window !== "undefined") {
      const handleStartPositionSelected = async (event: CustomEvent) => {
        console.log("🎯 ConstructTabState: Start position selected, transitioning to option picker", event.detail);
        setShowStartPositionPicker(false);

        const pictographData = event.detail.startPositionData?.pictographData;
        setSelectedStartPosition(pictographData || null);

        // Update the workbench with the start position
        if (pictographData && sequenceState) {
          console.log("🔧 ConstructTabState: Creating new sequence with start position");

          // Convert PictographData to BeatData format (same as BuildTabService.selectStartPosition)
          const beatData: BeatData = {
            id: `beat-${Date.now()}`,
            beatNumber: 0,
            pictographData: pictographData,
            duration: 1000,
            blueReversal: false,
            redReversal: false,
            isBlank: false,
          };

          // Create a new sequence first (following ConstructCoordinator pattern)
          const newSequence = await sequenceState.createSequence({
            name: `Sequence ${new Date().toLocaleTimeString()}`,
            length: 0 // Start with 0 beats - beats will be added progressively
          });

          if (newSequence) {
            // Set the current sequence
            sequenceState.setCurrentSequence(newSequence);
            console.log("🔧 ConstructTabState: Current sequence set, now calling setStartPosition...");

            // Now set the start position
            try {
              console.log("🔧 ConstructTabState: About to call setStartPosition with beatData:", beatData);
              console.log("🔧 ConstructTabState: sequenceState object:", sequenceState);
              
              sequenceState.setStartPosition(beatData);
              console.log("✅ ConstructTabState: setStartPosition call completed");
              
              // Verify the start position was actually set
              const updatedSequence = sequenceState.getCurrentSequence();
              console.log("🔍 ConstructTabState: After setStartPosition, sequence is:", updatedSequence);
              console.log("🔍 ConstructTabState: After setStartPosition, startingPositionBeat:", updatedSequence?.startingPositionBeat);
              console.log("🔍 ConstructTabState: After setStartPosition, startPosition:", updatedSequence?.startPosition);
              
            } catch (error) {
              console.error("❌ ConstructTabState: Error setting start position:", error);
            }
            
            console.log("✅ ConstructTabState: New sequence created and start position set");
          } else {
            console.error("❌ ConstructTabState: Failed to create new sequence");
          }
        }
      };

      window.addEventListener("start-position-selected", handleStartPositionSelected as unknown as EventListener);
      console.log("✅ ConstructTabState: Event listener added for start-position-selected on window");

      // Cleanup function
      return () => {
        console.log("🧹 ConstructTabState: Cleaning up event listener");
        window.removeEventListener("start-position-selected", handleStartPositionSelected as unknown as EventListener);
      };
    }
  });

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
    get currentSequenceData() {
      // Convert the current sequence beats to PictographData array for the option picker
      if (sequenceState?.getCurrentSequence?.()) {
        const sequence = sequenceState.getCurrentSequence();
        console.log("🔍 ConstructTabState: sequence found:", sequence);
        
        const beats = sequence.beats || [];
        console.log("🔍 ConstructTabState: sequence.beats:", beats);
        
        // Check for start position if there are no beats yet
        const startPosition = sequence.startingPositionBeat || sequence.startPosition;
        console.log("🔍 ConstructTabState: sequence.startingPositionBeat:", sequence.startingPositionBeat);
        console.log("🔍 ConstructTabState: sequence.startPosition:", sequence.startPosition);
        console.log("🔍 ConstructTabState: startPosition (combined):", startPosition);
        
        let result: PictographData[] = [];
        
        // If we have beats, use them
        if (beats.length > 0) {
          result = beats.map((beat: any) => beat.pictographData).filter(Boolean);
          console.log("🔍 ConstructTabState: using beats, result:", result);
        } 
        // If no beats but we have a start position, include it
        else if (startPosition?.pictographData) {
          result = [startPosition.pictographData];
          console.log("🔍 ConstructTabState: using start position, result:", result);
        }
        
        console.log("🔍 ConstructTabState: currentSequenceData getter called, returning:", result);
        return result;
      }
      console.log("🔍 ConstructTabState: currentSequenceData getter called, no sequence - returning empty array");
      return [];
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

