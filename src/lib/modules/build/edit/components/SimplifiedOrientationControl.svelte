<!--
SimplifiedOrientationControl.svelte - Always-visible stepper control for narrow screens

Research-backed design for 344px portrait (Z Fold):
- Zero interaction cost - all controls visible
- 44x44px touch targets (previous/next buttons)
- Horizontal stepper layout matching turn controls
- Current orientation prominently displayed
- Cycles through: In → Out → Clock → Counter → In
-->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  const {
    color,
    currentBeatData,
    onOrientationChanged,
  } = $props<{
    color: "blue" | "red";
    currentBeatData: BeatData | null;
    onOrientationChanged: (color: string, orientation: string) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Constants - orientation cycle order
  const orientations = ["in", "out", "clock", "counter"];

  // Derived values - Fixed: removed arrow functions to get actual values
  const displayLabel = $derived(color === "blue" ? "Left" : "Right");

  const currentOrientation = $derived.by(() => {
    if (!currentBeatData) return "in"; // Default to "in"
    // Fixed: access motions.blue.startOrientation instead of .blueOrientation
    const motion = color === "blue"
      ? currentBeatData.motions?.blue
      : currentBeatData.motions?.red;
    return motion?.startOrientation ?? "in";
  });

  // Get current orientation index
  const currentIndex = $derived.by(() => {
    const index = orientations.indexOf(currentOrientation);
    return index >= 0 ? index : 0;
  });

  // Get motion type from motion data (for badge display)
  const motionType = $derived.by(() => {
    if (!currentBeatData) return "";

    const motion = color === "blue"
      ? currentBeatData.motions?.blue
      : currentBeatData.motions?.red;

    if (!motion || !motion.motionType) return "Static";

    // Format motion type for display
    const type = motion.motionType;
    return type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
  });

  // Handlers - cycle through orientations
  function handlePrevious() {
    hapticService?.trigger("selection");
    const prevIndex = currentIndex === 0 ? orientations.length - 1 : currentIndex - 1;
    const newOrientation = orientations[prevIndex];
    onOrientationChanged(color, newOrientation);
  }

  function handleNext() {
    hapticService?.trigger("selection");
    const nextIndex = (currentIndex + 1) % orientations.length;
    const newOrientation = orientations[nextIndex];
    onOrientationChanged(color, newOrientation);
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<div
  class="simplified-orientation-control"
  class:blue={color === "blue"}
  class:red={color === "red"}
  data-testid={`simplified-orientation-control-${color}`}
>
  <!-- Left column: Color label -->
  <div class="color-label">
    {displayLabel}
  </div>

  <!-- Center column: Stepper controls (perfectly centered) -->
  <div class="center-controls">
    <!-- Previous button (←) -->
    <button
      class="stepper-btn previous"
      onclick={handlePrevious}
      aria-label={`Previous ${displayLabel} orientation`}
      type="button"
    >
      <i class="fas fa-chevron-left"></i>
    </button>

    <!-- Orientation display -->
    <div class="orientation-display">
      {currentOrientation.toUpperCase()}
    </div>

    <!-- Next button (→) -->
    <button
      class="stepper-btn next"
      onclick={handleNext}
      aria-label={`Next ${displayLabel} orientation`}
      type="button"
    >
      <i class="fas fa-chevron-right"></i>
    </button>
  </div>

  <!-- Right column: Motion type badge -->
  {#if motionType}
    <div class="motion-badge">
      {motionType}
    </div>
  {:else}
    <div></div>
  {/if}
</div>

<style>
  .simplified-orientation-control {
    display: grid;
    /* Flexible grid - allows side columns to shrink below 50px if needed */
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 10px; /* Reduced from 12px for tighter spacing */
    padding: 10px 12px; /* Reduced from 12px 16px */
    border-radius: 12px;
    border: 3px solid;
    background: white;
    min-height: 64px;
    container-type: inline-size;
    /* Ensure grid respects container width */
    width: 100%;
    box-sizing: border-box;
  }

  /* Color theming */
  .simplified-orientation-control.blue {
    border-color: #3b82f6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, white 100%);
  }

  .simplified-orientation-control.red {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, white 100%);
  }

  /* Color label - left column, centered */
  .color-label {
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.5px;
    justify-self: center; /* Center within the left column */
  }

  .simplified-orientation-control.blue .color-label {
    color: #3b82f6;
  }

  .simplified-orientation-control.red .color-label {
    color: #ef4444;
  }

  /* Center controls container - perfectly centered */
  .center-controls {
    display: flex;
    align-items: center;
    gap: 8px; /* Reduced from 12px */
    justify-content: center;
    /* Allow shrinking to fit container */
    min-width: 0;
  }

  /* Stepper buttons - Reduced from 44x44px for better fit */
  .stepper-btn {
    width: 40px; /* Reduced from 44px */
    height: 40px;
    min-width: 40px;
    min-height: 40px;
    border-radius: 8px;
    border: 2px solid;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 14px; /* Reduced from 16px */
    flex-shrink: 0;
  }

  .simplified-orientation-control.blue .stepper-btn {
    border-color: #3b82f6;
    color: #3b82f6;
  }

  .simplified-orientation-control.red .stepper-btn {
    border-color: #ef4444;
    color: #ef4444;
  }

  .stepper-btn:hover {
    transform: scale(1.05);
  }

  .stepper-btn:active {
    transform: scale(0.95);
  }

  .simplified-orientation-control.blue .stepper-btn:active {
    background: rgba(59, 130, 246, 0.1);
  }

  .simplified-orientation-control.red .stepper-btn:active {
    background: rgba(239, 68, 68, 0.1);
  }

  /* Orientation display - sized for longest text "COUNTER" */
  .orientation-display {
    font-size: 14px; /* Reduced from 16px to fit better */
    font-weight: 700;
    color: #1a1a2e;
    min-width: 60px; /* Reduced from 80px */
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.2px; /* Reduced from 0.3px */
    white-space: nowrap;
    /* Allow shrinking if needed */
    flex-shrink: 1;
  }

  /* Motion type badge - right column, centered */
  .motion-badge {
    padding: 4px 8px; /* Reduced from 6px 12px */
    background: rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    font-size: 10px; /* Reduced from 12px */
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px; /* Reduced from 0.5px */
    color: #666;
    white-space: nowrap;
    min-width: 50px; /* Reduced from 60px */
    text-align: center;
    justify-self: center; /* Center within the right column */
  }

  /* Responsive adjustments for very narrow containers */
  @container (max-width: 300px) {
    .simplified-orientation-control {
      gap: 8px;
      padding: 10px 12px;
    }

    .color-label {
      font-size: 14px;
      min-width: 40px;
    }

    .orientation-display {
      font-size: 16px;
      min-width: 50px; /* Match turn control for perfect alignment */
    }

    .motion-badge {
      font-size: 10px;
      padding: 4px 8px;
    }
  }
</style>
