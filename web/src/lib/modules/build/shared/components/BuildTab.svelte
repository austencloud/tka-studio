<!--
Build Tab - Main construction interface

Provides two-panel layout matching desktop app:
- Left Panel: Workbench for sequence visualization
- Right Panel: 4-tab interface (Construct, Edit, Generate, Export)
-->
<script lang="ts">
	import { GridMode } from "$shared/domain";
	import { resolve, TYPES } from "$shared/inversify";
	import type { IBuildTabService, ISequenceService, IStartPositionService } from "../../services/contracts";
	import { createBuildTabState } from "../state/build-tab-state.svelte";
	import { createConstructTabState } from "../../construct/shared/state/construct-tab-state.svelte";
	import { onMount } from "svelte";
  

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
      // TEMPORARY: Service usage commented out
      // Delegate to Application Service - handles all business logic
      // await buildTabService.selectOption(option);
      console.log("✅ BuildTab: Option selected (services disabled):", option);
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
    console.log("✅ BuildTab: Mounted (services temporarily disabled)");
    
    // TEMPORARY: All initialization commented out
    try {
      // Initialize build tab service
      await buildTabService.initialize();
      
      // Load start positions using the service
      await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);
      
      console.log("✅ BuildTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ BuildTab: Initialization failed:", err);
      error = err instanceof Error ? err.message : "Failed to initialize build tab";
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
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>🔧 Build Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Workbench with sequence visualization</li>
          <li>✅ Start position picker</li>
          <li>✅ Option picker with filtering</li>
          <li>✅ Sequence generation</li>
          <li>✅ Beat editing and manipulation</li>
          <li>✅ Export to multiple formats</li>
        </ul>
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
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
    display: flex;
    justify-content: center;
    align-items: center;
    /* Original layout: */
    /* display: grid;
    grid-template-columns: 1fr 1fr; /* 50/50 split between left panel and right panel */
    /* overflow: hidden;
    gap: var(--spacing-xs);
    padding: 8px; */
  }

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  /* Responsive adjustments */
  @media (max-width: 1024px) {
    .build-tab-layout {
      flex-direction: column;
    }
  }

  @media (max-width: 768px) {
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }
  }
</style>