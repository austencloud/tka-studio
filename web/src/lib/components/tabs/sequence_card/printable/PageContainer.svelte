<!-- PageContainer.svelte - Container for multiple printable pages with navigation -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { Page } from "$domain/pageLayout";
  import type { SequenceData } from "$services/interfaces/domain-types";
  import PrintablePage from "./PrintablePage.svelte";

  // Props
  interface Props {
    pages: Page[];
    scale?: number;
    showPageNumbers?: boolean;
    showMargins?: boolean;
    enableNavigation?: boolean;
    enableZoom?: boolean;
    onSequenceClick?: (sequence: SequenceData) => void;
    onPageChange?: (pageNumber: number) => void;
  }

  let {
    pages,
    scale = 0.5,
    showPageNumbers = true,
    showMargins = false,
    enableNavigation = true,
    enableZoom = true,
    onSequenceClick,
    onPageChange,
  }: Props = $props();

  // State
  let currentPage = $state(0);
  let containerElement: HTMLElement;
  let isFullscreen = $state(false);

  // Reactive values
  let totalPages = $derived(pages.length);
  let currentPageData = $derived(pages[currentPage]);
  let hasMultiplePages = $derived(totalPages > 1);

  // Zoom controls
  let zoomLevel = $state(scale);
  let minZoom = 0.1;
  let maxZoom = 2.0;
  let zoomStep = 0.1;

  // Navigation
  function goToPage(pageIndex: number) {
    if (pageIndex >= 0 && pageIndex < totalPages) {
      currentPage = pageIndex;
      onPageChange?.(pageIndex + 1);
    }
  }

  function nextPage() {
    if (currentPage < totalPages - 1) {
      goToPage(currentPage + 1);
    }
  }

  function previousPage() {
    if (currentPage > 0) {
      goToPage(currentPage - 1);
    }
  }

  function firstPage() {
    goToPage(0);
  }

  function lastPage() {
    goToPage(totalPages - 1);
  }

  // Zoom controls
  function zoomIn() {
    if (zoomLevel < maxZoom) {
      zoomLevel = Math.min(maxZoom, zoomLevel + zoomStep);
    }
  }

  function zoomOut() {
    if (zoomLevel > minZoom) {
      zoomLevel = Math.max(minZoom, zoomLevel - zoomStep);
    }
  }

  function resetZoom() {
    zoomLevel = scale;
  }

  function fitToWidth() {
    if (containerElement && currentPageData) {
      const containerWidth = containerElement.clientWidth - 40; // Account for padding
      const pageWidth = currentPageData.paperSize === "A4" ? 595 : 612; // Points
      const dpiScale = 96 / 72; // Convert points to pixels
      const pageWidthPx = pageWidth * dpiScale;
      zoomLevel = Math.min(maxZoom, containerWidth / pageWidthPx);
    }
  }

  // Keyboard navigation
  function handleKeydown(event: KeyboardEvent) {
    if (!enableNavigation) return;

    switch (event.key) {
      case "ArrowLeft":
      case "PageUp":
        event.preventDefault();
        previousPage();
        break;
      case "ArrowRight":
      case "PageDown":
        event.preventDefault();
        nextPage();
        break;
      case "Home":
        event.preventDefault();
        firstPage();
        break;
      case "End":
        event.preventDefault();
        lastPage();
        break;
      case "+":
      case "=":
        if (enableZoom) {
          event.preventDefault();
          zoomIn();
        }
        break;
      case "-":
        if (enableZoom) {
          event.preventDefault();
          zoomOut();
        }
        break;
      case "0":
        if (enableZoom) {
          event.preventDefault();
          resetZoom();
        }
        break;
      case "f":
      case "F11":
        if (event.key === "f" && !event.ctrlKey) {
          event.preventDefault();
          toggleFullscreen();
        }
        break;
    }
  }

  // Fullscreen
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      containerElement?.requestFullscreen?.();
      isFullscreen = true;
    } else {
      document.exitFullscreen?.();
      isFullscreen = false;
    }
  }

  // Handle sequence click
  function handleSequenceClick(sequence: SequenceData) {
    onSequenceClick?.(sequence);
  }

  // Mount effects
  onMount(() => {
    // Listen for fullscreen changes
    const handleFullscreenChange = () => {
      isFullscreen = !!document.fullscreenElement;
    };

    document.addEventListener("fullscreenchange", handleFullscreenChange);

    // Fit to width on mount
    if (enableZoom) {
      setTimeout(fitToWidth, 100);
    }

    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
    };
  });

  // Update current page when pages change
  $effect(() => {
    if (currentPage >= totalPages) {
      currentPage = Math.max(0, totalPages - 1);
    }
  });
</script>

<svelte:window onkeydown={handleKeydown} />

<div
  class="page-container"
  class:fullscreen={isFullscreen}
  class:single-page={!hasMultiplePages}
  bind:this={containerElement}
>
  <!-- Controls -->
  {#if enableNavigation || enableZoom}
    <div class="controls-bar">
      <!-- Navigation controls -->
      {#if enableNavigation && hasMultiplePages}
        <div class="navigation-controls">
          <button
            class="nav-btn"
            onclick={firstPage}
            disabled={currentPage === 0}
            title="First page (Home)"
          >
            ⏮
          </button>

          <button
            class="nav-btn"
            onclick={previousPage}
            disabled={currentPage === 0}
            title="Previous page (←)"
          >
            ◀
          </button>

          <div class="page-info">
            <span class="page-current">{currentPage + 1}</span>
            <span class="page-separator">of</span>
            <span class="page-total">{totalPages}</span>
          </div>

          <button
            class="nav-btn"
            onclick={nextPage}
            disabled={currentPage === totalPages - 1}
            title="Next page (→)"
          >
            ▶
          </button>

          <button
            class="nav-btn"
            onclick={lastPage}
            disabled={currentPage === totalPages - 1}
            title="Last page (End)"
          >
            ⏭
          </button>
        </div>
      {/if}

      <!-- Zoom controls -->
      {#if enableZoom}
        <div class="zoom-controls">
          <button
            class="zoom-btn"
            onclick={zoomOut}
            disabled={zoomLevel <= minZoom}
            title="Zoom out (-)"
          >
            🔍-
          </button>

          <span class="zoom-level">
            {Math.round(zoomLevel * 100)}%
          </span>

          <button
            class="zoom-btn"
            onclick={zoomIn}
            disabled={zoomLevel >= maxZoom}
            title="Zoom in (+)"
          >
            🔍+
          </button>

          <button class="zoom-btn" onclick={resetZoom} title="Reset zoom (0)">
            Reset
          </button>

          <button class="zoom-btn" onclick={fitToWidth} title="Fit to width">
            Fit
          </button>
        </div>
      {/if}

      <!-- View controls -->
      <div class="view-controls">
        <label class="toggle-control">
          <input type="checkbox" bind:checked={showMargins} />
          <span>Show margins</span>
        </label>

        <button
          class="view-btn"
          onclick={toggleFullscreen}
          title="Toggle fullscreen (F)"
        >
          {isFullscreen ? "🗗" : "🗖"}
        </button>
      </div>
    </div>
  {/if}

  <!-- Page display area -->
  <div class="pages-display">
    {#if totalPages === 0}
      <div class="empty-state">
        <div class="empty-icon">📄</div>
        <h3>No pages available</h3>
        <p>Create some sequences to generate printable pages.</p>
      </div>
    {:else if currentPageData}
      <div class="page-wrapper">
        <PrintablePage
          page={currentPageData}
          scale={zoomLevel}
          showPageNumber={showPageNumbers}
          {showMargins}
          onSequenceClick={handleSequenceClick}
        />
      </div>
    {/if}
  </div>

  <!-- Page thumbnails (for multi-page navigation) -->
  {#if hasMultiplePages && enableNavigation}
    <div class="page-thumbnails">
      {#each pages as page, index (page.id)}
        <button
          class="thumbnail"
          class:active={index === currentPage}
          onclick={() => goToPage(index)}
          title="Page {index + 1}"
        >
          <div class="thumbnail-preview">
            <PrintablePage
              {page}
              scale={0.1}
              showPageNumber={false}
              showMargins={false}
            />
          </div>
          <span class="thumbnail-label">{index + 1}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #f8fafc;
    border-radius: 8px;
    overflow: hidden;
  }

  .page-container.fullscreen {
    position: fixed;
    inset: 0;
    z-index: 1000;
    border-radius: 0;
    background: #1f2937;
  }

  /* Controls */
  .controls-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 16px;
    background: white;
    border-bottom: 1px solid #e5e7eb;
    gap: 16px;
    flex-wrap: wrap;
    min-height: 48px;
  }

  .fullscreen .controls-bar {
    background: #374151;
    border-bottom-color: #4b5563;
    color: white;
  }

  .navigation-controls,
  .zoom-controls,
  .view-controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .nav-btn,
  .zoom-btn,
  .view-btn {
    padding: 6px 12px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    background: white;
    color: #374151;
    cursor: pointer;
    font-size: 14px;
    transition: all var(--transition-fast);
  }

  .nav-btn:hover,
  .zoom-btn:hover,
  .view-btn:hover {
    background: #f9fafb;
    border-color: #9ca3af;
  }

  .nav-btn:disabled,
  .zoom-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .fullscreen .nav-btn,
  .fullscreen .zoom-btn,
  .fullscreen .view-btn {
    background: #4b5563;
    border-color: #6b7280;
    color: white;
  }

  .fullscreen .nav-btn:hover,
  .fullscreen .zoom-btn:hover,
  .fullscreen .view-btn:hover {
    background: #5b6678;
  }

  .page-info {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    font-weight: 500;
    color: #374151;
  }

  .fullscreen .page-info {
    color: #d1d5db;
  }

  .zoom-level {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    min-width: 40px;
    text-align: center;
  }

  .fullscreen .zoom-level {
    color: #d1d5db;
  }

  .toggle-control {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    color: #374151;
    cursor: pointer;
  }

  .fullscreen .toggle-control {
    color: #d1d5db;
  }

  /* Pages display */
  .pages-display {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: auto;
    padding: 16px;
  }

  .page-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100%;
  }

  /* Empty state */
  .empty-state {
    text-align: center;
    color: #6b7280;
    padding: 48px 24px;
  }

  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.6;
  }

  .empty-state h3 {
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: #374151;
  }

  .empty-state p {
    margin: 0;
    font-size: 14px;
  }

  /* Page thumbnails */
  .page-thumbnails {
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    background: white;
    border-top: 1px solid #e5e7eb;
    overflow-x: auto;
    max-height: 120px;
  }

  .fullscreen .page-thumbnails {
    background: #374151;
    border-top-color: #4b5563;
  }

  .thumbnail {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px;
    border: 2px solid transparent;
    border-radius: 4px;
    background: #f9fafb;
    cursor: pointer;
    transition: all var(--transition-fast);
    min-width: 60px;
  }

  .thumbnail.active {
    border-color: #3b82f6;
    background: #dbeafe;
  }

  .thumbnail:hover {
    background: #f3f4f6;
    border-color: #9ca3af;
  }

  .thumbnail.active:hover {
    background: #bfdbfe;
  }

  .fullscreen .thumbnail {
    background: #4b5563;
    border-color: transparent;
  }

  .fullscreen .thumbnail.active {
    border-color: #60a5fa;
    background: #1e3a8a;
  }

  .fullscreen .thumbnail:hover {
    background: #5b6678;
  }

  .thumbnail-preview {
    width: 40px;
    height: 56px;
    border: 1px solid #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
    background: white;
  }

  .thumbnail-label {
    font-size: 11px;
    font-weight: 600;
    color: #6b7280;
  }

  .fullscreen .thumbnail-label {
    color: #d1d5db;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .controls-bar {
      padding: 8px 12px;
      gap: 8px;
    }

    .navigation-controls,
    .zoom-controls,
    .view-controls {
      gap: 4px;
    }

    .nav-btn,
    .zoom-btn,
    .view-btn {
      padding: 4px 8px;
      font-size: 12px;
    }

    .page-thumbnails {
      padding: 8px 12px;
    }
  }

  /* Print styles */
  @media print {
    .controls-bar,
    .page-thumbnails {
      display: none;
    }

    .pages-display {
      padding: 0;
    }
  }
</style>
