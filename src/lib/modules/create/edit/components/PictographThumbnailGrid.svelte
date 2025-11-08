<!--
PictographThumbnailGrid.svelte - Display selected pictographs as thumbnails

Features:
- Shows up to 6 pictographs
- Displays "+X more" badge if > 6 selected
- Horizontal scrollable layout
- Compact size with spacing
-->
<script lang="ts">
  import type { BeatData } from "$shared";
  import { Pictograph } from "$shared";

  // Props
  const { selectedBeats = [] } = $props<{
    selectedBeats: BeatData[];
  }>();

  const MAX_VISIBLE = 6;
  const visibleBeats = $derived(selectedBeats.slice(0, MAX_VISIBLE));
  const remainingCount = $derived(
    Math.max(0, selectedBeats.length - MAX_VISIBLE)
  );
  const hasMore = $derived(remainingCount > 0);
</script>

<div class="thumbnail-grid">
  {#each visibleBeats as beat (beat.id || beat.beatNumber)}
    <div class="thumbnail-wrapper">
      <Pictograph pictographData={beat} disableContentTransitions={true} />
      <div class="beat-number-badge">
        {beat.beatNumber}
      </div>
    </div>
  {/each}

  {#if hasMore}
    <div class="more-badge">
      +{remainingCount}
    </div>
  {/if}
</div>

<style>
  .thumbnail-grid {
    display: flex;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) 0;
    overflow-x: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .thumbnail-grid::-webkit-scrollbar {
    height: 4px;
  }

  .thumbnail-grid::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
  }

  .thumbnail-wrapper {
    position: relative;
    flex-shrink: 0;
    width: 80px;
    height: 80px;
    border: 2px solid hsl(var(--border));
    border-radius: 8px;
    overflow: hidden;
    background: hsl(var(--muted) / 0.3);
  }

  .beat-number-badge {
    position: absolute;
    top: 4px;
    left: 4px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    z-index: 10;
  }

  .more-badge {
    flex-shrink: 0;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: hsl(var(--muted));
    border: 2px dashed hsl(var(--border));
    border-radius: 8px;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: hsl(var(--muted-foreground));
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .thumbnail-wrapper,
    .more-badge {
      width: 60px;
      height: 60px;
    }

    .beat-number-badge {
      font-size: 9px;
      padding: 1px 4px;
    }

    .more-badge {
      font-size: var(--font-size-lg);
    }
  }
</style>
