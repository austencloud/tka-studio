<!--
OptionViewerSwipeLayout.svelte - Horizontal swipe panel navigation

Displays option sections as swipeable panels using HorizontalSwipeContainer.
Each section becomes a full-width panel that users can swipe through.

Features:
- Horizontal panel swiping
- Panel position persistence in sessionStorage
- Smooth fade transitions between content
- Content area bounds for optimal sizing
-->

<script lang="ts">
  import type { PictographData } from "$shared";
  import { HorizontalSwipeContainer } from "$shared";
  import OptionPicker456Group from "./OptionViewer456Group.svelte";
  import OptionViewerSection from "./OptionViewerSection.svelte";

  // ===== Props =====
  const {
    organizedPictographs = [],
    onPictographSelected = () => {},
    onSectionChange = () => {},
    layoutConfig,
    currentSequence = [],
    isTransitioning = false,
    isFadingOut = false,
  } = $props<{
    organizedPictographs?: {
      title: string;
      pictographs: PictographData[];
      type: 'individual' | 'grouped';
    }[];
    onPictographSelected?: (pictograph: PictographData) => void;
    onSectionChange?: (sectionIndex: number) => void;
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
    isTransitioning?: boolean;
    isFadingOut?: boolean;
  }>();

  // ===== Panel Position Persistence =====
  const PANEL_STORAGE_KEY = 'tka-option-picker-panel';

  // Load panel position from storage (non-reactive, only read once on initialization)
  function getInitialPanelIndex(): number {
    if (typeof window !== 'undefined') {
      try {
        const stored = sessionStorage.getItem(PANEL_STORAGE_KEY);
        const panelIndex = stored ? parseInt(stored, 10) : 0;
        return isNaN(panelIndex) ? 0 : Math.max(0, panelIndex);
      } catch {
        return 0;
      }
    }
    return 0;
  }

  const initialPanelIndex = getInitialPanelIndex();

  // ===== State =====
  let contentAreaBounds = $state<{ left: number; right: number; width: number } | null>(null);

  // Freeze pictograph data during transitions to prevent layout shifts
  let frozenPictographs = $state(organizedPictographs);

  // Update frozen data only when not transitioning
  $effect(() => {
    if (!isTransitioning) {
      frozenPictographs = organizedPictographs;
    }
  });

  // ===== Event Handlers =====
  function handlePanelChange(panelIndex: number) {
    // Save panel position to sessionStorage
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem(PANEL_STORAGE_KEY, panelIndex.toString());
      } catch (error) {
        console.error('❌ Failed to save panel position to sessionStorage:', error);
      }
    }

    // Notify parent of section change for header update
    onSectionChange(panelIndex);
  }

  function handleContentAreaChange(bounds: { left: number; right: number; width: number }) {
    contentAreaBounds = bounds;
  }

  // ===== Transitions =====
  function fadeIn(node: Element) {
    return {
      delay: 0,
      duration: 150,
      css: (t: number) => `opacity: ${t}`
    };
  }

  function fadeOut(node: Element) {
    return {
      delay: 0,
      duration: 150,
      css: (t: number) => `opacity: ${t}`
    };
  }
</script>

<div class="swipe-layout">
  <HorizontalSwipeContainer
    panels={frozenPictographs}
    showIndicators={true}
    initialPanelIndex={initialPanelIndex}
    onPanelChange={handlePanelChange}
    onContentAreaChange={handleContentAreaChange}
    freezeNavigation={isTransitioning}
    loop={true}
    height="100%"
    width="100%"
    preservePosition={true}
    storageKey={PANEL_STORAGE_KEY}
  >
    {#each frozenPictographs as section, index (section.title)}
      <div
        class="panel"
        data-panel-index={index}
        data-section-type={section.type || 'individual'}
      >
        <div class="panel-content">
          {#if section.title === 'Types 4-6' || section.type === 'grouped'}
            <!-- Grouped section (Types 4-6) -->
            <OptionPicker456Group
              pictographs={isTransitioning ? section.pictographs : section.pictographs}
              {onPictographSelected}
              containerWidth={contentAreaBounds?.width || layoutConfig?.containerWidth || 800}
              pictographSize={layoutConfig?.pictographSize || 144}
              gridGap={layoutConfig?.gridGap || '8px'}
              layoutMode={layoutConfig?.optionsPerRow === 8 ? '8-column' : '4-column'}
              {currentSequence}
              {isFadingOut}
              {contentAreaBounds}
            />
          {:else}
            <!-- Individual section (Types 1-3) -->
            <OptionViewerSection
              letterType={section.title}
              pictographs={isTransitioning ? section.pictographs : section.pictographs}
              {onPictographSelected}
              {layoutConfig}
              {currentSequence}
              {isFadingOut}
              {contentAreaBounds}
              showHeader={false}
            />
          {/if}
        </div>
      </div>
    {/each}
  </HorizontalSwipeContainer>
</div>

<style>
  .swipe-layout {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .panel {
    width: 100%;
    height: 100%;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
  }

  .panel-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center content vertically */
    /* Dynamic offset calculated per-panel based on actual header heights */
    /* Uses CSS custom property set by applyCentering action */
    /* Removed transition to prevent layout shifts during option changes */
  }
</style>
