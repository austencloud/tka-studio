<script lang="ts">
  import { fade } from "svelte/transition";
  import LoadingSpinner from "../LoadingSpinner.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    isLoading = false,
    error = null,
    isEmpty = false,
    sequencesLength = 0,
    sortedSequencesLength = 0,
    onRetry = () => {},
    onBackToFilters = () => {},
  } = $props<{
    isLoading?: boolean;
    error?: string | null;
    isEmpty?: boolean;
    sequencesLength?: number;
    sortedSequencesLength?: number;
    onRetry?: () => void;
    onBackToFilters?: () => void;
  }>();

  function handleRetry() {
    onRetry();
  }

  function handleBackToFilters() {
    onBackToFilters();
  }
</script>

{#if isLoading}
  <div class="loading-container" transition:fade>
    <LoadingSpinner />
    <p>Loading sequences...</p>
  </div>
{:else if error}
  <div class="error-state" transition:fade>
    <div class="error-content">
      <div class="error-icon">⚠️</div>
      <h3>Error Loading Sequences</h3>
      <p>{error}</p>
      <button class="retry-button" onclick={handleRetry}> Try Again </button>
    </div>
  </div>
{:else if isEmpty}
  <div class="empty-state">
    <div class="empty-content">
      <div class="empty-icon">📭</div>
      <h3>No sequences found</h3>
      <p>Try adjusting your filter criteria or browse all sequences.</p>
      <p>
        Debug: sequences.length = {sequencesLength}, sortedSequences.length = {sortedSequencesLength}
      </p>
      <button
        class="browse-all-button"
        onclick={handleBackToFilters}
        type="button"
      >
        Browse All Sequences
      </button>
    </div>
  </div>
{/if}

<style>
  .loading-container,
  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: var(--spacing-md);
    color: var(--muted-foreground);
  }

  .error-content {
    text-align: center;
    max-width: 400px;
  }

  .error-icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
  }

  .error-content h3 {
    font-size: var(--font-size-xl);
    color: var(--foreground);
    margin-bottom: var(--spacing-sm);
  }

  .retry-button {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: var(--gradient-primary);
    border: none;
    border-radius: 8px;
    color: white;
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .retry-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  .empty-content {
    text-align: center;
    max-width: 400px;
  }

  .empty-icon {
    font-size: 4rem;
    margin-bottom: var(--spacing-lg);
  }

  .empty-content h3 {
    font-size: var(--font-size-xl);
    color: var(--foreground);
    margin-bottom: var(--spacing-md);
  }

  .empty-content p {
    color: var(--muted-foreground);
    margin-bottom: var(--spacing-lg);
    line-height: 1.5;
  }

  .browse-all-button {
    padding: var(--spacing-md) var(--spacing-lg);
    background: var(--gradient-primary);
    border: none;
    border-radius: 8px;
    color: white;
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .browse-all-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  }
</style>
