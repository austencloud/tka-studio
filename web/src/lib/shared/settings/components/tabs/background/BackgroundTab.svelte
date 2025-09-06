<!-- TEMPORARY: Simplified Background Tab during import migration -->
<script lang="ts">
  import { onMount } from "svelte";

  onMount(() => {
    console.log("✅ BackgroundTab: Mounted (services temporarily disabled)");
  });
</script>

<div class="background-tab">
  <div class="temporary-message">
    <h3>🎨 Background Settings</h3>
    <p>Temporarily disabled during import migration.</p>
  </div>
</div>

<style>
  .background-tab {
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