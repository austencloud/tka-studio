<!-- PictographGrid.svelte - Pictograph grid display for StartPositionPicker -->
<script lang="ts">
  import type { IHapticFeedbackService, PictographData } from "$shared";
  import {
    getLetterBorderColorSafe,
    Pictograph,
    resolve,
    TYPES,
  } from "$shared";
  import { onMount } from "svelte";

  const {
    pictographDataSet,
    selectedPictograph = null,
    onPictographSelect,
    isAnimating = false,
  }: {
    pictographDataSet: PictographData[];
    selectedPictograph?: PictographData | null;
    onPictographSelect: (pictograph: PictographData) => void;
    isAnimating?: boolean;
  } = $props();

  // Animation disabled - positions appear instantly for speed
  let shouldAnimate = $state(false);
  let animatedPictographs = $state(new Set<string>());

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Animation handlers (kept for compatibility but never trigger)
  function handleAnimationEnd(pictographId: string) {
    animatedPictographs.add(pictographId);
    animatedPictographs = new Set(animatedPictographs);
  }

  function shouldPictographAnimate(pictographId: string): boolean {
    return false; // Animation disabled
  }

  // Handle pictograph selection with haptic feedback
  function handlePictographSelect(pictograph: PictographData) {
    // Trigger selection haptic feedback for pictograph selection
    hapticService?.trigger("selection");

    onPictographSelect(pictograph);
  }
</script>

<div class="pictograph-row">
  {#each pictographDataSet as pictographData, index (pictographData.id)}
    <div
      class="pictograph-container"
      class:selected={selectedPictograph?.id === pictographData.id}
      class:animate={shouldPictographAnimate(pictographData.id)}
      role="button"
      tabindex="0"
      style:--letter-border-color={getLetterBorderColorSafe(
        pictographData.letter
      )}
      style:--animation-delay="{index * 80}ms"
      onclick={() => handlePictographSelect(pictographData)}
      onkeydown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handlePictographSelect(pictographData);
        }
      }}
      onanimationend={() => handleAnimationEnd(pictographData.id)}
    >
      <!-- Render pictograph using Pictograph component -->
      <div class="pictograph-wrapper">
        <Pictograph {pictographData} />
      </div>
    </div>
  {/each}
</div>

<style>
  .pictograph-row {
    display: grid;
    /* Default: 1x3 horizontal grid layout */
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr;
    gap: min(2cqmin, 1rem);

    flex: 1;
    width: 100%;
    height: 100%;
    padding: 0;

    /* Center items instead of stretching them */
    align-items: center;
    justify-items: center;
    align-content: center;
  }

  /* Tall container (portrait): Use 3x1 column layout */
  @container (aspect-ratio < 0.75) {
    .pictograph-row {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(3, 1fr);
    }
  }

  /* Wide container remains horizontal (same as default) */
  @container (aspect-ratio > 1.5) {
    .pictograph-row {
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: 1fr;
    }
  }

  .pictograph-container {
    width: 100%;
    /* Height determined by aspect-ratio and content, not stretched */
    aspect-ratio: 1 / 1;
    position: relative;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid transparent;
    border-radius: 0px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Initial state for animation - start invisible */
    opacity: 0;
    transform: scale(0.6) translateY(20px);
    box-shadow:
      0 1px 2px rgba(0, 0, 0, 0.1),
      0 2px 4px rgba(0, 0, 0, 0.06);
  }

  /* After animation completes, ensure visible state */
  .pictograph-container:not(.animate) {
    opacity: 1;
    transform: scale(1) translateY(0);
  }

  /* Entrance animation similar to BeatCell */
  .pictograph-container.animate {
    animation: scaleInStaggered 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    animation-delay: var(--animation-delay, 0ms);
  }

  /* Desktop hover - only on hover-capable devices */
  @media (hover: hover) {
    .pictograph-container:hover {
      transform: scale(1.05);
      border-color: var(--letter-border-color, var(--primary));
      box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.12),
        0 4px 8px rgba(0, 0, 0, 0.08),
        0 8px 16px rgba(0, 0, 0, 0.06);
      filter: brightness(1.05);
    }
  }

  /* Mobile/universal active state */
  .pictograph-container:active {
    transform: scale(0.97);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .pictograph-container.selected {
    border-color: var(--letter-border-color, var(--primary));
    background: var(--primary) / 10;
    box-shadow:
      0 0 12px rgba(100, 200, 255, 0.3),
      0 2px 4px rgba(0, 0, 0, 0.12),
      0 4px 8px rgba(0, 0, 0, 0.08);
  }

  .pictograph-wrapper {
    width: 100%;
    /* Height determined by pictograph content */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  @media (max-width: 768px) {
    .pictograph-row {
      flex-direction: row;
      gap: var(--spacing-md);
    }
  }

  /* Even smaller on very small screens */
  @media (max-width: 480px) {
    .pictograph-row {
      gap: var(--spacing-sm);
    }
  }

  /* Keyframe animation for staggered entrance effect */
  @keyframes scaleInStaggered {
    0% {
      opacity: 0;
      transform: scale(0.6) translateY(20px);
    }
    60% {
      opacity: 0.8;
      transform: scale(1.1) translateY(-5px);
    }
    100% {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
</style>
