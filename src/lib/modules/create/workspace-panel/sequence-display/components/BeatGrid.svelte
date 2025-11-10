<!-- BeatGrid.svelte - Responsive beat grid with display animations -->
<script lang="ts">
  import type {
    BeatData,
    IDeviceDetector,
    IHapticFeedbackService,
  } from "$shared";
  import { createBeatData, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { createBeatGridDisplayState, createScrollState } from "../state";
  import {
    calculateBeatPosition,
    calculateGridLayout,
  } from "../utils/grid-calculations";
  import BeatCell from "./BeatCell.svelte";

  // Services
  let hapticService: IHapticFeedbackService;
  let deviceDetector: IDeviceDetector;

  let {
    beats,
    startPosition = null,
    onBeatClick,
    onStartClick,
    onBeatDelete,
    selectedBeatNumber = null, // 0=start, 1=first beat, 2=second beat, etc.
    removingBeatIndex = null,
    removingBeatIndices = new Set<number>(),
    isClearing = false,
    practiceBeatNumber = null, // 0=start, 1=first beat, 2=second beat, etc.
    isSideBySideLayout = false,
    // Multi-select props
    isMultiSelectMode = false,
    selectedBeatNumbers = new Set<number>(),
    onBeatLongPress,
    onStartLongPress,
  } = $props<{
    beats: ReadonlyArray<BeatData> | BeatData[];
    startPosition?: BeatData | null;
    onBeatClick?: (beatNumber: number) => void;
    onStartClick?: () => void;
    onBeatDelete?: (beatNumber: number) => void;
    selectedBeatNumber?: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    removingBeatIndex?: number | null;
    removingBeatIndices?: Set<number>;
    isClearing?: boolean;
    practiceBeatNumber?: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    isSideBySideLayout?: boolean;
    // Multi-select
    isMultiSelectMode?: boolean;
    selectedBeatNumbers?: Set<number>;
    onBeatLongPress?: (beatNumber: number) => void;
    onStartLongPress?: () => void;
  }>();

  const placeholderBeat = createBeatData({
    beatNumber: 0,
    isBlank: true,
  });

  // State management - isolated concerns
  const displayState = createBeatGridDisplayState();
  const scrollState = createScrollState();

  // Container dimensions for responsive sizing (component-local reactive state)
  let containerWidth = $state(0);
  let containerHeight = $state(0);
  let containerRef: HTMLElement | undefined = $state();
  let scrollContainerRef: HTMLElement | undefined = $state();

  // Computed grid layout - reactive derivation using pure utility function
  // This stays in component because it depends on component-local reactive state
  // Pass layout mode awareness for column calculation
  const gridLayout = $derived(() => {
    return calculateGridLayout(
      beats.length,
      containerWidth,
      containerHeight,
      deviceDetector,
      { isSideBySideLayout }
    );
  });

  // Track previous beat state for change detection
  let previousBeatCount = beats.length;
  let previousBeatsRef: ReadonlyArray<BeatData> | BeatData[] = beats;

  // Helper to trigger animations
  async function triggerFullAnimation() {
    if (!containerRef) return;

    // Only trigger animation if we're prepared for it (i.e., from Generate, not Undo/Redo)
    // Generate dispatches "prepare-sequence-animation" event which sets isPreparingFullAnimation = true
    // Undo/Redo just updates the sequence directly without this flag
    if (!displayState.isPreparingFullAnimation) {
      return; // Skip animation for Undo/Redo operations
    }

    const dispatchEvent = (event: CustomEvent) =>
      containerRef?.dispatchEvent(event);
    const mode = displayState.isSequentialMode ? "sequential" : "all-at-once";

    if (mode === "sequential") {
      await displayState.triggerSequentialAnimation(beats, dispatchEvent);
    } else {
      displayState.triggerAllAtOnceAnimation();
    }
  }

  // Handle beat changes and trigger appropriate animations
  $effect(() => {
    const currentBeatCount = beats.length;
    const beatsArrayChanged = beats !== previousBeatsRef;

    if (beatsArrayChanged && currentBeatCount > 0) {
      const beatCountDiff = currentBeatCount - previousBeatCount;

      if (beatCountDiff === 1 && previousBeatCount > 0) {
        // 🚀 PERFORMANCE: Check only the last beat ID instead of iterating through all beats
        // This is O(1) instead of O(n), eliminating the 60-70ms setTimeout violations
        const lastPreviousBeat = previousBeatsRef[previousBeatCount - 1];
        const lastCurrentBeat = beats[previousBeatCount - 1];
        const previousBeatsUnchanged =
          lastPreviousBeat &&
          lastCurrentBeat &&
          lastPreviousBeat.id === lastCurrentBeat.id;

        if (previousBeatsUnchanged) {
          // Single beat added (Construct mode)
          displayState.handleSingleBeatAddition(currentBeatCount - 1);
        } else {
          // Beats replaced - trigger full animation
          triggerFullAnimation();
        }
      } else if (beatCountDiff === 0) {
        // Same number of beats - check if IDs are preserved
        // This happens during sequence transformations (mirror, rotate, color swap)
        // 🚀 PERFORMANCE: Quick check - compare first and last beat IDs
        const firstBeatIdMatch = previousBeatsRef[0]?.id === beats[0]?.id;
        const lastBeatIdMatch =
          previousBeatsRef[currentBeatCount - 1]?.id ===
          beats[currentBeatCount - 1]?.id;

        if (firstBeatIdMatch && lastBeatIdMatch && currentBeatCount > 0) {
          // Beat IDs preserved - this is a data update (transform), not a replacement
          // NO animation needed - beats will update in place
        } else {
          // Beat IDs changed - full sequence replacement (Generate mode)
          triggerFullAnimation();
        }
      } else {
        // Full sequence replacement (Generate mode)
        triggerFullAnimation();
      }
    } else if (currentBeatCount > previousBeatCount) {
      const beatsAdded = currentBeatCount - previousBeatCount;
      if (beatsAdded === 1) {
        // Single beat added
        displayState.handleSingleBeatAddition(currentBeatCount - 1);
      }
    }

    // Auto-scroll to bottom when beats added
    if (currentBeatCount > previousBeatCount) {
      scrollState.scrollToBottom();
    }

    previousBeatCount = currentBeatCount;
    previousBeatsRef = beats;
  });

  // Initialize services on mount
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
  });

  // Effect: Global animation event listeners
  // Consolidated reactive management of all animation-related window events
  $effect(() => {
    const handleAnimationModeChange = (event: CustomEvent) => {
      displayState.setAnimationMode(
        event.detail.isSequential ? "sequential" : "all-at-once"
      );
    };

    const handleClearSequenceAnimation = () => {
      displayState.handleClearSequence();
    };

    const handlePrepareSequenceAnimation = (event: CustomEvent) => {
      displayState.prepareSequenceAnimation(
        event.detail.beatCount,
        event.detail.isSequential ? "sequential" : "all-at-once"
      );
    };

    window.addEventListener(
      "animation-mode-change",
      handleAnimationModeChange as EventListener
    );
    window.addEventListener(
      "clear-sequence-animation",
      handleClearSequenceAnimation as EventListener
    );
    window.addEventListener(
      "prepare-sequence-animation",
      handlePrepareSequenceAnimation as EventListener
    );

    return () => {
      window.removeEventListener(
        "animation-mode-change",
        handleAnimationModeChange as EventListener
      );
      window.removeEventListener(
        "clear-sequence-animation",
        handleClearSequenceAnimation as EventListener
      );
      window.removeEventListener(
        "prepare-sequence-animation",
        handlePrepareSequenceAnimation as EventListener
      );
    };
  });

  // Effect: Container resize tracking for responsive grid layout
  $effect(() => {
    if (!containerRef) return;

    // Set initial dimensions
    const rect = containerRef.getBoundingClientRect();
    containerWidth = rect.width;
    containerHeight = rect.height;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        containerWidth = width;
        containerHeight = height;
      }
    });

    resizeObserver.observe(containerRef);

    return () => {
      resizeObserver.disconnect();
    };
  });

  // Effect: Scroll container setup and resize tracking
  $effect(() => {
    if (!scrollContainerRef) return;

    // Setup scroll state
    scrollState.setScrollContainer(scrollContainerRef);

    const scrollResizeObserver = new ResizeObserver(() => {
      scrollState.checkScrollbar();
    });

    scrollResizeObserver.observe(scrollContainerRef);

    return () => {
      scrollResizeObserver.disconnect();
    };
  });

  function handleBeatClick(beatNumber: number) {
    hapticService?.trigger("selection");
    onBeatClick?.(beatNumber);
  }

  function handleStartClick() {
    hapticService?.trigger("selection");
    onStartClick?.();
  }
</script>

<div class="beat-grid-container" bind:this={containerRef}>
  <div
    class="beat-grid-scroll"
    class:has-scrollbar={scrollState.hasVerticalScrollbar}
    bind:this={scrollContainerRef}
  >
    <div
      class="beat-grid"
      class:clearing={isClearing || displayState.isClearingForGeneration}
      style:--grid-rows={gridLayout().rows}
      style:--grid-cols={gridLayout().totalColumns}
      style:--cell-size="{gridLayout().cellSize}px"
    >
      <!-- Start Position -->
      <div
        class="start-tile"
        class:has-pictograph={startPosition && !startPosition.isBlank}
        title="Start Position"
        role="button"
        tabindex="0"
        style:grid-row="1"
        style:grid-column="1"
        onclick={handleStartClick}
        onkeydown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            handleStartClick();
          }
        }}
        aria-label="Start Position"
      >
        <BeatCell
          beat={startPosition || placeholderBeat}
          index={-1}
          shouldAnimate={displayState.shouldAnimateStartPosition}
          isSelected={isMultiSelectMode
            ? selectedBeatNumbers.has(0)
            : selectedBeatNumber === 0}
          {isMultiSelectMode}
          onLongPress={onStartLongPress}
        />
      </div>

      <!-- Beat Grid -->
      {#each beats as beat, index (beat.id)}
        {@const position = calculateBeatPosition(index, gridLayout().columns)}
        {@const gridRow = position.row}
        {@const gridCol = position.column}
        {@const isDeleting = removingBeatIndices.has(index)}
        {@const shouldSlide =
          removingBeatIndex !== null &&
          !isDeleting &&
          index > removingBeatIndex}
        {@const shouldAnimateBeat = displayState.shouldBeatAnimate(index)}
        {@const shouldHideBeat = displayState.shouldBeatBeHidden(index)}
        <div
          class="beat-container"
          class:deleting={isDeleting}
          class:sliding={shouldSlide}
          class:hidden-for-sequential={shouldHideBeat}
          style:grid-row={gridRow}
          style:grid-column={gridCol}
          style:animation-delay={shouldSlide
            ? `${Math.min(index - removingBeatIndex - 1, 5) * 50}ms`
            : "0ms"}
        >
          <BeatCell
            {beat}
            {index}
            onClick={() => handleBeatClick(beat.beatNumber)}
            onDelete={() => onBeatDelete?.(beat.beatNumber)}
            shouldAnimate={shouldAnimateBeat}
            isSelected={isMultiSelectMode
              ? selectedBeatNumbers.has(beat.beatNumber)
              : selectedBeatNumber === beat.beatNumber}
            isPracticeBeat={practiceBeatNumber === beat.beatNumber}
            {isMultiSelectMode}
            onLongPress={() => onBeatLongPress?.(beat.beatNumber)}
          />
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .beat-grid-container {
    position: relative;
    background: transparent;
    border-radius: 12px;
    overflow: hidden;
    width: 100%;
    height: 100%;
    flex: 1 1 auto;
    min-height: 0;
  }

  .beat-grid-scroll {
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 0 4px;
    box-sizing: border-box;
  }

  /* When scrollbar is present, align to top instead of center */
  .beat-grid-scroll.has-scrollbar {
    align-items: flex-start;
    justify-content: center; /* Keep horizontal centering */
  }

  .beat-grid {
    display: grid;
    grid-template-columns: repeat(var(--grid-cols), var(--cell-size));
    grid-auto-rows: var(--cell-size);
    gap: 1px; /* Subtle separator between pictographs - background shows through */
    max-width: 100%;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    opacity: 1;
    transform: scale(1) translateY(0);
    transition:
      opacity 300ms ease-out,
      transform 300ms ease-out;
  }

  .beat-grid.clearing {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }

  .beat-container,
  .start-tile {
    margin: 0;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    min-width: 0;
    min-height: 0;
  }

  .start-tile {
    border-radius: 8px;
    font-weight: 700;
    letter-spacing: 0.5px;
    background: transparent;
    transition: all 0.2s ease;
  }

  /* Beat deletion animations */
  .beat-container.deleting {
    animation: fadeOutDisintegrate 250ms ease-out forwards;
  }

  .beat-container.sliding {
    animation: slideIntoPlace 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94)
      forwards;
  }

  /* Hide beats waiting for sequential animation */
  .beat-container.hidden-for-sequential {
    opacity: 0;
    pointer-events: none;
  }

  @keyframes fadeOutDisintegrate {
    0% {
      opacity: 1;
      transform: scale(1) rotate(0deg);
      filter: blur(0px);
    }
    50% {
      opacity: 0.6;
      transform: scale(0.9) rotate(-2deg);
      filter: blur(1px);
    }
    100% {
      opacity: 0;
      transform: scale(0.7) rotate(-5deg);
      filter: blur(3px);
      pointer-events: none;
    }
  }

  @keyframes slideIntoPlace {
    0% {
      transform: translateX(0) translateY(0);
    }
    50% {
      transform: translateX(-10px) translateY(-5px);
    }
    100% {
      transform: translateX(0) translateY(0);
    }
  }
</style>
