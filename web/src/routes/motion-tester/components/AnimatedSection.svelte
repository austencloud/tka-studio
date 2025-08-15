<!--
AnimatedSection.svelte - Refactored animated pictograph section

Composed of smaller, focused components following SRP:
- AnimatedPictographDisplay: Renders pictograph or error state
- AnimationStatusIndicator: Shows playing state and progress
- AnimationPlaybackControls: Play/pause/reset buttons
- AnimationProgressSlider: Progress scrubbing
- KeyboardShortcutHandler: Keyboard shortcuts and hints

This is the right 1/3 section of the motion tester layout.
-->
<script lang="ts">
  import type { MotionTesterState } from "../state/motion-tester-state.svelte";
  import { resolve } from "$lib/services/bootstrap";
  import { IAnimatedPictographDataServiceInterface } from "$lib/services/di/interfaces/motion-tester-interfaces";
  import type { PictographData } from "$lib/domain";

  // Import focused components
  import AnimatedPictographDisplay from "./display/AnimatedPictographDisplay.svelte";
  import AnimationStatusIndicator from "./animation/AnimationStatusIndicator.svelte";
  import AnimationPlaybackControls from "./controls/AnimationPlaybackControls.svelte";
  import AnimationProgressSlider from "./controls/AnimationProgressSlider.svelte";
  import KeyboardShortcutHandler from "./controls/KeyboardShortcutHandler.svelte";

  interface Props {
    motionState: MotionTesterState;
  }

  let { motionState }: Props = $props();

  // Fixed size for consistent layout
  const PICTOGRAPH_SIZE = 280;

  // Resolve service from DI container
  const pictographDataService = resolve(
    IAnimatedPictographDataServiceInterface
  );

  // Create pictograph data using service (async)
  let pictographData = $state<PictographData | null>(null);
  let isLoadingPictograph = $state(false);

  // Effect to load pictograph data when motion state changes
  $effect(() => {
    // Explicitly access nested motion state properties to establish dependency tracking
    // These variables are intentionally "unused" - they establish reactive dependencies
    const blueStartLoc = motionState.blueMotionParams.startLoc;
    const blueEndLoc = motionState.blueMotionParams.endLoc;
    const blueMotionType = motionState.blueMotionParams.motionType;
    const blueTurns = motionState.blueMotionParams.turns;

    const redStartLoc = motionState.redMotionParams.startLoc;
    const redEndLoc = motionState.redMotionParams.endLoc;
    const redMotionType = motionState.redMotionParams.motionType;
    const redTurns = motionState.redMotionParams.turns;

    const gridType = motionState.gridType;

    // Trigger async load when motion state changes
    loadPictographData();
  });

  async function loadPictographData() {
    isLoadingPictograph = true;
    try {
      const data =
        await pictographDataService.createAnimatedPictographData(motionState);
      pictographData = data;
    } catch (error) {
      console.error("❌ Error loading pictograph data:", error);
      pictographData = null;
    } finally {
      isLoadingPictograph = false;
    }
  }

  // Event handlers - delegate to motion state
  function handlePlayToggle() {
    if (motionState.animationState.isPlaying) {
      motionState.stopAnimation();
    } else {
      motionState.startAnimation();
    }
  }

  function handleReset() {
    motionState.resetAnimation();
  }

  function handleProgressChange(progress: number) {
    motionState.setProgress(progress);
  }
</script>

<div class="animated-section-simplified">
  <!-- Keyboard shortcut handler (invisible, provides keyboard support) -->
  <KeyboardShortcutHandler
    onPlayToggle={handlePlayToggle}
    onReset={handleReset}
  />

  <!-- Animated Pictograph Display -->
  <div class="pictograph-container">
    <AnimatedPictographDisplay {pictographData} size={PICTOGRAPH_SIZE} />
  </div>

  <!-- Animation Controls -->
  <div class="animation-controls">
    <!-- Status Indicator -->
    <AnimationStatusIndicator
      isPlaying={motionState.animationState.isPlaying}
      progress={motionState.animationState.progress}
    />

    <!-- Playback Controls -->
    <AnimationPlaybackControls
      isPlaying={motionState.animationState.isPlaying}
      isEngineInitialized={motionState.isEngineInitialized}
      onPlayToggle={handlePlayToggle}
      onReset={handleReset}
    />

    <!-- Progress Control -->
    <AnimationProgressSlider
      progress={motionState.animationState.progress}
      isEngineInitialized={motionState.isEngineInitialized}
      onProgressChange={handleProgressChange}
    />
  </div>
</div>

<style>
  .animated-section-simplified {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.03),
      rgba(16, 185, 129, 0.03)
    );
    border-radius: 8px;
    overflow: hidden;
  }

  .pictograph-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    min-height: 300px;
  }

  .animation-controls {
    background: rgba(0, 0, 0, 0.1);
    padding: 16px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .pictograph-container {
      padding: 15px;
      min-height: 250px;
    }

    .animation-controls {
      padding: 12px;
    }
  }
</style>
