<!--
  VisibilityTab.svelte - Pictograph Visibility Settings

  Allows users to control which elements are visible in pictographs:
  - Motion visibility (Red/Blue)
  - Dependent glyphs (TKA, VTG, Elemental, Positions) - require both motions
  - Independent glyphs (Reversals)
  - Grid elements (Non-radial points)

  Features:
  - Interactive preview pictograph
  - Click-to-toggle on preview elements
  - Toggle buttons for each element type
  - Dependency warnings and constraints
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
  import Pictograph from "$lib/shared/pictograph/shared/components/Pictograph.svelte";
  import { Letter } from "$lib/shared/foundation/domain/models/Letter";
  import { GridMode } from "$lib/shared/pictograph/grid/domain/enums/grid-enums";
  import { GridPosition } from "$lib/shared/pictograph/grid/domain/enums/grid-enums";

  interface Props {
    currentSettings: Record<string, unknown>;
    onSettingUpdate: (event: { key: string; value: unknown }) => void;
  }

  let { currentSettings, onSettingUpdate }: Props = $props();

  // Visibility state manager
  const visibilityManager = getVisibilityStateManager();

  // Local reactive state for UI
  let redMotionVisible = $state(true);
  let blueMotionVisible = $state(true);
  let tkaVisible = $state(true);
  let vtgVisible = $state(false);
  let elementalVisible = $state(false);
  let positionsVisible = $state(false);
  let reversalsVisible = $state(true);
  let nonRadialVisible = $state(false);

  // Derived states
  const allMotionsVisible = $derived(redMotionVisible && blueMotionVisible);
  const showDependencyWarning = $derived(!allMotionsVisible);

  // Example pictograph data for preview - Letter A with proper MotionData
  // Use createMotionData to ensure all required fields including propPlacementData
  const examplePictographData = {
    id: "visibility-preview",
    letter: Letter.A,
    startPosition: GridPosition.ALPHA1,
    endPosition: GridPosition.ALPHA5,
    gridMode: GridMode.DIAMOND,
    motions: {
      blue: createMotionData({
        motionType: MotionType.PRO,
        rotationDirection: RotationDirection.CLOCKWISE,
        startLocation: GridLocation.SOUTH,
        endLocation: GridLocation.WEST,
        turns: 1,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.CLOCK,
        color: MotionColor.BLUE,
        isVisible: true,
        arrowLocation: GridLocation.WEST,
        gridMode: GridMode.DIAMOND,
      }),
      red: createMotionData({
        motionType: MotionType.ANTI,
        rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.EAST,
        turns: 1,
        startOrientation: Orientation.OUT,
        endOrientation: Orientation.COUNTER,
        color: MotionColor.RED,
        isVisible: true,
        arrowLocation: GridLocation.EAST,
        gridMode: GridMode.DIAMOND,
      }),
    },
  };

  onMount(() => {
    // Load initial state from visibility manager
    redMotionVisible = visibilityManager.getMotionVisibility(MotionColor.RED);
    blueMotionVisible = visibilityManager.getMotionVisibility(MotionColor.BLUE);
    tkaVisible = visibilityManager.getRawGlyphVisibility("TKA");
    vtgVisible = visibilityManager.getRawGlyphVisibility("VTG");
    elementalVisible = visibilityManager.getRawGlyphVisibility("Elemental");
    positionsVisible = visibilityManager.getRawGlyphVisibility("Positions");
    reversalsVisible = visibilityManager.getRawGlyphVisibility("Reversals");
    nonRadialVisible = visibilityManager.getNonRadialVisibility();

    // Register observer for external changes
    const observer = () => {
      redMotionVisible = visibilityManager.getMotionVisibility(MotionColor.RED);
      blueMotionVisible = visibilityManager.getMotionVisibility(MotionColor.BLUE);
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

  function toggleRedMotion() {
    const newValue = !redMotionVisible;
    redMotionVisible = newValue;
    visibilityManager.setMotionVisibility(MotionColor.RED, newValue);
    // Note: The manager might have adjusted the value due to constraints
    redMotionVisible = visibilityManager.getMotionVisibility(MotionColor.RED);
    blueMotionVisible = visibilityManager.getMotionVisibility(MotionColor.BLUE);
  }

  function toggleBlueMotion() {
    const newValue = !blueMotionVisible;
    blueMotionVisible = newValue;
    visibilityManager.setMotionVisibility(MotionColor.BLUE, newValue);
    // Note: The manager might have adjusted the value due to constraints
    redMotionVisible = visibilityManager.getMotionVisibility(MotionColor.RED);
    blueMotionVisible = visibilityManager.getMotionVisibility(MotionColor.BLUE);
  }

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
    <p class="description">
      Control which elements are visible in pictographs
    </p>
  </div>

  <!-- Main Content - 50/50 Split -->
  <div class="content">
    <!-- Left Side: Controls -->
    <div class="controls-section">
      <!-- Motion Controls -->
      <div class="control-group motion-group">
        <h4 class="group-title">Motion Visibility</h4>
        <p class="group-note">At least one motion must remain visible</p>

        <div class="toggle-row">
          <span class="toggle-label">Red Motion</span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={redMotionVisible}
              onchange={toggleRedMotion}
              aria-label="Toggle red motion visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Blue Motion</span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={blueMotionVisible}
              onchange={toggleBlueMotion}
              aria-label="Toggle blue motion visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>

      <!-- Dependency Warning -->
      {#if showDependencyWarning}
        <div class="dependency-warning">
          ⚠️ Dependent glyphs require both motions to be visible
        </div>
      {/if}

      <!-- Element Visibility Controls -->
      <div class="control-group element-group">
        <h4 class="group-title">Element Visibility</h4>

        <!-- Dependent Glyphs -->
        <div class="toggle-row" class:disabled={!allMotionsVisible}>
          <span class="toggle-label">
            TKA
            {#if !allMotionsVisible}
              <span class="disabled-badge">requires both motions</span>
            {/if}
          </span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={tkaVisible && allMotionsVisible}
              disabled={!allMotionsVisible}
              onchange={toggleTKA}
              aria-label="Toggle TKA glyph visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row" class:disabled={!allMotionsVisible}>
          <span class="toggle-label">
            VTG
            {#if !allMotionsVisible}
              <span class="disabled-badge">requires both motions</span>
            {/if}
          </span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={vtgVisible && allMotionsVisible}
              disabled={!allMotionsVisible}
              onchange={toggleVTG}
              aria-label="Toggle VTG glyph visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row" class:disabled={!allMotionsVisible}>
          <span class="toggle-label">
            Elemental
            {#if !allMotionsVisible}
              <span class="disabled-badge">requires both motions</span>
            {/if}
          </span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={elementalVisible && allMotionsVisible}
              disabled={!allMotionsVisible}
              onchange={toggleElemental}
              aria-label="Toggle elemental glyph visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row" class:disabled={!allMotionsVisible}>
          <span class="toggle-label">
            Positions
            {#if !allMotionsVisible}
              <span class="disabled-badge">requires both motions</span>
            {/if}
          </span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={positionsVisible && allMotionsVisible}
              disabled={!allMotionsVisible}
              onchange={togglePositions}
              aria-label="Toggle position glyph visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <!-- Independent Glyphs -->
        <div class="toggle-row">
          <span class="toggle-label">Reversals</span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={reversalsVisible}
              onchange={toggleReversals}
              aria-label="Toggle reversal indicators visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <!-- Grid Elements -->
        <div class="toggle-row">
          <span class="toggle-label">Non-radial Points</span>
          <label class="toggle-switch">
            <input
              type="checkbox"
              checked={nonRadialVisible}
              onchange={toggleNonRadial}
              aria-label="Toggle non-radial points visibility"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>
    </div>

    <!-- Right Side: Interactive Preview -->
    <div class="preview-section">
      <h4 class="preview-title">Interactive Preview</h4>
      <p class="preview-note">
        Click elements in the preview to toggle their visibility
      </p>

      <div class="preview-container">
        <Pictograph pictographData={examplePictographData} size={300} />
      </div>
    </div>
  </div>
</div>

<style>
  .visibility-tab {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 100%;
    padding: 0 8px;
  }

  /* Header */
  .header {
    text-align: center;
  }

  .title {
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 8px 0;
  }

  .description {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  /* Main Content - 50/50 Split */
  .content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
  }

  /* Controls Section */
  .controls-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .control-group {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 16px;
  }

  .motion-group {
    background: rgba(59, 130, 246, 0.08);
    border-color: rgba(59, 130, 246, 0.2);
  }

  .element-group {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
  }

  .group-title {
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 8px 0;
  }

  .group-note {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
    margin: 0 0 12px 0;
  }

  /* Dependency Warning */
  .dependency-warning {
    background: rgba(255, 193, 7, 0.1);
    border: 2px solid rgba(255, 193, 7, 0.3);
    border-radius: 8px;
    padding: 12px;
    color: rgba(255, 193, 7, 1);
    font-size: 13px;
    font-weight: 600;
    text-align: center;
  }

  /* Toggle Row */
  .toggle-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    transition: opacity 0.2s;
  }

  .toggle-row:last-child {
    border-bottom: none;
  }

  .toggle-row.disabled {
    opacity: 0.5;
  }

  .toggle-label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.95);
  }

  .disabled-badge {
    font-size: 11px;
    font-weight: 400;
    color: rgba(255, 193, 7, 0.9);
  }

  /* Toggle Switch */
  .toggle-switch {
    flex-shrink: 0;
    position: relative;
    display: inline-block;
    width: 48px;
    height: 28px;
    cursor: pointer;
  }

  .toggle-switch input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    margin: 0;
    z-index: 2;
    top: 0;
    left: 0;
  }

  .toggle-slider {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    transition: all 0.3s;
  }

  .toggle-slider:before {
    content: "";
    position: absolute;
    height: 22px;
    width: 22px;
    left: 3px;
    bottom: 3px;
    background: white;
    border-radius: 50%;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  input:checked + .toggle-slider {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
  }

  input:checked + .toggle-slider:before {
    transform: translateX(20px);
  }

  input:disabled + .toggle-slider {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Preview Section */
  .preview-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .preview-title {
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    text-align: center;
  }

  .preview-note {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
    margin: 0;
    text-align: center;
  }

  .preview-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    min-height: 300px;
  }

  /* Responsive Design */
  @media (max-width: 968px) {
    .content {
      grid-template-columns: 1fr;
      gap: 20px;
    }

    .preview-section {
      order: -1; /* Show preview first on mobile */
    }
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .toggle-row,
    .toggle-slider,
    .toggle-slider:before {
      transition: none;
    }
  }

  @media (prefers-contrast: high) {
    .control-group,
    .content {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.3);
    }

    .dependency-warning {
      border-width: 3px;
    }
  }
</style>
