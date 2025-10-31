<!-- WordCardTab.svelte - Simple page-based word card tab matching legacy desktop -->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IExploreLoader } from "../../explore/display/services/contracts/IExploreLoader";
  import WordCardNavigation from "./Navigation.svelte";
  import PageDisplay from "./PageDisplay.svelte";

  // Use the explore loader service directly
  const loaderService = resolve(TYPES.IExploreLoader) as IExploreLoader;

  // Simple state matching legacy desktop
  let sequences: SequenceData[] = $state([]);
  let isLoading = $state(false);
  let selectedLength = $state(16); // Default like desktop
  let columnCount = $state(3); // Default like desktop
  let error = $state<string | null>(null);

  // Note: We load directly from explore API instead of using sequence service

  // Filtered sequences based on selected length
  let filteredSequences = $derived(() => {
    if (selectedLength === 0) {
      return sequences; // Show all
    }
    return sequences.filter((seq) => seq.sequenceLength === selectedLength);
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

      // Load sequences directly from the loader service
      console.log("🔄 WordCard: Loading sequences from ExploreLoader...");
      const loadedSequences = await loaderService.loadSequenceMetadata();

      console.log(`✅ WordCard: Loaded ${loadedSequences.length} sequences`);
      sequences = loadedSequences;
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load sequences";
      console.error("❌ WordCard: Failed to load sequences:", err);
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
<div class="word-card-tab">
  <!-- Header -->
  <div class="header">
    <div class="header-content">
      <h1 class="title">Word Cards</h1>
      <p class="subtitle">{progressMessage}</p>
    </div>
  </div>

  <!-- Main content -->
  <div class="main-content">
    <!-- Navigation Sidebar -->
    <div class="navigation">
      <WordCardNavigation
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
  .word-card-tab {
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
