<!--
Build Tab - Main construction interface

Provides two-panel layout matching desktop app:
- Left Panel: Workbench for sequence visualization
- Right Panel: 4-tab interface (Construct, Edit, Generate, Export)
-->
<script lang="ts">
	import { GridMode } from "$shared/domain";
	import { resolve, TYPES } from "$shared/inversify";
	import { onMount } from "svelte";
	import { createConstructTabState } from "../../construct/shared/state/construct-tab-state.svelte";
	import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
	import type { ISequenceService } from "../../workbench/services/contracts";
	import type { IBuildTabService } from "../services/contracts";
	import { createBuildTabState } from "../state/build-tab-state.svelte";
	import ErrorBanner from './../../../browse/shared/components/ErrorBanner.svelte';
	import LeftPanel from './LeftPanel.svelte';
	import LoadingOverlay from './LoadingOverlay.svelte';
	import RightPanel from './RightPanel.svelte';
  

  const sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
  const startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
  const buildTabService = resolve(TYPES.IBuildTabService) as IBuildTabService;

  const buildTabState = createBuildTabState(sequenceService);
  const constructTabState = createConstructTabState(
    buildTabService,
    startPositionService
  );


  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioning = $state(false);

  async function handleOptionSelected(option: any): Promise<void> {
    try {
      // Delegate to Application Service - handles all business logic
      await buildTabService.selectOption(option);
      console.log("✅ BuildTab: Option selected successfully:", option);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to select option";
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
    console.log("✅ BuildTab: Mounted - Full functionality enabled");

    try {
      isLoading = true;

      // Initialize build tab service
      await buildTabService.initialize();

      // Load start positions using the service
      await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);

      console.log("✅ BuildTab: Initialization complete - All features enabled");
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
    <LeftPanel />

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