<!-- PageDisplay.svelte - Simple page display matching legacy desktop -->
<script lang="ts">
  import type { SequenceData } from "$services/interfaces/domain-types";
  import SequenceCard from "./SequenceCard.svelte";

  // Props
  interface Props {
    pages: Array<{
      id: string;
      sequences: SequenceData[];
      isEmpty: boolean;
    }>;
    isLoading: boolean;
    error: string | null;
    onRetry: () => void;
    columnCount?: number; // For page display layout (how many pages side-by-side)
  }

  let {
    pages,
    isLoading,
    error,
    onRetry,
    columnCount = 1, // Default to 1 page per row
  }: Props = $props();

  // Calculate responsive page size based on container and column count
  let containerElement: HTMLElement;
  let pageWidth = $state(816); // Default letter size width
  let pageHeight = $state(1056); // Default letter size height

  // Resize observer to handle window resizing
  let resizeObserver: ResizeObserver | null = null;

  // Update page size when container or column count changes
  function updatePageSize() {
    if (containerElement && columnCount > 0) {
      const containerWidth = containerElement.clientWidth;
      const containerHeight = containerElement.clientHeight;

      // Calculate optimal page size based on available space and column count
      // Account for padding and gaps between pages
      const totalPadding = 40; // 20px padding on each side
      const totalGaps = (columnCount - 1) * 20; // 20px gap between pages
      const availableWidth = containerWidth - totalPadding - totalGaps;

      // Calculate page width based on column count
      const calculatedPageWidth = Math.max(300, availableWidth / columnCount);

      // Calculate page height based on content needs rather than fixed aspect ratio
      // Account for: padding + (3 rows of sequences) + gaps between rows
      const pagePadding = 48 + 24; // top + bottom padding
      const estimatedSequenceHeight = calculatedPageWidth * 0.4; // Estimate sequence height
      const gridGap = 10; // Gap between grid items
      const rowsNeeded = 3; // 2 columns × 3 rows = 6 sequences
      const contentHeight =
        estimatedSequenceHeight * rowsNeeded + gridGap * (rowsNeeded - 1);
      const calculatedPageHeight = contentHeight + pagePadding;

      // Ensure pages don't exceed container height (with some margin)
      const maxHeight = containerHeight - 40; // Leave some margin
      if (calculatedPageHeight > maxHeight) {
        // If content doesn't fit, scale down proportionally
        const scaleFactor = maxHeight / calculatedPageHeight;
        pageHeight = maxHeight;
        pageWidth = calculatedPageWidth * scaleFactor;
      } else {
        pageWidth = calculatedPageWidth;
        pageHeight = calculatedPageHeight;
      }
    }
  }

  // Set up resize observer when container is available
  $effect(() => {
    if (containerElement) {
      // Initial size calculation
      updatePageSize();

      // Set up resize observer for responsive updates
      resizeObserver = new ResizeObserver(() => {
        updatePageSize();
      });

      resizeObserver.observe(containerElement);

      // Cleanup function
      return () => {
        if (resizeObserver) {
          resizeObserver.disconnect();
          resizeObserver = null;
        }
      };
    }
  });

  // Update when column count changes
  $effect(() => {
    updatePageSize();
  });

  // Also listen for window resize events for additional responsiveness
  $effect(() => {
    const handleWindowResize = () => {
      // Small delay to ensure container has updated
      setTimeout(updatePageSize, 10);
    };

    window.addEventListener("resize", handleWindowResize);

    return () => {
      window.removeEventListener("resize", handleWindowResize);
    };
  });
</script>

<div class="page-display" bind:this={containerElement}>
  {#if isLoading}
    <!-- Loading State -->
    <div class="state-container loading">
      <div class="loading-spinner"></div>
      <h3 class="state-title">Loading sequences...</h3>
      <p class="state-message">Please wait while we load your sequence cards</p>
    </div>
  {:else if error}
    <!-- Error State -->
    <div class="state-container error">
      <div class="error-icon">⚠️</div>
      <h3 class="state-title">Error Loading Sequences</h3>
      <p class="state-message">{error}</p>
      <button class="retry-button" onclick={onRetry}>Try Again</button>
    </div>
  {:else if pages.length === 1 && pages[0].isEmpty}
    <!-- Empty State -->
    <div class="state-container empty">
      <div class="empty-icon">📄</div>
      <h3 class="state-title">No Sequences Found</h3>
      <p class="state-message">
        No sequences match your current filter criteria
      </p>
    </div>
  {:else}
    <!-- Pages Display -->
    <div
      class="pages-container"
      style:grid-template-columns={`repeat(${columnCount}, 1fr)`}
    >
      {#each pages as page (page.id)}
        <div
          class="page"
          data-page-id={page.id}
          style:width="{pageWidth}px"
          style:height="{pageHeight}px"
        >
          <!-- Page Header -->
          <div class="page-header">
            <h3 class="page-title">Page {page.id.replace("page-", "")}</h3>
            <span class="page-info"
              >{page.sequences.length} sequences • 2 columns</span
            >
          </div>

          <!-- Page Content -->
          <div class="page-content">
            <div
              class="sequence-grid"
              style:grid-template-columns="repeat(2, 1fr)"
            >
              {#each page.sequences as sequence (sequence.id)}
                <SequenceCard {sequence} />
              {/each}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page-display {
    height: 100%;
    overflow-y: auto;
    background: #1a1a1a;
  }

  /* State Containers */
  .state-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 40px;
    text-align: center;
    color: #aaa;
  }

  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid #333;
    border-top: 4px solid #0066cc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 24px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error-icon,
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  .state-title {
    margin: 0 0 8px 0;
    font-size: 20px;
    font-weight: 600;
    color: white;
  }

  .state-message {
    margin: 0 0 24px 0;
    font-size: 14px;
    color: #aaa;
    max-width: 400px;
    line-height: 1.5;
  }

  .retry-button {
    background: #0066cc;
    border: none;
    color: white;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .retry-button:hover {
    background: #0088ff;
  }

  /* Pages Container - grid layout for multiple pages side-by-side */
  .pages-container {
    padding: 20px;
    display: grid;
    gap: 20px;
    max-width: none; /* Allow full width for multiple pages */
    margin: 0 auto;
    justify-items: center; /* Center pages in grid cells */
    /* grid-template-columns set via style attribute based on columnCount */
  }

  /* Individual Page - Responsive size based on container and column count */
  .page {
    background: white;
    border: 1px solid #ccc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    /* Dimensions set via style attributes based on container size and column count */
    position: relative;
    flex-shrink: 0; /* Prevent pages from shrinking */
  }

  /* Hide page headers - we want clean printable pages */
  .page-header {
    display: none;
  }

  .page-title {
    display: none;
  }

  .page-info {
    display: none;
  }

  .page-content {
    /* Legacy desktop margins: 18pt left/right, 36pt top/bottom */
    /* Convert points to pixels: 18pt = 24px, 36pt = 48px at 96 DPI */
    /* But reduce top padding to eliminate space above images */
    padding: 24px 24px 48px 24px; /* top right bottom left */
    height: 100%;
    box-sizing: border-box;
  }

  /* Sequence Grid - spacing matches legacy desktop exactly */
  .sequence-grid {
    display: grid;
    /* Legacy desktop spacing calculation: content_width / (columns * 40) */
    /* For 2 columns on letter size: ~768px / (2 * 40) = ~9.6px */
    gap: 10px; /* Close to legacy calculation */
    grid-template-columns: repeat(
      2,
      1fr
    ); /* Default 2 columns like legacy, overridden by style attribute */
    justify-items: center; /* Center sequence cards in grid cells */
    align-items: start; /* Align to top of grid cells */
  }

  /* Scrollbar styling */
  .page-display::-webkit-scrollbar {
    width: 8px;
  }

  .page-display::-webkit-scrollbar-track {
    background: #333;
  }

  .page-display::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 4px;
  }

  .page-display::-webkit-scrollbar-thumb:hover {
    background: #666;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .pages-container {
      padding: 16px;
      gap: 24px;
    }

    .page-header {
      padding: 12px 16px;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
    }

    .page-content {
      padding: 16px;
    }

    .sequence-grid {
      gap: 12px;
    }

    .page-title {
      font-size: 16px;
    }

    .page-info {
      font-size: 11px;
    }
  }
</style>
