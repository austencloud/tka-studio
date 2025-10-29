<!--
  InlineAnimatorPanel.svelte

  Minimalist inline animator panel that opens from Play button.
  - Slides up like edit panel (partial overlay)
  - Auto-starts animation on open
  - Only shows speed slider and pictograph
  - Loop is always enabled
-->
<script lang="ts">
  import AnimatorCanvas from "$build/animate/components/AnimatorCanvas.svelte";
  import type { IAnimationPlaybackController } from "$build/animate/services/contracts";
  import { createAnimationPanelState } from "$build/animate/state/animation-panel-state.svelte";
  import { loadSequenceForAnimation } from "$build/animate/utils/sequence-loader";
  import type { ISequenceService } from "$build/shared";
  import { BottomSheet, resolve, TYPES, type SequenceData } from "$shared";
  import type { IHapticFeedbackService } from "$shared/application/services/contracts";
  import { onMount } from "svelte";

  // Props
  let {
    sequence = null,
    show = false,
    onClose = () => {},
    toolPanelHeight = 0,
  }: {
    sequence?: SequenceData | null;
    show?: boolean;
    onClose?: () => void;
    toolPanelHeight?: number;
  } = $props();

  // Services
  let sequenceService: ISequenceService | null = null;
  let playbackController: IAnimationPlaybackController | null = null;
  let hapticService: IHapticFeedbackService | null = null;

  // Component state
  const panelState = createAnimationPanelState();

  // Dynamically measured navigation bar height
  let bottomNavHeight = $state(0);

  // Measure navigation bar height proactively on mount, so it's ready when panel opens
  onMount(() => {
    const measureNavHeight = () => {
      const bottomNav = document.querySelector('.bottom-navigation');
      if (bottomNav) {
        bottomNavHeight = bottomNav.clientHeight;
      }
    };

    // Initial measure
    measureNavHeight();

    // Measure again after a brief delay to ensure DOM is fully rendered
    const timeout = setTimeout(measureNavHeight, 50);

    // Re-measure on window resize
    const handleResize = () => measureNavHeight();
    window.addEventListener('resize', handleResize);

    return () => {
      clearTimeout(timeout);
      window.removeEventListener('resize', handleResize);
    };
  });

  // Calculate panel height dynamically - match tool panel height exactly
  const panelHeightStyle = $derived(() => {
    // Use tool panel height directly - no additional offsets needed
    // The panel will slide up to match the tool panel's visual space
    if (toolPanelHeight > 0) {
      return `height: ${toolPanelHeight}px;`;
    }

    return 'height: 70vh;';
  });

  // Derived: Current letter from sequence data
  let currentLetter = $derived.by(() => {
    if (!panelState.sequenceData) return null;

    const currentBeat = panelState.currentBeat;

    // Before animation starts (beat 0 and not playing) = start position
    if (currentBeat === 0 && !panelState.isPlaying && panelState.sequenceData.startPosition) {
      return panelState.sequenceData.startPosition.letter || null;
    }

    // During animation: show beat letters
    if (panelState.sequenceData.beats && panelState.sequenceData.beats.length > 0) {
      const beatIndex = Math.floor(currentBeat);
      const clampedIndex = Math.max(0, Math.min(beatIndex, panelState.sequenceData.beats.length - 1));
      return panelState.sequenceData.beats[clampedIndex]?.letter || null;
    }

    return null;
  });

  // Resolve services on mount
  onMount(() => {
    try {
      sequenceService = resolve<ISequenceService>(TYPES.ISequenceService);
      playbackController = resolve<IAnimationPlaybackController>(
        TYPES.IAnimationPlaybackController
      );
      hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    } catch (error) {
      console.error("Failed to resolve animation services:", error);
      panelState.setError("Failed to initialize animation services");
    }
  });

  // Load and auto-start animation when panel becomes visible
  // CRITICAL: Delay to allow slide animation to complete first
  $effect(() => {
    if (show && sequence && sequenceService && playbackController) {
      // Show loading state immediately
      panelState.setLoading(true);
      panelState.setError(null);

      // Wait for BottomSheet slide animation to complete (300ms) before loading
      const loadTimeout = setTimeout(() => {
        loadAndStartAnimation();
      }, 320); // Slightly longer than BottomSheet transition (300ms)

      return () => clearTimeout(loadTimeout);
    }
  });

  async function loadAndStartAnimation() {
    if (!sequenceService || !playbackController) return;

    panelState.setLoading(true);
    panelState.setError(null);

    try {
      // Load sequence
      const result = await loadSequenceForAnimation(sequence, sequenceService);

      if (!result.success || !result.sequence) {
        throw new Error(result.error || "Failed to load sequence");
      }

      // Initialize playback controller with sequence and panelState
      // Enable loop by default
      panelState.setShouldLoop(true);
      const success = playbackController.initialize(result.sequence, panelState);

      if (!success) {
        throw new Error("Failed to initialize animation playback");
      }

      panelState.setSequenceData(result.sequence);

      // Auto-start animation after a brief delay
      setTimeout(() => {
        playbackController?.togglePlayback();
      }, 100);

    } catch (err) {
      console.error("❌ Failed to load sequence:", err);
      panelState.setError(
        err instanceof Error ? err.message : "Failed to load sequence"
      );
    } finally {
      panelState.setLoading(false);
    }
  }

  // Speed change handler
  function handleSpeedChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newSpeed = parseFloat(target.value);
    hapticService?.trigger("selection");
    playbackController?.setSpeed(newSpeed);
  }

  // Close handler
  function handleClose() {
    hapticService?.trigger("selection");

    // Stop playback
    if (playbackController) {
      playbackController.dispose();
    }

    onClose();
  }

  // Cleanup on component destroy
  $effect(() => {
    return () => {
      if (playbackController) {
        playbackController.dispose();
      }
    };
  });

  function handleSheetClose() {
    handleClose();
  }
</script>

<BottomSheet
  isOpen={show}
  on:close={handleSheetClose}
  labelledBy="inline-animator-title"
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  showHandle={false}
  class="inline-animator-container glass-surface"
  backdropClass="inline-animator-backdrop"
>
  <div
    class="inline-animator-panel"
    style={panelHeightStyle()}
    role="dialog"
    aria-labelledby="inline-animator-title"
  >
    <button class="close-button" onclick={handleClose} aria-label="Close animator">
      <i class="fas fa-times"></i>
    </button>

    <h2 id="inline-animator-title" class="sr-only">Inline Animator</h2>

    {#if panelState.loading}
      <div class="loading-message">Loading animation...</div>
    {:else if panelState.error}
      <div class="error-message">{panelState.error}</div>
    {:else}
      <div class="canvas-container">
        <AnimatorCanvas
          blueProp={panelState.bluePropState}
          redProp={panelState.redPropState}
          gridVisible={true}
          letter={currentLetter}
        />
      </div>

      <div class="speed-control-container">
        <div class="speed-control">
          <label for="inline-speed-slider" class="speed-label">Speed</label>
          <input
            id="inline-speed-slider"
            type="range"
            min="0.25"
            max="2"
            step="0.25"
            value={panelState.speed}
            oninput={handleSpeedChange}
            aria-label="Animation speed"
          />
          <span class="speed-value">{panelState.speed.toFixed(2)}x</span>
        </div>
      </div>
    {/if}
  </div>
</BottomSheet>

<style>
  :global(.bottom-sheet-backdrop.inline-animator-backdrop) {
    background: transparent;
    backdrop-filter: none !important;
    pointer-events: none;
  }

  :global(.bottom-sheet.inline-animator-container) {
    background-size: 300% 300%;
    animation: meshGradientFlow 15s ease infinite;
    backdrop-filter: var(--glass-backdrop-strong);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    display: flex;
    flex-direction: column;
    min-height: 300px;
    pointer-events: auto;
  }

  :global(.bottom-sheet.inline-animator-container:hover) {
    background-size: 300% 300%;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: none;
  }

  .inline-animator-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    padding: 24px;
    padding-top: 56px; /* Extra padding at top for close button */
    padding-bottom: calc(24px + env(safe-area-inset-bottom));
    /* height set via inline style for reactive sizing */
    width: 100%;
    transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth height transitions */
  }

  /* Mesh Gradient Flow Animation - Subtle organic color movement */
  @keyframes meshGradientFlow {
    0%, 100% {
      background-position: 0% 50%;
    }
    25% {
      background-position: 50% 100%;
    }
    50% {
      background-position: 100% 50%;
    }
    75% {
      background-position: 50% 0%;
    }
  }

  .close-button {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 48px; /* Slightly larger for better visibility */
    height: 48px;
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15); /* More visible */
    backdrop-filter: blur(10px);
    color: rgba(255, 255, 255, 1); /* Full white for contrast */
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px; /* Larger icon */
    z-index: 1000; /* Much higher z-index to ensure it's always on top */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); /* Shadow for visibility */
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .canvas-container {
    /* CRITICAL: Enable container queries for AnimatorCanvas */
    container-type: size;
    container-name: animator-canvas;
    flex: 1;
    width: 100%;
    max-width: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
  }

  .speed-control-container {
    width: 100%;
    max-width: 400px;
    display: flex;
    justify-content: center;
    flex-shrink: 0;
  }

  .speed-control {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    width: 100%;
  }

  .speed-label {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }

  #inline-speed-slider {
    flex: 1;
    height: 6px;
    -webkit-appearance: none;
    appearance: none;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    outline: none;
    min-width: 80px;
  }

  #inline-speed-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease;
  }

  #inline-speed-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.5);
  }

  #inline-speed-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease;
  }

  #inline-speed-slider::-moz-range-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.5);
  }

  .speed-value {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    min-width: 45px;
    text-align: right;
  }

  .loading-message,
  .error-message {
    padding: 2rem;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }

  .error-message {
    color: rgba(255, 100, 100, 0.9);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .inline-animator-panel {
      padding: 16px;
      padding-top: 56px; /* Keep space for close button */
      padding-bottom: calc(16px + env(safe-area-inset-bottom));
      gap: 12px;
    }

    .speed-control {
      padding: 10px 14px;
      gap: 10px;
    }

    .speed-label {
      font-size: 11px;
    }

    .speed-value {
      font-size: 12px;
      min-width: 42px;
    }
  }

  @media (max-width: 480px) {
    .inline-animator-panel {
      padding: 12px;
      padding-top: 48px; /* Keep space for close button */
      padding-bottom: calc(12px + env(safe-area-inset-bottom));
      gap: 8px;
    }

    .close-button {
      top: 12px;
      right: 12px;
      width: 44px; /* Keep it large enough to tap easily */
      height: 44px;
      font-size: 18px;
    }

    .speed-control {
      padding: 8px 12px;
      gap: 8px;
    }

    .speed-label {
      font-size: 10px;
    }

    .speed-value {
      font-size: 11px;
      min-width: 40px;
    }

    #inline-speed-slider {
      min-width: 60px;
    }
  }

  /* Very narrow viewports */
  @media (max-width: 400px) {
    .speed-control {
      padding: 6px 10px;
      gap: 6px;
    }

    .speed-label {
      display: none; /* Hide label to save space */
    }

    .speed-value {
      font-size: 10px;
      min-width: 35px;
    }

    #inline-speed-slider {
      min-width: 50px;
    }
  }

  /* Landscape mobile: Adjust spacing */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .inline-animator-panel {
      /* Height still calculated dynamically */
      padding: 12px;
      padding-top: 48px; /* Keep space for close button */
      gap: 8px;
    }

    .canvas-container {
      max-width: 500px;
    }

    .speed-control-container {
      max-width: 350px;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    :global(.inline-animator-container) {
      background: rgba(0, 0, 0, 0.95);
      border-top: 2px solid white;
    }

    .speed-control {
      background: rgba(255, 255, 255, 0.15);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }
  }

  /* Reduced motion - disable gradient animation but keep static gradient */
  @media (prefers-reduced-motion: reduce) {
    .inline-animator-panel {
      animation: none;
      background-position: 0% 50%;
    }

    .close-button,
    #inline-speed-slider::-webkit-slider-thumb,
    #inline-speed-slider::-moz-range-thumb {
      transition: none;
    }

    .close-button:hover,
    .close-button:active,
    #inline-speed-slider::-webkit-slider-thumb:hover,
    #inline-speed-slider::-moz-range-thumb:hover {
      transform: none;
    }
  }
</style>
