<!-- PageGrid.svelte - Grid layout for sequence cards within a page -->
<script lang="ts">
  import type { GridConfig } from "$domain/pageLayout";
  import type { SequenceData } from "$services/interfaces/domain-types";
  // import SequenceCardPrintable from "./SequenceCardPrintable.svelte"; // TEMPORARILY DISABLED

  // Props
  interface Props {
    layout: GridConfig;
    sequences: SequenceData[];
    contentWidth: number;
    contentHeight: number;
    scale?: number;
    onsequenceclick?: (sequence: SequenceData) => void;
  }

  let {
    layout,
    sequences,
    contentWidth,
    contentHeight,
    scale = 1,
    onsequenceclick,
  }: Props = $props();

  // Calculate grid cell dimensions
  let cellWidth = $derived(contentWidth / layout.columns);
  let cellHeight = $derived(contentHeight / layout.rows);

  // Calculate card dimensions (accounting for spacing)
  let cardWidth = $derived(Math.max(0, layout.cardWidth * scale));
  let cardHeight = $derived(Math.max(0, layout.cardHeight * scale));

  // Calculate spacing between cards
  let spacing = $derived(layout.spacing * scale);

  // Generate grid positions for sequences
  let gridPositions = $derived(() => {
    const positions: Array<{
      sequence: SequenceData;
      row: number;
      column: number;
      x: number;
      y: number;
    }> = [];

    sequences.forEach((sequence, index) => {
      const row = Math.floor(index / layout.columns);
      const column = index % layout.columns;

      // Calculate position within the content area
      const x = column * cellWidth + (cellWidth - cardWidth) / 2;
      const y = row * cellHeight + (cellHeight - cardHeight) / 2;

      positions.push({
        sequence,
        row,
        column,
        x: Math.max(0, x),
        y: Math.max(0, y),
      });
    });

    return positions;
  });

  // Handle sequence click
  function handleSequenceClick(sequence: SequenceData) {
    onsequenceclick?.(sequence);
  }
</script>

<div
  class="page-grid"
  style:width="{contentWidth}px"
  style:height="{contentHeight}px"
  style:--rows={layout.rows}
  style:--columns={layout.columns}
  style:--cell-width="{cellWidth}px"
  style:--cell-height="{cellHeight}px"
  style:--card-width="{cardWidth}px"
  style:--card-height="{cardHeight}px"
  style:--spacing="{spacing}px"
>
  <!-- Debug grid lines (only visible in development) -->
  {#if import.meta.env.DEV}
    <div class="grid-lines">
      <!-- Vertical lines -->
      {#each Array(layout.columns + 1) as _, i}
        <div class="grid-line vertical" style:left="{i * cellWidth}px"></div>
      {/each}

      <!-- Horizontal lines -->
      {#each Array(layout.rows + 1) as _, i}
        <div class="grid-line horizontal" style:top="{i * cellHeight}px"></div>
      {/each}
    </div>
  {/if}

  <!-- Sequence cards positioned in grid -->
  {#each gridPositions() as { sequence, row, column, x, y } (sequence.id)}
    <div
      class="card-position"
      style:left="{x}px"
      style:top="{y}px"
      style:width="{cardWidth}px"
      style:height="{cardHeight}px"
      data-row={row}
      data-column={column}
    >
      <!-- TEMPORARILY DISABLED: SequenceCardPrintable -->
      <div
        style="width: 100%; height: 100%; background: #f0f0f0; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666;"
      >
        {sequence.name || "Sequence"}
      </div>
    </div>
  {/each}

  <!-- Empty slots (for development visualization) -->
  {#if import.meta.env.DEV}
    {#each Array(layout.rows * layout.columns - sequences.length) as _, i}
      {@const totalIndex = sequences.length + i}
      {@const row = Math.floor(totalIndex / layout.columns)}
      {@const column = totalIndex % layout.columns}
      {@const x = column * cellWidth + (cellWidth - cardWidth) / 2}
      {@const y = row * cellHeight + (cellHeight - cardHeight) / 2}

      <div
        class="empty-slot"
        style:left="{x}px"
        style:top="{y}px"
        style:width="{cardWidth}px"
        style:height="{cardHeight}px"
        data-row={row}
        data-column={column}
      >
        <div class="empty-indicator">
          <span class="empty-text">Empty</span>
          <span class="empty-coords">{row + 1},{column + 1}</span>
        </div>
      </div>
    {/each}
  {/if}
</div>

<style>
  .page-grid {
    position: relative;
    background: transparent;
    overflow: hidden;
  }

  /* Grid lines for development */
  .grid-lines {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.1;
  }

  .grid-line {
    position: absolute;
    background: #007acc;
  }

  .grid-line.vertical {
    width: 1px;
    height: 100%;
  }

  .grid-line.horizontal {
    width: 100%;
    height: 1px;
  }

  /* Card positioning */
  .card-position {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-fast);
  }

  .card-position:hover {
    z-index: 10;
    transform: scale(1.02);
  }

  /* Empty slots (development only) */
  .empty-slot {
    position: absolute;
    border: 1px dashed rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.02);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.5;
  }

  .empty-indicator {
    text-align: center;
    color: #999;
    font-size: 10px;
    font-family: "Arial", sans-serif;
  }

  .empty-text {
    display: block;
    font-weight: 500;
  }

  .empty-coords {
    display: block;
    font-size: 8px;
    opacity: 0.7;
  }

  /* Print styles */
  @media print {
    .grid-lines {
      display: none;
    }

    .empty-slot {
      display: none;
    }

    .card-position:hover {
      transform: none;
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .card-position:hover {
      transform: scale(1.01);
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .grid-line {
      background: #000;
      opacity: 0.3;
    }

    .empty-slot {
      border-color: #000;
      background: rgba(0, 0, 0, 0.05);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .card-position {
      transition: none;
    }

    .card-position:hover {
      transform: none;
    }
  }
</style>
