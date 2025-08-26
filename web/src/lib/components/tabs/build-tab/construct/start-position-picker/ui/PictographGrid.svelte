<!-- PictographGrid.svelte - Pictograph grid display for StartPositionPicker -->
<script lang="ts">
  import type { PictographData } from "$domain/PictographData";
  import Pictograph from "$lib/components/core/pictograph/Pictograph.svelte";
  import { getLetterBorderColorSafe } from "$lib/domain";

  const {
    pictographDataSet,
    selectedPictograph = null,
    onPictographSelect,
  } = $props<{
    pictographDataSet: PictographData[];
    selectedPictograph?: PictographData | null;
    onPictographSelect: (pictograph: PictographData) => void;
  }>();
</script>

<div class="pictograph-row">
  {#each pictographDataSet as pictographData (pictographData.id)}
    <div
      class="pictograph-container"
      class:selected={selectedPictograph?.id === pictographData.id}
      role="button"
      tabindex="0"
      style:--letter-border-color={getLetterBorderColorSafe(
        pictographData.letter
      )}
      onclick={() => onPictographSelect(pictographData)}
      onkeydown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onPictographSelect(pictographData);
        }
      }}
    >
      <!-- Render pictograph using Pictograph component -->
      <div class="pictograph-wrapper">
        <Pictograph {pictographData} />
      </div>

      <!-- Position label -->
      <div class="position-label">
        {pictographData.letter || "Start Position"}
      </div>
    </div>
  {/each}
</div>

<style>
  .pictograph-row {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 90%;
    gap: 3%;
    margin: auto;
    flex: 0 0 auto;
    padding: 2rem 0;
  }

  .pictograph-container {
    width: 25%;
    aspect-ratio: 1 / 1;
    height: auto;
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    border: 2px solid transparent;
    border-radius: var(--border-radius);
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pictograph-container:hover {
    transform: scale(1.05);
    border-color: var(--letter-border-color, var(--primary));
    box-shadow: var(--shadow-lg);
  }

  .pictograph-container.selected {
    border-color: var(--letter-border-color, var(--primary));
    background: var(--primary) / 10;
  }

  .pictograph-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .position-label {
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--foreground);
    text-align: center;
    white-space: nowrap;
  }

  @media (max-width: 768px) {
    .pictograph-row {
      flex-direction: column;
      gap: var(--spacing-lg);
    }

    .pictograph-container {
      width: 80%;
      max-width: 200px;
    }
  }
</style>
