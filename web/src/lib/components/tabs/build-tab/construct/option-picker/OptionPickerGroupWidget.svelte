<!--
OptionPickerGroupWidget.svelte - Horizontal group for Types 4, 5, 6

Matches the desktop version exactly:
- Horizontal layout for Types 4, 5, 6 (Dash, Dual-Dash, Static)
- Fixed size policy to prevent stretching
- Minimal spacing to prevent overflow
- Centered alignment
-->
<script lang="ts">
  import type { PictographData } from "$domain";

  // import { LetterType } from './types/LetterType'; // Temporarily disabled to avoid initialization issues
  import OptionPickerSection from "./OptionPickerSection.svelte";

  // Props
  const {
    pictographs = [],
    onPictographSelected = () => {},
    containerWidth = 800,
  } = $props<{
    pictographs?: PictographData[];
    onPictographSelected?: (pictograph: PictographData) => void;
    containerWidth?: number;
  }>();

  // Groupable types (Types 4, 5, 6) - matches desktop exactly
  const groupableTypes = ["Type4", "Type5", "Type6"];

  // Calculate section width for horizontal layout
  const sectionWidth = $derived(() => {
    // Divide available width among the 3 sections with minimal spacing
    const spacing = 2; // Minimal spacing like desktop (1px × 2 = 2px total)
    const totalSpacing = spacing * (groupableTypes.length - 1);
    const availableWidth = containerWidth - totalSpacing;
    return Math.floor(availableWidth / groupableTypes.length);
  });
</script>

<div class="group-widget">
  <div class="horizontal-layout">
    {#each groupableTypes as letterType (letterType)}
      <div class="section-container" style:width="{sectionWidth()}px">
        <OptionPickerSection
          {letterType}
          {pictographs}
          {onPictographSelected}
          containerWidth={sectionWidth()}
        />
      </div>
    {/each}
  </div>
</div>

<style>
  .group-widget {
    width: 100%;
    /* Fixed size policy like desktop to prevent stretching */
    flex-shrink: 0;
    flex-grow: 0;
  }

  .horizontal-layout {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    /* Minimal spacing to prevent overflow (matches desktop) */
    gap: 2px;
    width: 100%;
    /* Prevent content from overflowing */
    overflow: hidden;
  }

  .section-container {
    /* Fixed size policy to prevent stretching */
    flex-shrink: 0;
    flex-grow: 0;
    /* Ensure sections don't exceed their allocated width */
    min-width: 0;
    overflow: hidden;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .horizontal-layout {
      gap: 1px;
    }
  }

  @media (max-width: 480px) {
    /* Stack vertically on very small screens */
    .horizontal-layout {
      flex-direction: column;
      gap: 8px;
    }

    .section-container {
      width: 100% !important;
    }
  }
</style>
