<!--
ThumbnailMetadata Component - Metadata Display

Displays sequence metadata including title, difficulty, length, author, date, and tags.
Extracted from SequenceThumbnail.svelte for better separation of concerns.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    sequence,
    viewMode = "grid",
    showExtendedInfo = false,
  } = $props<{
    sequence: SequenceData;
    viewMode?: "grid" | "list";
    showExtendedInfo?: boolean;
  }>();

  // ✅ DERIVED RUNES: Computed values
  let difficultyColor = $derived.by(() => {
    switch (sequence.difficultyLevel) {
      case "beginner":
        return "#10b981"; // green
      case "intermediate":
        return "#f59e0b"; // amber
      case "advanced":
        return "#ef4444"; // red
      default:
        return "#6b7280"; // gray
    }
  });

  let difficultyLabel = $derived.by(() => {
    switch (sequence.difficultyLevel) {
      case "beginner":
        return "Beginner";
      case "intermediate":
        return "Intermediate";
      case "advanced":
        return "Advanced";
      default:
        return "Unknown";
    }
  });

  let formattedLength = $derived.by(() => {
    // Use the actual beats length without subtracting metadata beats
    // The sequence.beats array should represent the actual sequence length
    const beats = sequence.beats.length;
    return beats === 1 ? "1 beat" : `${beats} beats`;
  });
</script>

<div class="metadata-section" class:list-view={viewMode === "list"}>
  <!-- Title -->
  <h3 class="sequence-title">{sequence.word}</h3>

  <!-- Basic metadata row -->
  <div class="metadata-row">
    <!-- Difficulty badge -->
    <span class="difficulty-badge" style="background-color: {difficultyColor}">
      {difficultyLabel}
    </span>

    <!-- Length -->
    <span class="length-info">{formattedLength}</span>
  </div>

  <!-- Extended info (for list view or when requested) -->
  {#if showExtendedInfo || viewMode === "list"}
    <div class="extended-info">
      <!-- Author -->
      {#if sequence.author}
        <div class="info-item">
          <span class="info-label">Author:</span>
          <span class="info-value">{sequence.author}</span>
        </div>
      {/if}

      <!-- Date added -->
      {#if sequence.dateAdded}
        <div class="info-item">
          <span class="info-label">Added:</span>
          <span class="info-value">
            {new Date(sequence.dateAdded).toLocaleDateString()}
          </span>
        </div>
      {/if}
    </div>
  {/if}

  <!-- Tags (if any) -->
  {#if sequence.tags.length > 0}
    <div class="tags">
      {#each sequence.tags.slice(0, 3) as tag}
        <span class="tag">{tag}</span>
      {/each}
    </div>
  {/if}
</div>

<style>
  .metadata-section {
    padding: 12px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .metadata-section.list-view {
    padding: 8px 12px;
    justify-content: center;
  }

  .sequence-title {
    font-size: 1rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    line-height: 1.2;
    word-break: break-word;
  }

  .metadata-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .difficulty-badge {
    color: white;
    font-size: 0.625rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    white-space: nowrap;
  }

  .length-info {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
  }

  .extended-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.75rem;
  }

  .info-item {
    display: flex;
    gap: 4px;
  }

  .info-label {
    color: rgba(255, 255, 255, 0.6);
    font-weight: 500;
    min-width: 50px;
  }

  .info-value {
    color: rgba(255, 255, 255, 0.8);
    font-weight: 400;
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 8px;
  }

  .tag {
    background: rgba(255, 255, 255, 0.15);
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.625rem;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* Mobile-first responsive design with readable font sizes */
  @media (max-width: 480px) {
    .metadata-section {
      padding: 12px;
    }

    .sequence-title {
      font-size: 1rem;
      line-height: 1.3;
    }

    .difficulty-badge {
      font-size: 0.75rem;
      padding: 4px 8px;
      border-radius: 6px;
    }

    .length-info {
      font-size: 0.875rem;
    }

    .extended-info {
      font-size: 0.75rem;
    }

    .tag {
      font-size: 0.75rem;
      padding: 4px 8px;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 481px) and (max-width: 768px) {
    .metadata-section {
      padding: 10px;
    }

    .sequence-title {
      font-size: 0.9375rem;
    }

    .difficulty-badge {
      font-size: 0.6875rem;
      padding: 3px 6px;
    }

    .length-info {
      font-size: 0.75rem;
    }

    .extended-info {
      font-size: 0.6875rem;
    }
  }
</style>
