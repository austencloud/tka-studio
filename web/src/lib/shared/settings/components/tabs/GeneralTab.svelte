<!-- TEMPORARY: Simplified General Tab during import migration -->
<script lang="ts">
  import { onMount } from "svelte";

  onMount(() => {
    console.log("✅ GeneralTab: Mounted (services temporarily disabled)");
  });
</script>

<div class="general-tab">
  <div class="temporary-message">
    <h3>⚙️ General Settings</h3>
    <p>Temporarily disabled during import migration.</p>
  </div>
</div>

<style>
  .general-tab {
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