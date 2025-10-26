<!--
OptionViewerGridLayout.svelte - Traditional vertical scrolling grid layout

Displays option sections stacked vertically with smooth fade transitions.
Fallback layout when horizontal swipe is not suitable.

Features:
- Vertical scrolling
- All sections visible at once
- Smooth fade transitions between content
-->

<script lang="ts">
  import type { PictographData } from "$shared";
  import OptionPicker456Group from "./OptionViewer456Group.svelte";
  import OptionViewerSection from "./OptionViewerSection.svelte";

  // ===== Props =====
  const {
    organizedPictographs = [],
    onPictographSelected = () => {},
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

  const uniformPictographSize = $derived(() => layoutConfig?.pictographSize ?? 144);

  let frozenPictographs = $state(organizedPictographs);

  $effect(() => {
    if (!isTransitioning) {
      frozenPictographs = organizedPictographs;
    }
  });

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

<div class="grid-layout">
  {#each frozenPictographs as section (section.title)}
    <div
      class="section-wrapper"
      class:grouped-section={section.title === 'Types 4-6' || section.type === 'grouped'}
      in:fadeIn
      out:fadeOut
    >
      {#if section.title === 'Types 4-6' || section.type === 'grouped'}
        <!-- Grouped section (Types 4-6) -->
        <OptionPicker456Group
          pictographs={section.pictographs}
          {onPictographSelected}
          containerWidth={layoutConfig?.containerWidth || 800}
          pictographSize={layoutConfig?.pictographSize || 144}
          gridGap={layoutConfig?.gridGap || '8px'}
          layoutMode={layoutConfig?.optionsPerRow === 8 ? '8-column' : '4-column'}
          {currentSequence}
          {isFadingOut}
          forcedPictographSize={uniformPictographSize()}
        />
      {:else}
        <!-- Individual section (Types 1-3) -->
        <OptionViewerSection
          letterType={section.title}
          pictographs={section.pictographs}
          {onPictographSelected}
          {layoutConfig}
          {currentSequence}
          {isFadingOut}
          forcedPictographSize={uniformPictographSize()}
          contentAreaBounds={null}
        />
      {/if}
    </div>
  {/each}
</div>

<style>
  .grid-layout {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 16px;
    overflow-y: auto;
    padding-block: 24px;
  }

  .section-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
  }
</style>
