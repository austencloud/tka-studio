<script lang="ts">
  import { slide } from "svelte/transition";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const { sequenceCount = 0, isVisible = false } = $props<{
    sequenceCount?: number;
    isVisible?: boolean;
  }>();
</script>

{#if isVisible}
  <div class="results-footer" transition:slide>
    <span class="results-count">
      {sequenceCount} sequence{sequenceCount !== 1 ? "s" : ""} found
    </span>
  </div>
{/if}

<style>
  .results-footer {
    flex-shrink: 0;
    padding: var(--spacing-md) var(--spacing-lg);
    background: rgba(255, 255, 255, 0.03);
    border-top: var(--glass-border);
    text-align: center;
  }

  .results-count {
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
  }
</style>
