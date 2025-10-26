<!--
OptionViewer.svelte - Clean option display grid orchestrator

Refactored to be a lightweight orchestrator that delegates to specialized components:
- FilterButton: Floating filter button with styling and logic
- FilterStatusDisplay: Filter status information display
- Layout components: SwipeLayout and GridLayout for different interaction patterns

Business logic moved to state management and utility services.
-->
<script lang="ts">
  import type { IHapticFeedbackService, PictographData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  import type { ILayoutDetectionService } from "../../services/contracts/ILayoutDetectionService";
  import type { IOptionSizer } from "../services";
  import type {
    IOptionFilter,
    IOptionLoader,
    IOptionOrganizer,
    IOptionSorter
  } from "../services/contracts";
  import { createContainerDimensionTracker, createOptionPickerState } from "../state";
  import { LetterTypeTextPainter } from "../utils/letter-type-text-painter";
  import ContinuityToggle from "./ContinuityToggle.svelte";
  import OptionViewerGridLayout from "./OptionViewerGridLayout.svelte";
  import OptionViewerSwipeLayout from "./OptionViewerSwipeLayout.svelte";

  // Transition timing constants for coordinated animations
  const FADE_OUT_DURATION = 250; // Option picker fade-out duration
  const WORKBENCH_FADE_IN_DURATION = 250; // Workbench fade-in duration

  // Props
  let {
    onOptionSelected,
    currentSequence = [],
    isClearingSequence = false,
    isUndoingOption = false,
    isSideBySideLayout = () => false,
  }: {
    onOptionSelected: (option: PictographData) => void;
    currentSequence?: PictographData[];
    isClearingSequence?: boolean;
    isUndoingOption?: boolean;
    isSideBySideLayout?: () => boolean;
  } = $props();

  // Services - initialized asynchronously
  let optionPickerSizingService: IOptionSizer | null = null;
  let optionOrganizerService: IOptionOrganizer | null = null;
  let layoutDetectionService: ILayoutDetectionService | null = null;
  let optionPickerState = $state<ReturnType<typeof createOptionPickerState> | null>(null);
  let servicesReady = $state(false);
  let hapticService: IHapticFeedbackService;

  // Transition state to prevent empty state messages during option changes
  let isTransitioningOptions = $state(false);

  // Separate state for fade-out animation (starts immediately)
  let isFadingOut = $state(false);



  // Container dimension tracking
  const containerDimensions = createContainerDimensionTracker();

  // Container element reference
  let containerElement: HTMLElement;

  // Track current section for header display
  let currentSectionTitle = $state<string>("Type 1");

  // Type descriptions for colored formatting
  const typeDescriptions = {
    Type1: { description: "Dual-Shift", typeName: "Type 1" },
    Type2: { description: "Shift", typeName: "Type 2" },
    Type3: { description: "Cross-Shift", typeName: "Type 3" },
    Type4: { description: "Dash", typeName: "Type 4" },
    Type5: { description: "Dual-Dash", typeName: "Type 5" },
    Type6: { description: "Static", typeName: "Type 6" },
  };

  // Format section title with colored text
  function formatSectionTitle(rawTitle: string): string {
    // Handle grouped section - show all three types with colors
    if (rawTitle === "Types 4-6") {
      const type4 = LetterTypeTextPainter.formatSectionHeader("Type 4", "Dash");
      const type5 = LetterTypeTextPainter.formatSectionHeader("Type 5", "Dual-Dash");
      const type6 = LetterTypeTextPainter.formatSectionHeader("Type 6", "Static");
      return `${type4} <span style="color: rgba(255, 255, 255, 0.4); margin: 0 6px;">|</span> ${type5} <span style="color: rgba(255, 255, 255, 0.4); margin: 0 6px;">|</span> ${type6}`;
    }

    // Handle individual types
    const typeInfo = typeDescriptions[rawTitle as keyof typeof typeDescriptions];
    if (typeInfo) {
      return LetterTypeTextPainter.formatSectionHeader(typeInfo.typeName, typeInfo.description);
    }

    return rawTitle;
  }

  // Derived formatted title for display
  const formattedSectionTitle = $derived(formatSectionTitle(currentSectionTitle));

  // Continuity toggle handler
  function handleContinuityToggle(isContinuousOnly: boolean) {
    if (optionPickerState) {
      optionPickerState.setContinuousOnly(isContinuousOnly);
    }
  }

  // Handle section change from swipe container
  function handleSectionChange(sectionIndex: number) {
    const sections = organizedPictographs();
    if (sections[sectionIndex]) {
      currentSectionTitle = sections[sectionIndex].title;
    }
  }

  // Real-time overflow monitoring
  let overflowCheckInterval: number | null = null;
  let lastKnownOverflow = $state(false);
  let forceRecalculation = $state(0);

  // Start overflow monitoring when service becomes available
  $effect(() => {
    // Wait for both service and container to be available
    if (typeof window !== 'undefined' && optionPickerSizingService && containerElement) {
      // Immediate overflow check when monitoring starts
      try {
        const overflowStatus = optionPickerSizingService.detectActualOverflow();

        if (overflowStatus.hasOverflow) {
          // Force immediate layout recalculation using proper method
          containerDimensions.forceUpdate();
          forceRecalculation++; // Trigger reactive updates
        }

        lastKnownOverflow = overflowStatus.hasOverflow;
      } catch (error) {
        console.error('❌ Initial overflow detection error:', error);
      }

      // Set up periodic monitoring
      overflowCheckInterval = window.setInterval(() => {
        try {
          const overflowStatus = optionPickerSizingService!.detectActualOverflow();

          if (overflowStatus.hasOverflow !== lastKnownOverflow) {
            lastKnownOverflow = overflowStatus.hasOverflow;
            if (overflowStatus.hasOverflow) {
              // Force a layout recalculation using proper method
              containerDimensions.forceUpdate();
              forceRecalculation++; // Trigger reactive updates
            }
          }
        } catch (error) {
          console.error('❌ Overflow detection error:', error);
        }
      }, 2000); // Check every 2 seconds

      return () => {
        if (overflowCheckInterval) {
          window.clearInterval(overflowCheckInterval);
          overflowCheckInterval = null;
        }
      };
    }
  });

  // Layout configuration using sizing service
  const layoutConfig = $derived(() => {
    // Include forceRecalculation in dependency to trigger updates
    forceRecalculation;

    // Return fallback if services not ready
    if (!optionPickerSizingService || !optionPickerState) {
      return {
        optionsPerRow: 4,
        pictographSize: 144,
        spacing: 8,
        containerWidth: containerDimensions.width,
        containerHeight: containerDimensions.height,
        gridColumns: 'repeat(4, 1fr)',
        gridGap: '8px',
      };
    }

    // Get optimal columns from sizing service
    const optionsPerRow = optionPickerSizingService.getOptimalColumns(
      containerDimensions.width,
      containerDimensions.width < 600 // isMobileDevice - Z Fold 6 friendly breakpoint
    );

    // Determine layout mode and calculate maximum pictographs per section
    const layoutMode: '8-column' | '4-column' = optionsPerRow === 8 ? '8-column' : '4-column';

    // Calculate max pictographs per section from organized data
    const maxPictographsPerSection = Math.max(
      ...organizedPictographs().map(section => section.pictographs.length),
      8 // Minimum assumption for sizing calculations
    );

    // Use overflow-aware sizing to prevent content from being cut off
    const sizingParams = {
      containerWidth: containerDimensions.width,
      containerHeight: containerDimensions.height,
      layoutMode,
      maxPictographsPerSection,
      isMobileDevice: containerDimensions.width < 800, // align with layout breakpoint
      headerHeight: 40, // Approximate section header height
      targetOverflowBuffer: 30, // Increased buffer for better safety margin
    };

    const sizingResult = optionPickerSizingService.calculateOverflowAwareSize(sizingParams);

    const finalConfig = {
      optionsPerRow,
      pictographSize: sizingResult.pictographSize,
      spacing: parseInt(sizingResult.gridGap.replace('px', '')),
      containerWidth: containerDimensions.width,
      containerHeight: containerDimensions.height,
      gridColumns: `repeat(${optionsPerRow}, 1fr)`,
      gridGap: sizingResult.gridGap,
    };

    return finalConfig;
  });

  let frozenLayoutConfig = $state({
    optionsPerRow: 4,
    pictographSize: 144,
    spacing: 8,
    containerWidth: containerDimensions.width,
    containerHeight: containerDimensions.height,
    gridColumns: 'repeat(4, 1fr)',
    gridGap: '8px',
  });

  $effect(() => {
    const currentConfig = layoutConfig();
    if (!(isTransitioningOptions || isUndoingOption)) {
      frozenLayoutConfig = currentConfig;
    }
  });

  // Organize pictographs using service (business logic in service)
  const organizedPictographs = $derived(() => {
    if (!optionPickerState?.filteredOptions.length || !optionOrganizerService) {
      return [];
    }

    // Always organize by type for simplicity
    const serviceResult = optionOrganizerService.organizePictographs(
      optionPickerState.filteredOptions,
      'type'
    );

    // Convert service result to match expected format
    return serviceResult.map(section => ({
      title: section.title,
      pictographs: section.pictographs,
      type: section.type === 'grouped' ? 'grouped' as const : 'individual' as const
    }));
  });

  // Handle option selection with coordinated fade-out/fade-in animation
  function handleOptionSelected(option: PictographData) {
    if (!optionPickerState || isTransitioningOptions) return;

    try {
      performance.mark('option-click-start');

      // Trigger selection haptic feedback for option selection
      hapticService?.trigger("selection");

      // 🎯 INSTANT FEEDBACK: Add to workbench IMMEDIATELY so user sees the connection
      onOptionSelected(option); // Workbench update happens right away!
      performance.mark('option-selected-callback-complete');

      // 🎬 PARALLEL ANIMATIONS: Start fade-out transition simultaneously
      isFadingOut = true;
      isTransitioningOptions = true; // Freeze navigation during transition
      performance.mark('fade-out-started');

      // Update option picker state mid-transition
      setTimeout(() => {
        // Update option picker state while content is faded out
        optionPickerState!.selectOption(option);
        performance.mark('option-picker-state-complete');

        // Reload options while still faded out (invisible data update)
        if (optionPickerState && currentSequence && currentSequence.length > 0) {
          optionPickerState.loadOptions(currentSequence);
        }
        performance.mark('options-reloaded-while-faded-out');
      }, FADE_OUT_DURATION / 2); // Halfway through fade-out

      // Start fade-in with updated data (smooth transition with new data)
      setTimeout(() => {
        // Start fade-in with already-updated data (no visual glitch)
        isFadingOut = false;
        performance.mark('fade-in-started-with-new-data');
      }, FADE_OUT_DURATION); // After fade-out completes

      // Complete transition after fade-in completes
      setTimeout(() => {
        // End transition - everything is now updated and visible
        isTransitioningOptions = false;
        performance.mark('transition-complete');
      }, FADE_OUT_DURATION + 250); // After fade-in completes

    } catch (error) {
      console.error("Failed to select option:", error);
      isTransitioningOptions = false;
      isFadingOut = false;
    }
  }

  // Reactive effect to load options when sequence changes (but not during transitions)
  $effect(() => {
    // Don't reload options during transitions to prevent navigation flash and panel reset
    if (isTransitioningOptions) {
      return;
    }

    if (optionPickerState && servicesReady && currentSequence && currentSequence.length > 0) {
      optionPickerState.loadOptions(currentSequence);
    } else if (optionPickerState && servicesReady && (!currentSequence || currentSequence.length === 0)) {
      optionPickerState.reset();
    }
  });

  // NOTE: Transitions are now handled directly in handleOptionSelected for immediate response

  // Watch for undo option trigger and animate the transition
  $effect(() => {
    if (isUndoingOption && optionPickerState && !isTransitioningOptions) {
      console.log("🔄 OptionViewer: Undo option triggered, starting fade animation");

      // Start fade-out transition
      isFadingOut = true;
      isTransitioningOptions = true;

      // Reload options mid-transition (while faded out)
      setTimeout(() => {
        if (optionPickerState && currentSequence && currentSequence.length > 0) {
          optionPickerState.loadOptions(currentSequence);
        }
      }, FADE_OUT_DURATION / 2);

      // Start fade-in after fade-out completes
      setTimeout(() => {
        isFadingOut = false;
      }, FADE_OUT_DURATION);

      // Complete transition after fade-in completes
      setTimeout(() => {
        isTransitioningOptions = false;
      }, FADE_OUT_DURATION + 250);
    }
  });

  // Determine if we should use swipe layout
  // CRITICAL: When in stacked layout (workbench on top, option picker on bottom),
  // ALWAYS use horizontal swipe, even if container is wide. Traditional grid layout
  // should only be used in true side-by-side desktop/tablet layouts.
  const shouldUseSwipeLayout = $derived(() => {
    if (!layoutDetectionService || !layoutConfig() || organizedPictographs().length <= 1) {
      return false;
    }

    // If in stacked layout (mobile), always use swipe for multiple sections
    const isStackedLayout = !isSideBySideLayout();
    if (isStackedLayout && organizedPictographs().length > 1) {
      return true;
    }

    // Otherwise, use the layout detection service logic
    return layoutDetectionService.shouldUseHorizontalSwipe(
      layoutConfig(),
      organizedPictographs().length,
      true // enableHorizontalSwipe
    );
  });

  // Initialize services and setup container tracking
  onMount(() => {
    // Initialize services
    try {
      const optionLoader = resolve<IOptionLoader>(TYPES.IOptionLoader);
      const filterService = resolve<IOptionFilter>(TYPES.IOptionFilter);
      const optionSorter = resolve<IOptionSorter>(TYPES.IOptionSorter);
      optionOrganizerService = resolve<IOptionOrganizer>(TYPES.IOptionOrganizerService);
      optionPickerSizingService = resolve<IOptionSizer>(TYPES.IOptionPickerSizingService);
      layoutDetectionService = resolve<ILayoutDetectionService>(TYPES.ILayoutDetectionService);

      // Trigger immediate overflow check if container is ready
      if (containerElement) {
        setTimeout(() => {
          if (optionPickerSizingService) {
            try {
              const overflowStatus = optionPickerSizingService.detectActualOverflow();

              if (overflowStatus.hasOverflow) {
                // Force a layout recalculation using proper method
                containerDimensions.forceUpdate();
                forceRecalculation++;
              }
            } catch (error) {
              console.error('❌ Manual overflow detection error:', error);
            }
          }
        }, 100); // Small delay to ensure DOM is ready
      }
      hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
      optionPickerState = createOptionPickerState({
        optionLoader,
        filterService,
        optionSorter,
      });
      servicesReady = true;
    } catch (error) {
      console.error("Failed to initialize option picker services:", error);
    }

    // Setup container dimension tracking
    if (containerElement) {
      return containerDimensions.attachToElement(containerElement);
    }
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
    <!-- Continuity Toggle with Section Title -->
    <ContinuityToggle
      isContinuousOnly={optionPickerState.isContinuousOnly}
      sectionTitle={formattedSectionTitle}
      onToggle={handleContinuityToggle}
    />

    <!-- Main content -->
    <div class="option-picker-content">
      <!-- State handling: loading, error, empty states -->
      {#if !containerDimensions.isReady}
        <div class="loading-state">
          <p>Initializing container...</p>
        </div>
      {:else if optionPickerState.state === 'loading'}
        <div class="loading-state">
          <p>Loading options...</p>
        </div>
      {:else if optionPickerState.error}
        <div class="error-state">
          <p>Error loading options: {optionPickerState.error}</p>
          <button onclick={() => optionPickerState?.clearError()}>Retry</button>
        </div>
      {:else if optionPickerState.filteredOptions.length === 0 && !(isClearingSequence || isTransitioningOptions)}
        <div class="empty-state">
          <p>No options available for the current sequence.</p>
          <p>Debug: Total options: {optionPickerState.options.length}, Filtered: {optionPickerState.filteredOptions.length}</p>
          <p>Continuous only: {optionPickerState.isContinuousOnly}</p>
        </div>
      {:else if optionPickerState.filteredOptions.length > 0}
        <!-- Layout selection: Swipe or Grid -->
        {#if shouldUseSwipeLayout()}
          <OptionViewerSwipeLayout
            organizedPictographs={organizedPictographs()}
            onPictographSelected={handleOptionSelected}
            onSectionChange={handleSectionChange}
            layoutConfig={frozenLayoutConfig}
            {currentSequence}
            isTransitioning={isTransitioningOptions || isUndoingOption}
            {isFadingOut}
          />
        {:else}
          <OptionViewerGridLayout
            organizedPictographs={organizedPictographs()}
            onPictographSelected={handleOptionSelected}
            layoutConfig={frozenLayoutConfig}
            {currentSequence}
            isTransitioning={isTransitioningOptions || isUndoingOption}
            {isFadingOut}
          />
        {/if}
      {/if}
    </div>
  {/if}
</div>

<style>
  .option-picker-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;

    /* Beautiful glassmorphism background */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.05),
      rgba(255, 255, 255, 0.02)
    );
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);

    overflow: hidden; /* Changed from visible to hidden to enable proper scrolling */
  }

  .option-picker-content {
    flex: 1;
    position: relative;
    overflow: hidden;
    min-height: 0; /* Crucial for flex child to allow proper scrolling */
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
