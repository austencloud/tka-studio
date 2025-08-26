<!--
GeneratePanelHeader.svelte - Header section for the generate panel
Simple component containing the title and header styling
-->

<div class="header">
  <h3>Customize Your Sequence</h3>
</div>

<style>
  .header {
    flex-shrink: 0;
    text-align: center;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  /* Compact layout adjustments */
  :global(.generate-panel[data-layout="compact"]) .header h3 {
    font-size: 16px;
  }
</style>
