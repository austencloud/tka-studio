<!--
CAPExplanationPanel.svelte - Displays explanation of selected CAP transformations
Shows contextual information based on current selection
-->
<script lang="ts">
  let { explanationText } = $props<{
    explanationText: string;
  }>();
</script>

<div class="explanation-panel">
  <h3>What this does:</h3>
  <p>{explanationText}</p>
</div>

<style>
  .explanation-panel {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 10px 14px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
  }

  .explanation-panel h3 {
    color: white;
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 6px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .explanation-panel p {
    color: rgba(255, 255, 255, 0.95);
    font-size: 13px;
    line-height: 1.4;
    margin: 0;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }
</style>
