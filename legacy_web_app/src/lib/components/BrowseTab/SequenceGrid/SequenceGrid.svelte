<!-- src/lib/components/BrowseTab/SequenceGrid/SequenceGrid.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { groupedSequences, browseTabStore } from '$lib/stores/browseTab/browseTabStore';
  import SectionHeader from './SectionHeader.svelte';
  import Thumbnail from './Thumbnail.svelte';

  // Create event dispatcher
  const dispatch = createEventDispatcher<{
    selectSequence: string;
  }>();

  // Handle thumbnail click
  function handleThumbnailClick(sequenceId: string) {
    dispatch('selectSequence', sequenceId);
  }
</script>

<div class="sequence-grid">
  {#if $groupedSequences.length === 0}
    <div class="empty-state">
      <p>No sequences match the current filter criteria.</p>
      <button class="reset-button" on:click={() => browseTabStore.applyFilter({ type: 'all' })}>
        Reset Filters
      </button>
    </div>
  {:else}
    {#each $groupedSequences as group}
      <div class="sequence-section">
        <SectionHeader title={group.section} />

        <div class="thumbnails-container">
          {#each group.sequences as sequence}
            <Thumbnail
              sequence={sequence}
              isSelected={$browseTabStore.selectedSequenceId === sequence.id}
              on:click={() => handleThumbnailClick(sequence.id)}
            />
          {/each}
        </div>
      </div>
    {/each}
  {/if}
</div>

<style>
  .sequence-grid {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .sequence-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .thumbnails-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
    background-color: var(--background-color-secondary, #252525);
    border-radius: 8px;
  }

  .empty-state p {
    margin-bottom: 1rem;
    color: var(--text-color-secondary, #aaaaaa);
  }

  .reset-button {
    padding: 0.5rem 1rem;
    background-color: var(--primary-color, #4a90e2);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  .reset-button:hover {
    background-color: var(--primary-color-hover, #3a80d2);
  }

  /* Responsive layout */
  @media (max-width: 768px) {
    .thumbnails-container {
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    }
  }

  @media (max-width: 480px) {
    .thumbnails-container {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
  }
</style>
