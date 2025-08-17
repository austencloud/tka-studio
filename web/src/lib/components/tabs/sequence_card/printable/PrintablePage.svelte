<!-- PrintablePage.svelte - Individual printable page with fixed dimensions -->
<script lang="ts">
  import { resolve } from "$services/bootstrap";
  import type { IPrintablePageLayoutService } from "$services/interfaces/sequence-interfaces";
  import type { Page, PageDimensions } from "$domain/pageLayout";
  import type { SequenceData } from "$services/interfaces/domain-types";
  import PageGrid from "./PageGrid.svelte";

  // Props
  interface Props {
    page: Page;
    scale?: number;
    showPageNumber?: boolean;
    showMargins?: boolean;
    onSequenceClick?: (sequence: SequenceData) => void;
  }

  let {
    page,
    scale = 1,
    showPageNumber = true,
    showMargins = false,
    onSequenceClick,
  }: Props = $props();

  // Services
  const layoutService = resolve("IPrintablePageLayoutService") as IPrintablePageLayoutService;

  // Reactive page dimensions in pixels for display
  let pageDimensions = $derived(() => {
    return layoutService.getPageSizeInPixels(page.paperSize, page.orientation);
  });

  let contentArea = $derived(() => {
    const pageSize = layoutService.calculatePageDimensions(page.paperSize, page.orientation);
    return layoutService.calculateContentArea(pageSize, page.margins);
  });

  // Scaled dimensions for display
  let scaledWidth = $derived(pageDimensions().width * scale);
  let scaledHeight = $derived(pageDimensions().height * scale);

  // Margin calculations for display
  let marginStyles = $derived(() => {
    const dpi = layoutService.getDPIConfiguration();
    const scaleFactor = dpi.scaleFactor * scale;
    
    return {
      top: Math.round(page.margins.top * scaleFactor),
      right: Math.round(page.margins.right * scaleFactor),
      bottom: Math.round(page.margins.bottom * scaleFactor),
      left: Math.round(page.margins.left * scaleFactor),
    };
  });

  // Content area dimensions in pixels
  let contentDimensions = $derived(() => {
    const dpi = layoutService.getDPIConfiguration();
    const scaleFactor = dpi.scaleFactor * scale;
    
    return {
      width: Math.round(contentArea().width * scaleFactor),
      height: Math.round(contentArea().height * scaleFactor),
    };
  });

  // Handle sequence click
  function handleSequenceClick(sequence: SequenceData) {
    onSequenceClick?.(sequence);
  }
</script>

<div
  class="printable-page"
  class:show-margins={showMargins}
  data-page-id={page.id}
  data-page-number={page.pageNumber}
  style:width="{scaledWidth}px"
  style:height="{scaledHeight}px"
  style:--margin-top="{marginStyles().top}px"
  style:--margin-right="{marginStyles().right}px"
  style:--margin-bottom="{marginStyles().bottom}px"
  style:--margin-left="{marginStyles().left}px"
  style:--content-width="{contentDimensions().width}px"
  style:--content-height="{contentDimensions().height}px"
>
  <!-- Page margins visualization (only visible when showMargins is true) -->
  {#if showMargins}
    <div class="margin-guides">
      <div class="margin-top"></div>
      <div class="margin-right"></div>
      <div class="margin-bottom"></div>
      <div class="margin-left"></div>
    </div>
  {/if}

  <!-- Content area -->
  <div class="content-area">
    <PageGrid
      layout={page.layout}
      sequences={page.sequences}
      contentWidth={contentDimensions().width}
      contentHeight={contentDimensions().height}
      {scale}
      onsequenceclick={handleSequenceClick}
    />
  </div>

  <!-- Page number -->
  {#if showPageNumber}
    <div class="page-number">
      Page {page.pageNumber}
    </div>
  {/if}

  <!-- Paper size indicator (for development/preview) -->
  <div class="page-info">
    {page.paperSize} {page.orientation}
  </div>
</div>

<style>
  .printable-page {
    position: relative;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    margin: 16px;
    overflow: hidden;
    
    /* Ensure page maintains aspect ratio when scaled */
    flex-shrink: 0;
    
    /* Print-specific styles */
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .content-area {
    position: absolute;
    top: var(--margin-top);
    left: var(--margin-left);
    width: var(--content-width);
    height: var(--content-height);
    background: transparent;
  }

  /* Margin guides (only visible when showMargins is true) */
  .margin-guides {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity var(--transition-normal);
  }

  .show-margins .margin-guides {
    opacity: 1;
  }

  .margin-top,
  .margin-right,
  .margin-bottom,
  .margin-left {
    position: absolute;
    background: rgba(255, 0, 0, 0.1);
    border: 1px dashed rgba(255, 0, 0, 0.3);
  }

  .margin-top {
    top: 0;
    left: 0;
    right: 0;
    height: var(--margin-top);
  }

  .margin-right {
    top: 0;
    right: 0;
    bottom: 0;
    width: var(--margin-right);
  }

  .margin-bottom {
    bottom: 0;
    left: 0;
    right: 0;
    height: var(--margin-bottom);
  }

  .margin-left {
    top: 0;
    left: 0;
    bottom: 0;
    width: var(--margin-left);
  }

  /* Page number */
  .page-number {
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 10px;
    color: #666;
    font-family: 'Arial', sans-serif;
    background: rgba(255, 255, 255, 0.9);
    padding: 2px 6px;
    border-radius: 3px;
    pointer-events: none;
  }

  /* Page info (development helper) */
  .page-info {
    position: absolute;
    top: 8px;
    left: 12px;
    font-size: 9px;
    color: #999;
    font-family: 'Arial', sans-serif;
    background: rgba(255, 255, 255, 0.9);
    padding: 2px 6px;
    border-radius: 3px;
    pointer-events: none;
    opacity: 0.7;
  }

  /* Print styles */
  @media print {
    .printable-page {
      border: none;
      border-radius: 0;
      box-shadow: none;
      margin: 0;
      page-break-after: always;
      width: 100% !important;
      height: 100% !important;
    }

    .page-info {
      display: none;
    }

    .margin-guides {
      display: none;
    }
  }

  /* Hover effects for interactive mode */
  .printable-page:hover {
    border-color: #bbb;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }

  /* Responsive scaling */
  @media (max-width: 768px) {
    .printable-page {
      margin: 8px;
    }
  }

  /* High DPI display support */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .printable-page {
      border-width: 0.5px;
    }
  }
</style>
