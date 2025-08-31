<script lang="ts">
  import type { SequenceData } from "$domain";
  import type { IThumbnailService } from "$lib/services/contracts/browse-interfaces";
  import { slide } from "svelte/transition";
  import SequenceThumbnail from "../sequence-thumbnail/SequenceThumbnail.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequences = [],
    viewMode = "grid",
    thumbnailService,
    onAction = () => {},
  } = $props<{
    sequences?: SequenceData[];
    viewMode?: "grid" | "list";
    thumbnailService: IThumbnailService;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Handle sequence actions
  function handleSequenceAction(action: string, sequence: SequenceData) {
    onAction(action, sequence);
  }
</script>

{#if sequences.length > 0}
  <div
    class="sequences-grid"
    class:list-view={viewMode === "list"}
    class:grid-view={viewMode === "grid"}
    transition:slide={{ duration: 300 }}
  >
    {#each sequences as sequence}
      <SequenceThumbnail
        {sequence}
        {thumbnailService}
        {viewMode}
        onAction={handleSequenceAction}
      />
    {/each}
  </div>
{/if}

<style>
  /* 3-column responsive grid like desktop app */
  .sequences-grid.grid-view {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
    grid-auto-rows: max-content;
  }

  .sequences-grid.list-view {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
</style>
