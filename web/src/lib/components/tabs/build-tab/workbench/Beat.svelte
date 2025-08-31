<!--
Beat.svelte - Beat Component Wrapper

This component wraps the Pictograph component and handles all beat-specific concerns:
- Beat numbering and labeling
- Start position detection and display
- Reversal indicators
- Beat selection state
- Beat-specific interactions

The wrapped Pictograph component focuses purely on rendering pictograph data.
-->
<script lang="ts">
  import type { BeatData } from "$domain";
  import { Pictograph } from "$lib/components/core/pictograph";

  interface Props {
    /** Beat data containing pictograph and beat-specific information */
    beat: BeatData;
    /** Beat index for fallback numbering */
    index?: number;
    /** Is this beat currently selected? */
    isSelected?: boolean;
    /** Is this beat currently hovered? */
    isHovered?: boolean;
    /** Click handler */
    onClick?: () => void;
    /** Beat container dimensions */
    width?: number;
    height?: number;
  }

  let {
    beat,
    index = 0,
    isSelected = false,
    isHovered = false,
    onClick,
    width = 200,
    height = 200,
  }: Props = $props();

  // =============================================================================
  // BEAT-SPECIFIC LOGIC
  // =============================================================================

  /** Determine if this is a start position based on beat properties */
  const isStartPosition = $derived(() => {
    // Start position can be determined by:
    // 1. beatNumber === 0 (common convention)
    // 2. Explicit metadata flag
    // 3. Special beat properties
    return beat.beatNumber === 0;
  });

  /** Get the display beat number */
  const displayBeatNumber = $derived(() => {
    return beat.beatNumber || index + 1;
  });

  /** Get aria label for accessibility */
  const ariaLabel = $derived(() => {
    if (isStartPosition()) {
      return "Start Position";
    }
    return `Beat ${displayBeatNumber()} ${beat.pictographData ? "Pictograph" : "Empty"}`;
  });

  // =============================================================================
  // EVENT HANDLERS
  // =============================================================================

  function handleClick() {
    onClick?.();
  }

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onClick?.();
    }
  }
</script>

<div
  class="beat-wrapper"
  class:selected={isSelected}
  class:hovered={isHovered}
  class:start-position={isStartPosition()}
  class:has-reversals={beat.blueReversal || beat.redReversal}
  style:width="{width}px"
  style:height="{height}px"
  onclick={handleClick}
  onkeypress={handleKeyPress}
  role="button"
  tabindex="0"
  aria-label={ariaLabel()}
>
  <!-- Main Pictograph (simplified - no beat-specific props) -->
  {#if beat.pictographData}
    <Pictograph pictographData={beat.pictographData} />
  {:else}
    <!-- Empty beat state -->
    <div class="empty-beat" style:width="{width}px" style:height="{height}px">
      <div class="empty-beat-content">
        {displayBeatNumber()}
      </div>
    </div>
  {/if}

  <!-- Beat-specific overlays -->
  <div class="beat-overlays">
    <!-- Beat number label (only for non-start positions) -->
    {#if !isStartPosition() && beat.pictographData}
      <div class="beat-number-label">
        {displayBeatNumber()}
      </div>
    {/if}

    <!-- Start position label -->
    {#if isStartPosition()}
      <div class="start-position-label">START</div>
    {/if}

    <!-- Reversal indicators -->
    {#if beat.blueReversal || beat.redReversal}
      <div class="reversal-indicators">
        {#if beat.blueReversal}
          <div class="reversal-indicator blue" title="Blue Reversal"></div>
        {/if}
        {#if beat.redReversal}
          <div class="reversal-indicator red" title="Red Reversal"></div>
        {/if}
      </div>
    {/if}

    <!-- Selection highlight -->
    {#if isSelected}
      <div class="selection-highlight"></div>
    {/if}

    <!-- Hover highlight -->
    {#if isHovered}
      <div class="hover-highlight"></div>
    {/if}
  </div>
</div>

<style>
  .beat-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    transition: all 0.2s ease;
    cursor: pointer;
  }

  .beat-wrapper:hover {
    transform: scale(1.02);
  }

  .beat-wrapper.selected {
    box-shadow: 0 0 0 3px #3b82f6;
  }

  .beat-wrapper.start-position {
    border: 2px solid #10b981;
  }

  .beat-overlays {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }

  /* Beat number label */
  .beat-number-label {
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(75, 85, 99, 0.9);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    font-family: Arial, sans-serif;
    z-index: 10;
  }

  /* Start position label */
  .start-position-label {
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(16, 185, 129, 0.9);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    font-family: Arial, sans-serif;
    z-index: 10;
  }

  /* Reversal indicators */
  .reversal-indicators {
    position: absolute;
    bottom: 8px;
    right: 8px;
    display: flex;
    gap: 4px;
    z-index: 10;
  }

  .reversal-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid white;
  }

  .reversal-indicator.blue {
    background-color: #3b82f6;
  }

  .reversal-indicator.red {
    background-color: #ef4444;
  }

  /* Selection highlight */
  .selection-highlight {
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    border: 3px solid #3b82f6;
    border-radius: 10px;
    pointer-events: none;
  }

  /* Hover highlight */
  .hover-highlight {
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    border: 2px solid rgba(59, 130, 246, 0.5);
    border-radius: 9px;
    pointer-events: none;
  }

  /* Empty beat state */
  .empty-beat {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
    border: 2px dashed #dee2e6;
    border-radius: 8px;
  }

  .empty-beat-content {
    font-size: 18px;
    font-weight: 600;
    color: #6c757d;
    font-family: Arial, sans-serif;
  }
</style>
