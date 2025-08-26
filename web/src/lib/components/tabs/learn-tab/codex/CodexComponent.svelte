<!--
	Codex Component - Reference sidebar for browsing pictographs

	Matches desktop CodexComponent functionality with control panel,
	row-based pictograph organization, operations, and orientation selector.
	Now featuring beautiful glass scrollbars.
-->
<script lang="ts">
  import SimpleGlassScroll from "$lib/components/ui/SimpleGlassScroll.svelte";
  import type { PictographData } from "$lib/domain/PictographData";
  import { createCodexState } from "$lib/state/codex-state.svelte";
  import CodexControlPanel from "./CodexControlPanel.svelte";
  import CodexPictographGrid from "./CodexPictographGrid.svelte";

  // Props
  interface Props {
    isVisible?: boolean;
    onPictographSelected?: (pictograph: PictographData) => void;
    onToggleVisibility?: () => void;
  }

  let {
    isVisible = true,
    onPictographSelected,
    onToggleVisibility,
  }: Props = $props();

  // Create codex state using runes
  const codexState = createCodexState();
  console.log("🔧 CodexComponent: Created codex state instance");

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
    codexState.filteredPictographsByLetter()
  );
  let letterRows = $derived(codexState.letterRows);
  let isLoading = $derived(codexState.isLoading);
  let isInitialized = $derived(codexState.isInitialized);
  let currentOrientation = $derived(codexState.currentOrientation);
  let error = $derived(codexState.error);
  let isProcessingOperation = $derived(codexState.isProcessingOperation);

  // Methods

  function handlePictographClick(pictograph: PictographData) {
    onPictographSelected?.(pictograph);
  }

  function toggleCollapse() {
    onToggleVisibility?.();
  }

  // Control panel handlers
  function handleRotate() {
    codexState.rotatePictographs();
  }

  function handleMirror() {
    codexState.mirrorPictographs();
  }

  function handleColorSwap() {
    codexState.colorSwapPictographs();
  }

  function handleOrientationChange(orientation: string) {
    codexState.setOrientation(orientation);
  }
</script>

<div class="codex-component" class:collapsed={!isVisible}>
  <!-- Header with integrated toggle (Browse navigation style) -->
  <div class="codex-header">
    <div class="header-content">
      <div class="header-text">
        <h3 class="codex-title">Codex</h3>
        {#if isVisible}
          <div class="codex-subtitle">Pictograph Reference</div>
        {/if}
      </div>
      <button
        class="collapse-toggle"
        onclick={toggleCollapse}
        title={isVisible ? "Hide codex" : "Show codex"}
      >
        {isVisible ? "◀" : "▶"}
      </button>
    </div>
  </div>

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
            <button
              class="retry-button"
              onclick={() => codexState.refreshPictographs()}
            >
              Retry
            </button>
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
            pictographSize={80}
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
    backdrop-filter: blur(10px);
    transition: all var(--desktop-transition-slow);
  }

  .codex-component.collapsed {
    width: 48px;
    min-width: 48px;
  }

  .collapsed .codex-header {
    padding: var(--desktop-spacing-xs);
    text-align: center;
    border-bottom: none;
  }

  .collapsed .header-content {
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0;
  }

  .collapsed .header-text {
    display: none; /* Hide text in collapsed state */
  }

  .collapsed .collapse-toggle {
    padding: var(--desktop-spacing-sm);
    font-size: var(--desktop-font-size-lg);
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
  }

  .codex-header {
    padding: var(--desktop-spacing-lg);
    border-bottom: 1px solid var(--desktop-border-tertiary);
    background: rgba(255, 255, 255, 0.05);
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--desktop-spacing-md);
  }

  .header-text {
    display: flex;
    flex-direction: column;
    gap: var(--desktop-spacing-xs);
    flex: 1;
  }

  .codex-title {
    color: white;
    font-family: var(--desktop-font-family);
    font-size: var(--desktop-font-size-lg);
    font-weight: 600;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .collapsed .codex-title {
    font-size: var(--desktop-font-size-sm);
    margin: 0;
  }

  .codex-subtitle {
    font-size: var(--desktop-font-size-sm);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  .collapse-toggle {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.7);
    font-size: var(--desktop-font-size-sm);
    cursor: pointer;
    padding: var(--desktop-spacing-xs);
    border-radius: 4px;
    transition: all var(--desktop-transition-fast);
    flex-shrink: 0;
  }

  .collapse-toggle:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
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
