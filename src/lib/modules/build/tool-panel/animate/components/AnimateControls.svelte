<!--
AnimateControls.svelte

Context-aware button panel for the Animate tab.
Provides animation playback controls (play/pause, navigation, speed, fullscreen).
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props interface
  const {
    // Animation state
    isPlaying = false,
    currentBeat = 0,
    totalBeats = 0,
    speed = 1.0,
    shouldLoop = false,

    // Event handlers
    onPlayPause,
    onPrevious,
    onNext,
    onSpeedChange,
    onLoopToggle,

    // Panel visibility
    visible = true
  }: {
    // Animation state
    isPlaying?: boolean;
    currentBeat?: number;
    totalBeats?: number;
    speed?: number;
    shouldLoop?: boolean;

    // Event handlers
    onPlayPause?: () => void;
    onPrevious?: () => void;
    onNext?: () => void;
    onSpeedChange?: (speed: number) => void;
    onLoopToggle?: () => void;

    // Panel visibility
    visible?: boolean;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Button handlers
  function handlePlayPause() {
    hapticService?.trigger("selection");
    onPlayPause?.();
  }

  function handlePrevious() {
    hapticService?.trigger("selection");
    onPrevious?.();
  }

  function handleNext() {
    hapticService?.trigger("selection");
    onNext?.();
  }

  function handleSpeedInput(event: Event) {
    const target = event.target as HTMLInputElement;
    const newSpeed = parseFloat(target.value);
    hapticService?.trigger("selection");
    onSpeedChange?.(newSpeed);
  }

  function handleLoopToggle() {
    hapticService?.trigger("selection");
    onLoopToggle?.();
  }
</script>

{#if visible}
  <div class="animate-controls horizontal">
    <!-- Play/Pause Button -->
    <button
      class="panel-button play-pause-button"
      onclick={handlePlayPause}
      aria-label={isPlaying ? "Pause animation" : "Play animation"}
      title={isPlaying ? "Pause" : "Play"}
    >
      {#if isPlaying}
        <i class="fa-solid fa-pause" aria-hidden="true"></i>
      {:else}
        <i class="fa-solid fa-play" aria-hidden="true"></i>
      {/if}
    </button>

    <!-- Loop Toggle Button -->
    <button
      class="panel-button loop-button"
      class:active={shouldLoop}
      onclick={handleLoopToggle}
      aria-label={shouldLoop ? "Disable loop" : "Enable loop"}
      title={shouldLoop ? "Loop: On" : "Loop: Off"}
    >
      <i class="fa-solid fa-repeat" aria-hidden="true"></i>
    </button>

    <!-- Speed Control -->
    <div class="speed-control">
      <label for="speed-slider" class="speed-label">Speed</label>
      <input
        id="speed-slider"
        type="range"
        min="0.25"
        max="2"
        step="0.25"
        value={speed}
        oninput={handleSpeedInput}
        aria-label="Animation speed"
      />
      <span class="speed-value">{speed.toFixed(2)}x</span>
    </div>
  </div>
{/if}

<style>
  .animate-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(12px);
    z-index: 10;
    /* Prevent overflow beyond parent container */
    max-width: 100%;
    box-sizing: border-box;
    /* Handle overflow gracefully */
    overflow: hidden;
  }

  /* Horizontal orientation */
  .animate-controls.horizontal {
    flex-direction: row;
    gap: 16px;
    border-radius: 24px;
  }

  .panel-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 18px;
    color: #ffffff;

    /* Base button styling */
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .panel-button:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .panel-button:active:not(:disabled) {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .panel-button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .panel-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Play/Pause button styling */
  .play-pause-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .play-pause-button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.6);
  }

  /* Loop button styling */
  .loop-button {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .loop-button.active {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-color: rgba(16, 185, 129, 0.3);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  .loop-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .loop-button.active:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.6);
  }

  /* Speed control */
  .speed-control {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    min-width: 180px;
  }

  .speed-label {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  #speed-slider {
    flex: 1;
    height: 4px;
    -webkit-appearance: none;
    appearance: none;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    outline: none;
  }

  #speed-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
  }

  #speed-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 6px rgba(59, 130, 246, 0.4);
  }

  #speed-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
  }

  #speed-slider::-moz-range-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 6px rgba(59, 130, 246, 0.4);
  }

  .speed-value {
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
    min-width: 45px;
    text-align: right;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .animate-controls.horizontal {
      gap: 12px;
    }

    .panel-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }

    .speed-control {
      min-width: 140px;
      padding: 6px 12px;
    }

    .speed-label {
      font-size: 11px;
    }

    .speed-value {
      font-size: 12px;
      min-width: 40px;
    }
  }

  @media (max-width: 480px) {
    .animate-controls.horizontal {
      gap: 8px;
    }

    .panel-button {
      width: 40px;
      height: 40px;
      font-size: 14px;
    }

    .speed-control {
      min-width: 120px;
      padding: 4px 10px;
    }

    .speed-label {
      display: none; /* Hide label on very small screens */
    }

    .speed-value {
      font-size: 11px;
      min-width: 35px;
    }
  }

  /* Very narrow landscape viewports (Z Fold landscape, etc.) */
  @media (max-width: 400px) {
    .animate-controls.horizontal {
      gap: 6px;
    }

    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 12px;
    }

    .speed-control {
      min-width: 100px;
      padding: 3px 8px;
    }

    .speed-value {
      font-size: 10px;
      min-width: 30px;
    }
  }

  /* Extremely narrow viewports - hide speed control to prioritize core buttons */
  @media (max-width: 320px) {
    .animate-controls.horizontal {
      gap: 4px;
    }

    .panel-button {
      width: 32px;
      height: 32px;
      font-size: 11px;
    }

    .speed-control {
      display: none; /* Hide speed control when space is extremely limited */
    }
  }

  /* Ultra-narrow viewports - minimal viable layout */
  @media (max-width: 280px) {
    .animate-controls.horizontal {
      gap: 3px;
    }

    .panel-button {
      width: 28px;
      height: 28px;
      font-size: 10px;
    }
  }
</style>
