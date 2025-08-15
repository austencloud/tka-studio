<script lang="ts">
  /**
   * Simple Pictograph Selector Component
   * Shows actual rendered pictographs in a simple grid layout
   */

  import type { PictographData } from "$lib/domain/PictographData";
  import Pictograph from "$lib/components/pictograph/Pictograph.svelte";
  import { createCodexState } from "$lib/state/codex-state.svelte";

  // Props
  interface Props {
    onPictographSelected?: (pictograph: PictographData) => void;
    selectedPictograph?: PictographData | null;
  }

  let { onPictographSelected, selectedPictograph }: Props = $props();

  // Create codex state using runes
  const codexState = createCodexState();

  // Reactive values - get all pictographs as a flat array
  let allPictographs = $derived(() => {
    const byLetter = codexState.filteredPictographsByLetter();
    return Object.values(byLetter).flat();
  });
  let isLoading = $derived(codexState.isLoading);
  let error = $derived(codexState.error);

  // Methods
  function handlePictographClick(pictograph: PictographData) {
    onPictographSelected?.(pictograph);
  }

  function isSelected(pictograph: PictographData): boolean {
    return selectedPictograph?.id === pictograph.id;
  }
</script>

<div class="simple-pictograph-selector">
  <div class="selector-header">
    <h3>📚 Pictograph Selection</h3>
    <div class="pictograph-count">
      {#if isLoading}
        Loading...
      {:else}
        {allPictographs().length} pictographs
      {/if}
    </div>
  </div>

  {#if error}
    <div class="error-message">
      <p>❌ Error loading pictographs: {error}</p>
    </div>
  {:else if isLoading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading pictographs...</p>
    </div>
  {:else}
    <div class="pictographs-scroll">
      <div class="pictographs-grid">
        {#each allPictographs() as pictograph}
          {#if pictograph}
            <button
              class="pictograph-button"
              class:selected={isSelected(pictograph)}
              onclick={() => handlePictographClick(pictograph)}
              title="Letter: {pictograph.letter}"
            >
              <div class="pictograph-container">
                <Pictograph
                  pictographData={pictograph}
                  debug={false}
                  showLoadingIndicator={false}
                />
              </div>
            </button>
          {/if}
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .simple-pictograph-selector {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    overflow: hidden;
  }

  .selector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .selector-header h3 {
    color: #fbbf24;
    margin: 0;
    font-size: 1.1rem;
  }

  .pictograph-count {
    color: #c7d2fe;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .error-message {
    padding: 20px;
    text-align: center;
  }

  .error-message p {
    color: #f87171;
    margin: 0;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    gap: 16px;
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid #fbbf24;
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

  .loading-state p {
    color: #c7d2fe;
    margin: 0;
  }

  .pictographs-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
  }

  .pictographs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }

  .pictograph-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    aspect-ratio: 1;
  }

  .pictograph-container {
    flex: 1;
    margin: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 4px;
  }

  .pictograph-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .pictograph-button.selected {
    background: rgba(251, 191, 36, 0.2);
    border-color: #fbbf24;
    box-shadow: 0 0 0 2px rgba(251, 191, 36, 0.3);
  }

  .pictograph-label {
    color: #c7d2fe;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: center;
    min-height: 1.2em;
  }

  .pictograph-button.selected .pictograph-label {
    color: #fbbf24;
    font-weight: 600;
  }
</style>
