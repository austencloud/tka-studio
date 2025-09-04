<!-- TEMPORARY: Simplified Codex Exporter Tab during import migration -->
<script lang="ts">
  import { onMount } from "svelte";

  onMount(() => {
    console.log("✅ CodexExporterTab: Mounted (services temporarily disabled)");
  });
</script>

<div class="codex-exporter-tab">
  <div class="temporary-message">
    <h3>📤 Codex Exporter</h3>
    <p>Temporarily disabled during import migration.</p>
  </div>
</div>

<style>
  .codex-exporter-tab {
    padding: 1rem;
  }

  .temporary-message {
    text-align: center;
    padding: 1rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 4px;
    border: 1px dashed var(--color-border, #ccc);
  }
</style>