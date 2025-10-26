<!--
CAPExplanationPanel.svelte - Displays explanation of selected CAP transformations
Shows contextual information based on current selection
-->
<script lang="ts">
  let {
    explanationText
  } = $props<{
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
    border-radius: clamp(8px, 2cqi, 12px);
    padding: clamp(10px, 2cqh, 20px) clamp(12px, 2cqw, 18px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    flex: 0 1 auto; /* Allow shrinking but don't grow */
    min-height: 0; /* Critical for flex children to shrink below content size */
    overflow-y: auto; /* Allow scrolling if text is too long when compressed */
  }

  .explanation-panel h3 {
    color: white;
    font-size: clamp(11px, 2.5cqi, 16px);
    font-weight: 600;
    margin: 0 0 clamp(4px, 1cqh, 10px) 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .explanation-panel p {
    color: rgba(255, 255, 255, 0.9);
    font-size: clamp(10px, 2cqi, 14px);
    line-height: 1.4;
    margin: 0;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }
</style>
