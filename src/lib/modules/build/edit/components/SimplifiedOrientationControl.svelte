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
    grid-template-columns: minmax(50px, 1fr) auto minmax(50px, 1fr);
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 12px;
    border: 3px solid;
    background: white;
    min-height: 64px;
    container-type: inline-size;
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

  /* Color label - left column */
  .color-label {
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.5px;
    justify-self: start;
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
    gap: 12px;
    justify-content: center;
  }

  /* Stepper buttons - 44x44px minimum touch target */
  .stepper-btn {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 8px;
    border: 2px solid;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 16px;
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

  /* Orientation display */
  .orientation-display {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    min-width: 60px; /* Match turn control value display for perfect alignment */
    text-align: center;
    flex-shrink: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Motion type badge - right column */
  .motion-badge {
    padding: 6px 12px;
    background: rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #666;
    white-space: nowrap;
    min-width: 60px; /* Fixed width to prevent layout shifts when motion type changes */
    text-align: center;
    justify-self: end;
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
