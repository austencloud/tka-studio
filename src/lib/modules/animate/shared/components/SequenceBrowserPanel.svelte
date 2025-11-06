<!--
  SequenceBrowserPanel.svelte - Sequence Selection Panel

  A slide-in panel for selecting sequences to animate.
  Reuses Explore module's sequence grid/display logic.

  Props:
  - mode: Which sequence slot we're filling (primary, secondary, grid-0, etc.)
  - onSelect: Callback when sequence is selected
  - onClose: Callback to close the panel
-->
<script lang="ts">
  import { Drawer, type SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { IExploreLoader } from "../../../explore/display";
  import { onMount } from "svelte";

  // Props
  let {
    mode = "primary",
    show = false,
    onSelect = (sequence: SequenceData) => {},
    onClose = () => {},
  }: {
    mode: "primary" | "secondary" | "grid-0" | "grid-1" | "grid-2" | "grid-3";
    show?: boolean;
    onSelect?: (sequence: SequenceData) => void;
    onClose?: () => void;
  } = $props();

  // Services
  let loaderService = resolve(TYPES.IExploreLoader) as IExploreLoader;

  // State
  let sequences = $state<SequenceData[]>([]);
  let isLoading = $state(true);
  let error = $state<string | null>(null);
  let searchQuery = $state("");

  // Filtered sequences based on search
  const filteredSequences = $derived.by(() => {
    if (!searchQuery.trim()) return sequences;

    const query = searchQuery.toLowerCase();
    return sequences.filter(
      (seq) =>
        seq.word?.toLowerCase().includes(query) ||
        seq.name?.toLowerCase().includes(query) ||
        seq.author?.toLowerCase().includes(query)
    );
  });

  // Load sequences
  async function loadSequences() {
    try {
      isLoading = true;
      error = null;
      console.log("🔍 SequenceBrowserPanel: Loading sequences...");

      const loaded = await loaderService.loadSequenceMetadata();
      sequences = loaded;

      console.log(`✅ SequenceBrowserPanel: Loaded ${loaded.length} sequences`);
    } catch (err) {
      console.error("❌ SequenceBrowserPanel: Failed to load sequences:", err);
      error = err instanceof Error ? err.message : "Failed to load sequences";
    } finally {
      isLoading = false;
    }
  }

  // Handle sequence selection
  function handleSelect(sequence: SequenceData) {
    console.log("✅ SequenceBrowserPanel: Sequence selected:", sequence.id);
    onSelect(sequence);
    onClose();
  }

  // Load on mount
  onMount(() => {
    loadSequences();
  });

  // Mode label
  const modeLabel = $derived.by(() => {
    switch (mode) {
      case "primary":
        return "Primary Sequence";
      case "secondary":
        return "Secondary Sequence";
      case "grid-0":
        return "Grid Position 1 (Top-Left)";
      case "grid-1":
        return "Grid Position 2 (Top-Right)";
      case "grid-2":
        return "Grid Position 3 (Bottom-Left)";
      case "grid-3":
        return "Grid Position 4 (Bottom-Right)";
      default:
        return "Select Sequence";
    }
  });
</script>

<Drawer
  isOpen={show}
  onclose={onClose}
  position="right"
  class="sequence-browser-panel"
  labelledBy="sequence-browser-title"
>
  <div class="browser-content">
    <!-- Header -->
    <div class="browser-header">
      <button class="close-button" onclick={onClose} aria-label="Close">
        <i class="fas fa-times"></i>
      </button>
      <h2 id="sequence-browser-title">{modeLabel}</h2>
    </div>

    <!-- Search Bar -->
    <div class="search-container">
      <i class="fas fa-search search-icon"></i>
      <input
        type="text"
        class="search-input"
        placeholder="Search sequences..."
        bind:value={searchQuery}
      />
      {#if searchQuery}
        <button
          class="clear-search"
          onclick={() => (searchQuery = "")}
          aria-label="Clear search"
        >
          <i class="fas fa-times"></i>
        </button>
      {/if}
    </div>

    <!-- Sequence Grid -->
    <div class="sequence-grid-container">
      {#if isLoading}
        <div class="loading-state">
          <div class="spinner"></div>
          <p>Loading sequences...</p>
        </div>
      {:else if error}
        <div class="error-state">
          <i class="fas fa-exclamation-triangle"></i>
          <p>{error}</p>
          <button onclick={loadSequences}>Retry</button>
        </div>
      {:else if filteredSequences.length === 0}
        <div class="empty-state">
          <i class="fas fa-search"></i>
          <p>No sequences found</p>
        </div>
      {:else}
        <div class="sequence-grid">
          {#each filteredSequences as sequence (sequence.id)}
            <button class="sequence-card" onclick={() => handleSelect(sequence)}>
              <div class="sequence-thumbnail">
                <!-- TODO: Add actual thumbnail rendering -->
                <div class="placeholder-thumbnail">
                  <i class="fas fa-layer-group"></i>
                </div>
              </div>
              <div class="sequence-info">
                <div class="sequence-word">{sequence.word || "Untitled"}</div>
                <div class="sequence-meta">
                  {#if sequence.beats}
                    {sequence.beats.length} beats
                  {/if}
                  {#if sequence.author}
                    • {sequence.author}
                  {/if}
                </div>
              </div>
            </button>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</Drawer>

<style>
  :global(.sequence-browser-panel) {
    max-width: 500px;
  }

  .browser-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  /* Header */
  .browser-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .browser-header h2 {
    flex: 1;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .close-button {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Search */
  .search-container {
    position: relative;
    padding: var(--spacing-md) var(--spacing-lg);
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .search-icon {
    position: absolute;
    left: calc(var(--spacing-lg) + var(--spacing-md));
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.5;
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    padding-left: calc(var(--spacing-xl) + var(--spacing-sm));
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    color: white;
    font-size: 0.875rem;
  }

  .search-input:focus {
    outline: none;
    border-color: rgba(236, 72, 153, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .clear-search {
    position: absolute;
    right: calc(var(--spacing-lg) + var(--spacing-sm));
    top: 50%;
    transform: translateY(-50%);
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    opacity: 0.7;
    transition: all 0.2s ease;
  }

  .clear-search:hover {
    opacity: 1;
    background: rgba(255, 255, 255, 0.2);
  }

  /* Grid Container */
  .sequence-grid-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--spacing-lg);
  }

  .sequence-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: var(--spacing-md);
  }

  .sequence-card {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-sm);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
  }

  .sequence-card:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(236, 72, 153, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
  }

  .sequence-thumbnail {
    aspect-ratio: 1;
    border-radius: var(--border-radius-sm);
    overflow: hidden;
    margin-bottom: var(--spacing-sm);
  }

  .placeholder-thumbnail {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
    color: rgba(255, 255, 255, 0.5);
    font-size: 2rem;
  }

  .sequence-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .sequence-word {
    font-weight: 600;
    font-size: 0.875rem;
    color: white;
  }

  .sequence-meta {
    font-size: 0.75rem;
    opacity: 0.6;
  }

  /* Loading/Error/Empty States */
  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    gap: var(--spacing-md);
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-state i,
  .error-state i,
  .empty-state i {
    font-size: 3rem;
    opacity: 0.3;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: #ec4899;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .error-state button {
    padding: var(--spacing-sm) var(--spacing-lg);
    background: rgba(236, 72, 153, 0.2);
    border: 1px solid rgba(236, 72, 153, 0.3);
    border-radius: var(--border-radius-md);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .error-state button:hover {
    background: rgba(236, 72, 153, 0.3);
  }
</style>
