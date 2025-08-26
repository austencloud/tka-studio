<!--
OptionPickerContainer.svelte - Main container for the option picker

Integrates all option picker components:
- Uses optionPickerRunes for state management
- Handles scrolling with OptionPickerScroll
- Manages layout responsively
- Coordinates with sequence state
-->
<script lang="ts">
  import ErrorBanner from "../../shared/ErrorBanner.svelte";
  import LoadingOverlay from "../../shared/LoadingOverlay.svelte";
  import OptionPickerHeader from "./components/OptionPickerHeader.svelte";
  import OptionPickerScroll from "./components/OptionPickerScroll.svelte";
  import type { PictographData } from "$lib/domain/PictographData";
  import { createErrorState } from "$lib/utils/error-handling.svelte";
  import { onMount } from "svelte";
  import { createOptionDataState } from "$lib/state/construct/option-picker/focused/option-data-state.svelte";
  import { createOptionUIState } from "$lib/state/construct/option-picker/focused/option-ui-state.svelte";
  import { createOptionFilterState } from "$lib/state/construct/option-picker/focused/option-filter-state.svelte";
  import { createOptionPersistenceState } from "$lib/state/construct/option-picker/focused/option-persistence-state.svelte";

  // Props
  const { onOptionSelected = () => {}, initialSequence = [] } = $props<{
    onOptionSelected?: (option: PictographData) => void;
    initialSequence?: PictographData[];
  }>();

  // Create microservice states
  const dataState = createOptionDataState();
  const uiState = createOptionUIState();
  const filterState = createOptionFilterState(dataState, uiState);
  const persistenceState = createOptionPersistenceState();
  const errorState = createErrorState();

  // Container dimensions for responsive layout
  let containerElement: HTMLElement;
  let containerWidth = $state(800);
  let containerHeight = $state(600);

  // Initialize component
  onMount(() => {
    // Set up resize observer for responsive behavior
    if (containerElement) {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          containerWidth = entry.contentRect.width;
          containerHeight = entry.contentRect.height;
        }
      });
      resizeObserver.observe(containerElement);

      return () => resizeObserver.disconnect();
    }
  });

  // Track if we've loaded to prevent infinite loop
  let hasLoadedInitialSequence = $state(false);

  // Load options when sequence changes - prevent infinite loop
  $effect(() => {
    if (initialSequence.length >= 0 && !hasLoadedInitialSequence) {
      hasLoadedInitialSequence = true;
      loadOptionsForSequence(initialSequence);
    }
  });

  // Coordinated loading logic (moved from composition layer)
  async function loadOptionsForSequence(sequence: PictographData[]) {
    try {
      errorState.clearError();
      dataState.setSequence(sequence);

      // Check for preloaded options first to avoid loading state
      const preloadedOptions = persistenceState.checkPreloadedOptions();
      if (preloadedOptions) {
        dataState.setOptions(preloadedOptions);
        uiState.setLoading(false);
        uiState.setError(null);

        // Set default tab if needed
        if (
          !uiState.lastSelectedTab[uiState.sortMethod] ||
          uiState.lastSelectedTab[uiState.sortMethod] === null
        ) {
          uiState.setLastSelectedTabForSort(uiState.sortMethod, "all");
        }
        return;
      }

      // Check for bulk preloaded options
      const targetEndPosition = persistenceState.getTargetEndPosition(sequence);
      if (targetEndPosition) {
        const bulkOptions =
          persistenceState.checkBulkPreloadedOptions(targetEndPosition);
        if (bulkOptions && bulkOptions.length > 0) {
          dataState.setOptions(bulkOptions);
          uiState.setLoading(false);
          uiState.setError(null);

          if (
            !uiState.lastSelectedTab[uiState.sortMethod] ||
            uiState.lastSelectedTab[uiState.sortMethod] === null
          ) {
            uiState.setLastSelectedTabForSort(uiState.sortMethod, "all");
          }
          return;
        }
      }

      // Load from services
      await dataState.loadOptionsFromServices(sequence);
    } catch (error) {
      errorState.setError(error, "OPTION_LOAD_FAILED");
    }
  }

  // Handle option selection
  async function handleOptionSelected(option: PictographData) {
    try {
      await dataState.selectOption(option);
      onOptionSelected(option);
    } catch (error) {
      errorState.setError(error, "OPTION_SELECT_FAILED");
    }
  }

  // Handle sort method changes
  function handleSortMethodChanged(method: string) {
    uiState.setSortMethod(method as any); // Type assertion for now
  }
</script>

<div
  class="option-picker-container"
  bind:this={containerElement}
  data-testid="option-picker-container"
>
  <!-- Header with sorting controls -->
  <OptionPickerHeader />

  <!-- Error banner -->
  {#if errorState.state.hasError}
    <ErrorBanner
      message={errorState.state.errorMessage || "An error occurred"}
      onDismiss={errorState.clearError}
    />
  {/if}

  <!-- Main content -->
  <div class="option-picker-content">
    {#if uiState.isLoading}
      <LoadingOverlay message="Loading options..." />
    {:else if uiState.error}
      <div class="error-state">
        <p>Error loading options: {uiState.error}</p>
        <button onclick={() => loadOptionsForSequence(initialSequence)}>
          Retry
        </button>
      </div>
    {:else if filterState.filteredOptions.length === 0}
      <div class="empty-state">
        <p>No options available for the current sequence.</p>
      </div>
    {:else}
      <OptionPickerScroll
        pictographs={filterState.filteredOptions}
        onPictographSelected={handleOptionSelected}
        {containerWidth}
        {containerHeight}
      />
    {/if}
  </div>
</div>

<style>
  .option-picker-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: transparent;
    overflow: hidden;
  }

  .option-picker-content {
    flex: 1;
    position: relative;
    overflow: hidden;
  }

  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: var(--spacing-xl);
    text-align: center;
    color: var(--muted-foreground);
  }

  .error-state button {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--primary);
    color: var(--primary-foreground);
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .error-state button:hover {
    background: var(--primary-hover);
  }
</style>
