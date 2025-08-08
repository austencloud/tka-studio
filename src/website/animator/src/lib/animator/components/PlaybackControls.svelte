<script lang="ts">
  import { animationActions, isPlaying, speed } from '../stores/animation.js';

  let speedValue = $state(1.0);

  // Sync speed with store
  $effect(() => {
    speedValue = $speed;
  });

  function togglePlayPause() {
    if ($isPlaying) {
      animationActions.pause();
    } else {
      animationActions.play();
    }
  }

  function handleSpeedChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newSpeed = parseFloat(target.value);
    speedValue = newSpeed;
    animationActions.setSpeed(newSpeed);
  }
</script>

<div class="playback-controls">
  <div class="control-group">
    <button
      class="control-btn reset-btn"
      onclick={animationActions.reset}
      title="Reset to beginning"
    >
      ↻
    </button>

    <button
      class="control-btn play-pause-btn"
      class:playing={$isPlaying}
      onclick={togglePlayPause}
      title={$isPlaying ? 'Pause' : 'Play'}
    >
      {#if $isPlaying}
        ⏸
      {:else}
        ▶
      {/if}
    </button>
  </div>

  <div class="control-group">
    <label for="speed-slider">Speed:</label>
    <input
      id="speed-slider"
      type="range"
      min="0.1"
      max="3"
      step="0.1"
      value={speedValue}
      oninput={handleSpeedChange}
    />
    <span class="speed-value">{speedValue.toFixed(1)}x</span>
  </div>
</div>

<style>
  .playback-controls {
    display: flex;
    gap: 2rem;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
  }

  .control-group {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .control-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    background: #ffffff;
    color: #374151;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .control-btn:hover {
    background: #f3f4f6;
    border-color: #9ca3af;
  }

  .play-pause-btn.playing {
    background: #10b981;
    color: white;
    border-color: #059669;
  }

  .play-pause-btn.playing:hover {
    background: #059669;
  }

  #speed-slider {
    width: 6rem;
    accent-color: #3b82f6;
  }

  .speed-value {
    font-weight: 600;
    font-family: monospace;
    min-width: 3rem;
    text-align: center;
  }

  label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #4b5563;
  }
</style>
