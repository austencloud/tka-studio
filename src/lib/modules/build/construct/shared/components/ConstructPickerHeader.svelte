<!-- Shared header used by construct pickers (start positions & options) -->
<script lang="ts">
  import type { GridMode, IHapticFeedbackService } from "$shared";
  import { GridMode as GridModeEnum, resolve, TYPES } from "$shared";
  import SimpleAdvancedToggle from "../../start-position-picker/components/SimpleAdvancedToggle.svelte";
  import GridModeToggle from "./GridModeToggle.svelte";
  import { swipeGesture } from "$shared/utils/swipeGesture";

  type HeaderVariant = "start" | "options";

  const {
    variant = "start",
    title = "",
    titleHtml = "",
    isAdvanced = false,
    currentGridMode = GridModeEnum.BOX,
    isContinuousOnly = false,
    isFilterPanelOpen = false,
    onToggleAdvanced,
    onGridModeChange,
    onOpenFilters,
  }: {
    variant?: HeaderVariant;
    title?: string;
    titleHtml?: string;
    isAdvanced?: boolean;
    currentGridMode?: GridMode;
    isContinuousOnly?: boolean;
    isFilterPanelOpen?: boolean;
    onToggleAdvanced?: (isAdvanced: boolean) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
    onOpenFilters?: () => void;
  } = $props();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleAdvancedToggle(nextValue: boolean) {
    onToggleAdvanced?.(nextValue);
  }

  function handleFilterClick() {
    hapticService?.trigger("selection");
    onOpenFilters?.();
  }
</script>

<div class="construct-picker-header" data-variant={variant}>
  {#if variant === "start"}
    <!-- Start variant: traditional 3-column layout -->
    <div class="header-left">
      <SimpleAdvancedToggle isAdvanced={isAdvanced} onToggle={handleAdvancedToggle} />
    </div>

    <div class="header-center">
      {#if titleHtml}
        <span class="header-title rich" aria-live="polite">{@html titleHtml}</span>
      {:else if title}
        <span class="header-title">{title}</span>
      {/if}
    </div>

    <div class="header-right">
      <GridModeToggle currentGridMode={currentGridMode} onGridModeChange={onGridModeChange} />
    </div>
  {:else if variant === "options"}
    <!-- Options variant: entire header is clickable -->
    <button
      class="options-header-button"
      onclick={handleFilterClick}
      use:swipeGesture={{ onSwipeDown: handleFilterClick }}
      aria-label="Open filter options - {titleHtml ? 'Type information' : title}"
      aria-expanded={isFilterPanelOpen}
    >
      <div class="header-left-spacer"></div>

      <div class="header-center-content">
        {#if titleHtml}
          <span class="header-title rich" aria-live="polite">{@html titleHtml}</span>
        {:else if title}
          <span class="header-title">{title}</span>
        {/if}
      </div>

      <div class="header-right-indicator">
        <i class="fas fa-chevron-down chevron" class:open={isFilterPanelOpen}></i>
      </div>
    </button>
  {/if}
</div>

<style>
  .construct-picker-header {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.02) 100%);
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 4px 8px;
  }

  /* Grid layout for start variant */
  .construct-picker-header[data-variant="start"] {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    gap: 8px;
  }

  /* Full-width layout for options variant */
  .construct-picker-header[data-variant="options"] {
    display: flex;
    align-items: stretch;
  }

  .header-left,
  .header-right {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    min-height: 44px;
  }

  .header-right {
    justify-content: flex-end;
  }

  .header-center {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-width: 0;
    overflow: visible;
    min-height: 44px;
  }

  .header-title {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    white-space: nowrap;
    overflow: visible;
  }

  .header-title.rich :global(span) {
    white-space: nowrap;
  }

  /* Options variant: full-width clickable header button */
  .options-header-button {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr);
    align-items: center;
    justify-items: stretch;
    width: 100%;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    margin: 0;
    min-height: 44px;
    color: inherit;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    position: relative;
    overflow: hidden;
  }

  /* Subtle shine effect on hover */
  .options-header-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.03) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
  }

  .header-left-spacer {
    /* Empty space for symmetry */
    grid-column: 1;
    min-width: 0;
  }

  .header-center-content {
    grid-column: 2;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-width: 0;
    overflow: visible;
    padding: 0 8px;
  }

  .header-right-indicator {
    grid-column: 3;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 12px;
    min-width: 0;
  }

  .chevron {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: center;
    line-height: 1;
  }

  .chevron.open {
    transform: rotate(180deg);
  }

  @media (hover: hover) {
    .options-header-button:hover::before {
      opacity: 1;
    }

    .options-header-button:hover {
      background: rgba(255, 255, 255, 0.04);
    }

    .options-header-button:hover .chevron {
      color: rgba(147, 197, 253, 1);
    }
  }

  .options-header-button:active {
    transform: scale(0.99);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Mobile optimizations */
  @media (max-width: 600px) {
    .construct-picker-header {
      padding: 2px 6px;
      gap: 4px;
    }

    .header-center-content {
      padding: 0 4px;
    }

    .header-right-indicator {
      padding: 0 8px;
    }

    .chevron {
      font-size: 0.7rem;
    }
  }
</style>
