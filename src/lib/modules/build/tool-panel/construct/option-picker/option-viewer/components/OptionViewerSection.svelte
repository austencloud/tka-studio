<!--
OptionViewerSection.svelte - Section component for option picker

Renders a section with:
- Section header with letter type
- Grid of pictographs for that letter type
- Beautiful fade animations when options change
-->
<script lang="ts">
  import type { IReversalDetectionService, PictographWithReversals } from "$build/shared/services/contracts/IReversalDetectionService";
  import type { IHapticFeedbackService, PictographData } from "$shared";
  import { getLetterBorderColors, LETTER_TYPE_COLORS, Pictograph, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { LetterTypeTextPainter } from "../utils/letter-type-text-painter";

  // Props
  const {
    letterType,
    pictographs = [],
    onPictographSelected = () => {},
    layoutConfig,
    currentSequence = [],
    isFadingOut = false,
    contentAreaBounds = null,
    forcedPictographSize,
    showHeader = true,
  } = $props<{
    letterType: string;
    pictographs?: PictographData[];
    onPictographSelected?: (pictograph: PictographData) => void;
    layoutConfig?: {
      optionsPerRow: number;
      pictographSize: number;
      spacing: number;
      containerWidth: number;
      containerHeight: number;
      gridColumns: string;
      gridGap: string;
    };
    currentSequence?: PictographData[];
    isFadingOut?: boolean;
    contentAreaBounds?: { left: number; right: number; width: number } | null;
    forcedPictographSize?: number;
    showHeader?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Get type info using shared infrastructure
  const typeInfo = $derived.by(() => {
    const typeDescriptions = {
      Type1: { description: "Dual-Shift", typeName: "Type1" },
      Type2: { description: "Shift", typeName: "Type2" },
      Type3: { description: "Cross-Shift", typeName: "Type3" },
      Type4: { description: "Dash", typeName: "Type4" },
      Type5: { description: "Dual-Dash", typeName: "Type5" },
      Type6: { description: "Static", typeName: "Type6" },
    };
    const result = typeDescriptions[letterType as keyof typeof typeDescriptions] || {
      description: "Unknown",
      typeName: "Type ?",
    };
    return result;
  });

  // Get colors using shared infrastructure
  const colorPairs = $derived.by(() => {
    const letterTypeEnum = letterType as keyof typeof LETTER_TYPE_COLORS;
    const colors = LETTER_TYPE_COLORS[letterTypeEnum] || ["#666666", "#666666"];
    return {
      primary: colors[0],
      secondary: colors[1],
    };
  });



  // Generate colored button text like desktop
  const buttonText = $derived(LetterTypeTextPainter.formatSectionHeader(typeInfo.typeName, typeInfo.description));

  // Pictographs are already filtered when passed to this component
  const sectionPictographs = $derived(() => pictographs);

  // Get reversal detection service
  const reversalDetectionService = resolve(TYPES.IReversalDetectionService) as IReversalDetectionService;

  // Get pictographs with reversal information from service
  const pictographsWithReversals = $derived(() => {
    return reversalDetectionService.detectReversalsForOptions(
      currentSequence,
      sectionPictographs()
    );
  });

  // Reactive container element for measuring available space
  let sectionContainer = $state<HTMLDivElement>();
  let availableWidth = $state(0);
  let availableHeight = $state(0);
  let actualHeaderHeight = $state(0);

  // Effect 1: Width measurement from contentAreaBounds or container
  $effect(() => {
    // Use contentAreaBounds if available (from HorizontalSwipeContainer)
    if (contentAreaBounds && contentAreaBounds.width > 0) {
      availableWidth = contentAreaBounds.width;
      return;
    }

    // Otherwise measure container width
    if (!sectionContainer) return;

    const resizeObserver = new ResizeObserver(() => {
      const rect = sectionContainer.getBoundingClientRect();
      availableWidth = rect.width;
    });

    resizeObserver.observe(sectionContainer);

    // Initial measurement
    const rect = sectionContainer.getBoundingClientRect();
    availableWidth = rect.width;

    return () => {
      resizeObserver.disconnect();
    };
  });

  // Effect 2: Height measurement from viewport
  // The section container can overflow the viewport, so we need the viewport's actual height
  $effect(() => {
    if (!sectionContainer) return;

    const viewport = sectionContainer.closest(".embla__viewport") as HTMLElement;
    if (!viewport) return;

    const measureViewportHeight = () => {
      const viewportRect = viewport.getBoundingClientRect();
      const viewportStyles = window.getComputedStyle(viewport);
      const paddingTop = parseFloat(viewportStyles.paddingTop) || 0;
      const paddingBottom = parseFloat(viewportStyles.paddingBottom) || 0;

      // Available height = viewport height minus padding
      availableHeight = viewportRect.height - paddingTop - paddingBottom;
    };

    const resizeObserver = new ResizeObserver(() => {
      measureViewportHeight();
    });

    resizeObserver.observe(viewport);

    // Initial measurement
    measureViewportHeight();

    return () => {
      resizeObserver.disconnect();
    };
  });

  // Effect 3: Header height measurement
  $effect(() => {
    if (!showHeader) {
      actualHeaderHeight = 0;
      return;
    }

    if (!sectionContainer) return;

    const header = sectionContainer.querySelector(
      ".section-header"
    ) as HTMLElement;
    if (!header) return;

    const measureHeaderHeight = () => {
      const headerRect = header.getBoundingClientRect();
      actualHeaderHeight = headerRect.height;
    };

    const resizeObserver = new ResizeObserver(() => {
      measureHeaderHeight();
    });

    resizeObserver.observe(header);

    // Initial measurement
    measureHeaderHeight();

    return () => {
      resizeObserver.disconnect();
    };
  });

  // Calculate optimal pictograph size and grid columns based on available space
  // CRITICAL: Considers BOTH width AND height constraints to prevent overflow
  const optimalLayout = $derived(() => {
    const rawItemCount = pictographsWithReversals().length;
    const safeItemCount = Math.max(rawItemCount, 1);
    const maxColumns = layoutConfig?.optionsPerRow || 4;
    const columns = Math.min(maxColumns, safeItemCount);
    const basePictographSize = layoutConfig?.pictographSize || 144;
    const gridGapValue = parseInt(layoutConfig?.gridGap || '8px');
    const targetSize = forcedPictographSize ?? basePictographSize;

    if (forcedPictographSize !== undefined) {
      return {
        columns,
        pictographSize: targetSize,
        gridColumns: `repeat(${columns}, ${targetSize}px)`
      };
    }

    // If no available dimensions yet, use conservative fallback
    if (!availableWidth || !availableHeight) {
      // Use a conservative fallback size that accounts for potential arrow space
      const containerWidth = layoutConfig?.containerWidth || 800;
      const estimatedAvailableWidth = Math.max(containerWidth - 80, 300);
      const totalGapSpace = (columns - 1) * gridGapValue;
      const availableForPictographs = estimatedAvailableWidth - totalGapSpace;
      const conservativeMaxSize = Math.floor(availableForPictographs / columns);

      const conservativeSize = Math.min(basePictographSize, conservativeMaxSize);
      const fallbackSize = Math.max(conservativeSize, 40);

      return {
        columns,
        pictographSize: fallbackSize,
        gridColumns: `repeat(${columns}, ${fallbackSize}px)`
      };
    }

    const totalWidthGapSpace = (columns - 1) * gridGapValue;
    const availableWidthForPictographs = availableWidth - totalWidthGapSpace;
    const maxWidthBasedSize = Math.floor(availableWidthForPictographs / columns);

    const rows = Math.ceil(rawItemCount / columns) || 1;
    const totalHeightGapSpace = (rows - 1) * gridGapValue;
    const availableHeightForPictographs = availableHeight - actualHeaderHeight - totalHeightGapSpace;
    const maxHeightBasedSize = Math.floor(availableHeightForPictographs / rows);

    const maxPictographSize = Math.min(maxWidthBasedSize, maxHeightBasedSize);
    const optimalSize = Math.min(basePictographSize, maxPictographSize);
    const finalSize = Math.max(optimalSize, 40);

    return {
      columns,
      pictographSize: finalSize,
      gridColumns: `repeat(${columns}, ${finalSize}px)`
    };
  });

  // Handle pictograph selection
  function handlePictographClick(pictographWithReversals: PictographWithReversals) {
    // Trigger haptic feedback for pictograph selection
    hapticService?.trigger("selection");

    // Extract the original PictographData for selection (remove reversal flags)
    const { blueReversal, redReversal, ...pictographData } = pictographWithReversals;
    onPictographSelected(pictographData as PictographData);
  }
</script>

<div
  class="option-picker-section"
  bind:this={sectionContainer}
  style:--section-width={contentAreaBounds ? `${contentAreaBounds.width}px` : '100%'}
  data-letter-type={letterType}
>
  <!-- Section Header (visual only - no toggle functionality) -->
  {#if showHeader}
    <div class="section-header">
      <div class="header-layout">
        <!-- Stretch before button -->
        <div class="stretch"></div>

        <!-- Type label (visual only - no click functionality) -->
        <div class="type-label">
          <span class="label-text">
            {@html buttonText}
          </span>
        </div>

        <!-- Stretch after button -->
        <div class="stretch"></div>
      </div>
    </div>
  {/if}

  <!-- Section Content -->
  {#if pictographsWithReversals().length > 0}
  <div
    class="pictographs-grid"
    style:grid-template-columns={optimalLayout().gridColumns}
    style:gap={layoutConfig?.gridGap || '16px'}
  >
    {#each pictographsWithReversals() as pictograph (pictograph.id || `${pictograph.letter}-${pictograph.startPosition}-${pictograph.endPosition}`)}
      {@const borderColors = getLetterBorderColors(pictograph.letter)}
      <button
        class="pictograph-option"
        onclick={() => handlePictographClick(pictograph)}
        style:width="{optimalLayout().pictographSize}px"
        style:height="{optimalLayout().pictographSize}px"
        style:opacity={isFadingOut ? '0' : '1'}
        style:transition="opacity 250ms ease-out"
        style:--border-primary={borderColors.primary}
        style:--border-secondary={borderColors.secondary}
        style:--pictograph-size="{optimalLayout().pictographSize}px"
      >
        <Pictograph
          pictographData={pictograph}
          disableContentTransitions={true}
        />
      </button>
    {/each}
  </div>
  {/if}
</div>

<style>
  .option-picker-section {
    /* Use the content area bounds width when available */
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Section Header Styles (consolidated from OptionViewerSectionHeader) */

  .header-layout {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    margin-top: 8px;
    width: 100%;
  }

  .stretch {
    flex: 1;
  }

  .type-label {
    background: var(--header-bg-current, rgba(255, 255, 255, 0.15));
    border: var(--header-border-current, 1px solid rgba(255, 255, 255, 0.2));
    border-radius: 8px;
    padding: 6px 6px;
    font-weight: 600;
    font-size: 16px;
    min-width: 160px;
    text-align: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  /* Responsive header sizing for constrained screens */
  @media (max-height: 800px) {
    .type-label {
      font-size: 14px;
      padding: 4px 4px;
      min-width: 140px;
    }
  }

  @media (max-height: 700px) {
    .type-label {
      font-size: 12px;
      padding: 3px 3px;
      min-width: 120px;
    }
  }

  @media (max-height: 600px) {
    .type-label {
      font-size: 11px;
      padding: 2px 2px;
      min-width: 100px;
    }
  }

  .label-text {
    display: block;
    color: var(--header-text-current, var(--foreground, #000000));
  }

  .pictographs-grid {
    display: grid;
    justify-content: center;
    justify-items: center;
  }

  .pictograph-option {
    background: transparent;
    border: none;
    border-radius: 0px;
    padding: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-sizing: border-box;
    will-change: opacity;
    transform: translateZ(0);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    box-shadow:
      0 1px 2px rgba(0, 0, 0, 0.1),
      0 2px 4px rgba(0, 0, 0, 0.06);
  }

  /* Desktop hover - only on hover-capable devices */
  @media (hover: hover) {
    .pictograph-option:hover {
      transform: scale(1.05);
      filter: brightness(1.05);
      box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.12),
        0 4px 8px rgba(0, 0, 0, 0.08),
        0 8px 16px rgba(0, 0, 0, 0.06);
    }
  }

  /* Mobile/universal active state */
  .pictograph-option:active {
    transform: scale(0.97);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .pictograph-option:focus {
    outline: none;
    filter: brightness(1.05);
  }
</style>
