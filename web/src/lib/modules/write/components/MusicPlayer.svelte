<!-- MusicPlayer.svelte - Music player component with playback controls -->
<script lang="ts">
  import type { MusicPlayerState } from "$wordcard/domain";
  import { createDefaultMusicPlayerState, formatTime } from "$wordcard/domain";

  // Props
  interface Props {
    playerState?: MusicPlayerState;
    disabled?: boolean;
    onPlayRequested?: () => void;
    onPauseRequested?: () => void;
    onStopRequested?: () => void;
    onSeekRequested?: (position: number) => void;
  }

  let {
    playerState = createDefaultMusicPlayerState(),
    disabled = false,
    onPlayRequested,
    onPauseRequested,
    onStopRequested,
    onSeekRequested,
  }: Props = $props();

  // Local state for seeking
  let isSeeking = $state(false);
  let seekPosition = $state(0);

  // Handle play button
  function handlePlay() {
    if (disabled || !playerState.isLoaded) return;
    onPlayRequested?.();
  }

  // Handle pause button
  function handlePause() {
    if (disabled) return;
    onPauseRequested?.();
  }

  // Handle stop button
  function handleStop() {
    if (disabled) return;
    onStopRequested?.();
  }

  // Handle seek start
  function handleSeekStart() {
    if (disabled || !playerState.isLoaded) return;
    isSeeking = true;
    seekPosition = playerState.currentTime;
  }

  // Handle seek end
  function handleSeekEnd() {
    if (disabled || !playerState.isLoaded) return;
    isSeeking = false;
    onSeekRequested?.(seekPosition);
  }

  // Handle slider input
  function handleSliderInput(event: Event) {
    if (disabled || !playerState.isLoaded) return;
    const target = event.target as HTMLInputElement;
    const value = parseFloat(target.value);
    seekPosition = (value / 1000) * playerState.duration;
  }

  // Computed values
  const sliderValue = $derived(
    !playerState.isLoaded || playerState.duration === 0
      ? 0
      : ((isSeeking ? seekPosition : playerState.currentTime) /
          playerState.duration) *
          1000
  );

  const currentTimeDisplay = $derived(
    formatTime(isSeeking ? seekPosition : playerState.currentTime)
  );

  const totalTimeDisplay = $derived(formatTime(playerState.duration));

  const statusText = $derived(
    !playerState.isLoaded
      ? "No music loaded"
      : `♪ ${playerState.filename || "Music loaded"}`
  );

  const statusColor = $derived(
    playerState.isLoaded
      ? "rgba(100, 200, 100, 0.9)"
      : "rgba(255, 255, 255, 0.6)"
  );
</script>

<div class="music-player" class:disabled>
  <!-- Top row: Title and status -->
  <div class="title-row">
    <span class="title">🎵 Music Player</span>
    <span class="status" style="color: {statusColor}">
      {statusText}
    </span>
  </div>

  <!-- Position slider -->
  <div class="slider-container">
    <input
      type="range"
      class="position-slider"
      min="0"
      max="1000"
      value={sliderValue}
      disabled={disabled || !playerState.isLoaded}
      oninput={handleSliderInput}
      onmousedown={handleSeekStart}
      onmouseup={handleSeekEnd}
      ontouchstart={handleSeekStart}
      ontouchend={handleSeekEnd}
    />
  </div>

  <!-- Controls row -->
  <div class="controls-row">
    <!-- Time display -->
    <div class="time-display">
      <span class="current-time">{currentTimeDisplay}</span>
      <span class="time-separator">/</span>
      <span class="total-time">{totalTimeDisplay}</span>
    </div>

    <!-- Control buttons -->
    <div class="control-buttons">
      <button
        class="control-button play-button"
        disabled={disabled || !playerState.isLoaded || playerState.isPlaying}
        onclick={handlePlay}
        title="Play"
      >
        ▶
      </button>

      <button
        class="control-button pause-button"
        disabled={disabled || !playerState.isPlaying}
        onclick={handlePause}
        title="Pause"
      >
        ⏸
      </button>

      <button
        class="control-button stop-button"
        disabled={disabled || !playerState.isLoaded}
        onclick={handleStop}
        title="Stop"
      >
        ⏹
      </button>
    </div>
  </div>
</div>

<style>
  .music-player {
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    padding: var(--spacing-sm) var(--spacing-md);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    min-height: 85px;
    transition: all var(--transition-normal);
  }

  .music-player.disabled {
    opacity: 0.6;
    pointer-events: none;
  }

  .title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-md);
  }

  .title {
    color: rgba(255, 255, 255, 0.9);
    font-size: var(--font-size-sm);
    font-weight: bold;
    font-family: "Segoe UI", sans-serif;
  }

  .status {
    font-size: var(--font-size-sm);
    font-weight: 500;
    font-family: "Segoe UI", sans-serif;
    transition: color var(--transition-normal);
  }

  .slider-container {
    width: 100%;
  }

  .position-slider {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
    outline: none;
    cursor: pointer;
    transition: all var(--transition-normal);
    -webkit-appearance: none;
    appearance: none;
  }

  .position-slider::-webkit-slider-track {
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .position-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    height: 16px;
    width: 16px;
    background: var(--primary-color);
    border: 1px solid var(--primary-light);
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-fast);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .position-slider::-webkit-slider-thumb:hover {
    background: var(--primary-light);
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .position-slider::-moz-range-track {
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  .position-slider::-moz-range-thumb {
    height: 16px;
    width: 16px;
    background: var(--primary-color);
    border: 1px solid var(--primary-light);
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .position-slider:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .controls-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-md);
  }

  .time-display {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: var(--font-size-sm);
    font-family: "Segoe UI", sans-serif;
    color: var(--text-color);
  }

  .time-separator {
    color: var(--text-secondary);
  }

  .control-buttons {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .control-button {
    background: var(--primary-color);
    border: 1px solid var(--primary-light);
    border-radius: var(--border-radius-sm);
    color: white;
    font-weight: bold;
    font-size: var(--font-size-sm);
    width: 32px;
    height: 28px;
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .control-button:hover:not(:disabled) {
    background: var(--primary-light);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .control-button:active:not(:disabled) {
    background: var(--primary-dark);
    transform: translateY(0);
  }

  .control-button:disabled {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .music-player {
      padding: var(--spacing-xs) var(--spacing-sm);
      min-height: 70px;
    }

    .title-row {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-xs);
    }

    .title,
    .status {
      font-size: var(--font-size-xs);
    }

    .controls-row {
      flex-direction: column;
      gap: var(--spacing-xs);
    }

    .time-display {
      font-size: var(--font-size-xs);
    }

    .control-button {
      width: 28px;
      height: 24px;
      font-size: var(--font-size-xs);
    }
  }

  @media (max-width: 480px) {
    .music-player {
      padding: var(--spacing-xs);
      min-height: 60px;
    }

    .title,
    .status {
      font-size: 10px;
    }

    .time-display {
      font-size: 10px;
    }

    .control-button {
      width: 24px;
      height: 20px;
      font-size: 10px;
    }
  }
</style>
