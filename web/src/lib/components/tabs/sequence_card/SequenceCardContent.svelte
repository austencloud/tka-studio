<!-- SequenceCardContent.svelte - Enhanced content area for sequence cards -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { SequenceData } from "$services/interfaces/domain-types";
  import SequenceCard from "./SequenceCard.svelte";

  // Props
  interface Props {
    sequences?: SequenceData[];
    columnCount?: number;
    isLoading?: boolean;
    selectedLength?: number;
    layoutMode?: "grid" | "list" | "printable";
    onSequenceClick?: (sequence: SequenceData) => void;
  }

  let {
    sequences = [],
    columnCount = 2,
    isLoading = false,
    selectedLength = 16,
    layoutMode = "grid",
    onSequenceClick,
  }: Props = $props();

  // State
  let error = $state<string | null>(null);

  // Derived values
  let hasSequences = $derived(sequences.length > 0);
  let gridColumns = $derived(() => {
    if (layoutMode === "list") {
      return 1;
    }
    return Math.max(1, Math.min(6, columnCount));
  });

  // Calculate responsive column width based on count
  let gridTemplateColumns = $derived(() => {
    if (layoutMode === "list") {
      return "1fr";
    }

    // For grid mode, use dynamic columns with minimum card width
    const minCardWidth = 280; // Minimum card width in pixels
    return `repeat(${gridColumns()}, minmax(${minCardWidth}px, 1fr))`;
  });

  // Generate grid gap based on layout mode
  let gridGap = $derived(() => {
    if (layoutMode === "list") {
      return "12px";
    }
    return "16px";
  });

  // Handle sequence selection
  function handleSequenceSelect(sequence: SequenceData) {
    console.log("Selected sequence:", sequence.name);
    onSequenceClick?.(sequence);
  }

  // Handle error recovery
  function clearError() {
    error = null;
  }

  // Lifecycle
  onMount(() => {
    console.log("SequenceCardContent mounted with layout mode:", layoutMode);
  });
</script>

<!-- Content -->
<div class="sequence-card-content" data-layout-mode={layoutMode}>
  {#if isLoading}
    <div class="state-container loading">
      <div class="loading-spinner"></div>
      <h3 class="state-title">Loading sequences...</h3>
      <p class="state-message">
        {selectedLength === 0
          ? "Loading all sequences"
          : `Loading ${selectedLength}-beat sequences`}
      </p>
    </div>
  {:else if error}
    <div class="state-container error">
      <div class="error-icon">⚠️</div>
      <h3 class="state-title">Error Loading Sequences</h3>
      <p class="state-message">{error}</p>
      <button class="retry-button" onclick={clearError}> Try Again </button>
    </div>
  {:else if !hasSequences}
    <div class="state-container empty">
      <div class="empty-icon">
        {selectedLength === 0 ? "📝" : "🔍"}
      </div>
      <h3 class="state-title">
        {selectedLength === 0
          ? "No Sequences Available"
          : "No Matching Sequences"}
      </h3>
      <p class="state-message">
        {selectedLength === 0
          ? "Create some sequences to get started"
          : `No sequences found with ${selectedLength} beats`}
      </p>
      {#if selectedLength !== 0}
        <button class="clear-filter-button" onclick={() => {}}>
          Show All Sequences
        </button>
      {/if}
    </div>
  {:else}
    <!-- Sequence Grid/List -->
    <div
      class="sequence-layout"
      class:grid-layout={layoutMode === "grid"}
      class:list-layout={layoutMode === "list"}
      style:grid-template-columns={gridTemplateColumns()}
      style:gap={gridGap()}
    >
      {#each sequences as sequence (sequence.id)}
        <div class="sequence-item">
          <SequenceCard
            {sequence}
            variant={layoutMode === "list" ? "list" : "card"}
            onclick={() => handleSequenceSelect(sequence)}
          />
        </div>
      {/each}
    </div>

    <!-- Results Summary -->
    <div class="results-summary">
      <span class="results-count">
        {sequences.length} sequence{sequences.length === 1 ? "" : "s"}
      </span>
      {#if selectedLength !== 0}
        <span class="results-filter">
          with {selectedLength} beats
        </span>
      {/if}
      <span class="results-layout">
        in {layoutMode} layout ({gridColumns()} column{gridColumns() === 1
          ? ""
          : "s"})
      </span>
    </div>
  {/if}
</div>

<style>
  .sequence-card-content {
    padding: 16px;
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    background: transparent;
    position: relative;
  }

  /* State Containers */
  .state-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 48px 24px;
    flex: 1;
    min-height: 300px;
  }

  .state-title {
    margin: 16px 0 8px 0;
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
  }

  .state-message {
    margin: 0 0 24px 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    max-width: 400px;
    line-height: 1.5;
  }

  /* Loading State */
  .loading .state-title {
    color: rgba(255, 255, 255, 0.9);
  }

  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(255, 255, 255, 0.2);
    border-top: 4px solid rgba(99, 102, 241, 0.8);
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

  /* Error State */
  .error .state-title {
    color: #ef4444;
  }

  .error-icon {
    font-size: 64px;
    margin-bottom: 8px;
    opacity: 0.8;
  }

  .retry-button {
    background: var(--gradient-primary);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .retry-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  /* Empty State */
  .empty .state-title {
    color: rgba(255, 255, 255, 0.85);
  }

  .empty-icon {
    font-size: 72px;
    margin-bottom: 16px;
    opacity: 0.6;
  }

  .clear-filter-button {
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: 8px;
    padding: 8px 16px;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
    font-size: 13px;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: var(--shadow-glass);
  }

  .clear-filter-button:hover {
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }

  /* Sequence Layout */
  .sequence-layout {
    flex: 1;
    display: grid;
    align-content: start;
    padding: 8px 0;
  }

  .list-layout {
    /* List-specific styles */
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }

  .sequence-item {
    width: 100%;
    transition: transform var(--transition-fast);
  }

  .sequence-item:hover {
    transform: translateY(-2px);
    z-index: 10;
  }

  /* Results Summary */
  .results-summary {
    padding: 12px 16px;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border-radius: 8px;
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);
    margin-top: 16px;
    text-align: center;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    flex-shrink: 0;
  }

  .results-count {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  .results-filter,
  .results-layout {
    opacity: 0.8;
  }

  /* Responsive Design */
  @media (max-width: 1200px) {
    .sequence-layout.grid-layout {
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }
  }

  @media (max-width: 768px) {
    .sequence-card-content {
      padding: 12px;
    }

    .state-container {
      padding: 32px 16px;
      min-height: 250px;
    }

    .state-title {
      font-size: 18px;
    }

    .state-message {
      font-size: 13px;
    }

    .empty-icon {
      font-size: 56px;
    }

    .loading-spinner {
      width: 40px;
      height: 40px;
    }

    .sequence-layout.grid-layout {
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
    }

    .results-summary {
      font-size: 11px;
      padding: 10px 12px;
    }
  }

  @media (max-width: 480px) {
    .sequence-layout.grid-layout {
      grid-template-columns: 1fr;
      gap: 10px;
    }

    .sequence-card-content {
      padding: 8px;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .state-title {
      color: white;
    }

    .retry-button,
    .clear-filter-button {
      border: 2px solid white;
    }

    .results-summary {
      border: 1px solid rgba(255, 255, 255, 0.5);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .loading-spinner {
      animation: none;
    }

    .sequence-item:hover {
      transform: none;
    }

    .retry-button:hover,
    .clear-filter-button:hover {
      transform: none;
    }
  }

  /* Custom scrollbar */
  .sequence-card-content::-webkit-scrollbar {
    width: 8px;
  }

  .sequence-card-content::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }

  .sequence-card-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .sequence-card-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Layout mode specific adjustments */
  .sequence-card-content[data-layout-mode="list"] .sequence-layout {
    gap: 8px;
  }

  .sequence-card-content[data-layout-mode="grid"] .sequence-layout {
    gap: 16px;
  }
</style>
