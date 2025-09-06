<!-- StartPositionPicker.svelte - Thin component using proper state layer -->
<script lang="ts">
  import { GridMode } from "$shared/domain";
  import { resolve } from "$shared/inversify";
  import { TYPES } from "$shared/inversify/types";
  import { onMount } from "svelte";
  import type { IStartPositionService } from "../services/contracts";
  import { createStartPositionPickerState } from "../state/start-position-picker-state.svelte";
// UI Components
  import ErrorState from "./ErrorState.svelte";
  import LoadingState from "./LoadingState.svelte";
  import PictographGrid from "./PictographGrid.svelte";

  // Proper TKA architecture: Service → State → Component
  const startPositionService = resolve(
    TYPES.IStartPositionService
  ) as IStartPositionService;
  const state = createStartPositionPickerState(startPositionService);

  // Initialize on mount
  onMount(() => {
    state.loadStartPositions(GridMode.DIAMOND);
  });
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  {#if state.isLoading}
    <LoadingState />
  {:else if state.loadingError}
    <ErrorState message="Failed to load start positions" />
  {:else if state.startPositionPictographs.length === 0}
    <ErrorState
      message="No valid start positions found for the current configuration."
      hasRefreshButton={false}
    />
  {:else}
    <PictographGrid
      pictographDataSet={state.startPositionPictographs}
      selectedPictograph={state.selectedStartPos}
      onPictographSelect={(position) =>
        startPositionService.selectStartPosition(position)}
    />
  {/if}

  <!-- Debug info -->
  <div
    style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; padding: 5px; font-size: 10px;"
  >
    Debug: isLoading={state.isLoading}, pictographs={state
      .startPositionPictographs.length}, error={state.loadingError}
  </div>
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
