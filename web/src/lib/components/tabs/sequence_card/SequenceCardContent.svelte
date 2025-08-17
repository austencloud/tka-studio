<!-- SequenceCardContent.svelte - Content area for sequence cards -->
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
  }

  let {
    sequences = [],
    columnCount: _columnCount,
    isLoading: _isLoading,
    selectedLength: _selectedLength,
  }: Props = $props();

  // State
  let loading = $state(false);
  let error = $state<string | null>(null);

  // Lifecycle
  onMount(() => {
    // Component mounted
  });

  // Actions
  function handleSequenceSelect(sequence: SequenceData) {
    console.log("Selected sequence:", sequence);
  }
</script>

<!-- Content -->
<div class="sequence-card-content">
  {#if loading}
    <div class="loading">Loading sequences...</div>
  {:else if error}
    <div class="error">Error: {error}</div>
  {:else if sequences.length === 0}
    <div class="empty">
      <div class="empty-icon">📝</div>
      <p>No sequences available</p>
    </div>
  {:else}
    <div class="sequence-grid">
      {#each sequences as sequence (sequence.id)}
        <SequenceCard
          {sequence}
          onclick={() => handleSequenceSelect(sequence)}
        />
      {/each}
    </div>
  {/if}
</div>

<style>
  .sequence-card-content {
    padding: 1rem;
    height: 100%;
    overflow-y: auto;
  }

  .loading,
  .error,
  .empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    text-align: center;
  }

  .error {
    color: var(--color-error, #ef4444);
  }

  .empty {
    color: var(--color-text-muted, #6b7280);
  }

  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.7;
  }

  .sequence-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
    padding: 1rem 0;
  }
</style>
