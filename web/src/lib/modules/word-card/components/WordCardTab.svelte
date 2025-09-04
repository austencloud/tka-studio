<!--
Word Card Tab - Word card creation and export

Provides tools for creating printable word cards with pictographs:
- Word card layout and design
- Batch processing and export
- Print-ready formatting
- Custom styling options
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared/inversify/container";
  import { onDestroy, onMount } from "svelte";
  // Service interface imports
  import type {
    IPageFactoryService,
    IPageImageExportService,
    IWordCardExportOrchestrator,
  } from "../services/contracts";
  // Import word card components

  // ============================================================================
  // SERVICE RESOLUTION - TEMPORARY DISABLED
  // ============================================================================

  const pageFactoryService = resolve(
    TYPES.IPageFactoryService
  ) as IPageFactoryService;
  const exportService = resolve(
    TYPES.IPageImageExportService
  ) as IPageImageExportService;
  const exportOrchestrator = resolve(
    TYPES.IWordCardExportOrchestrator
  ) as IWordCardExportOrchestrator;

  // ============================================================================
  // COMPONENT STATE - TEMPORARY PLACEHOLDERS
  // ============================================================================

  let currentPage = $state(1);
  let totalPages = $state(5);
  let selectedWords = $state<string[]>(["example", "word", "card"]);
  let layoutMode = $state<"single" | "grid">("grid");
  let isExporting = $state(false);
  let error = $state<string | null>(null);

  // ============================================================================
  // EVENT HANDLERS - TEMPORARY DISABLED
  // ============================================================================

  function handlePageChange(page: number) {
    currentPage = page;
    console.log("✅ WordCardTab: Page changed (services disabled):", page);
    // pageFactoryService.navigateToPage(page);
  }

  function handleWordAdd(word: string) {
    selectedWords = [...selectedWords, word];
    console.log("✅ WordCardTab: Word added (services disabled):", word);
    // pageFactoryService.addWord(word);
  }

  function handleWordRemove(word: string) {
    selectedWords = selectedWords.filter((w) => w !== word);
    console.log("✅ WordCardTab: Word removed (services disabled):", word);
    // pageFactoryService.removeWord(word);
  }

  function handleLayoutChange(mode: "single" | "grid") {
    layoutMode = mode;
    console.log("✅ WordCardTab: Layout changed (services disabled):", mode);
    // pageFactoryService.setLayoutMode(mode);
  }

  async function handleExport() {
    isExporting = true;
    console.log("✅ WordCardTab: Export started (services disabled)");

    try {
      // TEMPORARY: Export logic commented out
      // await exportOrchestrator.exportAllPages();

      // Simulate export delay
      await new Promise((resolve) => setTimeout(resolve, 2000));
      console.log("✅ WordCardTab: Export completed (placeholder)");
    } catch (err) {
      console.error("❌ WordCardTab: Export failed:", err);
      error = err instanceof Error ? err.message : "Export failed";
    } finally {
      isExporting = false;
    }
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
    console.log("✅ WordCardTab: Mounted (services temporarily disabled)");

    // TEMPORARY: All initialization commented out
    try {
      // Initialize page factory
      // await pageFactoryService.initialize();

      // Load default word set
      // const defaultWords = await pageFactoryService.getDefaultWords();
      // selectedWords = defaultWords;

      console.log("✅ WordCardTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ WordCardTab: Initialization failed:", err);
      error =
        err instanceof Error
          ? err.message
          : "Failed to initialize word card tab";
    }
  });

  onDestroy(() => {
    console.log("✅ WordCardTab: Cleanup (services disabled)");
    // pageFactoryService?.cleanup();
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="word-card-tab" data-testid="word-card-tab">
  <!-- Error display -->
  {#if error}
    <div class="error-banner">
      <span>{error}</span>
      <button onclick={() => (error = null)}>×</button>
    </div>
  {/if}

  <div class="word-card-layout">
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>📝 Word Card Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Word card creation and design</li>
          <li>✅ Batch processing and export</li>
          <li>✅ Print-ready formatting</li>
          <li>✅ Custom layout options</li>
          <li>✅ Pictograph integration</li>
          <li>✅ PDF and image export</li>
        </ul>
      </div>

      <!-- Placeholder interface -->
      <div class="placeholder-interface">
        <h3>Word Card Interface (placeholder):</h3>
        <div class="layout-controls">
          <button
            onclick={() => handleLayoutChange("single")}
            class:active={layoutMode === "single"}
          >
            Single Card
          </button>
          <button
            onclick={() => handleLayoutChange("grid")}
            class:active={layoutMode === "grid"}
          >
            Grid Layout
          </button>
        </div>

        <div class="word-list">
          <strong>Selected Words:</strong>
          <div class="words">
            {#each selectedWords as word}
              <span class="word-tag">
                {word}
                <button onclick={() => handleWordRemove(word)}>×</button>
              </span>
            {/each}
          </div>
        </div>

        <div class="page-info">
          <span>Page: {currentPage} / {totalPages}</span>
          <span>Layout: {layoutMode}</span>
        </div>

        <div class="export-controls">
          <button onclick={handleExport} disabled={isExporting}>
            {isExporting ? "Exporting..." : "Export Cards"}
          </button>
        </div>
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
    <!-- Navigation Controls -->
    <!-- <div class="navigation-section">
      <Navigation
        {currentPage}
        {totalPages}
        onPageChange={handlePageChange}
      />
    </div> -->

    <!-- Main Content Area -->
    <!-- <div class="content-area">
      <PageDisplay
        {currentPage}
        {layoutMode}
        words={selectedWords}
      />
    </div> -->

    <!-- Word Card Preview -->
    <!-- <div class="preview-section">
      <WordCard
        words={selectedWords}
        layout={layoutMode}
      />
    </div> -->
  </div>

  <!-- Export overlay -->
  {#if isExporting}
    <div class="export-overlay">
      <div class="export-spinner"></div>
      <span>Exporting word cards...</span>
    </div>
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .word-card-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .word-card-layout {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Original layout: */
    /* flex-direction: column;
    overflow: hidden; */
  }

  .error-banner {
    background: var(--color-error, #ff4444);
    color: white;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .error-banner button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
  }

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  .placeholder-interface {
    margin-top: 1.5rem;
    padding: 1rem;
    background: var(--color-surface, #fff);
    border-radius: 4px;
    border: 1px solid var(--color-border, #ddd);
  }

  .placeholder-interface h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .layout-controls {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    justify-content: center;
  }

  .layout-controls button {
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .layout-controls button.active {
    background: var(--color-primary, #007acc);
    color: white;
    border-color: var(--color-primary, #007acc);
  }

  .layout-controls button:hover:not(.active) {
    background: var(--color-surface-hover, #f0f0f0);
  }

  .word-list {
    margin-bottom: 1rem;
    text-align: left;
  }

  .word-list strong {
    color: var(--color-text-primary, #333);
  }

  .words {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .word-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    background: var(--color-primary-light, #e6f3ff);
    border: 1px solid var(--color-primary, #007acc);
    border-radius: 4px;
    font-size: 0.9rem;
  }

  .word-tag button {
    background: none;
    border: none;
    color: var(--color-primary, #007acc);
    cursor: pointer;
    font-size: 1rem;
    line-height: 1;
  }

  .page-info {
    display: flex;
    gap: 1rem;
    justify-content: center;
    color: var(--color-text-secondary, #666);
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }

  .export-controls {
    display: flex;
    justify-content: center;
  }

  .export-controls button {
    padding: 0.75rem 1.5rem;
    border: 1px solid var(--color-primary, #007acc);
    background: var(--color-primary, #007acc);
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }

  .export-controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .export-controls button:hover:not(:disabled) {
    background: var(--color-primary-dark, #005a99);
  }

  .export-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
  }

  .export-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid var(--color-border, #ddd);
    border-top: 2px solid var(--color-primary, #007acc);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }

    .layout-controls {
      flex-direction: column;
      align-items: center;
    }

    .page-info {
      flex-direction: column;
      gap: 0.5rem;
    }

    .words {
      justify-content: center;
    }
  }
</style>
