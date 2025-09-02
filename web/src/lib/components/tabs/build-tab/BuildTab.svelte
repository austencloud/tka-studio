<!-- BuildTab.svelte - Master tab with clean service resolution -->
<script lang="ts">
  import LeftPanel from "./layout/LeftPanel.svelte";
  import RightPanel from "./layout/RightPanel.svelte";
  import ErrorBanner from "./shared/ErrorBanner.svelte";
  import LoadingOverlay from "./shared/LoadingOverlay.svelte";

  import { GridMode } from "$domain";
  import type { IStartPositionService } from "$contracts";
  import type { IBuildTabService } from "$lib/services/contracts/build-interfaces";
  import type { ISequenceService } from "$lib/services/contracts/sequence-interfaces";
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import { createBuildTabState } from "$lib/state/build-tab-state.svelte";
  import { createConstructTabState } from "$lib/state/construct-tab-state.svelte";
  import { onMount } from "svelte";

  // ✅ CLEAN SERVICE RESOLUTION: Resolve services using clean pattern (no 'as any')
  const sequenceService = resolve(TYPES.ISequenceService) as ISequenceService; // TODO: Fix typing
  const startPositionService = resolve(
    TYPES.IStartPositionService
  ) as IStartPositionService;
  const buildTabService = resolve(TYPES.IBuildTabService) as IBuildTabService;
  // Services are now resolved directly in components that need them
  // ✅ CREATE SEPARATED STATES: Master tab state + construct sub-tab state
  const buildTabState = createBuildTabState(sequenceService);
  const constructTabState = createConstructTabState(
    buildTabService,
    startPositionService
  );

  // Initialize start position service on mount
  onMount(async () => {
    // Load start positions using the service
    const startPositionService = resolve(
      TYPES.IStartPositionService
    ) as IStartPositionService;
    await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);
    console.log("✅ BuildTab: Start positions loaded via service");
  });

  // Start position selection is now handled directly by the unified service

  async function handleOptionSelected(option: any): Promise<void> {
    try {
      // Delegate to Application Service - handles all business logic
      await buildTabService.selectOption(option);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to select option";
      constructTabState.setError(errorMessage);
      console.error("❌ BuildTab: Error handling option selection:", err);
    }
  }
</script>

<div class="construct-tab" data-testid="construct-tab">
  <!-- Error display -->
  {#if constructTabState.error}
    <ErrorBanner
      message={constructTabState.error}
      onDismiss={constructTabState.clearError}
    />
  {/if}

  <!-- Main content area - Two panel layout like desktop app -->
  <div class="construct-content">
    <!-- Left Panel: Workbench (always visible) -->
    <LeftPanel />

    <!-- Right Panel: 4-Tab interface matching desktop -->
    <RightPanel
      {buildTabState}
      {constructTabState}
      onOptionSelected={handleOptionSelected}
    />
  </div>

  <!-- Loading overlay -->
  {#if constructTabState.isTransitioning}
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
