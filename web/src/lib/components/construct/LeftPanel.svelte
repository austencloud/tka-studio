<!--
	LeftPanel.svelte

	Left panel component extracted from ConstructTab.
	Contains the workbench with header showing sequence information.
-->
<script lang="ts">
  import Workbench from "$components/workbench/Workbench.svelte";
</script>

<div class="left-panel" data-testid="left-panel">
  <Workbench />
</div>

<style>
  .left-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    /* Transparent background to show beautiful background without blur */
    background: transparent;
    border: none;
    border-radius: var(--border-radius);
    overflow: hidden;
  }
</style>
