<!--
Build Tab - Main construction interface

Provides two-panel layout matching desktop app:
- Left Panel: Workbench for sequence visualization
- Right Panel: 4-tab interface (Construct, Edit, Generate, Export)

Testing HMR persistence functionality
-->
<script lang="ts">
  import { ErrorBanner, GridMode, navigationState, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
  import type { IBuildTabService, ISequencePersistenceService, ISequenceService, ISequenceStateService } from "../services/contracts";
  import { getBuildTabEventService } from "../services/implementations/BuildTabEventService";
  import { createBuildTabState } from "../state/build-tab-state.svelte";
  import { createConstructTabState } from "../state/construct-tab-state.svelte";
  import LeftPanel from './LeftPanel.svelte';
  import LoadingOverlay from './LoadingOverlay.svelte';
  import RightPanel from './RightPanel.svelte';
  

  const sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
  const sequenceStateService = resolve(TYPES.ISequenceStateService) as ISequenceStateService;
  const sequencePersistenceService = resolve(TYPES.ISequencePersistenceService) as ISequencePersistenceService;
  const startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
  const buildTabService = resolve(TYPES.IBuildTabService) as IBuildTabService;

  const buildTabState = createBuildTabState(sequenceService, sequenceStateService, sequencePersistenceService);
  const constructTabState = createConstructTabState(
    buildTabService,
    buildTabState.sequenceState,
    sequencePersistenceService
  );


  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioning = $state(false);

  // Sync navigation state with build tab state
  $effect(() => {
    const currentMode = navigationState.currentBuildMode;
    const buildTabCurrentMode = buildTabState.activeSubTab;

    // If navigation state differs from build tab state, update build tab
    if (currentMode !== buildTabCurrentMode && buildTabState.isPersistenceInitialized) {
      buildTabState.setActiveRightPanel(currentMode as any);
    }
  });

  // Sync build tab state changes back to navigation state
  $effect(() => {
    const buildTabCurrentMode = buildTabState.activeSubTab;
    if (buildTabCurrentMode && buildTabCurrentMode !== navigationState.currentBuildMode) {
      navigationState.setBuildMode(buildTabCurrentMode);
    }
  });



  async function handleOptionSelected(option: any): Promise<void> {
    try {
      // Delegate to Application Service - handles all business logic
      await buildTabService.selectOption(option);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to select option";
      error = errorMessage;
      console.error("❌ BuildTab: Error handling option selection:", err);
    }
  }

  function clearError() {
  error = null;
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
  try {
    isLoading = true;

    // Initialize build tab service
    await buildTabService.initialize();

    // Initialize build tab state with persistence (includes sequence state)
    await buildTabState.initializeWithPersistence();

    // Initialize construct tab with persistence
    await constructTabState.initializeConstructTab();

    // Set up sequence state callbacks for BuildTabEventService
    const buildTabEventService = getBuildTabEventService();
    buildTabEventService.setSequenceStateCallbacks(
      () => buildTabState.sequenceState.getCurrentSequence(),
      (sequence) => buildTabState.sequenceState.setCurrentSequence(sequence)
    );

    // Load start positions using the service
    await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);
  } catch (err) {
    console.error("❌ BuildTab: Initialization failed:", err);
    error = err instanceof Error ? err.message : "Failed to initialize build tab";
  } finally {
    isLoading = false;
  }
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="build-tab" data-testid="build-tab">
  <!-- Error display -->
  {#if error}
  <ErrorBanner
    message={error}
    onDismiss={clearError}
  />
  {/if}



  <div class="build-tab-layout">
  <!-- Left Panel: Workbench -->
  <LeftPanel
    sequenceState={buildTabState.sequenceState}
    onClearSequence={constructTabState.clearSequenceCompletely}
  />

  <!-- Right Panel: 4-Tab interface matching desktop -->
  <RightPanel
    {buildTabState}
    {constructTabState}
    onOptionSelected={handleOptionSelected}
  />
  </div>

  <!-- Loading overlay -->
  {#if isTransitioning}
  <LoadingOverlay message="Processing..." />
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .build-tab {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow: hidden;
  position: relative;
  }

  .build-tab-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr; /* 50/50 split between left panel and right panel */
  overflow: hidden;
  gap: var(--spacing-xs);
  padding: 8px;
  }



  /* Responsive adjustments */
  @media (max-width: 1024px) {
  .build-tab-layout {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  }
</style>
