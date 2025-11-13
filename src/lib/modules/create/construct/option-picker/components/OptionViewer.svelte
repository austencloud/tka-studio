<!--
OptionViewer.svelte - Clean option display orchestrator

Orchestrates specialized components and services:
- Services handle business logic (sizing, organizing, filtering, formatting)
- State files handle domain state (option-picker-state, container-dimension-tracker)
- This component coordinates them with reactive Svelte 5 runes
-->
<script lang="ts">
  import type {
    GridMode,
    IHapticFeedbackService,
    PictographData,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  import ConstructPickerHeader from "../../shared/components/ConstructPickerHeader.svelte";
  import type { ILayoutDetectionService } from "../../services/contracts/ILayoutDetectionService";
  import type {
    IOptionFilter,
    IOptionLoader,
    IOptionOrganizer,
    IOptionSizer,
    IOptionSorter,
    IOptionTransitionCoordinator,
    ISectionTitleFormatter,
  } from "../services/contracts";
  import {
    createContainerDimensionTracker,
    createOptionPickerState,
  } from "../state";
  import OptionFilterPanel from "./OptionFilterPanel.svelte";
  import OptionViewerGridLayout from "./OptionViewerGridLayout.svelte";
  import OptionViewerSwipeLayout from "./OptionViewerSwipeLayout.svelte";

  // ===== PROPS =====
  let {
    onOptionSelected,
    currentSequence = [],
    currentGridMode,
    isUndoingOption = false,
    isSideBySideLayout = () => false,
    onOpenFilters = () => {},
    onCloseFilters = () => {},
    isContinuousOnly = false,
    isFilterPanelOpen = false,
    onToggleContinuous = () => {},
  }: {
    onOptionSelected: (option: PictographData) => void;
    currentSequence?: PictographData[];
    currentGridMode: GridMode;
    isUndoingOption?: boolean;
    isSideBySideLayout?: () => boolean;
    onOpenFilters?: () => void;
    onCloseFilters?: () => void;
    isContinuousOnly?: boolean;
    isFilterPanelOpen?: boolean;
    onToggleContinuous?: (value: boolean) => void;
  } = $props();

  // ===== SERVICES =====
  let optionPickerSizingService: IOptionSizer | null = null;
  let optionOrganizerService: IOptionOrganizer | null = null;
  let layoutDetectionService: ILayoutDetectionService | null = null;
  let transitionCoordinator: IOptionTransitionCoordinator | null = null;
  let sectionTitleFormatter: ISectionTitleFormatter | null = null;
  let hapticService: IHapticFeedbackService | null = null;

  // ===== STATE =====
  let optionPickerState = $state<ReturnType<
    typeof createOptionPickerState
  > | null>(null);
  let servicesReady = $state(false);
  let currentSectionTitle = $state<string>("Type 1");
  let isFadingOut = $state(false);
  let isTransitioning = $state(false);

  const containerDimensions = createContainerDimensionTracker();
  let containerElement: HTMLElement;

  // Transition timing constants
  const FADE_OUT_DURATION = 250;
  const FADE_IN_DURATION = 250;

  // Header title constants
  const GRID_LAYOUT_TITLE = "Choose your next option!";

  // ===== DERIVED - Formatted title =====
  const formattedSectionTitle = $derived(() => {
    // When using grid layout (not swipe), show generic message
    // because all sections are visible at once
    if (!shouldUseSwipeLayout()) {
      return GRID_LAYOUT_TITLE;
    }

    // When using swipe layout, show section-specific title
    if (!sectionTitleFormatter) return currentSectionTitle;
    return sectionTitleFormatter.formatSectionTitle(currentSectionTitle);
  });

  // ===== DERIVED - Organized pictographs =====
  const organizedPictographs = $derived(() => {
    if (!optionPickerState?.filteredOptions.length || !optionOrganizerService) {
      return [];
    }

    const serviceResult = optionOrganizerService.organizePictographs(
      optionPickerState.filteredOptions,
      "type"
    );

    return serviceResult.map((section) => ({
      title: section.title,
      pictographs: section.pictographs,
      type:
        section.type === "grouped"
          ? ("grouped" as const)
          : ("section" as const),
    }));
  });

  // ===== DERIVED - Layout configuration =====
  const layoutConfig = $derived(() => {
    if (!optionPickerSizingService || !optionPickerState) {
      return {
        optionsPerRow: 4,
        pictographSize: 144,
        spacing: 8,
        containerWidth: containerDimensions.width,
        containerHeight: containerDimensions.height,
        gridColumns: "repeat(4, 1fr)",
        gridGap: "8px",
      };
    }

    const optionsPerRow = optionPickerSizingService.getOptimalColumns(
      containerDimensions.width,
      containerDimensions.width < 600
    );

    const layoutMode: "8-column" | "4-column" =
      optionsPerRow === 8 ? "8-column" : "4-column";

    const maxPictographsPerSection = Math.max(
      ...organizedPictographs().map((section) => section.pictographs.length),
      8
    );

    const sizingResult = optionPickerSizingService.calculateOverflowAwareSize({
      containerWidth: containerDimensions.width,
      containerHeight: containerDimensions.height,
      layoutMode,
      maxPictographsPerSection,
      isMobileDevice: containerDimensions.width < 800,
      headerHeight: 40,
      targetOverflowBuffer: 30,
    });

    return {
      optionsPerRow,
      pictographSize: sizingResult.pictographSize,
      spacing: parseInt(sizingResult.gridGap.replace("px", "")),
      containerWidth: containerDimensions.width,
      containerHeight: containerDimensions.height,
      gridColumns: `repeat(${optionsPerRow}, 1fr)`,
      gridGap: sizingResult.gridGap,
    };
  });

  // ===== DERIVED - Layout mode decisions =====
  const shouldUseSwipeLayout = $derived(() => {
    if (!layoutDetectionService || organizedPictographs().length <= 1) {
      return false;
    }

    // Stacked layout always uses swipe for multiple sections
    if (!isSideBySideLayout() && organizedPictographs().length > 1) {
      return true;
    }

    return layoutDetectionService.shouldUseHorizontalSwipe(
      layoutConfig(),
      organizedPictographs().length,
      true
    );
  });

  /**
   * Determine if header should be compact (when space is tight)
   *
   * Uses the same conditions that previously triggered the floating button:
   * - Pictographs are small (< 80px)
   * - Height is the constraining factor
   *
   * Instead of replacing the header with a floating button, we now just
   * make the header more compact (reduced padding, smaller font) to
   * preserve vertical space while maintaining UI symmetry.
   */
  const shouldUseCompactHeader = $derived(() => {
    if (
      !optionPickerState?.filteredOptions.length ||
      !optionPickerSizingService ||
      containerDimensions.height === 0
    ) {
      return false;
    }

    const config = layoutConfig();
    const maxPictographsPerSection = Math.max(
      ...organizedPictographs().map((section) => section.pictographs.length),
      8
    );

    return optionPickerSizingService.shouldUseFloatingButton({
      containerWidth: containerDimensions.width,
      containerHeight: containerDimensions.height,
      pictographSize: config.pictographSize,
      columns: config.optionsPerRow,
      maxPictographsPerSection,
    });
  });

  // Active transition timeouts for cleanup
  let transitionTimeouts: Array<ReturnType<typeof setTimeout>> = [];

  // ===== EFFECTS - Overflow monitoring =====
  $effect(() => {
    if (!optionPickerSizingService) return;

    const unsubscribe = optionPickerSizingService.subscribeToOverflowChanges(
      (hasOverflow, overflowAmount) => {
        if (hasOverflow) {
          console.log(`⚠️ Overflow detected: ${overflowAmount}px`);
          containerDimensions.forceUpdate();
        }
      }
    );

    return unsubscribe;
  });

  // ===== EFFECTS - Load options =====
  $effect(() => {
    if (isTransitioning) return;

    if (
      optionPickerState &&
      servicesReady &&
      currentSequence &&
      currentSequence.length > 0
    ) {
      optionPickerState.loadOptions(currentSequence, currentGridMode);
    } else if (
      optionPickerState &&
      servicesReady &&
      (!currentSequence || currentSequence.length === 0)
    ) {
      optionPickerState.reset();
    }
  });

  // ===== EFFECTS - Undo transitions =====
  $effect(() => {
    if (isUndoingOption && optionPickerState && !isTransitioning) {
      // Clear any existing timeouts
      transitionTimeouts.forEach((timeout) => clearTimeout(timeout));
      transitionTimeouts = [];

      // Start fade-out
      isFadingOut = true;
      isTransitioning = true;

      // Mid-fade-out: Reload options
      const midFadeTimeout = setTimeout(() => {
        if (
          optionPickerState &&
          currentSequence &&
          currentSequence.length > 0
        ) {
          optionPickerState.loadOptions(currentSequence, currentGridMode);
        }
      }, FADE_OUT_DURATION / 2);
      transitionTimeouts.push(midFadeTimeout);

      // Start fade-in
      const fadeInTimeout = setTimeout(() => {
        isFadingOut = false;
      }, FADE_OUT_DURATION);
      transitionTimeouts.push(fadeInTimeout);

      // Complete transition
      const completeTimeout = setTimeout(() => {
        isTransitioning = false;
        transitionTimeouts = [];
      }, FADE_OUT_DURATION + FADE_IN_DURATION);
      transitionTimeouts.push(completeTimeout);
    }
  });

  // ===== EFFECTS - Sync continuity state =====
  $effect(() => {
    if (
      optionPickerState &&
      optionPickerState.isContinuousOnly !== isContinuousOnly
    ) {
      optionPickerState.setContinuousOnly(isContinuousOnly);
    }
  });

  // ===== HANDLERS =====
  function handleOptionSelected(option: PictographData) {
    if (!optionPickerState || isTransitioning) return;

    try {
      performance.mark("option-click-start");
      hapticService?.trigger("selection");

      // Instant feedback
      onOptionSelected(option);
      performance.mark("option-selected-callback-complete");

      // Clear any existing timeouts
      transitionTimeouts.forEach((timeout) => clearTimeout(timeout));
      transitionTimeouts = [];

      // Start fade-out
      isFadingOut = true;
      isTransitioning = true;

      // Mid-fade-out: Update state
      const midFadeTimeout = setTimeout(() => {
        optionPickerState!.selectOption(option);
        if (
          optionPickerState &&
          currentSequence &&
          currentSequence.length > 0
        ) {
          optionPickerState.loadOptions(currentSequence, currentGridMode);
        }
        performance.mark("option-picker-state-complete");
      }, FADE_OUT_DURATION / 2);
      transitionTimeouts.push(midFadeTimeout);

      // Start fade-in
      const fadeInTimeout = setTimeout(() => {
        isFadingOut = false;
      }, FADE_OUT_DURATION);
      transitionTimeouts.push(fadeInTimeout);

      // Complete transition
      const completeTimeout = setTimeout(() => {
        isTransitioning = false;
        transitionTimeouts = [];
        performance.mark("transition-complete");
      }, FADE_OUT_DURATION + FADE_IN_DURATION);
      transitionTimeouts.push(completeTimeout);
    } catch (error) {
      console.error("Failed to select option:", error);
      isFadingOut = false;
      isTransitioning = false;
      transitionTimeouts.forEach((timeout) => clearTimeout(timeout));
      transitionTimeouts = [];
    }
  }

  function handleSectionChange(sectionIndex: number) {
    const sections = organizedPictographs();
    if (sections[sectionIndex]) {
      currentSectionTitle = sections[sectionIndex].title;
    }
  }

  // ===== LIFECYCLE =====
  onMount(() => {
    try {
      // Resolve services
      const optionLoader = resolve<IOptionLoader>(TYPES.IOptionLoader);
      const filterService = resolve<IOptionFilter>(TYPES.IOptionFilter);
      const optionSorter = resolve<IOptionSorter>(TYPES.IOptionSorter);
      optionOrganizerService = resolve<IOptionOrganizer>(
        TYPES.IOptionOrganizerService
      );
      optionPickerSizingService = resolve<IOptionSizer>(
        TYPES.IOptionPickerSizingService
      );
      layoutDetectionService = resolve<ILayoutDetectionService>(
        TYPES.ILayoutDetectionService
      );
      transitionCoordinator = resolve<IOptionTransitionCoordinator>(
        TYPES.IOptionTransitionCoordinator
      );
      sectionTitleFormatter = resolve<ISectionTitleFormatter>(
        TYPES.ISectionTitleFormatter
      );
      hapticService = resolve<IHapticFeedbackService>(
        TYPES.IHapticFeedbackService
      );

      // Create state
      optionPickerState = createOptionPickerState({
        optionLoader,
        filterService,
        optionSorter,
      });

      servicesReady = true;
    } catch (error) {
      console.error("Failed to initialize option picker services:", error);
    }

    // Setup container tracking
    if (containerElement) {
      return containerDimensions.attachToElement(containerElement);
    }
    return undefined;
  });
</script>

<div
  class="option-picker-container"
  bind:this={containerElement}
  data-testid="option-picker-container"
>
  {#if !optionPickerState}
    <div class="loading-state">
      <p>Initializing option picker...</p>
    </div>
  {:else}
    <!-- Header - always shown, compact when space is tight -->
    <div transition:fade={{ duration: 200 }}>
      <ConstructPickerHeader
        variant="options"
        title="Options"
        titleHtml={formattedSectionTitle()}
        {isContinuousOnly}
        {isFilterPanelOpen}
        {onOpenFilters}
        isSideBySideLayout={isSideBySideLayout()}
        compact={shouldUseCompactHeader()}
      />
    </div>

    <!-- Main content -->
    <div class="option-picker-content">
      {#if !containerDimensions.isReady}
        <div class="loading-state">
          <p>Initializing container...</p>
        </div>
      {:else if optionPickerState.state === "loading"}
        <div class="loading-state">
          <p>Loading options...</p>
        </div>
      {:else if optionPickerState.error}
        <div class="error-state">
          <p>Error loading options: {optionPickerState.error}</p>
          <button onclick={() => optionPickerState?.clearError()}>Retry</button>
        </div>
      {:else if optionPickerState.filteredOptions.length === 0 && !isTransitioning}
        <div class="empty-state">
          <p>No options available for the current sequence.</p>
        </div>
      {:else if optionPickerState.filteredOptions.length > 0}
        {#if shouldUseSwipeLayout()}
          <OptionViewerSwipeLayout
            organizedPictographs={organizedPictographs()}
            onPictographSelected={handleOptionSelected}
            onSectionChange={handleSectionChange}
            layoutConfig={layoutConfig()}
            {currentSequence}
            isTransitioning={isTransitioning || isUndoingOption}
            {isFadingOut}
          />
        {:else}
          <OptionViewerGridLayout
            organizedPictographs={organizedPictographs()}
            onPictographSelected={handleOptionSelected}
            layoutConfig={layoutConfig()}
            {currentSequence}
            isTransitioning={isTransitioning || isUndoingOption}
            {isFadingOut}
          />
        {/if}
      {/if}
    </div>

    <!-- Filter Panel -->
    <OptionFilterPanel
      isOpen={isFilterPanelOpen}
      {isContinuousOnly}
      onClose={onCloseFilters}
      {onToggleContinuous}
    />
  {/if}
</div>

<style>
  .option-picker-container {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 12px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    overflow: visible;
  }

  .option-picker-content {
    flex: 1;
    position: relative;
    overflow: visible;
    min-height: 0;
  }

  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: var(--spacing-xl);
    text-align: center;
    color: var(--text-muted);
  }

  .error-state button {
    margin-top: var(--spacing-md);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
  }

  .error-state button:hover {
    background: var(--primary-color-hover);
  }
</style>
