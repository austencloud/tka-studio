<!--
SimpleAdvancedToggle.svelte - Toggle between simple (3 positions) and advanced (16 variations) views
Modern segmented control matching the app's design system
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";

  const {
    isAdvanced = false,
    onToggle,
  } = $props<{
    isAdvanced?: boolean;
    onToggle?: (isAdvanced: boolean) => void;
  }>();

  // Resolve haptic feedback service
  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleToggle() {
    hapticService?.trigger("selection");
    onToggle?.(!isAdvanced);
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleToggle();
    }
  }
</script>

<div
  class="segmented-control"
  role="switch"
  aria-checked={isAdvanced}
  onclick={handleToggle}
  onkeydown={handleKeyDown}
  tabindex="0"
>
  <div class="slider" class:advanced={isAdvanced}></div>

  <div class="segment-button" class:active={!isAdvanced}>
    <span class="label">Simple</span>
  </div>

  <div class="segment-button" class:active={isAdvanced}>
    <span class="label">Advanced</span>
  </div>
</div>

<style>
  .segmented-control {
    display: inline-flex;
    align-items: center;
    position: relative;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 4px;
    cursor: pointer;
    user-select: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .segmented-control:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .segmented-control:active {
    transform: scale(0.98);
  }

  .segmented-control:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Slider background indicator */
  .slider {
    position: absolute;
    top: 4px;
    left: 4px;
    width: calc(50% - 4px);
    height: calc(100% - 8px);
    background: rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
    z-index: 0;
  }

  .slider.advanced {
    left: calc(50% + 4px);
  }

  /* Segment buttons */
  .segment-button {
    position: relative;
    z-index: 1;
    flex: 1;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
  }

  .segment-button .label {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    white-space: nowrap;
  }

  /* Active state styling */
  .segment-button.active .label {
    color: rgba(255, 255, 255, 0.95);
    font-weight: 600;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .segmented-control,
    .slider,
    .segment-button,
    .segment-button .label {
      transition: none;
    }

    .segmented-control:active {
      transform: none;
    }
  }

  /* Mobile responsive */
  @media (max-width: 480px) {
    .segmented-control {
      padding: 3px;
    }

    .segment-button {
      padding: 6px 12px;
    }

    .segment-button .label {
      font-size: 13px;
    }

    .slider {
      top: 3px;
      height: calc(100% - 6px);
    }
  }
</style>

