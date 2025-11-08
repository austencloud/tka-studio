<!--
Simple Arrow Component - Just renders an arrow with provided data
Now with click interaction and selection visual feedback
-->
<script lang="ts">
  import {
    resolve,
    TYPES,
    type IHapticFeedbackService,
    type MotionData,
    type PictographData,
  } from "$shared";
  import type { ArrowAssets, ArrowPosition } from "$shared/pictograph/arrow";
  import { selectedArrowState } from "../../../../../modules/create/shared/state/selected-arrow-state.svelte";

  let {
    motionData,
    arrowAssets,
    arrowPosition,
    shouldMirror = false,
    showArrow = true,
    color,
    pictographData = null,
    isClickable = false,
  } = $props<{
    motionData: MotionData;
    arrowAssets: ArrowAssets;
    arrowPosition: ArrowPosition;
    shouldMirror?: boolean;
    showArrow?: boolean;
    color: string;
    pictographData?: PictographData | null;
    isClickable?: boolean;
  }>();

  // Check if this arrow is currently selected
  const isSelected = $derived(
    isClickable && pictographData
      ? selectedArrowState.isSelected(motionData, color)
      : false
  );

  let hapticService: IHapticFeedbackService | null = null;

  // Initialize haptic service on mount (lazy load)
  $effect(() => {
    if (isClickable && !hapticService) {
      try {
        hapticService = resolve<IHapticFeedbackService>(
          TYPES.IHapticFeedbackService
        );
      } catch (error) {
        console.warn("Haptic service not available:", error);
      }
    }
  });

  // Handle arrow click
  function handleArrowClick(event: MouseEvent) {
    if (!isClickable || !pictographData) return;

    event.stopPropagation();

    console.log("[ArrowSvg] Arrow clicked:", {
      color,
      currentPosition: arrowPosition,
      motionData: motionData,
    });

    // Trigger haptic feedback
    hapticService?.trigger("selection");

    // Select the arrow in global state
    selectedArrowState.selectArrow(motionData, color, pictographData);
  }

  // Log when arrow position changes
  $effect(() => {
    if (isClickable) {
      console.log(`[ArrowSvg] ${color} arrow position updated:`, arrowPosition);
    }
  });
</script>

{#if showArrow}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <g
    class="arrow-svg {motionData.color}-arrow-svg"
    class:mirrored={shouldMirror}
    class:clickable={isClickable}
    class:selected={isSelected}
    onclick={handleArrowClick}
    role={isClickable ? "button" : null}
    tabindex={isClickable ? 0 : -1}
    aria-label={isClickable
      ? `${color} arrow - ${motionData.motion} ${motionData.turns}`
      : undefined}
    style="
      transform: translate({arrowPosition.x}px, {arrowPosition.y}px)
                 rotate({arrowPosition.rotation}deg)
                 {shouldMirror ? 'scale(-1, 1)' : ''};
    "
  >
    <!-- Position group at calculated coordinates, let SVG handle its own centering -->
    <g transform="translate({-arrowAssets.center.x}, {-arrowAssets.center.y})">
      {@html arrowAssets.imageSrc}
    </g>

    <!-- Selection highlight overlay -->
    {#if isSelected}
      <circle
        cx="0"
        cy="0"
        r="60"
        fill="none"
        stroke="var(--color-accent, #fbbf24)"
        stroke-width="4"
        class="selection-glow"
        opacity="0.8"
      />
    {/if}
  </g>
{/if}

<style>
  .arrow-svg {
    pointer-events: none;
    /* Smooth transition for position and rotation changes */
    /* IMPORTANT: transform must be a CSS property (not SVG attribute) for transitions to work */
    transition:
      transform 0.2s ease,
      filter 0.2s ease;
  }

  .arrow-svg.clickable {
    pointer-events: all;
    cursor: pointer;
  }

  .arrow-svg.clickable:hover {
    filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.6));
  }

  .arrow-svg.clickable:active {
    filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.4));
  }

  .arrow-svg.selected {
    filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.9));
  }

  .selection-glow {
    animation: pulse-glow 2s ease-in-out infinite;
  }

  @keyframes pulse-glow {
    0%,
    100% {
      opacity: 0.6;
      stroke-width: 4;
    }
    50% {
      opacity: 1;
      stroke-width: 6;
    }
  }
</style>
