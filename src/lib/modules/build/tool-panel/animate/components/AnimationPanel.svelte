<!--
Animation Panel - Main Container

Refactored component focused on display and coordination.
Business logic extracted to services, state, and utilities.
-->
<script lang="ts">
  import type { ISequenceService } from "$build/shared";
  import { resolve, TYPES, type SequenceData } from "$shared";
  import { onMount } from "svelte";
  import type { IAnimationPlaybackController } from "../services/contracts";
  import { createAnimationPanelState } from "../state/animation-panel-state.svelte";
  import { loadSequenceForAnimation } from "../utils/sequence-loader";
  import AnimateControls from "./AnimateControls.svelte";
  import AnimatorCanvas from "./AnimatorCanvas.svelte";

  // Local panel state interface expected by this component
  type AnimationPanelState = {
    isAnimationVisible: boolean;
    isAnimationCollapsed: boolean;
    toggleAnimationCollapse: () => void;
    setAnimationVisible: (visible: boolean) => void;
  };

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  let {
    sequence = null,
    panelState,
    onClose = () => {},
    animationStateRef = $bindable(null),
  }: {
    sequence?: SequenceData | null;
    panelState: AnimationPanelState;
    onClose?: () => void;
    animationStateRef?: any | null; // Reference object to expose animation state/methods
  } = $props();

  // Services - resolved on mount to avoid SSR issues
  let sequenceService: ISequenceService | null = null;
  let playbackController: IAnimationPlaybackController | null = null;

  // Component state using our factory
  const state = createAnimationPanelState();

  // ✅ DERIVED RUNES: Panel state
  let isVisible = $derived(panelState.isAnimationVisible);
  let isCollapsed = $derived(panelState.isAnimationCollapsed);

  // ✅ DERIVED RUNE: Current letter from sequence data and current beat
  let currentLetter = $derived.by(() => {
    if (!state.sequenceData) {
      return null;
    }

    const currentBeat = state.currentBeat;

    // Before animation starts (beat 0 and not playing) = start position
    if (currentBeat === 0 && !state.isPlaying && state.sequenceData.startPosition) {
      return state.sequenceData.startPosition.letter || null;
    }

    // During animation or after: show beat letters
    // currentBeat goes from 0 to totalBeats
    // When currentBeat is 0.0-0.999... = show beats[0] (first beat)
    // When currentBeat is 1.0-1.999... = show beats[1] (second beat)
    // When currentBeat is 2.0-2.999... = show beats[2] (third beat)
    if (state.sequenceData.beats && state.sequenceData.beats.length > 0) {
      const beatIndex = Math.floor(currentBeat);
      const clampedIndex = Math.max(0, Math.min(beatIndex, state.sequenceData.beats.length - 1));

      return state.sequenceData.beats[clampedIndex]?.letter || null;
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
    } catch (error) {
      console.error("Failed to resolve animation services:", error);
      state.setError("Failed to initialize animation services");
    }
  });

  // Expose animation state and methods via ref
  $effect(() => {
    if (animationStateRef && playbackController) {
      animationStateRef.isPlaying = state.isPlaying;
      animationStateRef.currentBeat = state.currentBeat;
      animationStateRef.totalBeats = state.totalBeats;
      animationStateRef.speed = state.speed;
      animationStateRef.shouldLoop = state.shouldLoop;
      animationStateRef.play = () => playbackController?.togglePlayback();
      animationStateRef.stop = () => playbackController?.stop();
      animationStateRef.jumpToBeat = (beat: number) =>
        playbackController?.jumpToBeat(beat);
      animationStateRef.setSpeed = (speed: number) =>
        playbackController?.setSpeed(speed);
      animationStateRef.setShouldLoop = (loop: boolean) =>
        state.setShouldLoop(loop);
      animationStateRef.nextBeat = () => playbackController?.nextBeat();
      animationStateRef.previousBeat = () => playbackController?.previousBeat();
    }
  });

  // Load sequence data when sequence changes or becomes visible
  $effect(() => {
    if (sequence && isVisible && sequenceService && playbackController) {
      loadSequenceData();
    }
  });

  async function loadSequenceData() {
    if (!sequenceService || !playbackController) return;

    state.setLoading(true);
    state.setError(null);

    try {
      // Load sequence using our utility
      const result = await loadSequenceForAnimation(sequence, sequenceService);

      if (!result.success || !result.sequence) {
        throw new Error(result.error || "Failed to load sequence");
      }

      // Initialize playback controller with sequence and state
      const success = playbackController.initialize(result.sequence, state);

      if (!success) {
        throw new Error("Failed to initialize animation playback");
      }

      state.setSequenceData(result.sequence);
      console.log("✅ Animation panel ready for playback");
    } catch (err) {
      console.error("❌ Failed to load sequence:", err);
      state.setError(
        err instanceof Error ? err.message : "Failed to load sequence"
      );
    } finally {
      state.setLoading(false);
    }
  }

  // ✅ PANEL ACTIONS: Use panel state manager
  function handleToggle() {
    panelState.toggleAnimationCollapse();
  }

  function handleClose() {
    // Clean up playback controller
    if (playbackController) {
      playbackController.dispose();
    }

    panelState.setAnimationVisible(false);
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
</script>

<div
  class="animation-panel"
  class:collapsed={isCollapsed}
  class:visible={isVisible}
>
  <!-- Panel Content -->
  <div class="panel-content">
    {#if state.loading}
      <div class="loading-message">Loading animation...</div>
    {:else if state.error}
      <div class="error-message">{state.error}</div>
    {:else}
      <div class="animation-canvas-container">
        <AnimatorCanvas
          blueProp={state.bluePropState}
          redProp={state.redPropState}
          gridVisible={true}
          letter={currentLetter}
        />
      </div>

      <!-- Animation Controls -->
      <div class="controls-container">
        <AnimateControls
          isPlaying={state.isPlaying}
          currentBeat={state.currentBeat}
          totalBeats={state.totalBeats}
          speed={state.speed}
          shouldLoop={state.shouldLoop}
          onPlayPause={() => playbackController?.togglePlayback()}
          onSpeedChange={(speed) => playbackController?.setSpeed(speed)}
          onLoopToggle={() => state.setShouldLoop(!state.shouldLoop)}
        />
      </div>
    {/if}
  </div>
</div>

<style>
  .animation-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }

  .animation-panel.collapsed {
    /* Collapsed state - only show minimal header */
    overflow: visible;
    background: rgba(255, 255, 255, 0.02);
  }

  /* Panel Content */
  .panel-content {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.02) 0%,
      rgba(255, 255, 255, 0.01) 100%
    );
    /* Remove justify-content: center to allow natural flow */
    align-items: center;
    padding: 1rem;
    gap: 1rem;
    min-height: 0; /* Allow flex children to shrink */
  }

  .animation-canvas-container {
    /* Enable container queries for BOTH width and height */
    container-type: size;
    /* Take available space but allow controls to have their space */
    flex: 1;
    width: 100%;
    /* Don't set height: 100% - let it be constrained by flex and aspect-ratio */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 0; /* Allow shrinking */
  }

  .controls-container {
    /* Fixed height for controls - doesn't grow */
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
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

  /* Responsive design */
  @media (max-width: 768px) {
    /* Mobile-specific styles can be added here */
  }

  /* Custom scrollbar for panel content */
  .panel-content::-webkit-scrollbar {
    width: 8px;
  }

  .panel-content::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
  }

  .panel-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    border: 2px solid transparent;
    background-clip: content-box;
  }

  .panel-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
    background-clip: content-box;
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .animation-panel {
      border-left-color: rgba(255, 255, 255, 0.5);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .animation-panel {
      transition: none;
    }
  }
</style>
