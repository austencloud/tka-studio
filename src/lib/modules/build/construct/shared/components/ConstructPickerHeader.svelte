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
    isContinuousOnly = false,
    onToggleContinuous,
  }: {
    variant?: HeaderVariant;
    title?: string;
    titleHtml?: string;
    isAdvanced?: boolean;
    currentGridMode?: GridMode;
    onToggleAdvanced?: (isAdvanced: boolean) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
    isContinuousOnly?: boolean;
    onToggleContinuous?: (isContinuousOnly: boolean) => void;
  } = $props();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleAdvancedToggle(nextValue: boolean) {
    onToggleAdvanced?.(nextValue);
  }

  function handleContinuityToggle() {
    hapticService?.trigger("selection");
    onToggleContinuous?.(!isContinuousOnly);
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
        class="continuity-toggle"
        class:continuous={isContinuousOnly}
        onclick={handleContinuityToggle}
        aria-label={isContinuousOnly ? "Showing continuous options only. Click to show all options." : "Showing all options. Click to show continuous only."}
        title={isContinuousOnly ? "Continuous options" : "All options"}
      >
        {isContinuousOnly ? "Continuous" : "All"}
      </button>
    {/if}
  </div>
</div>

<style>
  .construct-picker-header {
    display: grid;
    grid-template-columns: minmax(0, auto) 1fr minmax(0, auto);
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
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
  }

  .header-title {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .header-title.rich :global(span) {
    white-space: nowrap;
  }

  .continuity-toggle {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    padding: 6px 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.85);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }

  .continuity-toggle.continuous {
    background: rgba(59, 130, 246, 0.25);
    color: rgba(255, 255, 255, 0.95);
    border-color: rgba(59, 130, 246, 0.45);
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.25);
  }

  @media (hover: hover) {
    .continuity-toggle:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: scale(1.05);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .continuity-toggle.continuous:hover {
      background: rgba(59, 130, 246, 0.35);
    }
  }

  .continuity-toggle:active {
    transform: scale(0.95);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @media (max-width: 600px) {
    .construct-picker-header {
      padding: 8px 12px;
      gap: 10px;
    }

    .continuity-toggle {
      padding: 5px 12px;
      font-size: 0.7rem;
    }

    .header-left,
    .header-right {
      min-height: 28px;
    }
  }
</style>
