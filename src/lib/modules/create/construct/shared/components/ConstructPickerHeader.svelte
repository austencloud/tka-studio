<!-- Shared header used by construct pickers (start positions & options) -->
<script lang="ts">
  import type { GridMode, IHapticFeedbackService } from "$shared";
  import { GridMode as GridModeEnum, resolve, TYPES } from "$shared";
  import SimpleAdvancedToggle from "../../start-position-picker/components/SimpleAdvancedToggle.svelte";
  import GridModeToggle from "./GridModeToggle.svelte";
  import { swipeGesture } from "$shared/utils/swipeGesture";

  type HeaderVariant = "start" | "options" | "sequential";

  const {
    variant = "start",
    title = "",
    titleHtml = "",
    isAdvanced = false,
    currentGridMode = GridModeEnum.BOX,
    isContinuousOnly = false,
    isFilterPanelOpen = false,
    compact = false,
    showNextHandButton = false,
    nextHandButtonText = "Build Red Hand",
    onToggleAdvanced,
    onGridModeChange,
    onOpenFilters,
    onBackClick,
    onNextHand,
  }: {
    variant?: HeaderVariant;
    title?: string;
    titleHtml?: string;
    isAdvanced?: boolean;
    currentGridMode?: GridMode;
    isContinuousOnly?: boolean;
    isFilterPanelOpen?: boolean;
    compact?: boolean;
    showNextHandButton?: boolean;
    nextHandButtonText?: string;
    onToggleAdvanced?: (isAdvanced: boolean) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
    onOpenFilters?: () => void;
    onBackClick?: () => void;
    onNextHand?: () => void;
  } = $props();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleAdvancedToggle(nextValue: boolean) {
    onToggleAdvanced?.(nextValue);
  }

  function handleFilterClick() {
    hapticService?.trigger("selection");
    onOpenFilters?.();
  }

  function handleBackClick() {
    hapticService?.trigger("selection");
    onBackClick?.();
  }

  function handleNextHandClick() {
    hapticService?.trigger("selection");
    onNextHand?.();
  }
</script>

<div class="construct-picker-header" data-variant={variant} class:compact={compact}>
  {#if variant === "start"}
    <!-- Start variant: traditional 3-column layout -->
    <div class="header-left">
      <SimpleAdvancedToggle isAdvanced={isAdvanced} onToggle={handleAdvancedToggle} />
    </div>

    <div class="header-center">
      <!-- Title now shown in TopBar instead of here -->
    </div>

    <div class="header-right">
      {#if onGridModeChange}
        <GridModeToggle currentGridMode={currentGridMode} onGridModeChange={onGridModeChange} />
      {/if}
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
  {:else if variant === "sequential"}
    <!-- Sequential variant: back button, title, optional next hand button -->
    <div class="header-left">
      <button class="back-button" onclick={handleBackClick} aria-label="Reset">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>

    <div class="header-center">
      <h1 class="header-title">{title}</h1>
    </div>

    <div class="header-right">
      {#if showNextHandButton}
        <button class="next-hand-button" onclick={handleNextHandClick}>
          {nextHandButtonText}
          <i class="fas fa-arrow-right"></i>
        </button>
      {/if}
    </div>
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

  /* Grid layout for sequential variant */
  .construct-picker-header[data-variant="sequential"] {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1rem;
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

  /* Compact mode: Reduced height for tight spaces */
  .construct-picker-header.compact {
    padding: 2px 6px;
  }

  .construct-picker-header.compact .header-left,
  .construct-picker-header.compact .header-right,
  .construct-picker-header.compact .header-center {
    min-height: 36px;
  }

  .construct-picker-header.compact .options-header-button {
    min-height: 36px;
  }

  .construct-picker-header.compact .header-title {
    font-size: 0.85rem;
  }

  .construct-picker-header.compact .chevron {
    font-size: 0.7rem;
  }

  .construct-picker-header.compact .header-right-indicator {
    padding: 0 10px;
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

  /* Sequential variant button styles */
  .back-button {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
  }

  @media (hover: hover) {
    .back-button:hover {
      background: rgba(255, 255, 255, 0.12);
      transform: translateX(-2px);
    }
  }

  .back-button:active {
    transform: scale(0.95);
  }

  .next-hand-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    white-space: nowrap;
  }

  @media (hover: hover) {
    .next-hand-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
  }

  .next-hand-button:active {
    transform: translateY(0);
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

    /* Sequential variant mobile adjustments */
    .construct-picker-header[data-variant="sequential"] {
      gap: 0.5rem;
    }

    .next-hand-button {
      padding: 0.625rem 1rem;
      font-size: 0.875rem;
    }

    /* Extra compact on mobile when compact mode is active */
    .construct-picker-header.compact {
      padding: 1px 4px;
    }

    .construct-picker-header.compact .header-left,
    .construct-picker-header.compact .header-right,
    .construct-picker-header.compact .header-center {
      min-height: 32px;
    }

    .construct-picker-header.compact .options-header-button {
      min-height: 32px;
    }

    .construct-picker-header.compact .header-title {
      font-size: 0.8rem;
    }
  }
</style>
