<!--
AssemblyOptionGrid.svelte - Grid container for assembly option selection buttons

Displays 6 option buttons in one of four layouts:
- 3×2 grid (default - 3 columns, 2 rows)
- 2×3 grid (for moderately tall containers)
- 1×6 column (for very tall containers)
- 6×1 row (for very wide containers)
-->
<script lang="ts">
  import type { MotionColor, PictographData } from "$shared";
  import AssemblyOptionButton from "./AssemblyOptionButton.svelte";

  const {
    options,
    visibleHand,
    isDisabled = false,
    onOptionSelect,
    getOptionLabel,
  } = $props<{
    options: PictographData[];
    visibleHand: MotionColor;
    isDisabled?: boolean;
    onOptionSelect: (option: PictographData) => void;
    getOptionLabel?: (option: PictographData, index: number) => string;
  }>();
</script>

<div class="option-grid">
  {#each options as option, index (option.id)}
    <AssemblyOptionButton
      {option}
      {visibleHand}
      {isDisabled}
      ariaLabel={getOptionLabel?.(option, index)}
      onSelect={onOptionSelect}
    />
  {/each}
</div>

<style>
  .option-grid {
    display: grid;
    /* Default: 3×2 grid layout */
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    /* Flow items down columns so STATIC and DASH are in same column */
    grid-auto-flow: column;
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

  /* Moderately tall container: Use 2×3 grid layout */
  @container (aspect-ratio < 1.2) {
    .option-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(3, 1fr);
      /* Flow items across rows so STATIC and DASH are in same row */
      grid-auto-flow: row;
    }
  }

  /* Very tall container: Use 1×6 column layout */
  @container (aspect-ratio < 0.5) {
    .option-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(6, 1fr);
    }
  }

  /* Very wide container: Use 6×1 row layout */
  @container (aspect-ratio > 2.5) {
    .option-grid {
      grid-template-columns: repeat(6, 1fr);
      grid-template-rows: 1fr;
    }
  }
</style>
