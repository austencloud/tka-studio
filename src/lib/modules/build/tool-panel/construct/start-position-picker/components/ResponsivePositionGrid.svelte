<!-- ResponsivePositionGrid.svelte - Responsive grid layout with 650px breakpoint -->
<script lang="ts">
  import { onMount } from "svelte";

  const {
    isTransitioning = false,
    hasOverflow = false,
    isSideBySideLayout = () => false,
    children,
  }: {
    isTransitioning?: boolean;
    hasOverflow?: boolean;
    isSideBySideLayout?: () => boolean;
    children?: import('svelte').Snippet;
  } = $props();

  let gridWrapperElement: HTMLDivElement | null = null;
  let containerWidth = $state(0);
  let containerHeight = $state(0);

  // Calculate optimal columns based on layout mode and container width
  // When in side-by-side layout (desktop panels): Always use 4 columns
  // When in stacked layout (mobile/portrait): Use 650px threshold (8 or 4 columns)
  const optimalColumns = $derived(() => {
    if (isSideBySideLayout()) {
      // Side-by-side layout (desktop): Always 4 columns for better fit
      return 4;
    } else {
      // Stacked layout (mobile/portrait): Use width-based threshold
      return containerWidth >= 650 ? 8 : 4;
    }
  });

  // Check if we're in 8-column layout (for conditional spacing)
  const isEightColumnLayout = $derived(() => optimalColumns() === 8);

  // Calculate grid layout based on optimal columns
  const gridLayout = $derived(() => {
    const columns = optimalColumns();
    const totalItems = 16; // 4 Alpha + 4 Beta + 8 Gamma
    const rows = Math.ceil(totalItems / columns);

    return {
      columns,
      rows,
      gridColumns: `repeat(${columns}, 1fr)`,
      itemsPerRow: columns
    };
  });

  // Calculate maximum pictograph size to fit within container
  // Accounts for both width and height constraints
  const maxPictographSize = $derived(() => {
    if (containerWidth === 0 || containerHeight === 0) return 'auto';

    const layout = gridLayout();
    const gap = 8; // Gap between items
    const padding = 16; // Container padding

    // Available space after accounting for gaps and padding
    const availableWidth = containerWidth - padding - (gap * (layout.columns - 1));
    const availableHeight = containerHeight - padding - (gap * (layout.rows - 1));

    // Calculate max size based on width and height constraints
    const maxWidthPerItem = availableWidth / layout.columns;
    const maxHeightPerItem = availableHeight / layout.rows;

    // Use the smaller of the two to ensure everything fits
    const maxSize = Math.min(maxWidthPerItem, maxHeightPerItem);

    // Return as CSS value, minimum 40px to keep items clickable
    return Math.max(maxSize, 40) + 'px';
  });

  // Setup ResizeObserver to track container dimensions for responsive layout
  onMount(() => {
    if (!gridWrapperElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        containerWidth = entry.contentRect.width;
        containerHeight = entry.contentRect.height;
      }
    });

    resizeObserver.observe(gridWrapperElement);

    return () => {
      resizeObserver.disconnect();
    };
  });
</script>

<div
  class="pictograph-grid-wrapper"
  class:has-overflow={hasOverflow}
  bind:this={gridWrapperElement}
>
  <div
    class="pictograph-grid"
    class:transitioning={isTransitioning}
    class:eight-column={isEightColumnLayout()}
    style:--grid-columns={gridLayout().gridColumns}
    style:--max-pictograph-size={maxPictographSize()}
  >
    {@render children?.()}
  </div>
</div>

<style>
  .pictograph-grid-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .pictograph-grid {
    display: grid;
    grid-template-columns: var(--grid-columns, repeat(4, 1fr));
    gap: 8px;
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    padding: 8px;
    align-items: center;
    justify-items: center;
    transition: grid-template-columns 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .pictograph-grid > :global(*) {
    width: var(--max-pictograph-size, auto);
    height: var(--max-pictograph-size, auto);
  }

  /* Add extra spacing between Alpha/Beta rows and Gamma rows - ONLY in 8-column layout */
  /* In 8-column layout: items 9-16 are Gamma (after 8 Alpha+Beta items in row 1) */
  /* The extra margin-top creates visual separation between conceptual groups */
  .pictograph-grid.eight-column > :global(*:nth-child(n + 9)) {
    margin-top: 8px;
  }


</style>
