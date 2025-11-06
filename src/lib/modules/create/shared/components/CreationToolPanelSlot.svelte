<script lang="ts">
  /**
   * Creation Tool Panel Slot
   *
   * Conditionally renders either:
   * 1. Creation Method Selector (when workspace is empty and no method selected)
   * 2. Tool Panel (after method selection or when workspace has content)
   *
   * Handles smooth fade transitions between the two states.
   *
   * Extracted from CreateModule to reduce component size.
   *
   * Domain: Create module - Tool panel presentation
   */

  import { fade } from "svelte/transition";
  import { navigationState, type BuildModeId, type PictographData } from "$shared";
  import ToolPanel from "../../../tool-panel/core/ToolPanel.svelte";
  import CreationMethodSelector from "../../../workspace-panel/components/CreationMethodSelector.svelte";
  import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
  import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
  import type { IToolPanelMethods } from "../types/create-module-types";

  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // Props
  let {
    createModuleState,
    constructTabState,
    toolPanelRef = $bindable(),
    isSideBySideLayout,
    practiceBeatIndex,
    isFilterPanelOpen,
    onMethodSelected,
    onOptionSelected,
    onPracticeBeatIndexChange,
    onOpenFilters,
    onCloseFilters,
  }: {
    createModuleState: CreateModuleState;
    constructTabState: ConstructTabState;
    toolPanelRef?: IToolPanelMethods | null;
    isSideBySideLayout: () => boolean;
    practiceBeatIndex: number | null;
    isFilterPanelOpen: boolean;
    onMethodSelected: (method: BuildModeId) => void;
    onOptionSelected: (option: PictographData) => Promise<void>;
    onPracticeBeatIndexChange: (index: number | null) => void;
    onOpenFilters: () => void;
    onCloseFilters: () => void;
  } = $props();
</script>

{#if navigationState.isCreationMethodSelectorVisible}
  <!-- Creation Method Selector (shown when workspace is empty and no method selected) -->
  <div
    class="creation-method-container"
    in:fade={{ duration: 400 }}
    out:fade={{ duration: 400 }}
  >
    <CreationMethodSelector {onMethodSelected} />
  </div>
{:else}
  <!-- Normal Tool Panel (shown after method selection or when workspace has content) -->
  <div class="tool-panel-wrapper" in:fade={{ duration: 400, delay: 200 }}>
    <ToolPanel
      bind:this={toolPanelRef}
      {createModuleState}
      {constructTabState}
      {onOptionSelected}
      {isSideBySideLayout}
      onPracticeBeatIndexChange={onPracticeBeatIndexChange}
      {onOpenFilters}
      {onCloseFilters}
      {isFilterPanelOpen}
    />
  </div>
{/if}

<style>
  /* Creation method selector - absolutely positioned to prevent layout shift during transition */
  .creation-method-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 10; /* Above tool panel */
  }

  /* Tool panel wrapper - normal flexbox layout */
  .tool-panel-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
</style>
