<!--
Animation Controls Component

Contains play/pause/stop buttons, speed control, and beat info.
-->
<script lang="ts">
  // Props
  const {
    isPlaying = false,
    speed = 1.0,
    currentBeat = 0,
    totalBeats = 0,
    onPlay = () => {},
    onStop = () => {},
    onSpeedChange = (value: number) => {},
  } = $props<{
    isPlaying?: boolean;
    speed?: number;
    currentBeat?: number;
    totalBeats?: number;
    onPlay?: () => void;
    onStop?: () => void;
    onSpeedChange?: (value: number) => void;
  }>();

  function handleSpeedInput(event: Event) {
    const target = event.target as HTMLInputElement;
    onSpeedChange(parseFloat(target.value));
  }
</script>

<div class="animation-controls">
  <button class="control-button" onclick={onPlay}>
    {isPlaying ? "⏸️" : "▶️"}
  </button>
  <button class="control-button" onclick={onStop}> ⏹️ </button>
  <div class="speed-control">
    <label for="speed-slider">Speed: {speed.toFixed(1)}x</label>
    <input
      id="speed-slider"
      type="range"
      min="0.1"
      max="3.0"
      step="0.1"
      value={speed}
      oninput={handleSpeedInput}
    />
  </div>
  <div class="beat-info">
    Beat {Math.floor(currentBeat) + 1} of {totalBeats}
  </div>
</div>

<style>
  .animation-controls {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08) 0%,
      rgba(255, 255, 255, 0.04) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    flex-wrap: wrap;
    backdrop-filter: blur(15px);
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .control-button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.625rem 0.75rem;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.125rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    box-shadow:
      0 2px 8px rgba(99, 102, 241, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    height: 44px;
  }

  .control-button:hover {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    transform: translateY(-2px);
    box-shadow:
      0 6px 20px rgba(99, 102, 241, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .speed-control {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 140px;
  }

  .speed-control label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .speed-control input[type="range"] {
    width: 100%;
    height: 6px;
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.2) 100%
    );
    border-radius: 3px;
    outline: none;
    appearance: none;
    -webkit-appearance: none;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .speed-control input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow:
      0 2px 8px rgba(99, 102, 241, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .speed-control input[type="range"]::-webkit-slider-thumb:hover {
    transform: scale(1.1);
    box-shadow:
      0 4px 12px rgba(99, 102, 241, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
  }

  .speed-control input[type="range"]::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow:
      0 2px 8px rgba(99, 102, 241, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .beat-info {
    margin-left: auto;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .animation-controls {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }

    .beat-info {
      margin-left: 0;
      text-align: center;
    }
  }

  /* Focus improvements for accessibility */
  .control-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .control-button {
      transition: none;
    }
  }
</style>
