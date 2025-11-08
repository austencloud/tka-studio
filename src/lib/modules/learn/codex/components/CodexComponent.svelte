<!--
	Codex Component - Reference sidebar for browsing pictographs

	Matches desktop CodexComponent functionality with control panel,
	row-based pictograph organization, operations, and orientation selector.
	Now featuring beautiful glass scrollbars.
-->
<script lang="ts">
  import type { IHapticFeedbackService, PictographData } from "$shared";
  import { resolve, SimpleGlassScroll, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { createCodexState } from "../state/codex-state.svelte";
  import CodexControlPanel from "./CodexControlPanel.svelte";
  import CodexPictographGrid from "./CodexPictographGrid.svelte";

  // Props
  let { isVisible = true, onPictographSelected } = $props<{
    isVisible?: boolean;
    onPictographSelected?: (pictograph: PictographData) => void;
  }>();

  // Create codex state using runes
  const codexState = createCodexState();
  console.log("🔧 CodexComponent: Created codex state instance");

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Initialize pictographs when component mounts - only once
  $effect(() => {
    console.log(
      "🔧 CodexComponent $effect triggered, isVisible:",
      isVisible,
      "isInitialized:",
      codexState.isInitialized,
      "isLoading:",
      codexState.isLoading
    );
    // Only initialize if visible and not already initialized or loading
    if (isVisible && !codexState.isInitialized && !codexState.isLoading) {
      console.log("🚀 CodexComponent: Initializing codex state...");
      codexState.refreshPictographs();
    }
  });

  // Reactive values
  let filteredPictographsByLetter = $derived(
    codexState.filteredPictographsByLetter
  );
  let letterRows = $derived(codexState.letterRows);
  let isLoading = $derived(codexState.isLoading);
  let isInitialized = $derived(codexState.isInitialized);
  let currentOrientation = $derived(codexState.currentOrientation);
  let error = $derived(codexState.error);
  let isProcessingOperation = $derived(codexState.isProcessingOperation);

  // Methods

  function handlePictographClick(pictograph: PictographData) {
    // Trigger selection haptic for pictograph selection
    hapticService?.trigger("selection");
    onPictographSelected?.(pictograph);
  }

  // Control panel handlers
  function handleRotate() {
    // Trigger selection haptic for rotate action
    hapticService?.trigger("selection");
    codexState.rotatePictographs();
  }

  function handleMirror() {
    // Trigger selection haptic for mirror action
    hapticService?.trigger("selection");
    codexState.mirrorPictographs();
  }

  function handleColorSwap() {
    // Trigger selection haptic for color swap action
    hapticService?.trigger("selection");
    codexState.colorSwapPictographs();
  }

  function handleOrientationChange(orientation: string) {
    // Trigger selection haptic for orientation change
    hapticService?.trigger("selection");
    codexState.setOrientation(orientation);
  }

  function handleRetry() {
    // Trigger selection haptic for retry action
    hapticService?.trigger("selection");
    codexState.refreshPictographs();
  }
</script>

<div class="codex-component" class:collapsed={!isVisible}>
  {#if isVisible}
    <!-- Control Panel -->
    <CodexControlPanel
      {currentOrientation}
      onRotate={handleRotate}
      onMirror={handleMirror}
      onColorSwap={handleColorSwap}
      onOrientationChange={handleOrientationChange}
    />

    <!-- Content area with beautiful glass scrollbar -->
    <div class="content-wrapper">
      <SimpleGlassScroll variant="primary" height="100%">
        {#if error}
          <div class="error-state">
            <div class="error-icon">⚠️</div>
            <p class="error-message">{error}</p>
            <button class="retry-button" onclick={handleRetry}> Retry </button>
          </div>
        {:else if isLoading}
          <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading pictographs...</p>
          </div>
        {:else if isProcessingOperation}
          <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>Processing operation...</p>
          </div>
        {:else if !isInitialized}
          <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>Initializing codex...</p>
          </div>
        {:else if Object.keys(filteredPictographsByLetter).length === 0}
          <div class="empty-state">
            <p>No pictographs found</p>
          </div>
        {:else}
          <!-- Row-based pictograph grid -->
          <CodexPictographGrid
            pictographsByLetter={filteredPictographsByLetter}
            {letterRows}
            onPictographClick={handlePictographClick}
          />
        {/if}
      </SimpleGlassScroll>
    </div>
  {/if}
</div>

<style>
  .codex-component {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%; /* Take full width of parent container */
    min-width: 250px;
    background: var(--desktop-bg-secondary); /* Transparent background */
    border-radius: var(--desktop-border-radius);
    border: 1px solid var(--desktop-border-secondary);
    transition: all var(--desktop-transition-slow);
  }

  .codex-component.collapsed {
    width: 48px;
    min-width: 48px;
  }

  /* Content wrapper for glass scroll container */
  .content-wrapper {
    flex: 1;
    min-height: 0; /* Important for flex containers */
  }

  .collapsed .content-wrapper {
    display: none;
  }

  .loading-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: var(--desktop-text-muted);
    text-align: center;
    gap: var(--desktop-spacing-lg);
    padding: var(--desktop-spacing-lg);
  }

  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: var(--desktop-progress-poor);
    text-align: center;
    gap: var(--desktop-spacing-lg);
    padding: var(--desktop-spacing-lg);
  }

  .error-icon {
    font-size: 2rem;
  }

  .error-message {
    margin: 0;
    font-size: var(--desktop-font-size-sm);
    color: var(--desktop-text-muted);
  }

  .retry-button {
    padding: var(--desktop-spacing-sm) var(--desktop-spacing-lg);
    background-color: var(--desktop-restart-blue);
    border: 1px solid var(--desktop-restart-blue-border);
    border-radius: var(--desktop-border-radius-xs);
    color: var(--desktop-text-primary);
    font-size: var(--desktop-font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--desktop-transition-normal);
  }

  .retry-button:hover {
    background-color: var(--desktop-restart-blue-hover);
    border-color: var(--desktop-restart-blue-hover-border);
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--desktop-border-tertiary);
    border-left: 3px solid var(--desktop-primary-blue);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .codex-component {
      width: 250px;
      min-width: 200px;
    }
  }

  @media (max-width: 480px) {
    .codex-component {
      width: 100%;
      min-width: 250px;
    }
  }
</style>
