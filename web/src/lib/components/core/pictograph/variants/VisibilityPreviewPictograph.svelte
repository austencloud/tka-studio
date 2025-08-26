<!--
VisibilityPreviewPictograph.svelte - Live Preview for Visibility Settings

Replicates the desktop app's visibility pictograph that shows example data
with real-time opacity changes based on visibility settings.
-->
<script lang="ts">
  import type { PictographData } from "$lib/domain";
  import {
    createMotionData,
    createPictographData,
    Location,
    MotionColor,
    MotionType,
    Orientation,
    RotationDirection,
  } from "$lib/domain";
  import { getVisibilityStateManager } from "$lib/services/implementations/ui/VisibilityStateManager";
  import { onMount } from "svelte";
  import PictographWithVisibility from "./PictographWithVisibility.svelte";

  interface Props {
    /** Width of the preview */
    width?: number;
    /** Height of the preview */
    height?: number;
    /** Debug mode */
    debug?: boolean;
  }

  let { width = 300, height = 300, debug = false }: Props = $props();

  // Visibility state manager
  let visibilityManager = getVisibilityStateManager();
  let visibilityUpdateCount = $state(0);

  // Force re-render when visibility changes
  function handleVisibilityChange() {
    visibilityUpdateCount++;
  }

  onMount(() => {
    visibilityManager.registerObserver(handleVisibilityChange);

    return () => {
      visibilityManager.unregisterObserver(handleVisibilityChange);
    };
  });

  // Example pictograph data (matching desktop app's example)
  const exampleData: PictographData = createPictographData({
    motions: {
      blue: createMotionData({
        motionType: MotionType.PRO,
        startLocation: Location.SOUTH,
        endLocation: Location.WEST,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.CLOCKWISE,
        turns: 1.0,
        isVisible: true,
      }),
      red: createMotionData({
        motionType: MotionType.PRO,
        startLocation: Location.NORTH,
        endLocation: Location.EAST,
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.CLOCKWISE,
        turns: 1.0,
        isVisible: true,
      }),
    },
  });

  // Derived state - create preview data with opacity effects
  const previewData = $derived(() => {
    // Force reactivity
    visibilityUpdateCount;

    // Start with base example data
    let data = { ...exampleData };

    // For the preview, we always show all elements but use opacity
    // This is handled via CSS opacity manipulation
    return data;
  });
</script>

<!-- Visibility Preview Container -->
<div
  class="visibility-preview"
  class:debug-mode={debug}
  style:width="{width}px"
  style:height="{height}px"
>
  <!-- Preview Pictograph -->
  <div class="preview-pictograph">
    <PictographWithVisibility
      pictographData={previewData()}
      forceShowAll={true}
      enableVisibility={false}
    />

    <!-- Visibility Overlay Effects -->
    <div class="visibility-overlays">
      <!-- Red Motion Overlay -->
      <div
        class="motion-overlay red-motion"
        class:hidden={!visibilityManager.getMotionVisibility(MotionColor.RED)}
      ></div>

      <!-- Blue Motion Overlay -->
      <div
        class="motion-overlay blue-motion"
        class:hidden={!visibilityManager.getMotionVisibility(MotionColor.BLUE)}
      ></div>

      <!-- TKA Letter Overlay -->
      <div
        class="glyph-overlay letter-overlay"
        class:hidden={!visibilityManager.getGlyphVisibility("TKA")}
      ></div>

      <!-- Reversals Overlay -->
      <div
        class="glyph-overlay reversals-overlay"
        class:hidden={!visibilityManager.getGlyphVisibility("Reversals")}
      ></div>

      <!-- Positions Overlay -->
      <div
        class="glyph-overlay positions-overlay"
        class:hidden={!visibilityManager.getGlyphVisibility("Positions")}
      ></div>

      <!-- VTG Overlay -->
      <div
        class="glyph-overlay vtg-overlay"
        class:hidden={!visibilityManager.getGlyphVisibility("VTG")}
      ></div>

      <!-- Elemental Overlay -->
      <div
        class="glyph-overlay elemental-overlay"
        class:hidden={!visibilityManager.getGlyphVisibility("Elemental")}
      ></div>
    </div>
  </div>

  <!-- Preview Label -->
  <div class="preview-label">
    <div class="label-text">Live Preview</div>
    <div class="label-subtitle">Changes reflect in real-time</div>
  </div>

  <!-- Debug Information -->
  {#if debug}
    <div class="debug-panel">
      <div class="debug-title">Preview Debug</div>
      <div class="debug-section">
        <div>
          All Motions: {visibilityManager.areAllMotionsVisible() ? "YES" : "NO"}
        </div>
        <div>
          Dependent Available: {visibilityManager.areAllMotionsVisible()
            ? "YES"
            : "NO"}
        </div>
        <div>Update Count: {visibilityUpdateCount}</div>
      </div>
    </div>
  {/if}
</div>

<style>
  .visibility-preview {
    position: relative;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    background: linear-gradient(
      135deg,
      rgba(31, 41, 59, 0.05),
      rgba(55, 65, 81, 0.03)
    );
    overflow: hidden;
    backdrop-filter: blur(10px);
  }

  .preview-pictograph {
    position: relative;
    width: 100%;
    height: calc(100% - 60px); /* Reserve space for label */
    padding: 16px;
  }

  .visibility-overlays {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 10;
  }

  .motion-overlay,
  .glyph-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.85);
    transition: opacity 0.3s ease;
    opacity: 0;
  }

  .motion-overlay.hidden,
  .glyph-overlay.hidden {
    opacity: 1;
  }

  /* Specific overlay targeting */
  .red-motion {
    /* Target red elements via CSS filters */
    background: rgba(239, 68, 68, 0.2);
    mix-blend-mode: multiply;
  }

  .blue-motion {
    /* Target blue elements via CSS filters */
    background: rgba(59, 130, 246, 0.2);
    mix-blend-mode: multiply;
  }

  .letter-overlay {
    /* Target letter elements */
    background: rgba(75, 85, 99, 0.85);
  }

  .preview-label {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(5px);
  }

  .label-text {
    font-size: 14px;
    font-weight: 600;
    color: white;
    margin-bottom: 2px;
  }

  .label-subtitle {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.7);
    font-style: italic;
  }

  .debug-panel {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 10px;
    z-index: 100;
  }

  .debug-title {
    font-weight: bold;
    margin-bottom: 4px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    padding-bottom: 2px;
  }

  .debug-section div {
    margin-bottom: 2px;
  }

  /* Enhanced effects for motion visibility */
  .preview-pictograph :global(.motion-element) {
    transition:
      opacity 0.3s ease,
      filter 0.3s ease;
  }

  .preview-pictograph :global(.motion-element.red.hidden) {
    opacity: 0.1;
    filter: grayscale(100%);
  }

  .preview-pictograph :global(.motion-element.blue.hidden) {
    opacity: 0.1;
    filter: grayscale(100%);
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .preview-label {
      height: 50px;
    }

    .label-text {
      font-size: 12px;
    }

    .label-subtitle {
      font-size: 10px;
    }
  }
</style>
