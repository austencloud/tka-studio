<!-- Shared header used by construct pickers (start positions & options) -->
<script lang="ts">
  import type { GridMode, IHapticFeedbackService } from "$shared";
  import { GridMode as GridModeEnum, resolve, TYPES } from "$shared";
  import SimpleAdvancedToggle from "../../start-position-picker/components/SimpleAdvancedToggle.svelte";
  import GridModeToggle from "./GridModeToggle.svelte";

  type HeaderVariant = "start" | "options";

  const {
    variant = "start",
    title = "",
    titleHtml = "",
    isAdvanced = false,
    currentGridMode = GridModeEnum.BOX,
    onToggleAdvanced,
    onGridModeChange,
    onOpenFilters,
  }: {
    variant?: HeaderVariant;
    title?: string;
    titleHtml?: string;
    isAdvanced?: boolean;
    currentGridMode?: GridMode;
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
  <div class="header-left">
    {#if variant === "start"}
      <SimpleAdvancedToggle isAdvanced={isAdvanced} onToggle={handleAdvancedToggle} />
    {/if}
  </div>

  <div class="header-center">
    {#if titleHtml}
      <span class="header-title rich" aria-live="polite">{@html titleHtml}</span>
    {:else if title}
      <span class="header-title">{title}</span>
    {/if}
  </div>

  <div class="header-right">
    {#if variant === "start"}
      <GridModeToggle currentGridMode={currentGridMode} onGridModeChange={onGridModeChange} />
    {:else}
      <button
        class="filter-button"
        onclick={handleFilterClick}
        aria-label="Open filter options"
        title="Filter options"
      >
        <i class="fas fa-filter"></i>
      </button>
    {/if}
  </div>
</div>

<style>
  .construct-picker-header {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.02) 100%);
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .header-left,
  .header-right {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    min-height: 32px;
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

  .filter-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    width: 40px;
    height: 40px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.85);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    font-size: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }

  @media (hover: hover) {
    .filter-button:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: scale(1.05);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
      color: rgba(147, 197, 253, 1);
    }
  }

  .filter-button:active {
    transform: scale(0.95);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @media (max-width: 600px) {
    .filter-button {
      width: 36px;
      height: 36px;
      font-size: 0.9rem;
    }

    .header-left,
    .header-right {
      min-height: 28px;
    }
  }
</style>
