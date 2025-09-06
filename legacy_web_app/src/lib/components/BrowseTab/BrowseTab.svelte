<!-- src/lib/components/BrowseTab/BrowseTab.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { browseTabStore, selectedSequenceData } from '$lib/stores/browseTab/browseTabStore';
  import FilterPanel from './FilterPanel/FilterPanel.svelte';
  import SequenceGrid from './SequenceGrid/SequenceGrid.svelte';
  import SequenceViewer from './SequenceViewer/SequenceViewer.svelte';
  import DeleteConfirmationDialog from './DeleteConfirmationDialog.svelte';
  import LoadingSpinner from '$lib/components/MainWidget/loading/LoadingSpinner.svelte';

  // State for delete confirmation dialog
  let showDeleteDialog = false;
  let deleteType: 'sequence' | 'variation' = 'variation';
  let sequenceToDelete: string | null = null;
  let variationToDelete: string | null = null;

  // Handle sequence selection
  function handleSequenceSelect(event: CustomEvent<string>) {
    browseTabStore.selectSequence(event.detail);
  }

  // Handle variation selection
  function handleVariationSelect(event: CustomEvent<number>) {
    browseTabStore.selectVariation(event.detail);
  }

  // Handle favorite toggle
  function handleFavoriteToggle(event: CustomEvent<{sequenceId: string, variationId: string}>) {
    const { sequenceId, variationId } = event.detail;
    browseTabStore.toggleFavorite(sequenceId, variationId);
  }

  // Handle delete request
  function handleDeleteRequest(event: CustomEvent<{type: 'sequence' | 'variation', sequenceId: string, variationId?: string}>) {
    const { type, sequenceId, variationId } = event.detail;

    deleteType = type;
    sequenceToDelete = sequenceId;
    variationToDelete = variationId || null;

    showDeleteDialog = true;
  }

  // Handle delete confirmation
  function handleDeleteConfirm() {
    if (deleteType === 'sequence' && sequenceToDelete) {
      browseTabStore.deleteSequence(sequenceToDelete);
    } else if (deleteType === 'variation' && sequenceToDelete && variationToDelete) {
      browseTabStore.deleteVariation(sequenceToDelete, variationToDelete);
    }

    showDeleteDialog = false;
  }

  // Handle delete cancellation
  function handleDeleteCancel() {
    showDeleteDialog = false;
  }

  // Load initial data on mount
  onMount(() => {
    browseTabStore.loadInitialData();
  });
</script>

<div class="browse-tab">
  <div class="browse-tab-content">
    <!-- Left side: Filter panel -->
    <div class="filter-panel-container">
      <FilterPanel />
    </div>

    <!-- Middle: Sequence grid -->
    <div class="sequence-grid-container">
      {#if $browseTabStore.isLoading}
        <div class="loading-container">
          <LoadingSpinner size="large" />
          <p>Loading sequences...</p>
        </div>
      {:else if $browseTabStore.error}
        <div class="error-container">
          <p class="error-message">{$browseTabStore.error}</p>
          <button class="retry-button" on:click={() => browseTabStore.loadInitialData()}>
            Retry
          </button>
        </div>
      {:else}
        <SequenceGrid on:selectSequence={handleSequenceSelect} />
      {/if}
    </div>

    <!-- Right side: Sequence viewer (only shown when a sequence is selected) -->
    <div class="sequence-viewer-container" class:hidden={!$selectedSequenceData.sequence}>
      {#if $selectedSequenceData.sequence && $selectedSequenceData.variation}
        <SequenceViewer
          on:selectVariation={handleVariationSelect}
          on:toggleFavorite={handleFavoriteToggle}
          on:deleteRequest={handleDeleteRequest}
        />
      {/if}
    </div>
  </div>

  <!-- Delete confirmation dialog -->
  {#if showDeleteDialog}
    <DeleteConfirmationDialog
      type={deleteType}
      sequenceName={$selectedSequenceData.sequence?.word || ''}
      on:confirm={handleDeleteConfirm}
      on:cancel={handleDeleteCancel}
    />
  {/if}
</div>

<style>
  .browse-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background-color: var(--background-color, #1e1e1e);
    color: var(--text-color, #ffffff);
  }

  .browse-tab-content {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  .filter-panel-container {
    width: 250px;
    border-right: 1px solid var(--border-color, #333333);
    overflow-y: auto;
  }

  .sequence-grid-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    position: relative;
  }

  .sequence-viewer-container {
    width: 350px;
    border-left: 1px solid var(--border-color, #333333);
    overflow-y: auto;
    transition: transform 0.3s ease;
  }

  .sequence-viewer-container.hidden {
    transform: translateX(100%);
    position: absolute;
    right: 0;
    height: 100%;
  }

  .loading-container,
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 2rem;
    text-align: center;
  }

  .error-message {
    color: var(--error-color, #ff5555);
    margin-bottom: 1rem;
  }

  .retry-button {
    padding: 0.5rem 1rem;
    background-color: var(--primary-color, #4a90e2);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  .retry-button:hover {
    background-color: var(--primary-color-hover, #3a80d2);
  }

  /* Responsive layout */
  @media (max-width: 768px) {
    .browse-tab-content {
      flex-direction: column;
    }

    .filter-panel-container {
      width: 100%;
      height: auto;
      border-right: none;
      border-bottom: 1px solid var(--border-color, #333333);
    }

    .sequence-viewer-container {
      width: 100%;
      border-left: none;
      border-top: 1px solid var(--border-color, #333333);
    }

    .sequence-viewer-container.hidden {
      display: none;
    }
  }
</style>
