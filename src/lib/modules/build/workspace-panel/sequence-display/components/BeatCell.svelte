<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from "$shared";
  import { Pictograph, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    beat,
    index = 0,
    onClick,
    onDelete,
    shouldAnimate = false,
    isSelected = false,
    isPracticeBeat = false,
    // Multi-select props
    isMultiSelectMode = false,
    onLongPress,
  } = $props<{
    beat: BeatData;
    index?: number;
    onClick?: () => void;
    onDelete?: () => void;
    shouldAnimate?: boolean;
    isSelected?: boolean;
    isPracticeBeat?: boolean;
    // Multi-select
    isMultiSelectMode?: boolean;
    onLongPress?: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

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
    return `Beat ${displayBeatNumber()} ${beat.isBlank ? "Empty" : "Pictograph"}`;
  });

  // Create beat data with selection state for the Pictograph component
  const beatDataWithSelection = $derived(() => {
    return {
      ...beat,
      isSelected,
    };
  });



  let hasAnimated = $state(false);
  let currentAnimationName = $state("gentleBloom");
  let previousBeatId = beat.id;

  // Track when new pictograph data arrives for fade-in animation
  let enableTransitionsForNewData = $state(false);
  let previousPictographData = beat.isBlank ? null : beat;

  // Reset hasAnimated ONLY when the beat data itself changes (different beat loaded)
  // This prevents re-animating all beats when only one beat should animate
  $effect(() => {
    if (beat.id !== previousBeatId) {
      hasAnimated = false;
      previousBeatId = beat.id;
    }
  });

  // Enable transitions when new pictograph data arrives (for option selection animation)
  $effect(() => {
    const currentPictographData = beat.isBlank ? null : beat;
    const dataChanged = JSON.stringify(currentPictographData) !== JSON.stringify(previousPictographData);

    if (dataChanged && !beat.isBlank) {
      // New pictograph data - enable transitions for fade-in
      enableTransitionsForNewData = true;

      // Disable transitions after animation completes
      setTimeout(() => {
        enableTransitionsForNewData = false;
      }, 350); // Match pictograph fade-in duration
    }

    previousPictographData = currentPictographData;
  });

  const shouldAnimateIn = $derived(() => {
    return shouldAnimate && !hasAnimated && !beat.isBlank;
  });

  // Beats should be invisible ONLY if they're waiting to animate
  const isVisible = $derived(() => {
    // If it should animate but hasn't yet, hide it (will become visible via animation)
    // This applies to ALL beats, including start position during generation
    if (shouldAnimate && !hasAnimated) return false;

    // Special case: Start position tile (index -1) should be visible even when blank
    // This shows the "Start" placeholder before a start position is selected
    if (index === -1) return true;

    // If it's a blank beat in the main grid, never show it
    if (beat.isBlank) return false;

    // Otherwise, show it (either it has animated, or it doesn't need to animate)
    return true;
  });

  function handleAnimationEnd() {
    hasAnimated = true;
  }

  // Listen for animation changes from the AnimationSelector
  onMount(() => {
    const handleAnimationChange = (event: CustomEvent) => {
      currentAnimationName = event.detail.animation;
      console.log(`🎨 BeatCell: Animation changed to ${currentAnimationName}`);
    };

    window.addEventListener('animation-change', handleAnimationChange as EventListener);

    return () => {
      window.removeEventListener('animation-change', handleAnimationChange as EventListener);
    };
  });

  // Long-press detection
  let longPressTimer: number | null = $state(null);
  let longPressTriggered = $state(false);
  const LONG_PRESS_DURATION = 500; // ms

  function handlePointerDown(event: PointerEvent) {
    longPressTriggered = false;

    longPressTimer = window.setTimeout(() => {
      // Long-press detected
      longPressTriggered = true;
      hapticService?.trigger("selection"); // Haptic at 500ms
      onLongPress?.();
    }, LONG_PRESS_DURATION);
  }

  function handlePointerUp() {
    if (longPressTimer) {
      clearTimeout(longPressTimer);
      longPressTimer = null;
    }
  }

  function handlePointerCancel() {
    if (longPressTimer) {
      clearTimeout(longPressTimer);
      longPressTimer = null;
    }
    longPressTriggered = false;
  }

  function handleClick() {
    // Don't trigger regular click if long-press was triggered
    if (longPressTriggered) {
      longPressTriggered = false;
      return;
    }

    // Trigger haptic feedback for beat selection
    hapticService?.trigger("selection");
    onClick?.();
  }

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      // Trigger haptic feedback for keyboard interaction
      hapticService?.trigger("selection");
      onClick?.();
    } else if (event.key === "Delete" || event.key === "Backspace") {
      // Only allow deletion if beat is selected and not the start position
      if (isSelected && beat.beatNumber >= 1) {
        event.preventDefault();
        // Trigger warning haptic feedback for deletion
        hapticService?.trigger("warning");
        onDelete?.();
      }
    }
  }
</script>

<div
  class="beat-cell"
  class:invisible={!isVisible()}
  class:animate={shouldAnimateIn()}
  class:selected={isSelected}
  class:practice-beat={isPracticeBeat}
  class:multi-select-mode={isMultiSelectMode}
  class:anim-gentleBloom={currentAnimationName === "gentleBloom"}
  class:anim-softCascade={currentAnimationName === "softCascade"}
  class:anim-springPop={currentAnimationName === "springPop"}
  class:anim-microFade={currentAnimationName === "microFade"}
  class:anim-glassBlur={currentAnimationName === "glassBlur"}
  onclick={handleClick}
  onkeypress={handleKeyPress}
  onpointerdown={handlePointerDown}
  onpointerup={handlePointerUp}
  onpointercancel={handlePointerCancel}
  onanimationend={handleAnimationEnd}
  role="button"
  tabindex="0"
  aria-label={ariaLabel()}
>
  <Pictograph
    pictographData={beatDataWithSelection()}
    disableContentTransitions={!enableTransitionsForNewData}
  />
</div>

<style>
  .beat-cell {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0;
    cursor: pointer;
    margin: 0;
    padding: 0;
    /* NO transform or transition - let animations handle everything */

    /* Prevent text selection during long-press */
    user-select: none;
    -webkit-user-select: none;
    -webkit-touch-callout: none;
    touch-action: manipulation;
  }

  /* Invisible state - beat takes up space but pictograph is hidden */
  .beat-cell.invisible {
    opacity: 0;
    pointer-events: none;
    /* Start smaller when invisible - animation will scale up from here */
    transform: scale(0.3);
  }

  /* Default animation (Spring Pop) */
  .beat-cell.animate {
    animation: springPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  }

  /* Animation overrides based on selected animation */
  .beat-cell.animate.anim-gentleBloom {
    animation: gentleBloom 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  }

  .beat-cell.animate.anim-softCascade {
    animation: softCascade 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  .beat-cell.animate.anim-springPop {
    animation: springPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  }

  .beat-cell.animate.anim-microFade {
    animation: microFade 0.25s cubic-bezier(0.4, 0, 0.2, 1) both;
  }

  .beat-cell.animate.anim-glassBlur {
    animation: glassBlur 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  }

  .beat-cell:hover {
    opacity: 0.9;
    transform: scale(1.02);
  }

  /* Elevated Luxury - 2025/2026 Selection State */
  .beat-cell.selected {
    /* Ensure it appears above other beats */
    z-index: 10;
    position: relative;

    /* Gold gradient border - no background to keep pictograph visible */
    border: 3px solid transparent;
    background:
      linear-gradient(transparent, transparent) padding-box,
      linear-gradient(135deg, #fbbf24, #f59e0b, #d97706) border-box;
    border-radius: 12px;

    /* Layered shadows for depth and premium glow */
    box-shadow:
      0 0 20px rgba(251, 191, 36, 0.5),
      0 8px 32px rgba(251, 191, 36, 0.3),
      0 0 0 1px rgba(251, 191, 36, 0.2);

    /* Scale effect - expands equally on all sides */
    transform: scale(1.08);

    /* NO transparency - keep selected beat fully opaque */
    opacity: 1;

    /* Smooth spring animation */
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .beat-cell.selected:hover {
    /* Keep fully opaque even on hover */
    opacity: 1;
    transform: scale(1.12);
    box-shadow:
      0 0 30px rgba(251, 191, 36, 0.7),
      0 12px 48px rgba(251, 191, 36, 0.4),
      0 0 0 1px rgba(251, 191, 36, 0.3);
  }

  /* Practice beat styling - gold border with pulse animation */
  .beat-cell.practice-beat {
    border: 3px solid #fbbf24;
    border-radius: 8px;
    background: rgba(251, 191, 36, 0.15);
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.6);
    transform: scale(1.1);
    animation: practicePulse 1s ease-in-out infinite;
    z-index: 10;
  }

  .beat-cell.practice-beat:hover {
    transform: scale(1.12);
    box-shadow: 0 0 24px rgba(251, 191, 36, 0.8);
  }

  @keyframes practicePulse {
    0%, 100% {
      box-shadow: 0 0 20px rgba(251, 191, 36, 0.6);
      transform: scale(1.1);
    }
    50% {
      box-shadow: 0 0 30px rgba(251, 191, 36, 0.9);
      transform: scale(1.12);
    }
  }

  /* FAVORITE: Gentle Bloom - soft float-up with blur */
  @keyframes gentleBloom {
    0% {
      transform: scale(0.7) translateY(10px);
      opacity: 0;
      filter: blur(2px);
    }
    60% {
      opacity: 0.8;
      filter: blur(0px);
    }
    100% {
      transform: scale(1) translateY(0);
      opacity: 1;
      filter: blur(0px);
    }
  }

  /* OPTION 2: Soft Cascade - smooth slide from left with fade */
  @keyframes softCascade {
    0% {
      transform: translateX(-20px) scale(0.9);
      opacity: 0;
    }
    50% {
      opacity: 0.6;
    }
    100% {
      transform: translateX(0) scale(1);
      opacity: 1;
    }
  }

  /* OPTION 3: Spring Pop - elastic bounce (TRENDY 2025!) */
  @keyframes springPop {
    0% {
      transform: scale(0.3);
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* OPTION 4: Micro Fade - minimal, fast, modern */
  @keyframes microFade {
    0% {
      transform: scale(0.95);
      opacity: 0;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* OPTION 5: Glass Blur - glassmorphism trend */
  @keyframes glassBlur {
    0% {
      transform: scale(0.8);
      opacity: 0;
      filter: blur(8px);
      backdrop-filter: blur(0px);
    }
    100% {
      transform: scale(1);
      opacity: 1;
      filter: blur(0px);
      backdrop-filter: blur(4px);
    }
  }
</style>
