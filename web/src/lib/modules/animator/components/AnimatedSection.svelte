<!--
AnimatedSection.svelte - Refactored animated pictograph section

Composed of smaller, focused components following SRP:
- AnimatedPictographDisplay: Renders pictograph or error state
- AnimationStatusIndicator: Shows playing state and progress
- AnimationPlaybackControls: Play/pause/reset buttons
- AnimationProgressSlider: Progress scrubbing
- KeyboardShortcutHandler: Keyboard shortcuts and hints

This is the right 1/3 section of the animator layout.
-->
<script lang="ts">
  import type { AnimatorState } from "../state";

  // Import focused components - all in same directory
  import AnimationPlaybackControls from "./AnimationPlaybackControls.svelte";
  import AnimationProgressSlider from "./AnimationProgressSlider.svelte";
  import AnimationStatusIndicator from "./AnimationStatusIndicator.svelte";
  import KeyboardShortcutHandler from "./KeyboardShortcutHandler.svelte";

  interface Props {
    motionState: AnimatorState;
  }

  let { motionState }: Props = $props();

  // Animation section simplified - no pictograph data loading needed

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

  <!-- Animation Placeholder - Pictograph removed for debugging -->
  <div class="pictograph-container">
    <div style="color: rgba(255,255,255,0.5); text-align: center;">
      <p>🎬 Animation Section</p>
      <p>(Pictograph removed for debugging)</p>
    </div>
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
