<!--
  SequencesView.svelte - Sequences Library View

  Displays:
  - My Creations: Sequences created by the user
  - Starred: Sequences starred/bookmarked by the user
  - Organization tools: Folders, tags, search, sort, filter
-->
<script lang="ts">
  import { onMount } from "svelte";

  type ViewFilter = "all" | "mine" | "starred";

  // State
  let currentFilter = $state<ViewFilter>("all");
  let sequences = $state<any[]>([]);
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  // Filter handlers
  function handleFilterChange(filter: ViewFilter) {
    currentFilter = filter;
    loadSequences();
  }

  // Load sequences
  async function loadSequences() {
    isLoading = true;
    error = null;

    try {
      // TODO: Implement actual data loading from your services
      // For now, show a placeholder message
      await new Promise((resolve) => setTimeout(resolve, 500));
      sequences = [];
      isLoading = false;
    } catch (err) {
      console.error("Failed to load sequences:", err);
      error = err instanceof Error ? err.message : "Failed to load sequences";
      isLoading = false;
    }
  }

  onMount(() => {
    loadSequences();
  });
</script>

<div class="sequences-view">
  <!-- Filter Tabs -->
  <div class="filter-tabs glass-surface">
    <button
      class="filter-tab"
      class:active={currentFilter === "all"}
      onclick={() => handleFilterChange("all")}
    >
      <i class="fas fa-th"></i>
      <span>All</span>
    </button>
    <button
      class="filter-tab"
      class:active={currentFilter === "mine"}
      onclick={() => handleFilterChange("mine")}
    >
      <i class="fas fa-user"></i>
      <span>My Creations</span>
    </button>
    <button
      class="filter-tab"
      class:active={currentFilter === "starred"}
      onclick={() => handleFilterChange("starred")}
    >
      <i class="fas fa-star"></i>
      <span>Starred</span>
    </button>
  </div>

  <!-- Content Area -->
  <div class="content-area">
    {#if isLoading}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Loading sequences...</p>
      </div>
    {:else if error}
      <div class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <h3>Error Loading Sequences</h3>
        <p>{error}</p>
        <button class="retry-button" onclick={loadSequences}>
          <i class="fas fa-redo"></i>
          Retry
        </button>
      </div>
    {:else if sequences.length === 0}
      <div class="empty-state">
        <i class="fas fa-folder-open"></i>
        <h3>
          {#if currentFilter === "mine"}
            No Sequences Created Yet
          {:else if currentFilter === "starred"}
            No Starred Sequences
          {:else}
            Library is Empty
          {/if}
        </h3>
        <p>
          {#if currentFilter === "mine"}
            Create your first sequence in the Create module!
          {:else if currentFilter === "starred"}
            Star sequences from the Explore tab to add them here.
          {:else}
            Start creating or exploring sequences to populate your library.
          {/if}
        </p>
      </div>
    {:else}
      <!-- TODO: Display sequences in a grid -->
      <div class="sequences-grid">
        {#each sequences as sequence (sequence.id)}
          <div class="sequence-card">
            {sequence.word || "Untitled"}
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .sequences-view {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  /* Filter Tabs */
  .filter-tabs {
    display: flex;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: var(--glass-backdrop-medium);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    overflow-x: auto;
    overflow-y: hidden;
    flex-shrink: 0;
  }

  .filter-tab {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .filter-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .filter-tab.active {
    background: rgba(16, 185, 129, 0.2);
    border-color: rgba(16, 185, 129, 0.4);
    color: rgba(255, 255, 255, 1);
  }

  .filter-tab i {
    font-size: 1rem;
  }

  /* Content Area */
  .content-area {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--spacing-lg);
  }

  /* Loading State */
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: rgba(255, 255, 255, 0.7);
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: rgba(16, 185, 129, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: var(--spacing-md);
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Empty State */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    padding: var(--spacing-xl);
  }

  .empty-state i {
    font-size: 4rem;
    margin-bottom: var(--spacing-lg);
    opacity: 0.5;
  }

  .empty-state h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    color: rgba(255, 255, 255, 0.9);
  }

  .empty-state p {
    font-size: 1rem;
    line-height: 1.6;
    max-width: 400px;
  }

  /* Error State */
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    padding: var(--spacing-xl);
  }

  .error-state i {
    font-size: 4rem;
    margin-bottom: var(--spacing-lg);
    color: rgba(239, 68, 68, 0.7);
  }

  .error-state h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    color: rgba(255, 255, 255, 0.9);
  }

  .error-state p {
    font-size: 1rem;
    margin-bottom: var(--spacing-lg);
    max-width: 400px;
  }

  .retry-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: var(--border-radius-md);
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .retry-button:hover {
    background: rgba(16, 185, 129, 0.3);
    border-color: rgba(16, 185, 129, 0.5);
  }

  /* Sequences Grid (placeholder) */
  .sequences-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: var(--spacing-md);
  }

  .sequence-card {
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    color: rgba(255, 255, 255, 0.9);
  }
</style>
