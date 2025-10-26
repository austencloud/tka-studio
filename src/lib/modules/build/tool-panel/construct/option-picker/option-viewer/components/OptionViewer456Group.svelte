<!--
OptionPicker456Group.svelte - Horizontal group for Types 4, 5, 6

Matches the desktop version exactly:
- Horizontal layout for Types 4, 5, 6 (Dash, Dual-Dash, Static)
- Fixed size policy to prevent stretching
- Minimal spacing to prevent overflow
- Centered alignment
- Beautiful fade animations for option changes
-->
<script lang="ts">
  import type { IAnimationService, PictographData } from "$shared";
  import { getLetterType, Letter, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { TypeFilter } from "../domain";
  import OptionViewerSection from "./OptionViewerSection.svelte";

  // Services
  let animationService: IAnimationService;

  onMount(() => {
    animationService = resolve<IAnimationService>(TYPES.IAnimationService);
  });

  // Animation functions following established app patterns
  const sectionFadeOut = (_node: Element) => {
    if (!animationService) {
      return { duration: 0 };
    }
    return animationService.createFadeOutTransition({
      duration: 200,
    });
  };

  const sectionFadeIn = (_node: Element) => {
    if (!animationService) {
      return { duration: 0 };
    }
    return animationService.createFadeInTransition({
      duration: 250,
      outDuration: 200, // Wait for fade-out to complete
    });
  };

  // Props
  const {
    pictographs = [],
    onPictographSelected = () => {},
    containerWidth = 800,
    pictographSize = 144,
    gridGap = '8px',
    layoutMode = '8-column',
    typeFilter,
    currentSequence = [],
    isFadingOut = false,
    contentAreaBounds = null,
    forcedPictographSize,
  } = $props<{
    pictographs?: PictographData[];
    onPictographSelected?: (pictograph: PictographData) => void;
    containerWidth?: number;
    pictographSize?: number;
    gridGap?: string;
    layoutMode?: '4-column' | '8-column';
    typeFilter?: TypeFilter;
    currentSequence?: PictographData[];
    isFadingOut?: boolean;
    contentAreaBounds?: { left: number; right: number; width: number } | null;
    forcedPictographSize?: number;
  }>();

  const effectivePictographSize = $derived(() => forcedPictographSize ?? pictographSize);

  // Reactive container dimension tracking (width AND height)
  let actualContainerWidth = $state(containerWidth);
  let actualContainerHeight = $state(600); // Default height
  let containerElement: HTMLDivElement;
  let resizeObserver: ResizeObserver | null = null;

  // Update actual container dimensions when the DOM element changes
  $effect(() => {
    if (containerElement && typeof ResizeObserver !== 'undefined') {
      // Clean up existing observer
      if (resizeObserver) {
        resizeObserver.disconnect();
      }

      // Observe the group-widget itself to get the actual available width after padding
      const observeTarget = containerElement;

      // Create new observer - update immediately for snappy resize
      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const newWidth = entry.contentRect.width;
          const newHeight = entry.contentRect.height;

          if (newWidth > 0 && newWidth !== actualContainerWidth) {
            actualContainerWidth = newWidth;
          }
          if (newHeight > 0 && newHeight !== actualContainerHeight) {
            actualContainerHeight = newHeight;
          }
        }
      });

      // Start observing the group-widget container
      resizeObserver.observe(observeTarget);

      // Get initial measurement from group-widget container
      const rect = observeTarget.getBoundingClientRect();
      if (rect.width > 0) {
        actualContainerWidth = rect.width;
      }
      if (rect.height > 0) {
        actualContainerHeight = rect.height;
      }

      // Cleanup function
      return () => {
        if (resizeObserver) {
          resizeObserver.disconnect();
          resizeObserver = null;
        }
      };
    }
  });

  // Fallback to prop values if no actual measurement available
  const effectiveContainerWidth = $derived(() => {
    const observedWidth = actualContainerWidth > 0 ? actualContainerWidth : containerWidth;
    // Subtract group-widget padding (8px on each side = 16px total)
    const GROUP_WIDGET_PADDING = 16;
    return observedWidth - GROUP_WIDGET_PADDING;
  });

  const effectiveContainerHeight = $derived(() => {
    return actualContainerHeight > 0 ? actualContainerHeight : 600;
  });

  // Calculate aspect ratio for layout decisions
  const containerAspectRatio = $derived(() => {
    const width = effectiveContainerWidth();
    const height = effectiveContainerHeight();
    return width / height;
  });

  // Groupable types (Types 4, 5, 6) - matches desktop exactly
  const groupableTypes = ["Type4", "Type5", "Type6"];

  // Helper function to get letter type from pictograph letter using existing utilities
  function getLetterTypeFromString(letter: string): string {
    try {
      // Convert string to Letter enum
      const letterEnum = Object.values(Letter).find(l => l === letter);
      if (!letterEnum) {
        return 'Unknown';
      }

      // Use the existing getLetterType function
      const letterType = getLetterType(letterEnum as Letter);
      return letterType;
    } catch (error) {
      return 'Unknown';
    }
  }

  // No longer need toggle states - sections are always visible when type is enabled

  // Filter pictographs by type for each section using local logic
  const pictographsByType = $derived(() => {
    const result: Record<string, PictographData[]> = {};

    // Initialize empty arrays for each type
    groupableTypes.forEach(type => {
      result[type] = [];
    });

    // Filter pictographs by type using existing utilities
    if (pictographs.length > 0) {
      groupableTypes.forEach(type => {
        const filtered = pictographs.filter((p: PictographData) => p.letter && getLetterTypeFromString(p.letter) === type);
        result[type] = filtered;
      });
    }

    return result;
  });

  // Store the result to avoid multiple function calls in template
  const currentPictographsByType = $derived(() => pictographsByType());


  // Helper function to check if a type is enabled in the filter
  function isTypeEnabled(letterType: string): boolean {
    if (!typeFilter) return true; // If no filter provided, show all types

    switch (letterType) {
      case 'Type4': return typeFilter.type4;
      case 'Type5': return typeFilter.type5;
      case 'Type6': return typeFilter.type6;
      default: return true;
    }
  }

  // Aspect-ratio-based layout calculation
  function calculateOptimalLayout(
    typeCounts: Array<{type: string, count: number}>,
    containerWidth: number,
    containerHeight: number,
    aspectRatio: number,
    targetPictographSize: number,
    gridGap: string
  ) {
    const gap = parseInt(gridGap.replace('px', ''));
    const minSectionWidth = targetPictographSize + gap * 2;
    const hasMultipleTypes = typeCounts.length > 1;

    // Single type: always use full width
    if (!hasMultipleTypes) {
      return [{
        types: typeCounts.map(item => item.type),
        containerWidth: containerWidth,
        layout: 'single'
      }];
    }

    let chosenLayout: string;
    let result: Array<{types: string[], containerWidth: number, layout: string}>;

    /**
     * ASPECT RATIO LAYOUT STRATEGY (adjusted thresholds for better UX):
     *
     * Portrait (aspectRatio < 0.6): Stack vertically (3 rows)
     * - Type 4 on top
     * - Type 5 in middle
     * - Type 6 on bottom
     * - Use stricter threshold so slightly-portrait layouts get 2-row treatment
     *
     * Square-ish (0.6 <= aspectRatio < 1.6): 2-row layout
     * - Row 1: Type 4 (full width)
     * - Row 2: Types 5 & 6 (side by side)
     * - Wider range to accommodate more device orientations
     *
     * Wide/Landscape (aspectRatio >= 1.6): Single row
     * - Type 4 | Type 5 | Type 6 (left to right)
     */

    if (aspectRatio < 0.6) {
      // Portrait: Stack vertically (only for very tall layouts)
      chosenLayout = 'vertical-stack (portrait)';
      result = typeCounts.map(item => ({
        types: [item.type],
        containerWidth: containerWidth,
        layout: 'vertical'
      }));
    } else if (aspectRatio < 1.6) {
      // Square-ish: 2-row layout (Type 4 on top, Types 5&6 below)
      // This now covers a wider range including slightly portrait/landscape
      chosenLayout = '2-row (square)';
      result = [
        {
          types: [typeCounts[0].type], // Type 4
          containerWidth: containerWidth,
          layout: 'row-1'
        },
        {
          types: typeCounts.slice(1).map(item => item.type), // Types 5 & 6
          containerWidth: containerWidth,
          layout: 'row-2'
        }
      ];
    } else {
      // Wide/Landscape: Single horizontal row
      chosenLayout = 'single-row (wide)';
      result = [{
        types: typeCounts.map(item => item.type),
        containerWidth: containerWidth,
        layout: 'horizontal'
      }];
    }

    return result;
  }

  // Smart layout organization based on context and available space
  const layoutSections = $derived(() => {
    // Filter types based on typeFilter state
    const enabledTypes = groupableTypes.filter(type => isTypeEnabled(type));

    // If no types are enabled, return empty layout
    if (enabledTypes.length === 0) {
      return [];
    }

    // Get pictograph counts for each enabled type
    const typeCounts = enabledTypes.map(type => ({
      type,
      count: currentPictographsByType()[type]?.length || 0
    })).filter(item => item.count > 0);

    if (typeCounts.length === 0) {
      return [];
    }

    // Calculate optimal layout based on container dimensions and content
    return calculateOptimalLayout(
      typeCounts,
      effectiveContainerWidth(),
      effectiveContainerHeight(),
      containerAspectRatio(),
      effectivePictographSize(),
      gridGap
    );
  });

  // Calculate section width for each layout row with improved spacing
  const getSectionWidth = (types: string[], rowContainerWidth: number, layout: string) => {
    if (layout === 'vertical' || types.length === 1) {
      // Vertical layout or single type: use full width
      return rowContainerWidth;
    }

    // Horizontal layout: distribute width evenly accounting for CSS gap
    // rowContainerWidth is the group-widget's clientWidth (already accounts for padding)
    const gap = parseInt(gridGap.replace('px', '')) || 8;
    const totalGaps = gap * (types.length - 1);
    const availableWidth = rowContainerWidth - totalGaps;

    // Return width per section, floored to prevent overflow
    return Math.floor(availableWidth / types.length);
  };

  // Create layout config for a specific section
  const createSectionLayoutConfig = (
    sectionWidth: number,
    letterType: string,
    numPictographs: number,
    targetSize: number
  ) => {
    const gap = parseInt(gridGap.replace('px', '')) || 8;

    // For Types 4-6, use responsive grid that fits pictographs at target size
    // Calculate how many pictographs can fit per row at target size
    const pictographsPerRow = Math.max(1, Math.floor(sectionWidth / (targetSize + gap)));

    // Use the target size (don't scale down) - let the grid wrap naturally
    const effectiveSize = targetSize;

    // Auto-fit grid that wraps pictographs naturally
    const gridColumns = `repeat(auto-fit, minmax(${effectiveSize}px, 1fr))`;

    return {
      optionsPerRow: pictographsPerRow,
      pictographSize: effectiveSize,
      spacing: gap,
      containerWidth: sectionWidth,
      containerHeight: 600, // Default height
      gridColumns,
      gridGap,
    };
  };

</script>

<div class="group-widget" bind:this={containerElement}>
  {#each layoutSections() as row, rowIndex (rowIndex)}
    <div class="layout-row">
      {#each row.types as letterType (letterType)}
        {@const sectionWidth = getSectionWidth(row.types, row.containerWidth, row.layout || 'horizontal')}
        {@const sectionPictographs = currentPictographsByType()[letterType]}
        {@const sectionLayoutConfig = createSectionLayoutConfig(sectionWidth, letterType, sectionPictographs.length, effectivePictographSize())}
        {#if sectionPictographs.length > 0}
          <div
            class="section-container"
            style:width="{sectionWidth}px"
            in:sectionFadeIn
            out:sectionFadeOut
          >
            <OptionViewerSection
              {letterType}
              pictographs={sectionPictographs}
              {onPictographSelected}
              layoutConfig={sectionLayoutConfig}
              {currentSequence}
              {isFadingOut}
              {contentAreaBounds}
              forcedPictographSize={forcedPictographSize}
              showHeader={false}
            />
          </div>
        {/if}
      {/each}
    </div>
  {/each}
</div>

<style>
  .group-widget {
    width: 100%;
    padding: 8px; /* Add container padding for better spacing */
    /* Fixed size policy like desktop to prevent stretching */
    flex-shrink: 0;
    flex-grow: 0;
  }

  .layout-row {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    width: 100%;
    /* Prevent content from overflowing */
    overflow: hidden;
    /* FLIP-inspired smooth layout transitions */
    transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  }

  /* Horizontal layout: side-by-side with aesthetic spacing */
  .layout-row:has(.section-container:nth-child(2)) {
    gap: 8px; /* Aesthetic spacing between sections */
    margin-bottom: 12px; /* Space between rows */
  }

  /* Vertical layout: stacked with optimal spacing for portrait */
  .layout-row:has(.section-container:only-child) {
    margin-bottom: 16px; /* More space for vertical stacking visibility */
  }

  .layout-row:last-child {
    margin-bottom: 0;
  }

  .section-container {
    /* Fixed size policy to prevent stretching */
    flex-shrink: 0;
    flex-grow: 0;
    /* Ensure sections don't exceed their allocated width */
    min-width: 0;
    max-width: 100%; /* Prevent overflow */
    overflow: hidden; /* Clip content that exceeds section width */
    box-sizing: border-box; /* Include padding in width calculations */
  }

  /* Removed media query that was forcing column layout - aspect ratio logic now handles all layout decisions */
</style>
