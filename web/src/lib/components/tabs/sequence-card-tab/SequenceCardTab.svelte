<!-- SequenceCardTab.svelte - Simple page-based sequence card tab matching legacy desktop -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { SequenceData } from "$services/interfaces/domain-types";
  // Note: Loading directly from dictionary API
  import SequenceCardNavigation from "./Navigation.svelte";
  import PageDisplay from "./PageDisplay.svelte";
  import { PngMetadataExtractor } from "$lib/utils/png-metadata-extractor";

  // Simple state matching legacy desktop
  let sequences: SequenceData[] = $state([]);
  let isLoading = $state(false);
  let selectedLength = $state(16); // Default like desktop
  let columnCount = $state(3); // Default like desktop
  let error = $state<string | null>(null);

  // Note: We load directly from dictionary API instead of using sequence service

  // Filtered sequences based on selected length
  let filteredSequences = $derived(() => {
    if (selectedLength === 0) {
      return sequences; // Show all
    }
    return sequences.filter((seq) => seq.beats.length === selectedLength);
  });

  // Create pages from filtered sequences (columnCount doesn't affect page content)
  let pages = $derived(() => {
    return createPages(filteredSequences());
  });

  // Load sequences on mount
  onMount(async () => {
    await loadSequences();
  });

  async function loadSequences() {
    try {
      isLoading = true;
      error = null;

      // Load sequences directly from dictionary API instead of local storage
      const response = await fetch("/api/sequences");
      const data = await response.json();

      if (data.success) {
        // Convert API response to SequenceData format with actual metadata extraction
        const sequencePromises = data.sequences.map(async (seq: any) => {
          try {
            // Extract metadata from PNG to get actual sequence length
            const metadata = await PngMetadataExtractor.extractSequenceMetadata(
              seq.word
            );

            // Calculate actual sequence length from metadata
            // Exclude metadata entry (index 0) and start position entries
            const realBeats = metadata
              .slice(1)
              .filter(
                (step: any) => step.letter && !step.sequence_start_position
              );

            const actualLength = realBeats.length;

            console.log(
              `📏 ${seq.word}: ${actualLength} beats (from metadata)`
            );

            return {
              id: seq.word,
              name: seq.word,
              beats: new Array(actualLength).fill({}), // Use actual length from metadata
              metadata: {
                imagePath: seq.path,
                word: seq.word,
                actualLength: actualLength,
                rawMetadata: metadata,
              },
            };
          } catch (error) {
            console.warn(
              `⚠️ Failed to extract metadata for ${seq.word}, using default length:`,
              error
            );
            // Fallback to default length if metadata extraction fails
            return {
              id: seq.word,
              name: seq.word,
              beats: new Array(16).fill({}), // Default fallback
              metadata: {
                imagePath: seq.path,
                word: seq.word,
                actualLength: 16,
                extractionError: error,
              },
            };
          }
        });

        // Wait for all metadata extractions to complete
        sequences = await Promise.all(sequencePromises);
      } else {
        throw new Error(data.error || "Failed to load sequences");
      }
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load sequences";
      console.error("Failed to load sequences:", err);
    } finally {
      isLoading = false;
    }
  }

  // Note: Sequence length is now extracted from PNG metadata

  // Handle length selection from navigation
  function handleLengthSelected(length: number) {
    selectedLength = length;
  }

  // Handle column count change from navigation
  function handleColumnCountChanged(count: number) {
    columnCount = count;
  }

  // Page creation logic matching legacy desktop exactly
  function createPages(sequences: SequenceData[]) {
    if (sequences.length === 0) {
      return [
        {
          id: "empty-page",
          sequences: [],
          isEmpty: true,
        },
      ];
    }

    // Legacy desktop default: 2 columns × 3 rows = 6 sequences per page
    // This matches the printable_factory.py default grid configuration
    const sequencesPerPage = 6;
    const pages = [];

    for (let i = 0; i < sequences.length; i += sequencesPerPage) {
      const pageSequences = sequences.slice(i, i + sequencesPerPage);
      pages.push({
        id: `page-${Math.floor(i / sequencesPerPage) + 1}`,
        sequences: pageSequences,
        isEmpty: false,
      });
    }

    return pages;
  }

  // Progress message - simplified to avoid compilation issues
  let progressMessage = $state("Ready");

  // Update progress message when state changes
  $effect(() => {
    if (isLoading) {
      progressMessage = `Loading ${selectedLength === 0 ? "all" : `${selectedLength}-beat`} sequences...`;
    } else {
      const pageCount = pages().length;
      const sequenceCount = filteredSequences().length;

      if (pageCount === 1 && pages()[0].isEmpty) {
        progressMessage = `No ${selectedLength === 0 ? "" : `${selectedLength}-beat `}sequences found`;
      } else {
        progressMessage = `${pageCount} page${pageCount === 1 ? "" : "s"} • ${sequenceCount} sequence${sequenceCount === 1 ? "" : "s"}`;
      }
    }
  });
</script>

<!-- Simple layout: navigation sidebar + page display -->
<div class="sequence-card-tab">
  <!-- Header -->
  <div class="header">
    <div class="header-content">
      <h1 class="title">Sequence Cards</h1>
      <p class="subtitle">{progressMessage}</p>
    </div>
  </div>

  <!-- Main content -->
  <div class="main-content">
    <!-- Navigation Sidebar -->
    <div class="navigation">
      <SequenceCardNavigation
        {selectedLength}
        {columnCount}
        onLengthSelected={handleLengthSelected}
        onColumnCountChanged={handleColumnCountChanged}
      />
    </div>

    <!-- Page Display Area -->
    <div class="content">
      <PageDisplay
        pages={pages()}
        {isLoading}
        {error}
        {columnCount}
        onRetry={loadSequences}
      />
    </div>
  </div>
</div>

<style>
  .sequence-card-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: transparent;
    color: var(--text-color);
  }

  /* Header */
  .header {
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border-bottom: var(--glass-border);
    border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    box-shadow: var(--shadow-glass);
    padding: var(--spacing-lg) var(--spacing-xl);
    flex-shrink: 0;
    margin: var(--spacing-md);
    margin-bottom: 0;
  }

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
  }

  .title {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--text-color);
    text-shadow: var(--text-shadow-glass);
  }

  .subtitle {
    margin: 0;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  /* Main Content */
  .main-content {
    display: flex;
    flex: 1;
    min-height: 0;
    gap: var(--spacing-md);
    padding: 0 var(--spacing-md) var(--spacing-md);
  }

  .navigation {
    width: 250px;
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    flex-shrink: 0;
  }

  .content {
    flex: 1;
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    overflow: hidden;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .main-content {
      flex-direction: column;
      gap: var(--spacing-sm);
    }

    .navigation {
      width: 100%;
      height: auto;
      max-height: 200px;
      border-right: none;
    }

    .title {
      font-size: var(--font-size-xl);
    }

    .subtitle {
      font-size: var(--font-size-xs);
    }

    .header {
      margin: var(--spacing-sm);
      margin-bottom: 0;
      padding: var(--spacing-md) var(--spacing-lg);
    }

    .main-content {
      padding: 0 var(--spacing-sm) var(--spacing-sm);
    }
  }
</style>
