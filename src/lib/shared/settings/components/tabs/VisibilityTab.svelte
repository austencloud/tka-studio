<!--
  VisibilityTab.svelte - Pictograph Visibility Settings

  Allows users to control which elements are visible in pictographs:
  - Glyphs (TKA, VTG, Elemental, Positions, Reversals)
  - Grid elements (Non-radial points)

  Features:
  - Interactive preview pictograph
  - Click-to-toggle on preview elements
  - Toggle buttons for each element type
-->
<script lang="ts">
  import { getVisibilityStateManager } from "$lib/shared/pictograph/shared/state/visibility-state.svelte";
  import {
    MotionColor,
    MotionType,
    RotationDirection,
    GridLocation,
    Orientation,
    createMotionData,
  } from "$shared";
  import { onMount } from "svelte";
  import { Letter } from "$lib/shared/foundation/domain/models/Letter";
  import { GridMode } from "$lib/shared/pictograph/grid/domain/enums/grid-enums";
  import { GridPosition } from "$lib/shared/pictograph/grid/domain/enums/grid-enums";
  import { ElementVisibilityControls, PreviewSection } from "./visibility";

  interface Props {
    currentSettings: Record<string, unknown>;
    onSettingUpdate: (event: { key: string; value: unknown }) => void;
  }

  let { currentSettings, onSettingUpdate }: Props = $props();

  // Visibility state manager
  const visibilityManager = getVisibilityStateManager();

  // Local reactive state for UI
  let tkaVisible = $state(true);
  let vtgVisible = $state(false);
  let elementalVisible = $state(false);
  let positionsVisible = $state(false);
  let reversalsVisible = $state(true);
  let nonRadialVisible = $state(false);

  // Preview visibility toggle for small screens
  let showPreview = $state(false);

  // Example pictograph data for preview - Letter A with proper MotionData
  // Use createMotionData to ensure all required fields including propPlacementData
  const examplePictographData = {
    id: "visibility-preview",
    letter: Letter.A,
    startPosition: GridPosition.ALPHA1,
    endPosition: GridPosition.ALPHA3,
    gridMode: GridMode.DIAMOND,
    motions: {
      blue: createMotionData({
        motionType: MotionType.PRO,
        rotationDirection: RotationDirection.CLOCKWISE,
        startLocation: GridLocation.SOUTH,
        endLocation: GridLocation.WEST,
        turns: 0,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        color: MotionColor.BLUE,
        isVisible: true,
        arrowLocation: GridLocation.WEST,
        gridMode: GridMode.DIAMOND,
      }),
      red: createMotionData({
        motionType: MotionType.PRO,
        rotationDirection: RotationDirection.CLOCKWISE,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.EAST,
        turns: 0,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        color: MotionColor.RED,
        isVisible: true,
        arrowLocation: GridLocation.EAST,
        gridMode: GridMode.DIAMOND,
      }),
    },
  };

  onMount(() => {
    // Load initial state from visibility manager
    tkaVisible = visibilityManager.getRawGlyphVisibility("TKA");
    vtgVisible = visibilityManager.getRawGlyphVisibility("VTG");
    elementalVisible = visibilityManager.getRawGlyphVisibility("Elemental");
    positionsVisible = visibilityManager.getRawGlyphVisibility("Positions");
    reversalsVisible = visibilityManager.getRawGlyphVisibility("Reversals");
    nonRadialVisible = visibilityManager.getNonRadialVisibility();

    // Register observer for external changes
    const observer = () => {
      tkaVisible = visibilityManager.getRawGlyphVisibility("TKA");
      vtgVisible = visibilityManager.getRawGlyphVisibility("VTG");
      elementalVisible = visibilityManager.getRawGlyphVisibility("Elemental");
      positionsVisible = visibilityManager.getRawGlyphVisibility("Positions");
      reversalsVisible = visibilityManager.getRawGlyphVisibility("Reversals");
      nonRadialVisible = visibilityManager.getNonRadialVisibility();
    };

    visibilityManager.registerObserver(observer, ["all"]);

    return () => {
      visibilityManager.unregisterObserver(observer);
    };
  });

  function toggleTKA() {
    tkaVisible = !tkaVisible;
    visibilityManager.setGlyphVisibility("TKA", tkaVisible);
  }

  function toggleVTG() {
    vtgVisible = !vtgVisible;
    visibilityManager.setGlyphVisibility("VTG", vtgVisible);
  }

  function toggleElemental() {
    elementalVisible = !elementalVisible;
    visibilityManager.setGlyphVisibility("Elemental", elementalVisible);
  }

  function togglePositions() {
    positionsVisible = !positionsVisible;
    visibilityManager.setGlyphVisibility("Positions", positionsVisible);
  }

  function toggleReversals() {
    reversalsVisible = !reversalsVisible;
    visibilityManager.setGlyphVisibility("Reversals", reversalsVisible);
  }

  function toggleNonRadial() {
    nonRadialVisible = !nonRadialVisible;
    visibilityManager.setNonRadialVisibility(nonRadialVisible);
  }
</script>

<div class="visibility-tab">
  <!-- Title and Description -->
  <div class="header">
    <h3 class="title">Visibility Settings</h3>
    <p class="description">Control which elements are visible in pictographs</p>

    <!-- Preview Toggle Button (only visible on small containers) -->
    <button
      class="preview-toggle-btn"
      onclick={() => (showPreview = !showPreview)}
      aria-expanded={showPreview}
      aria-controls="preview-section"
    >
      <span class="toggle-icon" class:expanded={showPreview}>▼</span>
      {showPreview ? "Hide" : "Show"} Preview
    </button>
  </div>

  <!-- Main Content - 50/50 Split -->
  <div class="content">
    <!-- Left Side: Controls (hidden on small screens when preview is shown) -->
    <div class="controls-section" class:hidden-mobile={showPreview}>
      <ElementVisibilityControls
        {tkaVisible}
        {vtgVisible}
        {elementalVisible}
        {positionsVisible}
        {reversalsVisible}
        {nonRadialVisible}
        onToggleTKA={toggleTKA}
        onToggleVTG={toggleVTG}
        onToggleElemental={toggleElemental}
        onTogglePositions={togglePositions}
        onToggleReversals={toggleReversals}
        onToggleNonRadial={toggleNonRadial}
      />
    </div>

    <!-- Right Side: Interactive Preview (only shown on small screens when toggled) -->
    <div
      id="preview-section"
      class="preview-wrapper"
      class:visible-mobile={showPreview}
    >
      <PreviewSection pictographData={examplePictographData} />
    </div>
  </div>
</div>

<style>
  .visibility-tab {
    display: flex;
    flex-direction: column;
    gap: clamp(1rem, 2.5vw, 1.5rem);
    max-width: 100%;
    padding: 0 clamp(0.5rem, 1vw, 1rem);
    container-type: inline-size;
  }

  /* Header */
  .header {
    display: flex;
    flex-direction: column;
    gap: clamp(0.75rem, 2vw, 1rem);
    text-align: center;
  }

  .title {
    font-size: clamp(1.125rem, 2vw + 0.5rem, 1.5rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .description {
    font-size: clamp(0.813rem, 1.5vw + 0.25rem, 1rem);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  /* Main Content - Fluid Container Query Layout */
  .content {
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(1rem, 2.5vw, 2rem);
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(0.625rem, 1vw, 0.875rem);
    padding: clamp(1rem, 2.5vw, 1.75rem);
    align-items: start;
  }

  /* Controls Section */
  .controls-section {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  /* Hide controls on small screens when preview is active */
  .controls-section.hidden-mobile {
    display: none;
  }

  /* Preview Toggle Button - Only visible on small containers */
  .preview-toggle-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    max-width: 20rem;
    margin: 0 auto;
    padding: clamp(0.625rem, 1.5vw, 0.875rem);
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    border: none;
    border-radius: clamp(0.5rem, 1vw, 0.75rem);
    font-size: clamp(0.813rem, 1.5vw, 0.938rem);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    min-height: 44px;
  }

  .preview-toggle-btn:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    transform: translateY(-1px);
  }

  .preview-toggle-btn:active {
    transform: translateY(0);
  }

  .preview-toggle-btn:focus-visible {
    outline: 2px solid rgba(191, 219, 254, 0.7);
    outline-offset: 2px;
  }

  .toggle-icon {
    display: inline-block;
    transition: transform 0.3s ease;
    font-size: 0.75em;
  }

  .toggle-icon.expanded {
    transform: rotate(180deg);
  }

  /* Preview Wrapper - Hidden by default on small screens, shows when toggled */
  .preview-wrapper {
    display: none;
  }

  .preview-wrapper.visible-mobile {
    display: block;
  }

  /* Container Query - Two Column Layout for Wider Containers */
  @container (min-width: 700px) {
    .content {
      grid-template-columns: minmax(min(100%, 20rem), 1fr) minmax(
          min(100%, 25rem),
          2fr
        );
      gap: clamp(1.5rem, 3vw, 2.5rem);
    }

    /* Hide toggle button on larger containers */
    .preview-toggle-btn {
      display: none;
    }

    /* Always show both sections on larger containers */
    .controls-section,
    .controls-section.hidden-mobile {
      display: flex;
    }

    .preview-wrapper,
    .preview-wrapper.visible-mobile {
      display: block;
      overflow: visible;
    }
  }

  /* Container Query - Balanced Layout for Very Wide Containers */
  @container (min-width: 1000px) {
    .content {
      grid-template-columns: minmax(22rem, 1fr) minmax(30rem, 2.5fr);
    }
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .preview-toggle-btn,
    .toggle-icon,
    .preview-wrapper {
      transition: none;
    }

    .preview-toggle-btn:hover {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .content {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.3);
    }

    .preview-toggle-btn {
      border: 2px solid rgba(255, 255, 255, 0.3);
    }
  }
</style>
