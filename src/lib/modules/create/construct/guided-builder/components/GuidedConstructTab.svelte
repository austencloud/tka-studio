<!--
GuidedConstructTab.svelte - Wrapper for Guided Construct mode

Integrates GuidedBuilder with the Create module's workspace.
Handles real-time workspace updates and sequence completion.
-->
<script lang="ts">
  import type { PictographData, GridMode } from "$shared";
  import GuidedBuilder from "./GuidedBuilder.svelte";

  const {
    onSequenceUpdate,
    onSequenceComplete,
    onHeaderTextChange,
    onGridModeChange,
  } = $props<{
    onSequenceUpdate?: (sequence: PictographData[]) => void;
    onSequenceComplete?: (sequence: PictographData[]) => void;
    onHeaderTextChange?: (text: string) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
  }>();

  // Handle sequence updates (during building)
  function handleSequenceUpdate(sequence: PictographData[]) {
    onSequenceUpdate?.(sequence);
  }

  // Handle sequence completion
  function handleSequenceComplete(sequence: PictographData[]) {
    onSequenceComplete?.(sequence);
  }
</script>

<div class="guided-construct-tab">
  <GuidedBuilder
    onSequenceUpdate={handleSequenceUpdate}
    onSequenceComplete={handleSequenceComplete}
    {onHeaderTextChange}
    {onGridModeChange}
  />
</div>

<style>
  .guided-construct-tab {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
    width: 100%;
  }
</style>
