<script lang="ts">
  import { createBeatData, type BeatData } from "$shared";
  import { onMount } from "svelte";
  import BeatCell from "./BeatCell.svelte";

  let {
    beats,
    startPosition = null,
    onBeatClick,
    onStartClick,
  } = $props<{
    beats: ReadonlyArray<BeatData> | BeatData[];
    startPosition?: BeatData | null;
    onBeatClick?: (index: number) => void;
    onStartClick?: () => void;
  }>();

  const placeholderBeat = createBeatData({
    beatNumber: 0,
    pictographData: null,
    isBlank: true
  });



  // Container dimensions for responsive sizing
  let containerWidth = $state(0);
  let containerHeight = $state(0);
  let containerRef: HTMLElement | undefined = $state();

  const gridLayout = $derived(() => {
    const beatCount = beats.length;
    const columns = beatCount <= 4 ? beatCount : 4;
    const rows = Math.ceil(beatCount / columns);
    const totalColumns = columns + 1; // +1 for start position

    // Calculate responsive cell size
    let cellSize = 160; // Default
    if (containerWidth > 0 && containerHeight > 0) {
      // Use 90% of container width to create breathing room on the sides
      const maxCellWidth = (containerWidth * 0.9) / totalColumns;
      const maxCellHeight = containerHeight / rows;
      const maxCellSize = Math.min(maxCellWidth, maxCellHeight);
      cellSize = Math.max(50, Math.min(300, Math.floor(maxCellSize)));
    }

    return {
      rows,
      columns,
      totalColumns,
      cellSize,
    };
  });

  let newlyAddedBeatIndex = $state<number | null>(null);
  let previousBeatCount = beats.length;

  $effect(() => {
    if (beats.length > previousBeatCount) {
      newlyAddedBeatIndex = beats.length - 1;
      setTimeout(() => {
        newlyAddedBeatIndex = null;
      }, 400);
    }
    previousBeatCount = beats.length;
  });

  // Simple ResizeObserver for responsive sizing
  onMount(() => {
    if (containerRef) {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          containerWidth = width - 8; // Account for padding
          containerHeight = height - 8;
        }
      });

      resizeObserver.observe(containerRef);

      // Initial size
      const rect = containerRef.getBoundingClientRect();
      containerWidth = rect.width - 8;
      containerHeight = rect.height - 8;

      return () => resizeObserver.disconnect();
    }
  });

  function handleBeatClick(index: number) {
    onBeatClick?.(index);
  }


</script>

<div class="beat-grid-container" bind:this={containerRef}>
  <div class="beat-grid-scroll">
    <div
      class="beat-grid"
      style:--grid-rows="{gridLayout().rows}"
      style:--grid-cols="{gridLayout().totalColumns}"
      style:--cell-size="{gridLayout().cellSize}px"
    >
      <!-- Start Position tile positioned in grid column 1, row 1 -->
      <div
          class="start-tile"
          class:has-pictograph={startPosition?.pictographData}
          title="Start Position"
          role="button"
          tabindex="0"
          style:grid-row="1"
          style:grid-column="1"
          onclick={() => onStartClick?.()}
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              onStartClick?.();
            }
          }}
          aria-label="Start Position"
        >
          <!-- Single BeatCell that transitions its internal content -->
          <BeatCell
            beat={startPosition?.pictographData ? startPosition : placeholderBeat}
            index={-1}
          />
        </div>

      {#each beats as beat, index}
        {@const gridRow = Math.floor(index / gridLayout().columns) + 1}
        {@const gridCol = (index % gridLayout().columns) + 2}
        <div
          class="beat-container"
          style:grid-row="{gridRow}"
          style:grid-column="{gridCol}"
        >
          <BeatCell
            {beat}
            {index}
            onClick={() => handleBeatClick(index)}
            shouldAnimate={index === newlyAddedBeatIndex}
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
    /* Constrain width to parent and prevent horizontal scrollbars */
    width: 100%;
    max-width: 100%;
    overflow-x: hidden; /* Never allow horizontal scrollbars */
    overflow-y: auto; /* Allow vertical scrolling when needed */
    display: flex;
    justify-content: center; /* center like Qt AlignCenter */
    align-items: center; /* center vertically as well */
    height: 100%; /* fill available height to center content properly */
    /* Add small padding to prevent content from touching edges */
    padding: 0 4px;
    box-sizing: border-box;
  }



  .beat-grid {
    display: grid;
    grid-template-columns: repeat(var(--grid-cols), var(--cell-size)); /* Fixed size columns for square cells */
    grid-auto-rows: var(--cell-size); /* Fixed size rows for square cells */
    gap: 0; /* No gap between cells like legacy */
    /* Ensure grid doesn't exceed container width */
    max-width: 100%;
    margin: 0;
    padding: 0;
    /* Prevent horizontal overflow */
    box-sizing: border-box;
  }

  .beat-container,
  .start-tile {
    /* Grid positioning - no absolute positioning needed */
    margin: 0;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    min-width: 0;
    min-height: 0;
    /* Remove aspect-ratio so beats fill grid columns completely */
  }

  .start-tile {
    border-radius: 8px;
    font-weight: 700;
    letter-spacing: 0.5px;
    /* Clean container - BeatView handles all styling and centering */
    background: transparent;
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
