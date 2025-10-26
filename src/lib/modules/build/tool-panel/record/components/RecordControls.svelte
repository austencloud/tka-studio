<!--
RecordControls.svelte

Playback controls for the Record tab.
Provides play/pause, speed adjustment (BPM), reset, and metronome toggle.
-->
<script lang="ts">
  // Props
  const {
    isPlaying = false,
    bpm = 60,
    minBpm = 30,
    maxBpm = 180,
    isMetronomeEnabled = true,
    onPlayPause,
    onSpeedChange,
    onReset,
    onMetronomeToggle,
  }: {
    isPlaying?: boolean;
    bpm?: number;
    minBpm?: number;
    maxBpm?: number;
    isMetronomeEnabled?: boolean;
    onPlayPause: () => void;
    onSpeedChange: (bpm: number) => void;
    onReset: () => void;
    onMetronomeToggle: (enabled: boolean) => void;
  } = $props();

  // Local state for slider interaction
  let localBpm = $state(bpm);

  // Sync local BPM with prop changes
  $effect(() => {
    localBpm = bpm;
  });

  function handleBpmChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newBpm = parseInt(target.value, 10);
    localBpm = newBpm;
    onSpeedChange(newBpm);
  }

  function incrementBpm(delta: number) {
    const newBpm = Math.max(minBpm, Math.min(maxBpm, localBpm + delta));
    localBpm = newBpm;
    onSpeedChange(newBpm);
  }
</script>

<div class="record-controls">
  <!-- Main playback controls -->
  <div class="main-controls">
    <button
      class="control-button play-pause-button"
      class:playing={isPlaying}
      onclick={onPlayPause}
      title={isPlaying ? "Pause" : "Play"}
    >
      {#if isPlaying}
        <span class="icon">⏸️</span>
      {:else}
        <span class="icon">▶️</span>
      {/if}
      <span class="label">{isPlaying ? "Pause" : "Play"}</span>
    </button>

    <button
      class="control-button reset-button"
      onclick={onReset}
      title="Reset to beginning"
    >
      <span class="icon">⏮️</span>
      <span class="label">Reset</span>
    </button>
  </div>

  <!-- Speed control -->
  <div class="speed-control">
    <div class="speed-label">
      <span class="label-text">Speed (BPM)</span>
      <div class="speed-display">{localBpm}</div>
    </div>

    <div class="speed-slider-container">
      <button
        class="bpm-adjust-button"
        onclick={() => incrementBpm(-10)}
        title="Decrease by 10 BPM"
      >
        −
      </button>

      <input
        type="range"
        class="speed-slider"
        min={minBpm}
        max={maxBpm}
        value={localBpm}
        oninput={handleBpmChange}
        step="5"
      />

      <button
        class="bpm-adjust-button"
        onclick={() => incrementBpm(10)}
        title="Increase by 10 BPM"
      >
        +
      </button>
    </div>


  </div>

  <!-- Metronome toggle -->
  <div class="metronome-control">
    <label class="metronome-toggle">
      <input
        type="checkbox"
        checked={isMetronomeEnabled}
        onchange={(e) =>
          onMetronomeToggle((e.target as HTMLInputElement).checked)}
      />
      <span class="toggle-icon">{isMetronomeEnabled ? "🔊" : "🔇"}</span>
      <span class="toggle-label">Metronome</span>
    </label>
  </div>
</div>

<style>
  .record-controls {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs, --spacing-xs);
    padding: var(--spacing-xs, --spacing-xs);
    background: var(--surface-glass, rgba(0, 0, 0, 0.5));
    backdrop-filter: blur(10px);
    border-radius: var(--border-radius-lg, 12px);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  }

  /* Main controls */
  .main-controls {
    display: flex;
    flex-direction: row;
    gap: var(--spacing-md, 16px);
  }

  .control-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm, 8px);
    padding: var(--spacing-md, 16px) var(--spacing-lg, 24px);
    background: var(--surface-light, #333);
    color: var(--foreground, #ffffff);
    border: 2px solid transparent;
    border-radius: var(--border-radius-md, 8px);
    font-size: var(--font-size-md, 16px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .control-button:hover {
    background: var(--surface-lighter, #444);
    border-color: var(--primary, #3b82f6);
    transform: translateY(-2px);
  }

  .control-button:active {
    transform: translateY(0);
  }

  .play-pause-button.playing {
    background: var(--error, #ef4444);
  }

  .play-pause-button.playing:hover {
    background: var(--error-hover, #dc2626);
  }

  .icon {
    font-size: 24px;
  }

  .label {
    font-size: var(--font-size-sm, 14px);
  }

  /* Speed control */
  .speed-control {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md, 16px);
  }

  .speed-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--foreground, #ffffff);
  }

  .label-text {
    font-size: var(--font-size-sm, 14px);
    font-weight: 600;
  }

  .speed-display {
    font-size: var(--font-size-xl, 24px);
    font-weight: 700;
    color: var(--primary, #3b82f6);
  }

  .speed-slider-container {
    display: flex;
    align-items: center;
    gap: var(--spacing-md, 16px);
  }

  .bpm-adjust-button {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface-light, #333);
    color: var(--foreground, #ffffff);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    border-radius: var(--border-radius-sm, 6px);
    font-size: var(--font-size-lg, 20px);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .bpm-adjust-button:hover {
    background: var(--surface-lighter, #444);
    border-color: var(--primary, #3b82f6);
  }

  .speed-slider {
    flex: 1;
    height: 8px;
    background: var(--surface-light, #333);
    border-radius: 4px;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
  }

  .speed-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: var(--primary, #3b82f6);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .speed-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
  }

  .speed-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: var(--primary, #3b82f6);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .speed-slider::-moz-range-thumb:hover {
    transform: scale(1.2);
  }



  /* Metronome control */
  .metronome-control {
    padding-top: var(--spacing-md, 16px);
    border-top: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  }

  .metronome-toggle {
    display: flex;
    align-items: center;
    gap: var(--spacing-md, 16px);
    cursor: pointer;
    color: var(--foreground, #ffffff);
  }

  .metronome-toggle input[type="checkbox"] {
    width: 48px;
    height: 24px;
    appearance: none;
    background: var(--surface-light, #333);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    border-radius: 12px;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .metronome-toggle input[type="checkbox"]::before {
    content: "";
    position: absolute;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--foreground, #ffffff);
    left: 2px;
    top: 2px;
    transition: all 0.3s ease;
  }

  .metronome-toggle input[type="checkbox"]:checked {
    background: var(--primary, #3b82f6);
  }

  .metronome-toggle input[type="checkbox"]:checked::before {
    left: 26px;
  }

  .toggle-icon {
    font-size: 24px;
  }

  .toggle-label {
    font-size: var(--font-size-md, 16px);
    font-weight: 600;
  }

  /* Responsive adjustments - aligned with mobile breakpoint (768px) */
  @media (max-width: 768px) {
    .record-controls {
      padding: var(--spacing-sm, 16px);
      gap: var(--spacing-sm, 16px);
    }

    .main-controls {
      flex-direction: row;
    }

    .control-button {
      padding: var(--spacing-sm, 8px) var(--spacing-sm, 16px);
    }
  }
</style>
