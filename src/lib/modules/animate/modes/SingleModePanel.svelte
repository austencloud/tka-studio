<!--
  SingleModePanel.svelte - Single Sequence Animation Mode

  Full-screen canvas showing one sequence.
  Similar to simple animator but with more controls and full-screen layout.
-->
<script lang="ts">
  import type { AnimateModuleState } from "../shared/state/animate-module-state.svelte";
  import { SingleModeCanvas } from "./components";
  import SequenceBrowserPanel from "../shared/components/SequenceBrowserPanel.svelte";

  // Props
  let {
    animateState,
  }: {
    animateState: AnimateModuleState;
  } = $props();

  // Local state for animation playback
  let animatingBeatNumber = $state<number | null>(null);
</script>

<div class="single-mode-panel">
  <!-- Sequence Selection Area (when no sequence selected) -->
  {#if !animateState.primarySequence}
    <div class="selection-prompt">
      <div class="prompt-content">
        <i class="fas fa-layer-group" style="font-size: 5rem; opacity: 0.2;"
        ></i>
        <h2>Select a Sequence to Animate</h2>
        <p>
          Choose a sequence from your library to view in full-screen animation
          mode
        </p>
        <button
          class="select-button"
          onclick={() => animateState.openSequenceBrowser("primary")}
        >
          <i class="fas fa-folder-open"></i>
          Browse Sequences
        </button>
      </div>
    </div>
  {:else}
    <!-- Full-Screen Animation Canvas -->
    <div class="animation-area">
      <!-- Canvas will be rendered here by AnimationSheetCoordinator -->
      <!-- For now, show sequence info -->
      <div class="sequence-header">
        <div class="sequence-title">
          <h3>{animateState.primarySequence.word || "Untitled Sequence"}</h3>
          {#if animateState.primarySequence.author}
            <p class="author">by {animateState.primarySequence.author}</p>
          {/if}
        </div>
        <button
          class="change-button"
          onclick={() => animateState.openSequenceBrowser("primary")}
        >
          <i class="fas fa-exchange-alt"></i>
          Change Sequence
        </button>
      </div>

      <!-- Animation Controls -->
      <div class="controls-panel">
        <div class="playback-controls">
          <button
            class="control-button"
            class:active={animateState.isPlaying}
            aria-label={animateState.isPlaying ? "Pause" : "Play"}
            onclick={() => animateState.setIsPlaying(!animateState.isPlaying)}
          >
            <i class="fas fa-{animateState.isPlaying ? 'pause' : 'play'}"></i>
          </button>
          <button
            class="control-button"
            aria-label="Stop"
            onclick={() => {
              animateState.setIsPlaying(false);
              animatingBeatNumber = null;
            }}
          >
            <i class="fas fa-stop"></i>
          </button>
          <button
            class="control-button"
            class:active={animateState.shouldLoop}
            aria-label="Loop"
            onclick={() => animateState.setShouldLoop(!animateState.shouldLoop)}
          >
            <i class="fas fa-repeat"></i>
          </button>
        </div>

        <div class="speed-control">
          <label for="single-mode-speed">
            <i class="fas fa-gauge"></i>
            Speed
          </label>
          <input
            id="single-mode-speed"
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={animateState.speed}
            oninput={(e) =>
              animateState.setSpeed(parseFloat(e.currentTarget.value))}
          />
          <span class="speed-value">{animateState.speed.toFixed(1)}x</span>
        </div>

        <button class="export-button">
          <i class="fas fa-download"></i>
          Export GIF
        </button>
      </div>

      <!-- Animation Canvas -->
      <div class="canvas-container">
        <SingleModeCanvas
          sequence={animateState.primarySequence}
          bind:isPlaying={animateState.isPlaying}
          bind:animatingBeatNumber
        />
      </div>
    </div>
  {/if}

  <!-- Sequence Browser Panel -->
  <SequenceBrowserPanel
    mode="primary"
    show={animateState.isSequenceBrowserOpen &&
      animateState.browserMode === "primary"}
    onSelect={(sequence) => {
      animateState.setPrimarySequence(sequence);
      animateState.closeSequenceBrowser();
    }}
    onClose={animateState.closeSequenceBrowser}
  />
</div>

<style>
  .single-mode-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
  }

  /* Selection Prompt */
  .selection-prompt {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: var(--spacing-xl);
  }

  .prompt-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-lg);
    text-align: center;
    max-width: 500px;
  }

  .prompt-content h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
  }

  .prompt-content p {
    font-size: 1.125rem;
    opacity: 0.7;
    margin: 0;
  }

  .select-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-xl);
    background: linear-gradient(135deg, #ec4899, #8b5cf6);
    border: none;
    border-radius: var(--border-radius-lg);
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .select-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(236, 72, 153, 0.4);
  }

  /* Animation Area */
  .animation-area {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Sequence Header */
  .sequence-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .sequence-title h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
  }

  .author {
    margin: 4px 0 0 0;
    font-size: 0.875rem;
    opacity: 0.6;
  }

  .change-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-md);
    color: white;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .change-button:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  /* Canvas Container */
  .canvas-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  /* Controls Panel */
  .controls-panel {
    display: flex;
    align-items: center;
    gap: var(--spacing-xl);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .playback-controls {
    display: flex;
    gap: var(--spacing-sm);
  }

  .control-button {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .control-button:hover {
    background: rgba(236, 72, 153, 0.3);
    border-color: rgba(236, 72, 153, 0.5);
  }

  .control-button.active {
    background: rgba(236, 72, 153, 0.4);
    border-color: rgba(236, 72, 153, 0.7);
    color: #ec4899;
  }

  .speed-control {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    flex: 1;
    max-width: 300px;
  }

  .speed-control label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: 0.875rem;
    white-space: nowrap;
  }

  .speed-control input[type="range"] {
    flex: 1;
  }

  .speed-value {
    font-size: 0.875rem;
    font-weight: 600;
    min-width: 40px;
    text-align: right;
  }

  .export-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    border-radius: var(--border-radius-md);
    color: white;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .export-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .controls-panel {
      flex-wrap: wrap;
    }

    .speed-control {
      flex: 1 1 100%;
      max-width: none;
    }
  }
</style>
