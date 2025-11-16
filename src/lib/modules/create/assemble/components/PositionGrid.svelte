<!--
PositionGrid.svelte - Grid container for position selection buttons

Displays 4 position buttons in one of three layouts:
- 2x2 grid (default)
- 4x1 column (for tall containers)
- 1x4 row (for wide containers)
-->
<script lang="ts">
  import type { GridMode, PictographData } from "$shared";
  import { GridLocation, MotionColor } from "$shared";
  import PositionButton from "./PositionButton.svelte";

  const { positions, locations, handColor, gridMode, onPositionSelect } =
    $props<{
      positions: PictographData[];
      locations: GridLocation[];
      handColor: MotionColor;
      gridMode: GridMode;
      onPositionSelect: (
        pictograph: PictographData,
        location: GridLocation
      ) => void;
    }>();
</script>

<div class="position-grid">
  {#each positions as pictograph, index}
    {@const location = locations[index]}

    {#if location}
      <PositionButton
        {pictograph}
        {location}
        {handColor}
        {gridMode}
        onSelect={onPositionSelect}
      />
    {/if}
  {/each}
</div>

<style>
  .position-grid {
    display: grid;
    /* Default: 2x2 grid layout */
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: min(2cqmin, 1rem);

    flex: 1;
    width: 100%;
    height: 100%;
    padding: 0;

    /* Stretch items to fill grid cells completely */
    align-items: stretch;
    justify-items: stretch;
    align-content: stretch;

    container-type: size;
  }

  /* Tall container: Use 4x1 column layout */
  @container (aspect-ratio < 0.75) {
    .position-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr);
    }
  }

  /* Wide container: Use 1x4 row layout */
  @container (aspect-ratio > 1.5) {
    .position-grid {
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 1fr;
    }
  }
</style>
