<!--
Animator Tab - Sequence animation and visualization

Provides animation controls and visualization for sequences:
- Animation playback controls
- Beat-by-beat visualization
- Motion parameter adjustment
- Prop interpolation
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared/inversify/container";
  import { onDestroy, onMount } from "svelte";
// TEMPORARY: All service resolution commented out until container is restored


  // Import animation components
  import type { IAnimationControlService, IMotionParameterService, ISequenceAnimationEngine } from "../services";

  // ============================================================================
  // SERVICE RESOLUTION - TEMPORARY DISABLED
  // ============================================================================

  // TEMPORARY: All service resolution commented out until container is restored
  const animationControlService = resolve(TYPES.IAnimationControlService) as IAnimationControlService;
  const motionParameterService = resolve(TYPES.IMotionParameterService) as IMotionParameterService;
  const animationEngine = resolve(TYPES.ISequenceAnimationEngine) as ISequenceAnimationEngine;

  // ============================================================================
  // COMPONENT STATE - TEMPORARY PLACEHOLDERS
  // ============================================================================

  let isPlaying = $state(false);
  let currentBeat = $state(0);
  let totalBeats = $state(8);
  let animationSpeed = $state(1.0);
  let error = $state<string | null>(null);

  // ============================================================================
  // EVENT HANDLERS - TEMPORARY DISABLED
  // ============================================================================

  function handlePlay() {
    isPlaying = true;
    console.log("✅ AnimatorTab: Play (services disabled)");
    // animationControlService.play();
  }

  function handlePause() {
    isPlaying = false;
    console.log("✅ AnimatorTab: Pause (services disabled)");
    // animationControlService.pause();
  }

  function handleStop() {
    isPlaying = false;
    currentBeat = 0;
    console.log("✅ AnimatorTab: Stop (services disabled)");
    // animationControlService.stop();
  }

  function handleBeatChange(beat: number) {
    currentBeat = beat;
    console.log("✅ AnimatorTab: Beat changed (services disabled):", beat);
    // animationControlService.seekToBeat(beat);
  }

  function handleSpeedChange(speed: number) {
    animationSpeed = speed;
    console.log("✅ AnimatorTab: Speed changed (services disabled):", speed);
    // animationControlService.setSpeed(speed);
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
    console.log("✅ AnimatorTab: Mounted (services temporarily disabled)");

    // TEMPORARY: All initialization commented out
    try {
      // Initialize animation engine with default sequence
      // Note: Using initializeWithDomainData instead of initialize
      // await animationEngine.initializeWithDomainData(defaultSequence);

      // Load default sequence for animation (method doesn't exist)
      // await animationEngine.loadSequence(defaultSequence);

      console.log("✅ AnimatorTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ AnimatorTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize animator";
    }
  });

  onDestroy(() => {
    console.log("✅ AnimatorTab: Cleanup (services disabled)");
    // animationControlService?.cleanup();
    // animationEngine?.cleanup();
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="animator-tab" data-testid="animator-tab">
  <!-- Error display -->
  {#if error}
    <div class="error-banner">
      <span>{error}</span>
      <button onclick={() => (error = null)}>×</button>
    </div>
  {/if}

  <div class="animator-layout">
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>🎬 Animator Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Sequence animation playback</li>
          <li>✅ Beat-by-beat visualization</li>
          <li>✅ Motion parameter controls</li>
          <li>✅ Prop interpolation</li>
          <li>✅ Animation speed control</li>
          <li>✅ Canvas-based rendering</li>
        </ul>
      </div>

      <!-- Placeholder controls -->
      <div class="placeholder-controls">
        <h3>Animation Controls (placeholder):</h3>
        <div class="control-buttons">
          <button onclick={handlePlay} disabled={isPlaying}>Play</button>
          <button onclick={handlePause} disabled={!isPlaying}>Pause</button>
          <button onclick={handleStop}>Stop</button>
        </div>
        <div class="beat-info">
          <span>Beat: {currentBeat} / {totalBeats}</span>
          <span>Speed: {animationSpeed}x</span>
        </div>
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
    <!-- Top Panel: Animation Controls -->
    <!-- <div class="controls-panel">
      <AnimationControls
        {isPlaying}
        {currentBeat}
        {totalBeats}
        {animationSpeed}
        onPlay={handlePlay}
        onPause={handlePause}
        onStop={handleStop}
        onBeatChange={handleBeatChange}
        onSpeedChange={handleSpeedChange}
      />
    </div> -->

    <!-- Main Panel: Canvas and Info -->
    <!-- <div class="main-panel">
      <div class="canvas-container">
        <AnimatorCanvas
          {currentBeat}
          {isPlaying}
        />
      </div>
      
      <div class="info-panel">
        <SequenceInfo />
        <AnimationPanel />
      </div>
    </div> -->
  </div>
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .animator-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .animator-layout {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Original layout: */
    /* flex-direction: column;
    overflow: hidden; */
  }

  .error-banner {
    background: var(--color-error, #ff4444);
    color: white;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .error-banner button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
  }

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  .placeholder-controls {
    margin-top: 1.5rem;
    padding: 1rem;
    background: var(--color-surface, #fff);
    border-radius: 4px;
    border: 1px solid var(--color-border, #ddd);
  }

  .placeholder-controls h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .control-buttons {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    justify-content: center;
  }

  .control-buttons button {
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    border-radius: 4px;
    cursor: pointer;
  }

  .control-buttons button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .control-buttons button:hover:not(:disabled) {
    background: var(--color-surface-hover, #f0f0f0);
  }

  .beat-info {
    display: flex;
    gap: 1rem;
    justify-content: center;
    color: var(--color-text-secondary, #666);
    font-size: 0.9rem;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }

    .control-buttons {
      flex-direction: column;
      align-items: center;
    }

    .beat-info {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
</style>
