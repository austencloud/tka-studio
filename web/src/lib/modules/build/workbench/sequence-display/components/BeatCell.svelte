<script lang="ts">
  import type { BeatData } from "$shared";
  import { Pictograph } from "$shared";

  let {
    beat,
    index = 0,
    onClick,
    shouldAnimate = false,
  } = $props<{
    beat: BeatData;
    index?: number;
    onClick?: () => void;
    shouldAnimate?: boolean;
  }>();

  const isStartPosition = $derived(() => {
    return beat.beatNumber === 0;
  });

  const displayBeatNumber = $derived(() => {
    return beat.beatNumber || index + 1;
  });

  const ariaLabel = $derived(() => {
    if (isStartPosition()) {
      return "Start Position";
    }
    return `Beat ${displayBeatNumber()} ${beat.pictographData ? "Pictograph" : "Empty"}`;
  });

  // Debug logging for reversal data
  $effect(() => {
    if (beat.blueReversal || beat.redReversal) {
      console.log(`🎯 BeatCell: Beat ${displayBeatNumber()} has reversals:`, {
        blueReversal: beat.blueReversal,
        redReversal: beat.redReversal,
        letter: beat.pictographData?.letter
      });
    }
  });

  let hasAnimated = $state(false);
  let isVisible = $state(true);

  const shouldAnimateIn = $derived(() => {
    return shouldAnimate && !hasAnimated && isVisible && beat.pictographData;
  });

  function handleAnimationEnd() {
    hasAnimated = true;
  }

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
  class="beat-cell"
  class:animate={shouldAnimateIn()}
  class:visible={isVisible}
  onclick={handleClick}
  onkeypress={handleKeyPress}
  onanimationend={handleAnimationEnd}
  role="button"
  tabindex="0"
  aria-label={ariaLabel()}
>
  <Pictograph
    pictographData={beat.pictographData}
    beatNumber={displayBeatNumber()}
    isStartPosition={isStartPosition()}
    blueReversal={beat.blueReversal}
    redReversal={beat.redReversal}
    showBeatNumber={true}
  />
</div>

<style>
  .beat-cell {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0; 
    transition: all 0.2s ease;
    cursor: pointer;
    margin: 0; 
    padding: 0; 
    transform: scale(0.8);
    aspect-ratio: 1 / 1;
    will-change: transform;
  }

  .beat-cell.visible {
    transform: scale(1);
  }

  .beat-cell.animate {
    animation: scaleIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  }

  .beat-cell:hover {
    opacity: 0.9;
  }



  @keyframes scaleIn {
    0% {
      transform: scale(0.6);
      opacity: 0.7;
    }
    50% {
      transform: scale(1.05);
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>
