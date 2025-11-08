<!--
PathControlPanel.svelte - Control panel for path builder configuration

Displays current state, beat progress, rotation selector, and action buttons.
-->
<script lang="ts">
  import { GridMode, HandMotionType, RotationDirection } from "$shared";
  import type { GesturalPathState } from "../state";

  // Props
  let {
    pathState,
    onRotationSelected,
    onComplete,
    onReset,
    onBackToSettings,
  }: {
    pathState: GesturalPathState;
    onRotationSelected?: (direction: RotationDirection) => void;
    onComplete?: () => void;
    onReset?: () => void;
    onBackToSettings?: () => void;
  } = $props();

  // Reset confirmation state
  let resetConfirmationActive = $state(false);
  let resetConfirmationTimeout: number | null = $state(null);

  // Handle rotation selection
  function selectRotation(direction: RotationDirection): void {
    pathState.setRotationDirection(direction);
    onRotationSelected?.(direction);
  }

  // Handle reset with inline confirmation
  function handleResetClick(): void {
    if (resetConfirmationActive) {
      // Second click - actually reset
      onReset?.();
      resetConfirmationActive = false;
      if (resetConfirmationTimeout) {
        clearTimeout(resetConfirmationTimeout);
        resetConfirmationTimeout = null;
      }
    } else {
      // First click - show confirmation
      resetConfirmationActive = true;
      // Auto-cancel after 3 seconds
      resetConfirmationTimeout = window.setTimeout(() => {
        resetConfirmationActive = false;
        resetConfirmationTimeout = null;
      }, 3000);
    }
  }

  // Get hand motion type display text
  function getMotionTypeText(type: HandMotionType): string {
    switch (type) {
      case HandMotionType.SHIFT:
        return "Shift";
      case HandMotionType.DASH:
        return "Dash";
      case HandMotionType.STATIC:
        return "Static";
      default:
        return "Unknown";
    }
  }
</script>

<div class="control-panel">
  <!-- Progress bar -->
  <div class="progress-section">
    <div class="progress-label">
      Beat {pathState.currentBeatNumber} of {pathState.config?.sequenceLength ||
        0}
    </div>
    <div class="progress-bar">
      <div
        class="progress-fill"
        style="width: {pathState.progressPercentage}%"
        class:blue={pathState.currentHand === "blue"}
        class:red={pathState.currentHand === "red"}
      ></div>
    </div>
  </div>

  <!-- Rotation selector -->
  <div class="rotation-section">
    <div class="section-label">Rotation Direction</div>
    <div class="rotation-buttons">
      <button
        class="rotation-btn"
        class:selected={pathState.selectedRotationDirection ===
          RotationDirection.CLOCKWISE}
        onclick={() => selectRotation(RotationDirection.CLOCKWISE)}
        aria-label="Clockwise rotation"
      >
        <i class="fas fa-rotate-right"></i>
        <span>CW</span>
      </button>
      <button
        class="rotation-btn"
        class:selected={pathState.selectedRotationDirection ===
          RotationDirection.COUNTER_CLOCKWISE}
        onclick={() => selectRotation(RotationDirection.COUNTER_CLOCKWISE)}
        aria-label="Counter-clockwise rotation"
      >
        <i class="fas fa-rotate-left"></i>
        <span>CCW</span>
      </button>
      <button
        class="rotation-btn"
        class:selected={pathState.selectedRotationDirection ===
          RotationDirection.NO_ROTATION}
        onclick={() => selectRotation(RotationDirection.NO_ROTATION)}
        aria-label="No rotation"
      >
        <i class="fas fa-minus"></i>
        <span>None</span>
      </button>
    </div>
  </div>

  <!-- Recent segments -->
  {#if pathState.completedSegments.length > 0}
    <div class="recent-segments">
      <div class="section-label">Recent Beats</div>
      <div class="segment-list">
        {#each pathState.completedSegments.slice(-3) as segment}
          <div class="segment-item">
            <span class="beat-num">Beat {segment.beatNumber}:</span>
            <span class="motion-type"
              >{getMotionTypeText(segment.handMotionType)}</span
            >
            <span class="locations">
              {segment.startLocation} → {segment.endLocation}
            </span>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Action buttons -->
  <div class="action-buttons">
    {#if pathState.isCurrentHandComplete}
      <button class="action-btn primary" onclick={onComplete}>
        {pathState.currentHand === "blue" ? "Draw Red Hand" : "Finish"}
      </button>
    {/if}
    <button
      class="action-btn secondary"
      class:confirmation={resetConfirmationActive}
      onclick={handleResetClick}
    >
      {#if resetConfirmationActive}
        <i class="fas fa-exclamation-triangle"></i>
        Confirm Reset?
      {:else}
        <i class="fas fa-redo"></i>
        Reset
      {/if}
    </button>
    <button class="action-btn tertiary" onclick={onBackToSettings}>
      <i class="fas fa-cog"></i>
      Settings
    </button>
  </div>
</div>

<style>
  .control-panel {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0.75rem;
    width: 100%;
    box-sizing: border-box;
  }

  .progress-section {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
  }

  .progress-label {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.8);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .progress-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    transition: width 0.3s ease;
    border-radius: 6px;
  }

  .progress-fill.blue {
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
  }

  .progress-fill.red {
    background: linear-gradient(90deg, #ef4444, #f87171);
  }

  .rotation-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .section-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .rotation-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .rotation-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.65);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.75rem;
    min-height: 44px;
  }

  .rotation-btn:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .rotation-btn.selected {
    background: linear-gradient(135deg, #10b981, #059669);
    border-color: #10b981;
    color: white;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }

  .rotation-btn:active {
    transform: translateY(0);
  }

  .rotation-btn i {
    font-size: 1.1rem;
  }

  .recent-segments {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .segment-list {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
  }

  .segment-item {
    display: flex;
    flex-wrap: wrap;
    gap: 0.375rem;
    padding: 0.375rem 0.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.8);
    align-items: center;
  }

  .beat-num {
    font-weight: 600;
    color: white;
    white-space: nowrap;
  }

  .motion-type {
    color: #60a5fa;
    font-weight: 500;
    white-space: nowrap;
  }

  .locations {
    margin-left: auto;
    font-family: monospace;
    font-size: 0.7rem;
    white-space: nowrap;
  }

  /* Stack segment info on very narrow panels */
  @media (max-width: 350px) {
    .segment-item {
      flex-direction: column;
      align-items: flex-start;
    }

    .locations {
      margin-left: 0;
    }
  }

  .action-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  /* Side-by-side buttons on wider panels */
  @media (min-width: 400px) {
    .action-buttons {
      flex-direction: row;
    }
  }

  .action-btn {
    flex: 1;
    padding: 0.75rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 44px;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  }

  .action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
  }

  .action-btn.primary:active {
    transform: translateY(0);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.85);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.35);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
  }

  .action-btn.secondary:active {
    transform: translateY(0);
  }

  .action-btn.secondary.confirmation {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border-color: #fbbf24;
    color: white;
    animation: pulse 0.6s ease-in-out;
  }

  .action-btn.secondary.confirmation:hover {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-color: #f87171;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  .action-btn.tertiary {
    background: rgba(59, 130, 246, 0.12);
    border: 2px solid rgba(59, 130, 246, 0.3);
    color: rgba(96, 165, 250, 0.95);
  }

  .action-btn.tertiary:hover {
    background: rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.5);
    color: #60a5fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }

  .action-btn.tertiary:active {
    transform: translateY(0);
  }

  @keyframes pulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  /* Compact mode for small mobile screens (iPhone SE, etc.) */
  @media (max-width: 400px) and (max-height: 700px) {
    .control-panel {
      padding: 0.4375rem;
      gap: 0.375rem;
    }

    .progress-section {
      gap: 0.1875rem;
    }

    .progress-label {
      font-size: 0.6875rem;
      gap: 0.25rem;
    }

    .progress-bar {
      height: 5px;
    }

    .rotation-section {
      gap: 0.3125rem;
    }

    .section-label {
      font-size: 0.65625rem;
    }

    .rotation-buttons {
      gap: 0.3125rem;
    }

    .rotation-btn {
      padding: 0.25rem;
      min-height: 44px; /* Maintain accessibility */
      gap: 0.125rem;
      font-size: 0.65625rem;
    }

    .rotation-btn i {
      font-size: 0.875rem;
    }

    .action-buttons {
      gap: 0.3125rem;
    }

    .action-btn {
      padding: 0.375rem 0.5rem;
      min-height: 44px; /* Maintain accessibility */
      font-size: 0.8125rem;
    }
  }

  /* Ultra-compact mode for landscape mobile */
  @media (max-height: 500px) and (orientation: landscape) {
    .control-panel {
      padding: 0.5rem;
      gap: 0.5rem;
    }

    .rotation-btn {
      padding: 0.375rem;
      min-height: 32px;
    }

    .action-btn {
      padding: 0.5rem;
      min-height: 36px;
    }

    .progress-bar {
      height: 6px;
    }
  }
</style>
