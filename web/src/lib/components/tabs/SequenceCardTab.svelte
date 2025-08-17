<!-- SequenceCardTab.svelte - Enhanced sequence card tab with printable page support -->
<script lang="ts">
  import { resolve } from "$services/bootstrap";
  import { createSequenceState } from "$lib/state/sequence-state.svelte";
  import { createEnhancedSequenceCardState } from "$lib/state/sequence-card-state.svelte";
  import type {
    IPrintablePageLayoutService,
    IPageFactoryService,
  } from "$services/interfaces/sequence-interfaces";
  import type { SequenceData } from "$services/interfaces/domain-types";
  import { onMount } from "svelte";
  import SequenceCardContent from "./sequence_card/SequenceCardContent.svelte";
  import SequenceCardHeader from "./sequence_card/SequenceCardHeader.svelte";
  import SequenceCardNavigation from "./sequence_card/SequenceCardNavigation.svelte";
  import PageContainer from "./sequence_card/printable/PageContainer.svelte";

  // Get services from DI container
  const sequenceService = resolve("ISequenceService") as any;
  const layoutService = resolve(
    "IPrintablePageLayoutService"
  ) as IPrintablePageLayoutService;
  const pageFactoryService = resolve(
    "IPageFactoryService"
  ) as IPageFactoryService;
  const exportIntegrationService = resolve(
    "ISequenceCardExportIntegrationService"
  ) as any;

  // Create base sequence state
  const sequenceState = createSequenceState(sequenceService);

  // Create enhanced sequence card state with page layout support
  let enhancedState = $state<ReturnType<
    typeof createEnhancedSequenceCardState
  > | null>(null);

  onMount(async () => {
    console.log("🎴 Enhanced SequenceCardTab mounted");

    // Load sequences first
    await sequenceState.loadSequences();

    // Create enhanced state with loaded sequences
    enhancedState = createEnhancedSequenceCardState(
      layoutService,
      pageFactoryService,
      sequenceState.sequences
    );

    console.log("✅ Enhanced sequence card state created");
  });

  // Reactive values from enhanced state
  let allSequences = $derived(sequenceState.sequences);
  let isLoading = $derived(sequenceState.isLoading);
  let filteredSequences = $derived(enhancedState?.filteredSequences || []);
  let currentPageSequences = $derived(
    enhancedState?.currentPageSequences || []
  );
  let progressMessage = $derived(
    enhancedState?.progressMessage || "Loading..."
  );
  let canExport = $derived(enhancedState?.canExport || false);
  let totalPages = $derived(enhancedState?.totalPages || 0);

  // Current layout mode and settings
  let layoutMode = $derived(
    enhancedState?.sequenceCardState.layoutMode || "grid"
  );
  let selectedLength = $derived(
    enhancedState?.sequenceCardState.selectedLength || 16
  );
  let columnCount = $derived(enhancedState?.sequenceCardState.columnCount || 2);
  let isExporting = $derived(
    enhancedState?.sequenceCardState.isExporting || false
  );
  let isRegenerating = $derived(
    enhancedState?.sequenceCardState.isRegenerating || false
  );
  let exportProgress = $derived(
    enhancedState?.sequenceCardState.exportProgress || 0
  );

  // Page layout state
  let pageLayoutState = $derived(enhancedState?.pageLayoutState);
  let pages = $derived(pageLayoutState?.pages || []);
  let currentPage = $derived(pageLayoutState?.currentPage || 0);
  let paperSize = $derived(pageLayoutState?.paperSize || "A4");
  let orientation = $derived(pageLayoutState?.orientation || "Portrait");
  let showMargins = $derived(pageLayoutState?.showMargins || false);

  // Update sequences when sequenceState changes
  $effect(() => {
    if (enhancedState && allSequences.length > 0) {
      enhancedState.updateSequences(allSequences);
    }
  });

  // Handle length selection from navigation
  function handleLengthSelected(length: number) {
    enhancedState?.sequenceCardState &&
      (enhancedState.sequenceCardState.selectedLength = length);
    console.log("Length selected:", length);
  }

  // Handle column count change from navigation
  function handleColumnCountChanged(count: number) {
    enhancedState?.sequenceCardState &&
      (enhancedState.sequenceCardState.columnCount = count);
    console.log("Column count changed:", count);
  }

  // Handle view mode change
  function handleViewModeChanged(mode: "grid" | "list" | "printable") {
    if (!enhancedState) return;

    console.log("View mode changed:", mode);

    if (mode === "printable") {
      enhancedState.switchToPageView();
    } else {
      enhancedState.switchToGridView();
      enhancedState.sequenceCardState.layoutMode = mode;
    }
  }

  // Handle paper size change
  function handlePaperSizeChanged(size: string) {
    if (pageLayoutState) {
      pageLayoutState.setPaperSize(size as any);
      console.log("Paper size changed:", size);
    }
  }

  // Handle orientation change
  function handleOrientationChanged(orient: string) {
    if (pageLayoutState) {
      pageLayoutState.setOrientation(orient as any);
      console.log("Orientation changed:", orient);
    }
  }

  // Handle export all request from header
  async function handleExportAll() {
    if (!enhancedState || !exportIntegrationService) {
      console.error("Export service not available");
      alert("Export service is not available. Please try refreshing the page.");
      return;
    }

    try {
      // Set exporting state
      enhancedState.sequenceCardState.isExporting = true;
      enhancedState.sequenceCardState.exportProgress = 0;

      console.log("🚀 Starting real export functionality");

      // Validate export capability
      const validation = exportIntegrationService.validateExportCapability();
      if (!validation.canExport) {
        throw new Error(`Export not possible: ${validation.issues.join(", ")}`);
      }

      console.log(`📄 Found ${validation.pageCount} pages to export`);

      // Progress callback to update UI
      const onProgress = (current: number, total: number, message: string) => {
        if (enhancedState) {
          enhancedState.sequenceCardState.exportProgress = Math.round(
            (current / total) * 100
          );
          console.log(`Export progress: ${current}/${total} - ${message}`);
        }
      };

      // Export with high quality settings
      const exportOptions = {
        format: "PNG" as const,
        quality: 0.95,
        scale: 2.0, // High quality for printing
        filenamePrefix: "sequence-cards",
      };

      // Perform the actual export
      const result =
        await exportIntegrationService.exportPrintablePagesAsImages(
          exportOptions,
          onProgress
        );

      // Show results to user
      if (result.successCount > 0) {
        const message =
          result.failureCount > 0
            ? `Export completed! ${result.successCount} files exported successfully, ${result.failureCount} failed.`
            : `Export completed successfully! ${result.successCount} files exported.`;

        alert(message);
        console.log("✅ Export completed:", result);
      } else {
        throw new Error(
          `Export failed: ${result.errors.map((e: any) => e.message).join(", ")}`
        );
      }
    } catch (error) {
      console.error("❌ Export failed:", error);
      const errorMessage =
        error instanceof Error ? error.message : "Unknown export error";
      alert(`Export failed: ${errorMessage}`);
    } finally {
      if (enhancedState) {
        enhancedState.sequenceCardState.isExporting = false;
        enhancedState.sequenceCardState.exportProgress = 0;
      }
    }
  }

  // Handle refresh request from header
  function handleRefresh() {
    console.log("Refreshing sequence cards...");
    enhancedState?.refreshPages();
  }

  // Handle regenerate images request from header
  async function handleRegenerateImages() {
    if (!enhancedState) return;

    try {
      enhancedState.sequenceCardState.isRegenerating = true;
      enhancedState.sequenceCardState.exportProgress = 0;

      // Simulate regeneration progress
      for (let i = 0; i <= 100; i += 5) {
        enhancedState.sequenceCardState.exportProgress = i;
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      // TODO: Implement actual image regeneration
      console.log("Regenerating all images...");
      alert("Image regeneration completed! (This is a demo)");
    } catch (error) {
      console.error("Image regeneration failed:", error);
      alert("Image regeneration failed. Please try again.");
    } finally {
      if (enhancedState) {
        enhancedState.sequenceCardState.isRegenerating = false;
        enhancedState.sequenceCardState.exportProgress = 0;
      }
    }
  }

  // Handle sequence click
  function handleSequenceClick(sequence: SequenceData) {
    console.log("Sequence clicked:", sequence.name);
    // TODO: Implement sequence detail view or editing
  }

  // Handle page change in printable mode
  function handlePageChange(pageNumber: number) {
    if (pageLayoutState) {
      pageLayoutState.setCurrentPage(pageNumber - 1); // Convert to 0-based index
    }
  }
</script>

<div class="sequence-card-tab" data-testid="sequence-card-tab">
  <!-- Header Component -->
  <div class="header-section">
    <SequenceCardHeader
      {isExporting}
      {isRegenerating}
      progressValue={exportProgress}
      {progressMessage}
      showProgress={isLoading ||
        isExporting ||
        isRegenerating ||
        pageLayoutState?.isLoading ||
        false}
      onexportall={handleExportAll}
      onrefresh={handleRefresh}
      onregenerateimages={handleRegenerateImages}
    />
  </div>

  <!-- Main Content Area -->
  <div class="main-content">
    <!-- Navigation Sidebar -->
    <div class="navigation-section">
      <SequenceCardNavigation
        {selectedLength}
        {columnCount}
        {layoutMode}
        {paperSize}
        {orientation}
        {showMargins}
        onlengthselected={handleLengthSelected}
        oncolumncountchanged={handleColumnCountChanged}
        onviewmodechanged={handleViewModeChanged}
        onpapersizechanged={handlePaperSizeChanged}
        onorientationchanged={handleOrientationChanged}
        onshowmarginschanged={(show) => pageLayoutState?.setShowMargins(show)}
      />
    </div>

    <!-- Content Display Area -->
    <div class="content-section">
      {#if layoutMode === "printable"}
        <!-- Printable Page View -->
        <PageContainer
          {pages}
          scale={0.6}
          showPageNumbers={pageLayoutState?.showPageNumbers || true}
          {showMargins}
          enableNavigation={true}
          enableZoom={true}
          onSequenceClick={handleSequenceClick}
          onPageChange={handlePageChange}
        />
      {:else}
        <!-- Grid/List View -->
        <SequenceCardContent
          sequences={filteredSequences}
          {columnCount}
          {isLoading}
          {selectedLength}
          {layoutMode}
          onSequenceClick={handleSequenceClick}
        />
      {/if}
    </div>
  </div>
</div>

<style>
  .sequence-card-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: transparent;
    overflow: hidden;
  }

  .header-section {
    flex-shrink: 0;
    padding: var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    box-shadow: var(--shadow-glass);
  }

  .main-content {
    flex: 1;
    display: flex;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    overflow: hidden;
  }

  .navigation-section {
    flex-shrink: 0;
    width: 280px;
    display: flex;
    flex-direction: column;
  }

  .content-section {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    background: var(--surface-glass-subtle);
    border-radius: 8px;
    overflow: hidden;
  }

  /* Responsive Design */
  @media (max-width: 1024px) {
    .main-content {
      flex-direction: column;
    }

    .navigation-section {
      width: auto;
      order: 2;
    }

    .content-section {
      order: 1;
      flex: 0 0 60%;
    }
  }

  @media (max-width: 768px) {
    .header-section {
      padding: var(--spacing-md);
    }

    .main-content {
      padding: var(--spacing-md);
      gap: var(--spacing-md);
    }

    .navigation-section {
      order: 1;
    }

    .content-section {
      order: 2;
      flex: 1;
    }
  }
</style>
