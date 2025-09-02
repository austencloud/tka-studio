<script lang="ts">
  import type { BeatData } from "$domain";
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import { createBeatFrameState } from "$state";
  import { onMount } from "svelte";
  import BeatView from "./BeatView.svelte";

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

  // Get service from DI container and create component-scoped state
  const beatFrameService = resolve<import("$contracts").IBeatFrameService>(
    TYPES.IBeatFrameService
  );
  const beatFrameState = createBeatFrameState(beatFrameService);

  const config = $derived(beatFrameState.config);
  const hoveredBeatIndex = $derived(beatFrameState.hoveredBeatIndex);

  // Use layout info instead of just dimensions for better responsiveness
  const layoutInfo = $derived(beatFrameState.calculateLayoutInfo(beats.length));
  const frameDimensions = $derived({
    width: layoutInfo.totalWidth,
    height: layoutInfo.totalHeight,
  });

  let containerRef: HTMLElement;
  let beatFrameScrollRef: HTMLElement = $state()!;
  let beatFrameRef: HTMLElement = $state()!;
  let startTileRef: HTMLElement = $state()!;

  // Track container dimensions and update beat frame service
  onMount(() => {
    if (containerRef) {
      // Set up resize observer with debouncing
      let timeoutId: ReturnType<typeof setTimeout>;
      const resizeObserver = new ResizeObserver((entries) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          for (const entry of entries) {
            const { width, height } = entry.contentRect;
            beatFrameState.updateContainerDimensions({
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
      beatFrameState.updateContainerDimensions({
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
        beatFrameState.updateContainerDimensions({
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
      if (Math.abs(layoutInfo.cellSize - beatFrameState.config.beatSize) > 1) {
        beatFrameState.setConfig({
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
    beatFrameState.setHoveredBeatIndex(index);
  }

  function handleBeatLeave() {
    beatFrameState.clearHover();
  }
</script>

<div
  class="beat-frame-container"
  class:scrollable-active={effectiveScrollable}
  bind:this={containerRef}
>
  <div class="beat-frame-scroll" bind:this={beatFrameScrollRef}>
    <div
      class="beat-frame"
      bind:this={beatFrameRef}
      style:width="{frameDimensions.width}px"
      style:height="{frameDimensions.height}px"
    >
      <!-- Start Position tile at [0,0] when enabled -->
      {#if config.hasStartTile}
        {@const startPositionCoords = beatFrameState.calculateStartPosition(
          beats.length
        )}
        <div
          class="start-tile"
          bind:this={startTileRef}
          class:has-pictograph={startPosition?.pictographData}
          style:left="{startPositionCoords.x}px"
          style:top="{startPositionCoords.y}px"
          style:width="{config.beatSize}px"
          style:height="{config.beatSize}px"
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
          {#if startPosition?.pictographData}
            <!-- Display actual start position pictograph -->
            <BeatView
              beat={startPosition}
              index={-1}
              isSelected={false}
              isHovered={false}
            />
          {:else}
            <!-- Default START label when no start position is set -->
            <div class="start-label">START</div>
          {/if}
        </div>
      {/if}

      {#each beats as beat, index}
        {@const position = beatFrameState.calculateBeatPosition(
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
          <BeatView
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
  .beat-frame-container {
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

  .beat-frame-scroll {
    overflow: auto;
    display: flex;
    justify-content: center; /* center like Qt AlignCenter */
    align-items: center; /* center vertically as well */
    height: 100%; /* fill available height to center content properly */
  }

  /* Scroll mode parity with legacy */
  .beat-frame-container.scrollable-active {
    height: 100%;
    overflow: hidden; /* inner scroll element handles y-scroll */
  }

  .beat-frame-container.scrollable-active .beat-frame-scroll {
    overflow-y: auto;
    overflow-x: hidden;
    align-items: flex-start;
    padding-right: 8px; /* space for scrollbar */
  }

  .beat-frame-container.scrollable-active
    .beat-frame-scroll::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  .beat-frame-container.scrollable-active
    .beat-frame-scroll::-webkit-scrollbar-track {
    background: transparent;
  }
  .beat-frame-container.scrollable-active
    .beat-frame-scroll::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  .beat-frame {
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
    position: relative;
    left: 0;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  /* Empty start tile styling */
  .start-tile:not(.has-pictograph) {
    border: 2px dashed #ced4da;
    background: #f8f9fa;
    color: #6c757d;
  }

  /* Start tile with pictograph - no border, no background */
  .start-tile.has-pictograph {
    border: none;
  }

  .start-label {
    font-size: 14px;
  }

  .beat-container {
    position: absolute;
    transition: all 0.2s ease;
  }

  /* Subtle grid pattern for parity feel */
  .beat-frame::before {
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
