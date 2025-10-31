<script lang="ts">
  import type { SequenceData } from "$shared";
  import { slide } from "svelte/transition";
  import type { SequenceSection } from "../../shared/domain/models/explore-models";
  import type { IExploreThumbnailService } from "../services/contracts/IExploreThumbnailService";
  import SequenceThumbnail from "./ExploreThumbnail.svelte";
  import SectionHeader from "./SectionHeader.svelte";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequences = [],
    sections = [],
    viewMode = "grid",
    thumbnailService,
    showSections = false,
    onAction = () => {},
  } = $props<{
    sequences?: SequenceData[];
    sections?: SequenceSection[];
    viewMode?: "grid" | "list";
    thumbnailService: IExploreThumbnailService;
    showSections?: boolean;
    onAction?: (action: string, sequence: SequenceData) => void;
  }>();

  // Handle sequence actions
  function handleSequenceAction(action: string, sequence: SequenceData) {
    onAction(action, sequence);
  }
</script>

{#if showSections && sections.length > 0}
  <!-- Section-based organization (desktop app style) -->
  <div class="sections-container">
    {#each sections as section (section.id)}
      <div class="sequence-section" data-section={section.title}>
        <SectionHeader title={section.title} />

        {#if section.sequences.length > 0}
          <div
            class="sequences-grid"
            class:list-view={viewMode === "list"}
            class:grid-view={viewMode === "grid"}
          >
            {#each section.sequences as sequence, index}
              <SequenceThumbnail
                {sequence}
                {thumbnailService}
                {viewMode}
                priority={index < 8}
                onAction={handleSequenceAction}
              />
            {/each}
          </div>
        {/if}
      </div>
    {/each}
  </div>
{:else if sequences.length > 0}
  <!-- Flat organization (fallback) -->
  <div
    class="sequences-grid"
    class:list-view={viewMode === "list"}
    class:grid-view={viewMode === "grid"}
    transition:slide={{ duration: 300 }}
  >
    {#each sequences as sequence, index}
      <SequenceThumbnail
        {sequence}
        {thumbnailService}
        {viewMode}
        priority={index < 8}
        onAction={handleSequenceAction}
      />
    {/each}
  </div>
{/if}

<style>
  /* Sections container for organized display */
  .sections-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .sequence-section {
    display: flex;
    flex-direction: column;
  }

  /* Responsive grid that adapts to container width */
  .sequences-grid.grid-view {
    display: grid;
    grid-template-columns: repeat(
      2,
      1fr
    ); /* Default to 2 columns for narrow containers */
    gap: var(--spacing-lg);
    grid-auto-rows: max-content;
  }

  .sequences-grid.list-view {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

  /* Container queries for responsive columns based on available width */
  @container (max-width: 480px) {
    .sequences-grid.grid-view {
      grid-template-columns: repeat(1, 1fr); /* 1 column for mobile phones */
      gap: var(--spacing-sm);
    }
  }

  /* Tablet breakpoint */
  @container (min-width: 481px) and (max-width: 768px) {
    .sequences-grid.grid-view {
      grid-template-columns: repeat(2, 1fr); /* 2 columns for tablets */
      gap: var(--spacing-md);
    }
  }

  /* Desktop breakpoints */
  @container (min-width: 769px) and (max-width: 1199px) {
    .sequences-grid.grid-view {
      grid-template-columns: repeat(3, 1fr); /* 3 columns for medium desktop */
    }
  }

  @container (min-width: 1200px) {
    .sequences-grid.grid-view {
      grid-template-columns: repeat(4, 1fr); /* 4 columns for wide containers */
    }
  }
</style>
