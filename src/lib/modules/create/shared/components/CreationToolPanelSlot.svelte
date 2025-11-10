<script lang="ts">
  /**
   * Creation Tool Panel Slot
   *
   * Renders the tool panel for the Create module.
   *
   * Domain: Create module - Tool panel presentation
   */

  import type { PictographData } from "$shared";
  import type { IToolPanelMethods } from "../types/create-module-types";
  import { ToolPanel } from ".";
  import { getCreateModuleContext } from "../context";

  // Get context
  const ctx = getCreateModuleContext();
  const {
    CreateModuleState: createModuleState,
    constructTabState,
    panelState,
    layout,
  } = ctx;

  // Derive values from context
  const isSideBySideLayout = () => layout.shouldUseSideBySideLayout;
  const isFilterPanelOpen = $derived(panelState.isFilterPanelOpen);

  // Props (only callbacks and bindable refs)
  let {
    toolPanelRef = $bindable(),
    onOptionSelected,
    onPracticeBeatIndexChange,
    onOpenFilters,
    onCloseFilters,
  }: {
    toolPanelRef?: IToolPanelMethods | null;
    onOptionSelected: (option: PictographData) => Promise<void>;
    onPracticeBeatIndexChange: (index: number | null) => void;
    onOpenFilters: () => void;
    onCloseFilters: () => void;
  } = $props();
</script>

<div class="tool-panel-wrapper">
  <ToolPanel
    bind:this={toolPanelRef}
    {createModuleState}
    {constructTabState}
    {onOptionSelected}
    {isSideBySideLayout}
    {onPracticeBeatIndexChange}
    {onOpenFilters}
    {onCloseFilters}
    {isFilterPanelOpen}
  />
</div>

<style>
  .tool-panel-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
</style>
