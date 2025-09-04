<!--
AnimationPlaybackControls.svelte - Play/pause and reset controls

Single responsibility: Handle playback control buttons (play/pause/reset).
No progress scrubbing, no status display - just playback actions.
-->
<script lang="ts">
  interface Props {
    isPlaying: boolean;
    isEngineInitialized: boolean;
    onPlayToggle: () => void;
    onReset: () => void;
  }

  let { isPlaying, isEngineInitialized, onPlayToggle, onReset }: Props =
    $props();

  let playButtonLabel = $derived(
    isPlaying ? "Pause animation" : "Play animation"
  );
</script>

<div class="playback-controls">
  <button
    class="control-btn play-btn"
    onclick={onPlayToggle}
    disabled={!isEngineInitialized}
    aria-label={playButtonLabel}
    title={playButtonLabel}
  >
    <span class="btn-icon" aria-hidden="true">
      {isPlaying ? "⏸️" : "▶️"}
    </span>
  </button>

  <button
    class="control-btn reset-btn"
    onclick={onReset}
    disabled={!isEngineInitialized}
    aria-label="Reset animation to beginning"
    title="Reset animation"
  >
    <span class="btn-icon" aria-hidden="true">⏹️</span>
  </button>
</div>

<style>
  .playback-controls {
    display: flex;
    gap: 8px;
    justify-content: center;
  }

  .control-btn {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    color: #c7d2fe;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
  }

  .control-btn:hover:not(:disabled) {
    background: rgba(139, 92, 246, 0.2);
    border-color: rgba(139, 92, 246, 0.4);
    color: white;
  }

  .control-btn:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.5);
  }

  .control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
