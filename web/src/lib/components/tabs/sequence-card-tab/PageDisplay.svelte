<!-- PageDisplay.svelte - Simple page display matching legacy desktop -->
<script lang="ts">
  import type { SequenceData } from "$domain";
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
    background: transparent;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  .page-display::-webkit-scrollbar {
    width: 8px;
  }

  .page-display::-webkit-scrollbar-track {
    background: transparent;
    border-radius: var(--border-radius-sm);
  }

  .page-display::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .page-display::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  /* State Containers */
  .state-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: var(--spacing-2xl);
    text-align: center;
    color: var(--text-secondary);
  }

  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-xl);
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
    margin-bottom: var(--spacing-lg);
  }

  .state-title {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--text-color);
    text-shadow: var(--text-shadow-glass);
  }

  .state-message {
    margin: 0 0 var(--spacing-xl) 0;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    max-width: 400px;
    line-height: 1.5;
  }

  .retry-button {
    background: var(--primary-color);
    border: 1px solid var(--primary-light);
    color: white;
    padding: var(--spacing-md) var(--spacing-xl);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-normal);
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
  }

  .retry-button:hover {
    background: var(--primary-light);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
  }

  /* Pages Container - grid layout for multiple pages side-by-side */
  .pages-container {
    padding: var(--spacing-xl);
    display: grid;
    gap: var(--spacing-xl);
    max-width: none; /* Allow full width for multiple pages */
    margin: 0 auto;
    justify-items: center; /* Center pages in grid cells */
    /* grid-template-columns set via style attribute based on columnCount */
  }

  /* Individual Page - Responsive size based on container and column count */
  .page {
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-lg);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      0 4px 16px rgba(0, 0, 0, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    /* Dimensions set via style attributes based on container size and column count */
    position: relative;
    flex-shrink: 0; /* Prevent pages from shrinking */
    overflow: hidden;
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
    padding: var(--spacing-xl) var(--spacing-xl) var(--spacing-2xl)
      var(--spacing-xl);
    height: 100%;
    box-sizing: border-box;
  }

  /* Sequence Grid - spacing matches legacy desktop exactly */
  .sequence-grid {
    display: grid;
    /* Legacy desktop spacing calculation: content_width / (columns * 40) */
    /* For 2 columns on letter size: ~768px / (2 * 40) = ~9.6px */
    gap: var(--spacing-sm); /* Close to legacy calculation */
    grid-template-columns: repeat(
      2,
      1fr
    ); /* Default 2 columns like legacy, overridden by style attribute */
    justify-items: center; /* Center sequence cards in grid cells */
    align-items: start; /* Align to top of grid cells */
  }

  /* Responsive */
  @media (max-width: 768px) {
    .pages-container {
      padding: var(--spacing-lg);
      gap: var(--spacing-xl);
    }

    .page-header {
      padding: var(--spacing-md) var(--spacing-lg);
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-xs);
    }

    .page-content {
      padding: var(--spacing-lg);
    }

    .sequence-grid {
      gap: var(--spacing-md);
    }

    .page-title {
      font-size: var(--font-size-lg);
    }

    .page-info {
      font-size: var(--font-size-xs);
    }

    .state-container {
      padding: var(--spacing-xl);
    }
  }
</style>
