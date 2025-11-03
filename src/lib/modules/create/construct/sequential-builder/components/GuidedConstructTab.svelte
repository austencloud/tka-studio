<!--
GuidedConstructTab.svelte - Wrapper for Guided Construct mode

Integrates SequentialBuilder with the Create module's workspace.
Handles real-time workspace updates and sequence completion.
-->
<script lang="ts">
  import type { PictographData } from "$shared";
  import SequentialBuilder from "./SequentialBuilder.svelte";

  const {
    onSequenceUpdate,
    onSequenceComplete,
  } = $props<{
    onSequenceUpdate?: (sequence: PictographData[]) => void;
    onSequenceComplete?: (sequence: PictographData[]) => void;
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
  <SequentialBuilder
    onSequenceUpdate={handleSequenceUpdate}
    onSequenceComplete={handleSequenceComplete}
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
