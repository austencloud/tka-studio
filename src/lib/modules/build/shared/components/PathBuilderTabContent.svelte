<!--
  PathBuilderTabContent.svelte

  Wrapper component for the Path Builder tab.
  Handles sequence completion and integration with the build system.
-->
<script lang="ts">
  import { GesturalPathBuilder } from "../../construct";

  let {
    onPathBuilderSequenceComplete,
  } = $props<{
    onPathBuilderSequenceComplete?: (motions: { blue: any[]; red: any[] }) => void;
  }>();

  function handleSequenceComplete(motions: { blue: any[]; red: any[] }): void {
    console.log("Path builder sequence complete:", motions);
    onPathBuilderSequenceComplete?.(motions);
  }

  function handleCancel(): void {
    console.log("Path builder cancelled");
    // User can navigate back to construct using the nav buttons
  }
</script>

<div class="path-builder-tab-content" data-testid="path-builder-tab-content">
  <GesturalPathBuilder
    onSequenceComplete={handleSequenceComplete}
    onCancel={handleCancel}
  />
</div>

<style>
  .path-builder-tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
    width: 100%;
  }
</style>
