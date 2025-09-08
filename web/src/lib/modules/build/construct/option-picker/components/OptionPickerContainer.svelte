<!--
OptionPickerContainer.svelte - Simplified UI-only component

Clean, minimal component that focuses only on UI concerns:
- No business logic or reactive effects that cause infinite loops
- Simple props-based interface
- Responsive container dimensions tracking only
-->
<script lang="ts">
  import type { PictographData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import ErrorBanner from '../../../shared/components/ErrorBanner.svelte';
  import LoadingOverlay from '../../../shared/components/LoadingOverlay.svelte';
  import type { IOptionPickerServiceAdapter } from "../services/contracts";
  import { createOptionPickerState } from "../state/option-picker-state.svelte";
  import OptionPickerHeader from "./OptionPickerHeader.svelte";
  import OptionPickerScroll from "./OptionPickerScroll.svelte";
// Create services directly since they're not in DI container yet
  import { OptionPickerErrorHandler } from "../services/implementations/OptionPickerErrorHandler";
  import { OptionPickerStateValidator } from "../services/implementations/OptionPickerStateValidator";

  // Props
  interface Props {
    onOptionSelected: (option: PictographData) => void;
    currentSequence?: PictographData[];
  }

  let { onOptionSelected, currentSequence = [] }: Props = $props();

  // Services
  const optionPickerService = resolve(
    TYPES.IOptionPickerServiceAdapter
  ) as IOptionPickerServiceAdapter;
  const errorHandler = new OptionPickerErrorHandler();
  const validator = new OptionPickerStateValidator();

  const optionPickerState = createOptionPickerState({
    optionPickerService,
    errorHandler,
    validator
  });

  // Component state (UI concerns only)
  let containerElement: HTMLElement;
  let containerWidth = $state(800);
  let containerHeight = $state(600);
  let isContainerReady = $state(false);

  // Initialize component and load options
  onMount(() => {
    // Set up resize observer for responsive behavior
    if (containerElement) {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          containerWidth = entry.contentRect.width;
          containerHeight = entry.contentRect.height;

          // Mark container as ready after first measurement
          if (!isContainerReady && containerWidth > 0 && containerHeight > 0) {
            isContainerReady = true;
          }

          // Only recalculate layout if container is ready
          if (isContainerReady) {
            optionPickerState.recalculateLayout(containerWidth, containerHeight);
          }
        }
      });
      resizeObserver.observe(containerElement);

      // Force initial measurement
      const rect = containerElement.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        containerWidth = rect.width;
        containerHeight = rect.height;
        isContainerReady = true;
        optionPickerState.recalculateLayout(containerWidth, containerHeight);
      }

      return () => resizeObserver.disconnect();
    }
  });

  // Load options when sequence changes
  $effect(() => {
    if (isContainerReady && currentSequence && containerWidth > 0 && containerHeight > 0) {
      console.log("🔍 OptionPickerContainer: Loading options for sequence:", currentSequence.length);
      optionPickerState.loadOptionsForSequence(currentSequence, containerWidth, containerHeight);
    }
  });

  // Handle option selection
  async function handleOptionSelected(option: PictographData) {
  try {
    await optionPickerState.selectOption(option);
    onOptionSelected(option);
  } catch (error) {
    console.error("Failed to select option:", error);
  }
  }
</script>

<div
  class="option-picker-container"
  bind:this={containerElement}
  data-testid="option-picker-container"
>
  <!-- Header with sorting controls -->
  <OptionPickerHeader
  sortMethod={optionPickerState.sortMethod}
  reversalFilter={optionPickerState.reversalFilter}
  onSortMethodChanged={optionPickerState.setSortMethod}
  onReversalFilterChanged={optionPickerState.setReversalFilter}
  />

  <!-- Error banner -->
  {#if optionPickerState.error}
  <ErrorBanner message={optionPickerState.error?.userMessage || "An error occurred"} onDismiss={optionPickerState.clearError} />
  {/if}

  <!-- Main content -->
  <div class="option-picker-content">
  {#if !isContainerReady}
    <LoadingOverlay message="Initializing container..." />
  {:else if optionPickerState.isLoading}
    <LoadingOverlay message="Loading options..." />
  {:else if optionPickerState.error}
    <div class="error-state">
    <p>Error loading options: {optionPickerState.error}</p>
    <button onclick={() => optionPickerState.retryLastOperation()}> Retry </button>
    </div>
  {:else if optionPickerState.filteredOptions.length === 0}
    <div class="empty-state">
    <p>No options available for the current sequence.</p>
    </div>
  {:else}
    <OptionPickerScroll
    pictographs={optionPickerState.filteredOptions}
    onPictographSelected={handleOptionSelected}
    {containerWidth}
    {containerHeight}
    layout={optionPickerState.layout}
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

  /* Beautiful glassmorphism background */
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05),
    rgba(255, 255, 255, 0.02)
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);

  overflow: hidden;
  }

  .option-picker-content {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.02);
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
