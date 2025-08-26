<!-- StartPositionPicker.svelte - Clean component following TKA architecture -->
<script lang="ts">
  import { GridMode } from "$lib/domain";
  import { resolve } from "$services/bootstrap";
  // UI Components
  import ErrorState from "./ui/ErrorState.svelte";
  import LoadingState from "./ui/LoadingState.svelte";
  import PictographGrid from "./ui/PictographGrid.svelte";
  import TransitionOverlay from "./ui/TransitionOverlay.svelte";

  // Props
  let { sequenceState } = $props<{
    sequenceState: import("$lib/state/sequence/sequence-state.svelte").SequenceState;
  }>();

  // Get service from DI container (sequence state comes from props)
  const sequenceStateService = resolve(
    "ISequenceStateService"
  ) as import("$lib/services/interfaces/sequence-state-interfaces").ISequenceStateService;

  // Get start position service from DI container
  const startPositionService = resolve(
    "IStartPositionService"
  ) as import("$lib/services/interfaces/application-interfaces").IStartPositionService;

  // Reactive state
  let isLoading = $state(true);
  let loadingError = $state<string | null>(null);
  let startPositions = $state<any[]>([]);
  let selectedStartPos = $state<any | null>(null);
  let isTransitioning = $state(false);

  // Load start positions when component mounts
  $effect(() => {
    loadStartPositions();
  });

  async function loadStartPositions() {
    if (!startPositionService) {
      console.error(
        "❌ StartPositionPicker: No start position service available"
      );
      loadingError = "Start position service not available";
      isLoading = false;
      return;
    }

    try {
      isLoading = true;
      loadingError = null;

      // Load start positions from the service
      const positions = await startPositionService.getDefaultStartPositions(
        GridMode.DIAMOND
      );
      startPositions = positions;
    } catch (error) {
      console.error(
        "❌ StartPositionPicker: Failed to load start positions",
        error
      );
      loadingError =
        error instanceof Error
          ? error.message
          : "Failed to load start positions";
      startPositions = [];
    } finally {
      isLoading = false;
    }
  }

  async function handleSelect(position: any) {
    selectedStartPos = position;

    try {
      // Create or get current sequence
      let currentSequence = sequenceState.currentSequence;

      if (!currentSequence) {
        // Create a new sequence if none exists
        currentSequence = sequenceStateService.createNewSequence(
          "New Sequence",
          16
        );
        sequenceState.setCurrentSequence(currentSequence);
      }

      // Convert the pictograph position to a beat data for start position
      const startPositionBeat = {
        id: crypto.randomUUID(),
        beatNumber: 0, // Start position is beat 0
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
        pictographData: position,
        metadata: {
          isStartPosition: true,
          endPosition: position.letter || "unknown",
        },
      };

      // Set the start position in the sequence
      const updatedSequence = sequenceStateService.setStartPosition(
        currentSequence,
        startPositionBeat
      );
      sequenceState.setCurrentSequence(updatedSequence);
    } catch (error) {
      console.error(
        "❌ StartPositionPicker: Failed to set start position",
        error
      );
    }
  }

  // Listen for sequence state changes to clear transition state
  $effect(() => {
    const currentSequence = sequenceState.currentSequence;

    // If a sequence with startPosition exists and we're transitioning, clear the transition
    if (currentSequence && currentSequence.startPosition && isTransitioning) {
      isTransitioning = false;
    }
  });
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  {#if isLoading}
    <LoadingState />
  {:else if loadingError}
    <ErrorState />
  {:else if startPositions.length === 0}
    <ErrorState
      message="No valid start positions found for the current configuration."
      hasRefreshButton={false}
    />
  {:else}
    <PictographGrid
      pictographDataSet={startPositions}
      selectedPictograph={selectedStartPos}
      onPictographSelect={handleSelect}
    />
  {/if}

  <!-- Debug info -->
  <div
    style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; padding: 5px; font-size: 10px;"
  >
    Debug: isLoading={isLoading}, pictographs={startPositions.length}, error={loadingError}
  </div>

  <!-- Loading overlay during transition -->
  {#if isTransitioning}
    <TransitionOverlay />
  {/if}
</div>

<style>
  .start-pos-picker {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: var(--spacing-lg);
    background: transparent;
    position: relative;
  }
</style>
