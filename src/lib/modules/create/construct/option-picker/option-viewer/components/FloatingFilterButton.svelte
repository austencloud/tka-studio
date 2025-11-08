<!--
FloatingFilterButton.svelte - Compact floating button for filter access

A space-efficient alternative to the full header for small screens.
Positioned at the top-left of the option viewer container as a floating button
that triggers the filter panel dropdown.
-->

<script lang="ts">
  import type { IHapticFeedbackService } from "$shared/application/services/contracts/IHapticFeedbackService";
  import { container } from "$shared/inversify/container";
  import { TYPES } from "$shared/inversify/types";
  import { swipeGesture } from "$shared/utils/swipeGesture";

  const {
    isFilterPanelOpen = false,
    isContinuousOnly = false,
    onOpenFilters,
    containerWidth = 0,
    pictographSize = 0,
    columns = 4,
    gridGap = 2,
  } = $props<{
    isFilterPanelOpen?: boolean;
    isContinuousOnly?: boolean;
    onOpenFilters?: () => void;
    containerWidth?: number;
    pictographSize?: number;
    columns?: number;
    gridGap?: number;
  }>();

  let hapticService: IHapticFeedbackService | undefined = undefined;

  // Resolve service safely
  if (container.isBound(TYPES.IHapticFeedbackService)) {
    hapticService = container.get<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  }

  /**
   * Calculate safe padding for floating button that won't overlap the grid.
   *
   * Logic:
   * 1. Calculate actual grid width based on pictograph size and columns
   * 2. Measure leftover space that naturally occurs when grid is smaller than container
   * 3. Check if button + safety margin + desired padding fits in leftover space
   * 4. Only apply padding if there's sufficient room
   *
   * This ensures the button never overlaps pictographs while providing
   * visual breathing room when space permits.
   */
  const buttonPadding = $derived(() => {
    // Button size varies by screen width
    const buttonSize = containerWidth <= 375 ? 40 : 44;

    // Safety margin to ensure button doesn't touch grid content
    const safetyMargin = 4;

    // Calculate actual grid width
    // gridWidth = (pictographSize × columns) + (gap × (columns - 1))
    const actualGridWidth = pictographSize * columns + gridGap * (columns - 1);

    // Calculate leftover space on each side
    const totalLeftoverSpace = containerWidth - actualGridWidth;
    const leftoverSpacePerSide = totalLeftoverSpace / 2;

    // Calculate maximum safe padding within leftover space
    // Formula: available space = leftoverSpace - buttonSize - safetyMargin
    const maxSafePadding = Math.max(
      0,
      leftoverSpacePerSide - buttonSize - safetyMargin
    );

    // Desired padding based on container width (aesthetic preference)
    let desiredPadding: number;
    if (containerWidth <= 375) {
      desiredPadding = 0; // Flush on tiny screens
    } else if (containerWidth <= 600) {
      desiredPadding = 8; // Small breathing room
    } else if (containerWidth <= 1024) {
      desiredPadding = 10; // Moderate spacing
    } else {
      desiredPadding = 12; // Comfortable desktop spacing
    }

    // Use the smaller of desired padding or maximum safe padding
    const actualPadding = Math.min(desiredPadding, maxSafePadding);

    return actualPadding;
  });

  function handleFilterClick() {
    hapticService?.trigger("selection");
    onOpenFilters?.();
  }
</script>

<button
  class="floating-filter-button"
  class:open={isFilterPanelOpen}
  class:continuous-active={isContinuousOnly}
  onclick={handleFilterClick}
  use:swipeGesture={{ onSwipeDown: handleFilterClick }}
  aria-label="Open filter options"
  aria-expanded={isFilterPanelOpen}
  type="button"
  style="--button-padding: {buttonPadding()}px;"
>
  <i class="fas fa-filter"></i>
  {#if isContinuousOnly}
    <span class="filter-indicator" aria-label="Continuous filter active"></span>
  {/if}
</button>

<style>
  /* Updated: Smart padding that adapts to container size */
  .floating-filter-button {
    /* Positioning - with intelligent padding that respects grid layout */
    position: absolute;
    top: var(--button-padding, 0);
    left: var(--button-padding, 0);
    z-index: 100;

    /* Size - optimized for touch targets */
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;

    display: flex;
    align-items: center;
    justify-content: center;

    /* Appearance */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.15) 0%,
      rgba(255, 255, 255, 0.08) 100%
    );
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    /* Icon */
    color: rgba(255, 255, 255, 0.85);
    font-size: 1.1rem;

    /* Interaction */
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Hover effects */
  @media (hover: hover) {
    .floating-filter-button:hover {
      background: linear-gradient(
        135deg,
        rgba(59, 130, 246, 0.25) 0%,
        rgba(59, 130, 246, 0.15) 100%
      );
      border-color: rgba(59, 130, 246, 0.4);
      box-shadow:
        0 6px 20px rgba(59, 130, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
      color: rgba(147, 197, 253, 1);
    }
  }

  /* Active/pressed state */
  .floating-filter-button:active {
    transform: translateY(0) scale(0.95);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Open state */
  .floating-filter-button.open {
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.3) 0%,
      rgba(59, 130, 246, 0.2) 100%
    );
    border-color: rgba(59, 130, 246, 0.5);
    color: rgba(147, 197, 253, 1);
    box-shadow:
      0 6px 24px rgba(59, 130, 246, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  /* Continuous filter active indicator */
  .filter-indicator {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    box-shadow: 0 2px 6px rgba(59, 130, 246, 0.5);
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.7;
      transform: scale(0.9);
    }
  }

  /* Extra small screens (iPhone SE) - maximize space with flush positioning */
  @media (max-width: 375px) {
    .floating-filter-button {
      /* Note: padding already set to 0 via buttonPadding logic */
      width: 40px;
      height: 40px;
      min-width: 40px;
      min-height: 40px;
      font-size: 1rem;
    }

    .filter-indicator {
      top: 4px;
      right: 4px;
      width: 7px;
      height: 7px;
    }
  }
</style>
