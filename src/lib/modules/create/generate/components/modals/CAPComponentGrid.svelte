<!--
CAPComponentGrid.svelte - Grid layout for CAP component selection buttons
Displays all available CAP transformations in a responsive 2x2 grid
-->
<script lang="ts">
  import {
    CAP_COMPONENTS,
    CAPComponent,
  } from "$create/generate/shared/domain/constants/cap-components";
  import CAPComponentButton from "./CAPComponentButton.svelte";

  let {
    selectedComponents,
    isMultiSelectMode = false,
    onToggleComponent,
  } = $props<{
    selectedComponents: Set<CAPComponent>;
    isMultiSelectMode?: boolean;
    onToggleComponent: (component: CAPComponent) => void;
  }>();
</script>

<div class="cap-component-grid">
  {#each CAP_COMPONENTS as componentInfo}
    <CAPComponentButton
      {componentInfo}
      {isMultiSelectMode}
      isSelected={selectedComponents.has(componentInfo.component)}
      onClick={() => onToggleComponent(componentInfo.component)}
    />
  {/each}
</div>

<style>
  .cap-component-grid {
    display: grid;
    width: 100%;
    flex: 1; /* Take up available space */
    gap: 10px;
    min-height: 0;

    /* 🎯 2x2 grid layout */
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
  }
</style>
