<!--
CAPComponentGrid.svelte - Grid layout for CAP component selection buttons
Displays all available CAP transformations in a responsive 2x2 grid
-->
<script lang="ts">
  import { CAP_COMPONENTS, CAPComponent } from "$build/generate/shared/domain/constants/cap-components";
  import CAPComponentButton from "./CAPComponentButton.svelte";

  let {
    selectedComponents,
    onToggleComponent
  } = $props<{
    selectedComponents: Set<CAPComponent>;
    onToggleComponent: (component: CAPComponent) => void;
  }>();
</script>

<div class="cap-component-grid">
  {#each CAP_COMPONENTS as componentInfo}
    <CAPComponentButton
      {componentInfo}
      isSelected={selectedComponents.has(componentInfo.component)}
      onClick={() => onToggleComponent(componentInfo.component)}
    />
  {/each}
</div>

<style>
  .cap-component-grid {
    display: grid;
    width: 100%;
    flex: 1 1 auto; /* Allow shrinking and growing */
    min-height: 0; /* Critical for flex children to shrink below content size */
    overflow-y: auto; /* Allow scrolling if compressed too much */
    overflow-x: hidden; /* Allow scrolling if compressed too much */
    gap: clamp(8px, 1.5cqi, 16px);

    /* 🎯 DEFAULT: 2x2 grid for square-ish containers */
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
  }

  /* 🌅 WIDE CONTAINERS: Single row when aspect ratio > 1.5 (landscape) */
  @container cap-modal (aspect-ratio > 1.5) {
    .cap-component-grid {
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 1fr;
      max-height: 50cqh; /* Cap height to leave room for header/explanation */
    }
  }

  /* 📱 TALL CONTAINERS: Single column when aspect ratio < 0.7 (portrait) */
  @container cap-modal (aspect-ratio < 0.7) {
    .cap-component-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr);
      margin: 0 auto;
    }
  }

  /* 🎯 SQUARE-ISH CONTAINERS: 2x2 grid (0.7 ≤ aspect ratio ≤ 1.5) */
  /* This is the default, no override needed */
</style>
