<!-- ConstructTab.svelte - Refactored with factory-based state management -->
<script lang="ts">
	import RightPanel from './layout/RightPanel.svelte';
	import LoadingOverlay from './shared/LoadingOverlay.svelte';
	import LeftPanel from './layout/LeftPanel.svelte';
	import ErrorBanner from './shared/ErrorBanner.svelte';

  import { constructTabEventService } from "$services/implementations/construct/ConstructTabEventService";
  import { resolve } from "$services/bootstrap";
  import { createSequenceState } from "$lib/state/sequence-state.svelte";
  import { createConstructTabState } from "$lib/state/construct-tab-state.svelte";
  import { onMount } from "svelte";

  // Create component-scoped state using factory functions
  const sequenceService = resolve("ISequenceService") as any; // TODO: Fix typing
  const sequenceState = createSequenceState(sequenceService);
  const constructTabState = createConstructTabState(sequenceState);

  // Reactive state from store
  let errorMessage = $derived(constructTabState.errorMessage);
  let isTransitioning = $derived(constructTabState.isTransitioning);

  // Create derived props for child components
  const rightPanelProps = $derived({
    activeRightPanel: constructTabState.activeRightPanel,
    isSubTabTransitionActive: constructTabState.isSubTabTransitionActive,
    setActiveRightPanel: constructTabState.setActiveRightPanel,
    // Sequence state for GraphEditor
    currentSequence: sequenceState.currentSequence,
    selectedBeatIndex: sequenceState.selectedBeatIndex,
    selectedBeatData:
      sequenceState.selectedBeatIndex !== null
        ? (sequenceState.currentSequence?.beats[
            sequenceState.selectedBeatIndex
          ] ?? null)
        : null,
  });

  // Setup component coordination and reactive state updates on mount
  onMount(() => {
    constructTabEventService().setupComponentCoordination();

    // Initialize start position picker state once on mount
    constructTabState?.updateShouldShowStartPositionPicker();
  });
</script>

<div class="construct-tab" data-testid="construct-tab">
  <!-- Error display -->
  {#if errorMessage}
    <ErrorBanner
      message={errorMessage}
      onDismiss={() => constructTabState.clearError()}
    />
  {/if}

  <!-- Main content area - Two panel layout like desktop app -->
  <div class="construct-content">
    <!-- Left Panel: Workbench (always visible) -->
    <LeftPanel />

    <!-- Right Panel: 4-Tab interface matching desktop -->
    <RightPanel constructTabState={rightPanelProps} />
  </div>

  <!-- Loading overlay -->
  {#if isTransitioning}
    <LoadingOverlay message="Processing..." />
  {/if}
</div>

<style>
  .construct-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  /* Main two-column layout: 50/50 split between left and right panels */
  .construct-content {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr; /* 50/50 split between left panel and right panel */
    overflow: hidden;
    gap: var(--spacing-xs); /* Add small gap between content and button panel */

    padding: 8px;
  }

  /* Responsive adjustments */
  @media (max-width: 1024px) {
    .construct-content {
      flex-direction: column;
    }
  }
</style>
