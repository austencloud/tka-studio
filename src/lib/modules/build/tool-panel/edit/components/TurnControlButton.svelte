<!-- TurnControlButton.svelte - Collapsible button with preview and swipe gestures -->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from '$shared';
  import { resolve, TYPES } from '$shared';
  import { onMount } from 'svelte';
  import type { ITurnControlService } from '../services/TurnControlService';

  // Props
  const {
    color,
    currentBeatData,
    isExpanded = false,
    layoutMode = 'comfortable',
    onExpand,
    onTurnAmountChanged
  } = $props<{
    color: 'blue' | 'red';
    currentBeatData: BeatData | null;
    isExpanded?: boolean;
    layoutMode?: 'compact' | 'balanced' | 'comfortable';
    onExpand: () => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
  }>();

  // Services
  const turnControlService = resolve(TYPES.ITurnControlService) as ITurnControlService;
  let hapticService: IHapticFeedbackService;

  // Touch/swipe state
  let touchStartX = $state(0);
  let touchStartY = $state(0);
  let isSwiping = $state(false);

  // Get display values
  const displayLabel = $derived(() => color === 'blue' ? 'Left' : 'Right');
  const turnValue = $derived(() => {
    const value = turnControlService.getCurrentTurnValue(currentBeatData, color);
    return turnControlService.getTurnValue(value);
  });
  const motionType = $derived(() => {
    if (!currentBeatData) return 'Static';
    const motion = color === 'blue' ? currentBeatData.motions?.blue : currentBeatData.motions?.red;
    if (!motion) return 'Static';
    const type = motion.motionType || 'static';
    return type.charAt(0).toUpperCase() + type.slice(1);
  });
  const previewText = $derived(() => {
    const turns = turnValue();
    const motion = motionType();
    return `${displayLabel()}: ${turns}, ${motion}`;
  });

  // Separate line display for compact mode
  const previewLine1 = $derived(() => `${displayLabel()}: ${turnValue()}`);
  const previewLine2 = $derived(() => motionType());

  // Handle swipe gestures for quick turn adjustments
  function handleTouchStart(event: TouchEvent) {
    touchStartX = event.touches[0].clientX;
    touchStartY = event.touches[0].clientY;
    isSwiping = false;
  }

  function handleTouchMove(event: TouchEvent) {
    const touchCurrentX = event.touches[0].clientX;
    const touchCurrentY = event.touches[0].clientY;
    const deltaX = touchCurrentX - touchStartX;
    const deltaY = touchCurrentY - touchStartY;

    // Check if horizontal swipe (more horizontal than vertical)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 30) {
      isSwiping = true;
      event.preventDefault(); // Prevent scrolling during swipe
    }
  }

  function handleTouchEnd(event: TouchEvent) {
    if (!isSwiping) {
      return; // Normal click/tap - let onclick handler deal with it
    }

    const touchEndX = event.changedTouches[0].clientX;
    const deltaX = touchEndX - touchStartX;

    // Swipe threshold
    const swipeThreshold = 50;

    if (Math.abs(deltaX) > swipeThreshold) {
      const currentValue = turnControlService.getCurrentTurnValue(currentBeatData, color);

      if (deltaX > 0) {
        // Swipe right - increment
        const canIncrement = turnControlService.canIncrementTurn(currentValue);
        if (canIncrement) {
          const newValue = turnControlService.incrementTurn(currentValue);
          hapticService?.trigger("selection");
          onTurnAmountChanged(color, newValue);
          console.log(`${color} turn incremented to ${newValue} via swipe`);
        }
      } else {
        // Swipe left - decrement
        const canDecrement = turnControlService.canDecrementTurn(currentValue);
        if (canDecrement) {
          const newValue = turnControlService.decrementTurn(currentValue);
          hapticService?.trigger("selection");
          onTurnAmountChanged(color, newValue);
          console.log(`${color} turn decremented to ${newValue} via swipe`);
        }
      }
    }

    isSwiping = false;
  }

  function handleClick() {
    if (!isSwiping) {
      hapticService?.trigger("selection");
      onExpand();
    }
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<button
  class="turn-control-button"
  class:blue={color === 'blue'}
  class:red={color === 'red'}
  class:expanded={isExpanded}
  class:swiping={isSwiping}
  class:compact={layoutMode === 'compact'}
  class:balanced={layoutMode === 'balanced'}
  class:comfortable={layoutMode === 'comfortable'}
  onclick={handleClick}
  ontouchstart={handleTouchStart}
  ontouchmove={handleTouchMove}
  ontouchend={handleTouchEnd}
  aria-label={previewText()}
  data-testid={`turn-control-button-${color}`}
>
  <div class="button-content">
    {#if isExpanded}
      <!-- Other panel is expanded - show two-line compact layout to save space -->
      <div class="preview-text two-line">
        <div class="line-1">{previewLine1()}</div>
        <div class="line-2">{previewLine2()}</div>
      </div>
      <div class="chevron">
        <i class="fas fa-chevron-down"></i>
      </div>
    {:else}
      <!-- Both panels collapsed - show single-line format -->
      <div class="preview-text">{previewText()}</div>
      <div class="chevron">
        <i class="fas fa-chevron-down"></i>
      </div>
    {/if}
  </div>
</button>

<style>
  .turn-control-button {
    flex: 1;
    border: 4px solid;
    border-radius: 12px;
    background: white;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    user-select: none;
    -webkit-user-select: none;
    -webkit-tap-highlight-color: transparent;
    container-type: inline-size; /* Enable container queries for intelligent text sizing */
  }

  /* Comfortable mode - Mobile, full sizing */
  .turn-control-button.comfortable {
    min-height: 60px;
  }

  /* Balanced mode - Tablet landscape */
  .turn-control-button.balanced {
    min-height: 48px;
    border-width: 3px;
  }

  /* Compact mode - Desktop, minimal vertical space */
  .turn-control-button.compact {
    min-height: 40px;
    border-width: 2px;
    border-radius: 8px;
  }

  .turn-control-button.blue {
    border-color: #3b82f6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(59, 130, 246, 0.04) 100%);
  }

  .turn-control-button.red {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.04) 100%);
  }

  .turn-control-button:hover:not(.expanded) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .turn-control-button.blue:hover:not(.expanded) {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(59, 130, 246, 0.06) 100%);
  }

  .turn-control-button.red:hover:not(.expanded) {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.06) 100%);
  }

  .turn-control-button:active:not(.expanded) {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .turn-control-button.expanded {
    flex: 0 0 auto;
    min-width: 80px;
    opacity: 0.6;
  }

  .turn-control-button.swiping {
    transition: none;
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .preview-text {
    font-weight: 600;
    flex: 1;
    text-align: left;
  }

  /* Two-line layout for collapsed state */
  .preview-text.two-line {
    display: flex;
    flex-direction: column;
    gap: 2px;
    line-height: 1.2;
  }

  .preview-text.two-line .line-1 {
    font-weight: 700;
    font-size: clamp(12px, 3cqw, 15px);
  }

  .preview-text.two-line .line-2 {
    font-size: clamp(10px, 2.5cqw, 13px);
    opacity: 0.8;
    font-weight: 500;
  }

  /* Font sizes by layout mode (for expanded state) */
  .turn-control-button.comfortable .preview-text:not(.two-line) {
    font-size: 16px;
  }

  .turn-control-button.balanced .preview-text:not(.two-line) {
    font-size: 15px;
  }

  .turn-control-button.compact .preview-text:not(.two-line) {
    font-size: 14px;
  }

  .turn-control-button.blue .preview-text {
    color: #3b82f6;
  }

  .turn-control-button.red .preview-text {
    color: #ef4444;
  }

  .turn-control-button.expanded .preview-text {
    font-size: 14px;
    text-align: center;
  }

  .turn-control-button.expanded.compact .preview-text {
    font-size: 12px;
  }

  .chevron {
    font-size: 12px;
    opacity: 0.6;
    transition: transform 0.3s ease;
  }

  .turn-control-button.compact .chevron {
    font-size: 10px;
  }

  .turn-control-button.blue .chevron {
    color: #3b82f6;
  }

  .turn-control-button.red .chevron {
    color: #ef4444;
  }

  /* Responsive adjustments for very small screens */
  @media (max-width: 400px) {
    .turn-control-button {
      min-height: 50px;
    }

    .preview-text {
      font-size: 14px;
    }

    .turn-control-button.expanded .preview-text {
      font-size: 12px;
    }
  }
</style>
