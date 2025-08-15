<!--
AnimationProgressSlider.svelte - Progress scrubbing control

Single responsibility: Handle animation progress scrubbing with slider.
No playback controls, no status display - just progress manipulation.
-->
<script lang="ts">
  interface Props {
    progress: number;
    isEngineInitialized: boolean;
    onProgressChange: (progress: number) => void;
  }

  let { progress, isEngineInitialized, onProgressChange }: Props = $props();

  let progressPercent = $derived(Math.round(progress * 100));
  let progressLabel = $derived(`Animation progress: ${progressPercent}%`);

  function handleProgressChange(event: Event) {
    const target = event.currentTarget as HTMLInputElement;
    const newProgress = parseFloat(target.value);
    onProgressChange(newProgress);
  }
</script>

<div class="progress-control">
  <input
    type="range"
    class="progress-slider"
    min="0"
    max="1"
    step="0.01"
    value={progress}
    oninput={handleProgressChange}
    disabled={!isEngineInitialized}
    aria-label={progressLabel}
    title="Scrub animation progress"
  />
  <div class="progress-labels">
    <span>0%</span>
    <span>{progressPercent}%</span>
    <span>100%</span>
  </div>
</div>

<style>
  .progress-control {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .progress-slider {
    width: 100%;
    height: 6px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 3px;
    outline: none;
    cursor: pointer;
    -webkit-appearance: none;
    appearance: none;
  }

  .progress-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    background: #8b5cf6;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .progress-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background: #8b5cf6;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #a5b4fc;
  }
</style>
