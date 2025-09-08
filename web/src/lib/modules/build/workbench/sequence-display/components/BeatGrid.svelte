<script lang="ts">
  import {  resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { crossfade } from "svelte/transition";
  import { createBeatGridState } from "../state";
  import BeatCellView from "./BeatCellView.svelte";
  import type { BeatData } from "../../shared";
  import { createBeatData } from "../../shared/domain/factories";

  interface Props {
    beats: ReadonlyArray<BeatData> | BeatData[];
    startPosition?: BeatData | null;
    selectedBeatIndex?: number;
    onBeatClick?: (index: number) => void;

    onStartClick?: () => void;
    isScrollable?: boolean;
    fullScreenMode?: boolean;
    onnaturalheightchange?: (data: { height: number }) => void;
  }

  let {
    beats,
    startPosition = null,
    selectedBeatIndex = -1,
    onBeatClick,
    onStartClick,
    isScrollable = false,
    fullScreenMode = false,
    onnaturalheightchange,
  }: Props = $props();

  // Debug logs removed for cleaner output

  // Get service from DI container and create component-scoped state
  const beatGridService = resolve<import("../services/contracts").IBeatGridService>(
    TYPES.IBeatGridService
  );
  const beatGridState = createBeatGridState(beatGridService);

  const config = $derived(beatGridState.config);
  const hoveredBeatIndex = $derived(beatGridState.hoveredBeatIndex);

  // Create placeholder beat for empty start position - uses Beat component's built-in empty state
  const placeholderBeat = createBeatData({
    beatNumber: 0,
    pictographData: null,
    isBlank: true
  });

  // Set up crossfade transition for smooth start position transitions
  const [send, receive] = crossfade({
    duration: 400,
    // Completely disable the default crossfade transform calculations
    fallback: () => ({
      duration: 400,
      css: (t: number) => `opacity: ${t};`
    }),
    // Override the default crossfade function to prevent NaN calculations
    easing: (t: number) => t
  });

  // Use layout info instead of just dimensions for better responsiveness
  const layoutInfo = $derived(beatGridState.calculateLayoutInfo(beats.length));
  const frameDimensions = $derived({
    width: layoutInfo.totalWidth,
    height: layoutInfo.totalHeight,
  });

  let containerRef: HTMLElement;

  // Track container dimensions and update beat grid service
  onMount(() => {
    if (containerRef) {
      // Set up resize observer with debouncing
      let timeoutId: ReturnType<typeof setTimeout>;
      const resizeObserver = new ResizeObserver((entries) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          for (const entry of entries) {
            const { width, height } = entry.contentRect;
            beatGridState.updateContainerDimensions({
              width,
              height,
              isFullscreen: fullScreenMode,
            });
          }
        }, 100); // Debounce by 100ms
      });

      resizeObserver.observe(containerRef);

      // Initial dimension setting
      const rect = containerRef.getBoundingClientRect();
      beatGridState.updateContainerDimensions({
        width: rect.width,
        height: rect.height,
        isFullscreen: fullScreenMode,
      });

      return () => {
        clearTimeout(timeoutId);
        resizeObserver.disconnect();
      };
    }
  });

  // Update fullscreen mode when it changes (debounced)
  let fullscreenUpdateTimeout: ReturnType<typeof setTimeout>;
  $effect(() => {
    clearTimeout(fullscreenUpdateTimeout);
    fullscreenUpdateTimeout = setTimeout(() => {
      if (containerRef) {
        const rect = containerRef.getBoundingClientRect();
        beatGridState.updateContainerDimensions({
          width: rect.width,
          height: rect.height,
          isFullscreen: fullScreenMode,
        });
      }
    }, 50);
  });

  // Emit natural height whenever calculated frame dimensions change
  $effect(() => {
    if (frameDimensions?.height != null) {
      onnaturalheightchange?.({ height: frameDimensions.height });
    }
  });

  // Determine if scrolling is needed based on layout info
  const shouldScroll = $derived(layoutInfo.shouldScroll);

  // Use shouldScroll for internal logic, but still respect the isScrollable prop from parent
  const effectiveScrollable = $derived(isScrollable || shouldScroll);

  // Update service configuration when layout info changes (outside derived) - with safeguards
  let lastCellSize = 0;
  let lastColumns = 0;
  $effect(() => {
    // Only update if values actually changed and are valid
    if (
      layoutInfo.cellSize > 0 &&
      layoutInfo.cellSize !== lastCellSize &&
      layoutInfo.columns !== lastColumns
    ) {
      lastCellSize = layoutInfo.cellSize;
      lastColumns = layoutInfo.columns;

      // Only update if significantly different to prevent micro-adjustments
      if (Math.abs(layoutInfo.cellSize - beatGridState.config.beatSize) > 1) {
        beatGridState.setConfig({
          beatSize: layoutInfo.cellSize,
          columns: layoutInfo.columns,
        });
      }
    }
  });

  function handleBeatClick(index: number) {
    onBeatClick?.(index);
  }

  function handleBeatHover(index: number) {
    beatGridState.setHoveredBeatIndex(index);
  }

  function handleBeatLeave() {
    beatGridState.clearHover();
  }
</script>

<div
  class="beat-grid-container"
  class:scrollable-active={effectiveScrollable}
  bind:this={containerRef}
>
  <div class="beat-grid-scroll">
    <div
      class="beat-grid"
      style:width="{frameDimensions.width}px"
      style:height="{frameDimensions.height}px"
    >
      <!-- Start Position tile centered when enabled -->
      {#if config.hasStartTile}
        <div
          class="start-tile"
          class:has-pictograph={startPosition?.pictographData}
          title="Start Position"
          role="button"
          tabindex="0"
          onclick={() => onStartClick?.()}
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              onStartClick?.();
            }
          }}
          aria-label="Start Position"
        >
          <!-- True crossfade between placeholder and actual start position -->
          {#if startPosition?.pictographData}
            <div
              class="transition-wrapper"
              in:receive={{ key: 'start-position' }}
              out:send={{ key: 'start-position' }}
            >
              <BeatCellView
                beat={startPosition}
                index={-1}
                isSelected={false}
                isHovered={false}
              />
            </div>
          {:else}
            <div
              class="transition-wrapper"
              in:receive={{ key: 'start-position' }}
              out:send={{ key: 'start-position' }}
            >
              <BeatCellView
                beat={placeholderBeat}
                index={-1}
                isSelected={false}
                isHovered={false}
              />
            </div>
          {/if}
        </div>
      {/if}

      {#each beats as beat, index}
        {@const position = beatGridState.calculateBeatPosition(
          index,
          beats.length
        )}
        <div
          class="beat-container"
          style:left="{position.x}px"
          style:top="{position.y}px"
          style:width="{config.beatSize}px"
          style:height="{config.beatSize}px"
        >
          <BeatCellView
            {beat}
            {index}
            isSelected={index === selectedBeatIndex}
            isHovered={index === hoveredBeatIndex}
            onClick={handleBeatClick}
            onHover={handleBeatHover}
            onLeave={handleBeatLeave}
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

    border: 1px solid rgba(0, 0, 0, 0.1);
  }

  .beat-grid-scroll {
    overflow: auto;
    display: flex;
    justify-content: center; /* center like Qt AlignCenter */
    align-items: center; /* center vertically as well */
    height: 100%; /* fill available height to center content properly */
  }

  /* Scroll mode parity with legacy */
  .beat-grid-container.scrollable-active {
    height: 100%;
    overflow: hidden; /* inner scroll element handles y-scroll */
  }

  .beat-grid-container.scrollable-active .beat-grid-scroll {
    overflow-y: auto;
    overflow-x: hidden;
    align-items: flex-start;
    padding-right: 8px; /* space for scrollbar */
  }

  .beat-grid-container.scrollable-active
    .beat-grid-scroll::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  .beat-grid-container.scrollable-active
    .beat-grid-scroll::-webkit-scrollbar-track {
    background: transparent;
  }
  .beat-grid-container.scrollable-active
    .beat-grid-scroll::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  .beat-grid {
    position: relative;
    margin: 0; /* legacy parity: no padding/margins on grid area */
    padding: 0;
  }

  .beat-container,
  .start-tile {
    /* zero gaps between cells for parity */
    margin: 0;
  }

  .start-tile {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 8px;
    font-weight: 700;
    letter-spacing: 0.5px;
    /* Clean container - BeatView handles all styling and centering */
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .transition-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .beat-container {
    position: absolute;
    transition: all 0.2s ease;
  }

  /* Subtle grid pattern for parity feel */
  .beat-grid::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: radial-gradient(
      circle at 1px 1px,
      rgba(0, 0, 0, 0.05) 1px,
      transparent 0
    );
    background-size: 20px 20px;
    pointer-events: none;
    border-radius: inherit;
  }
</style>
