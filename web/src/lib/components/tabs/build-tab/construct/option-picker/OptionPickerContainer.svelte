<!--
OptionPickerContainer.svelte - Simplified UI-only component

Clean, minimal component that focuses only on UI concerns:
- No business logic or reactive effects that cause infinite loops
- Simple props-based interface
- Responsive container dimensions tracking only
-->
<script lang="ts">
  import type { PictographData } from "$domain";
  import { onMount } from "svelte";
  import ErrorBanner from "../../shared/ErrorBanner.svelte";
  import LoadingOverlay from "../../shared/LoadingOverlay.svelte";
  import OptionPickerHeader from "./OptionPickerHeader.svelte";
  import OptionPickerScroll from "./OptionPickerScroll.svelte";

  // Props - all data comes from parent, no business logic here
  const {
    onOptionSelected = () => {},
    initialSequence = [],
    // UI state props (passed from parent)
    isLoading = false,
    error = null,
    filteredOptions = [],
    sortMethod = "alphabetical",
    reversalFilter = "all",
    layout = null,
    // Event handlers (passed from parent)
    onSortMethodChanged = () => {},
    onReversalFilterChanged = () => {},
    onRetryLoading = () => {},
  } = $props<{
    onOptionSelected?: (option: PictographData) => void;
    initialSequence?: PictographData[];
    // UI state
    isLoading?: boolean;
    error?: string | null;
    filteredOptions?: PictographData[];
    sortMethod?: string;
    reversalFilter?: string;
    layout?: any;
    // Event handlers
    onSortMethodChanged?: (method: string) => void;
    onReversalFilterChanged?: (filter: string) => void;
    onRetryLoading?: () => void;
  }>();

  // Component state (UI concerns only)
  let containerElement: HTMLElement;
  let containerWidth = $state(800);
  let containerHeight = $state(600);

  // Initialize component - UI only, no business logic
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
</script>

<div
  class="option-picker-container"
  bind:this={containerElement}
  data-testid="option-picker-container"
>
  <!-- Header with sorting controls -->
  <OptionPickerHeader
    {sortMethod}
    {reversalFilter}
    {onSortMethodChanged}
    {onReversalFilterChanged}
  />

  <!-- Error banner -->
  {#if error}
    <ErrorBanner message={error} onDismiss={() => {}} />
  {/if}

  <!-- Main content -->
  <div class="option-picker-content">
    {#if isLoading}
      <LoadingOverlay message="Loading options..." />
    {:else if error}
      <div class="error-state">
        <p>Error loading options: {error}</p>
        <button onclick={onRetryLoading}> Retry </button>
      </div>
    {:else if filteredOptions.length === 0}
      <div class="empty-state">
        <p>No options available for the current sequence.</p>
      </div>
    {:else}
      <OptionPickerScroll
        pictographs={filteredOptions}
        onPictographSelected={onOptionSelected}
        {containerWidth}
        {containerHeight}
        {layout}
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
    background: var(--background);
    border-radius: var(--border-radius);
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
    color: var(--text-muted);
  }

  .error-state button {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
  }

  .error-state button:hover {
    background: var(--primary-color-hover);
  }
</style>
