<!--
  TunnelModePanel.svelte - Tunnel Mode (Overlay Animation)

  Overlays two sequences with different colors to create "tunneling" effect.
  Primary performer: Red/Blue
  Secondary performer: Green/Purple
-->
<script lang="ts">
  import type { AnimateModuleState } from "../shared/state/animate-module-state.svelte";
  import SequenceBrowserPanel from "../shared/components/SequenceBrowserPanel.svelte";

  // Props
  let {
    animateState,
  }: {
    animateState: AnimateModuleState;
  } = $props();

  // Derived: Check if both sequences are selected
  const bothSequencesSelected = $derived(
    animateState.primarySequence && animateState.secondarySequence
  );

  // Derived: Check which sequences are missing
  const needsPrimary = $derived(!animateState.primarySequence);
  const needsSecondary = $derived(!animateState.secondarySequence);
</script>

<div class="tunnel-mode-panel">
  <!-- Sequence Selection Area (when sequences not selected) -->
  {#if !bothSequencesSelected}
    <div class="selection-area">
      <div class="selection-header">
        <h2>Tunnel Mode Setup</h2>
        <p>Select two sequences to overlay with different colors</p>
      </div>

      <div class="sequence-selectors">
        <!-- Primary Sequence Selector -->
        <button
          class="sequence-selector"
          class:selected={!needsPrimary}
          onclick={() => animateState.openSequenceBrowser("primary")}
        >
          <div class="selector-header" style="background: linear-gradient(135deg, #3b82f6, #ef4444);">
            <i class="fas fa-user"></i>
            <span>Primary Performer</span>
          </div>
          <div class="selector-content">
            {#if animateState.primarySequence}
              <div class="selected-sequence">
                <i class="fas fa-check-circle" style="color: #10b981;"></i>
                <div class="sequence-name">
                  {animateState.primarySequence.word || "Untitled"}
                </div>
              </div>
            {:else}
              <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <span>Click to select sequence</span>
              </div>
            {/if}
          </div>
          <div class="color-indicators">
            <div class="color-dot" style="background: #3b82f6;" title="Blue"></div>
            <div class="color-dot" style="background: #ef4444;" title="Red"></div>
          </div>
        </button>

        <!-- Plus Icon -->
        <div class="plus-icon">
          <i class="fas fa-plus"></i>
        </div>

        <!-- Secondary Sequence Selector -->
        <button
          class="sequence-selector"
          class:selected={!needsSecondary}
          onclick={() => animateState.openSequenceBrowser("secondary")}
        >
          <div class="selector-header" style="background: linear-gradient(135deg, #10b981, #a855f7);">
            <i class="fas fa-user"></i>
            <span>Secondary Performer</span>
          </div>
          <div class="selector-content">
            {#if animateState.secondarySequence}
              <div class="selected-sequence">
                <i class="fas fa-check-circle" style="color: #10b981;"></i>
                <div class="sequence-name">
                  {animateState.secondarySequence.word || "Untitled"}
                </div>
              </div>
            {:else}
              <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <span>Click to select sequence</span>
              </div>
            {/if}
          </div>
          <div class="color-indicators">
            <div class="color-dot" style="background: #10b981;" title="Green"></div>
            <div class="color-dot" style="background: #a855f7;" title="Purple"></div>
          </div>
        </button>
      </div>

      <!-- Help Text -->
      <div class="help-text">
        <i class="fas fa-info-circle"></i>
        <p>
          Tunneling overlays two performers on the same canvas with different colors,
          allowing you to see how they interact in the same space.
        </p>
      </div>
    </div>
  {:else}
    <!-- Tunnel Animation View -->
    <div class="animation-area">
      <!-- Header with Sequence Info -->
      <div class="animation-header">
        <div class="performers-info">
          <div class="performer-tag primary">
            <i class="fas fa-user"></i>
            <span>{animateState.primarySequence!.word}</span>
            <div class="color-dots">
              <div class="mini-dot" style="background: #3b82f6;"></div>
              <div class="mini-dot" style="background: #ef4444;"></div>
            </div>
          </div>

          <div class="overlay-icon">
            <i class="fas fa-layer-group"></i>
          </div>

          <div class="performer-tag secondary">
            <i class="fas fa-user"></i>
            <span>{animateState.secondarySequence!.word}</span>
            <div class="color-dots">
              <div class="mini-dot" style="background: #10b981;"></div>
              <div class="mini-dot" style="background: #a855f7;"></div>
            </div>
          </div>
        </div>

        <div class="header-actions">
          <button
            class="change-button"
            onclick={() => {
              animateState.setPrimarySequence(null);
              animateState.setSecondarySequence(null);
            }}
          >
            <i class="fas fa-exchange-alt"></i>
            Change Sequences
          </button>
        </div>
      </div>

      <!-- Canvas Area -->
      <div class="canvas-area">
        <div class="canvas-placeholder">
          <div class="placeholder-content">
            <i class="fas fa-layer-group"></i>
            <p>Tunnel Canvas</p>
            <small>Overlay rendering coming soon</small>
          </div>
        </div>
      </div>

      <!-- Controls Panel -->
      <div class="controls-panel">
        <div class="playback-controls">
          <button class="control-button" aria-label="Play animation">
            <i class="fas fa-play"></i>
          </button>
          <button class="control-button" aria-label="Stop animation">
            <i class="fas fa-stop"></i>
          </button>
          <button class="control-button" aria-label="Loop animation">
            <i class="fas fa-repeat"></i>
          </button>
        </div>

        <div class="tunnel-settings">
          <div class="setting-group">
            <label for="tunnel-opacity">
              <i class="fas fa-droplet"></i>
              Opacity
            </label>
            <input
              id="tunnel-opacity"
              type="range"
              min="0.3"
              max="1"
              step="0.05"
              value={animateState.tunnelOpacity}
              oninput={(e) => animateState.setTunnelOpacity(parseFloat(e.currentTarget.value))}
            />
            <span class="setting-value">{Math.round(animateState.tunnelOpacity * 100)}%</span>
          </div>

          <div class="setting-group">
            <label for="tunnel-speed">
              <i class="fas fa-gauge"></i>
              Speed
            </label>
            <input
              id="tunnel-speed"
              type="range"
              min="0.5"
              max="2"
              step="0.1"
              value={animateState.speed}
              oninput={(e) => animateState.setSpeed(parseFloat(e.currentTarget.value))}
            />
            <span class="setting-value">{animateState.speed.toFixed(1)}x</span>
          </div>
        </div>

        <button class="export-button">
          <i class="fas fa-download"></i>
          Export Tunnel GIF
        </button>
      </div>
    </div>
  {/if}

  <!-- Sequence Browser Panel -->
  <SequenceBrowserPanel
    mode={animateState.browserMode}
    show={animateState.isSequenceBrowserOpen}
    onSelect={(sequence) => {
      if (animateState.browserMode === "primary") {
        animateState.setPrimarySequence(sequence);
      } else if (animateState.browserMode === "secondary") {
        animateState.setSecondarySequence(sequence);
      }
      animateState.closeSequenceBrowser();
    }}
    onClose={animateState.closeSequenceBrowser}
  />
</div>

<style>
  .tunnel-mode-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Selection Area */
  .selection-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: var(--spacing-xl);
    gap: var(--spacing-xl);
  }

  .selection-header {
    text-align: center;
  }

  .selection-header h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 var(--spacing-sm) 0;
  }

  .selection-header p {
    font-size: 1.125rem;
    opacity: 0.7;
    margin: 0;
  }

  /* Sequence Selectors */
  .sequence-selectors {
    display: flex;
    align-items: center;
    gap: var(--spacing-xl);
    max-width: 800px;
    width: 100%;
  }

  .sequence-selector {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 200px;
  }

  .sequence-selector:hover {
    border-color: rgba(236, 72, 153, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(236, 72, 153, 0.3);
  }

  .sequence-selector.selected {
    border-color: rgba(16, 185, 129, 0.5);
  }

  .selector-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    color: white;
    font-weight: 600;
  }

  .selector-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
  }

  .selected-sequence {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .selected-sequence i {
    font-size: 2rem;
  }

  .sequence-name {
    font-size: 1.125rem;
    font-weight: 600;
    text-align: center;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    opacity: 0.5;
  }

  .empty-state i {
    font-size: 2.5rem;
  }

  .color-indicators {
    display: flex;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm);
    justify-content: center;
    background: rgba(0, 0, 0, 0.2);
  }

  .color-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid white;
  }

  .plus-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    opacity: 0.3;
    flex-shrink: 0;
  }

  /* Help Text */
  .help-text {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: var(--border-radius-md);
    max-width: 600px;
  }

  .help-text i {
    font-size: 1.5rem;
    color: #60a5fa;
    flex-shrink: 0;
  }

  .help-text p {
    margin: 0;
    opacity: 0.8;
    line-height: 1.6;
  }

  /* Animation Area */
  .animation-area {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }

  .animation-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .performers-info {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .performer-tag {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: 0.875rem;
    font-weight: 600;
  }

  .performer-tag.primary {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(239, 68, 68, 0.2));
    border: 1px solid rgba(59, 130, 246, 0.3);
  }

  .performer-tag.secondary {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(168, 85, 247, 0.2));
    border: 1px solid rgba(16, 185, 129, 0.3);
  }

  .color-dots {
    display: flex;
    gap: 4px;
  }

  .mini-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid white;
  }

  .overlay-icon {
    opacity: 0.3;
    font-size: 1.25rem;
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

  /* Canvas */
  .canvas-area {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(20, 25, 35, 0.5) 0%, rgba(15, 20, 30, 0.5) 100%);
  }

  .canvas-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
    opacity: 0.3;
  }

  .placeholder-content i {
    font-size: 5rem;
  }

  .placeholder-content p {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
  }

  /* Controls */
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
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .control-button:hover {
    background: rgba(236, 72, 153, 0.3);
    border-color: rgba(236, 72, 153, 0.5);
  }

  .tunnel-settings {
    display: flex;
    gap: var(--spacing-xl);
    flex: 1;
  }

  .setting-group {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    flex: 1;
    max-width: 250px;
  }

  .setting-group label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: 0.875rem;
    white-space: nowrap;
  }

  .setting-group input[type="range"] {
    flex: 1;
  }

  .setting-value {
    font-size: 0.875rem;
    font-weight: 600;
    min-width: 45px;
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
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .export-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .sequence-selectors {
      flex-direction: column;
    }

    .plus-icon {
      transform: rotate(90deg);
    }

    .tunnel-settings {
      flex-direction: column;
      gap: var(--spacing-md);
    }

    .setting-group {
      max-width: none;
    }
  }
</style>
