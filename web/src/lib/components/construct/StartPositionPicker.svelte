<!-- StartPositionPicker.svelte - Clean component following TKA architecture -->
<script lang="ts">
  import type { PictographData } from "$domain/PictographData";
  import { resolve } from "$services/bootstrap";
  import type { IStartPositionService } from "$services/interfaces/application-interfaces";
  import type { IStartPositionSelectionService } from "$lib/services/interfaces/IStartPositionSelectionService";
  import { onMount } from "svelte";
  import { GridMode } from "$lib/domain";

  // UI Components
  import LoadingState from "./start-position/ui/LoadingState.svelte";
  import ErrorState from "./start-position/ui/ErrorState.svelte";
  import PictographGrid from "./start-position/ui/PictographGrid.svelte";
  import TransitionOverlay from "./start-position/ui/TransitionOverlay.svelte";

  // Props using runes
  const { gridMode = GridMode.DIAMOND } = $props<{
    gridMode?: GridMode;
  }>();

  // Simple reactive state directly in component
  let isLoading = $state(true);
  let startPositions = $state<PictographData[]>([]);
  let loadingError = $state(false);
  let selectedStartPos = $state<PictographData | null>(null);
  let isTransitioning = $state(false);

  // Services
  let startPositionService: IStartPositionService | null = null;
  let selectionService: IStartPositionSelectionService | null = null;

  // Initialize services once
  function initializeServices() {
    try {
      console.log("StartPositionPicker: Attempting to resolve services...");

      // Resolve services
      try {
        startPositionService = resolve("IStartPositionService");
        console.log("StartPositionPicker: ✅ IStartPositionService resolved");
      } catch (error) {
        console.log(
          "StartPositionPicker: ❌ Failed to resolve IStartPositionService:",
          error
        );
        return false; // Container not ready yet
      }

      try {
        selectionService = resolve("IStartPositionSelectionService");
        console.log(
          "StartPositionPicker: ✅ IStartPositionSelectionService resolved"
        );
      } catch (error) {
        console.log(
          "StartPositionPicker: ❌ Failed to resolve IStartPositionSelectionService:",
          error
        );
        return false; // Container not ready yet
      }

      return true;
    } catch (error) {
      console.error("StartPositionPicker: Failed to resolve services:", error);
      return false;
    }
  }

  // Load start positions directly
  async function loadStartPositions() {
    console.log("StartPositionPicker: loadStartPositions called");

    if (!startPositionService) {
      console.log(
        "StartPositionPicker: Service not available, trying to initialize..."
      );
      if (!initializeServices()) {
        console.log("StartPositionPicker: Failed to initialize services");
        return;
      }
    }

    if (!startPositionService) {
      console.log("StartPositionPicker: Still no service available");
      return;
    }

    try {
      console.log("StartPositionPicker: Setting loading to true");
      isLoading = true;
      loadingError = false;

      console.log(
        "StartPositionPicker: Calling getDefaultStartPositions with gridMode:",
        gridMode
      );
      const positions =
        await startPositionService.getDefaultStartPositions(gridMode);

      console.log(
        "StartPositionPicker: Received positions:",
        positions?.length || 0
      );
      startPositions = positions || [];

      console.log("StartPositionPicker: Setting loading to false");
      isLoading = false;

      console.log(
        "StartPositionPicker: Final state - isLoading:",
        isLoading,
        "positions:",
        startPositions.length
      );
    } catch (error) {
      console.error(
        "StartPositionPicker: Error loading start positions:",
        error
      );
      loadingError = true;
      startPositions = [];
      isLoading = false;
    }
  }

  // Handle start position selection using service
  async function handleSelect(startPosPictograph: PictographData) {
    if (!selectionService || !startPositionService) {
      console.error("Services not available for start position selection");
      return;
    }

    try {
      // Set transition state
      isTransitioning = true;
      selectedStartPos = startPosPictograph;

      // Use selection service to handle the complex business logic
      await selectionService.selectStartPosition(
        startPosPictograph,
        startPositionService
      );

      // Clear transition state after a short delay
      setTimeout(() => {
        isTransitioning = false;
      }, 200);
    } catch (error) {
      console.error(
        "StartPositionPicker: Error selecting start position:",
        error
      );
      isTransitioning = false;

      // Show user-friendly error
      alert(
        `Failed to select start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  // Initialize on mount
  onMount(() => {
    console.log("StartPositionPicker: onMount called");
    loadStartPositions();
  });

  // Reload when grid mode changes
  $effect(() => {
    if (gridMode) {
      loadStartPositions();
    }
  });

  // Listen for sequence state changes to clear transition state
  import { sequenceStateService } from "$lib/services/SequenceStateService.svelte";

  $effect(() => {
    const currentSequence = sequenceStateService.currentSequence;

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
