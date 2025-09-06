<script lang="ts">
  import type { Snippet } from "svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const { panelName = "", children } = $props<{
    panelName?: string;
    children: Snippet;
  }>();
</script>

<div class="panel-container" data-panel={panelName}>
  {@render children()}
</div>

<style>
  .panel-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
</style>
