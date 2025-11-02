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
  }: {
    pathState: GesturalPathState;
    onRotationSelected?: (direction: RotationDirection) => void;
    onComplete?: () => void;
    onReset?: () => void;
  } = $props();

  // Handle rotation selection
  function selectRotation(direction: RotationDirection): void {
    pathState.setRotationDirection(direction);
    onRotationSelected?.(direction);
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
  <!-- Hand indicator -->
  <div class="hand-indicator">
    <div
      class="hand-badge"
      class:blue={pathState.currentHand === "blue"}
      class:red={pathState.currentHand === "red"}
    >
      {pathState.currentHand === "blue" ? "Blue Hand" : "Red Hand"}
    </div>
  </div>

  <!-- Progress bar -->
  <div class="progress-section">
    <div class="progress-label">
      Beat {pathState.currentBeatNumber} of {pathState.config?.sequenceLength || 0}
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
        class:selected={pathState.selectedRotationDirection === RotationDirection.CLOCKWISE}
        onclick={() => selectRotation(RotationDirection.CLOCKWISE)}
        aria-label="Clockwise rotation"
      >
        <i class="fas fa-rotate-right"></i>
        <span>CW</span>
      </button>
      <button
        class="rotation-btn"
        class:selected={pathState.selectedRotationDirection === RotationDirection.COUNTER_CLOCKWISE}
        onclick={() => selectRotation(RotationDirection.COUNTER_CLOCKWISE)}
        aria-label="Counter-clockwise rotation"
      >
        <i class="fas fa-rotate-left"></i>
        <span>CCW</span>
      </button>
      <button
        class="rotation-btn"
        class:selected={pathState.selectedRotationDirection === RotationDirection.NO_ROTATION}
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
            <span class="motion-type">{getMotionTypeText(segment.handMotionType)}</span>
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
    <button class="action-btn secondary" onclick={onReset}>
      <i class="fas fa-redo"></i>
      Reset
    </button>
  </div>
</div>

<style>
  .control-panel {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .hand-indicator {
    display: flex;
    justify-content: center;
  }

  .hand-badge {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .hand-badge.blue {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
  }

  .hand-badge.red {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
  }

  .progress-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .progress-label {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.8);
    text-align: center;
  }

  .progress-bar {
    height: 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
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
    gap: 0.75rem;
  }

  .section-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.05em;
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
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.85rem;
  }

  .rotation-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
  }

  .rotation-btn.selected {
    background: rgba(59, 130, 246, 0.3);
    border-color: #3b82f6;
    color: white;
  }

  .rotation-btn i {
    font-size: 1.5rem;
  }

  .recent-segments {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .segment-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .segment-item {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.8);
  }

  .beat-num {
    font-weight: 600;
    color: white;
  }

  .motion-type {
    color: #60a5fa;
    font-weight: 500;
  }

  .locations {
    margin-left: auto;
    font-family: monospace;
  }

  .action-buttons {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }

  .action-btn {
    flex: 1;
    padding: 0.875rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .action-btn.primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
  }

  .action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    color: white;
  }
</style>
