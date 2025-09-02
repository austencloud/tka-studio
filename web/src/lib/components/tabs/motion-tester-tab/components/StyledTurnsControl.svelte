<!--
StyledTurnsControl.svelte - Enhanced turns control

Improved styling for the +/- turns control to match the new visual design.
Supports float motion with "fl" value and automatic motion type switching.
Shows Pro/Anti selection modal when leaving float.
-->
<script lang="ts">
  import { MotionType } from "$domain";
  import ProAntiSelectionModal from "./ProAntiSelectionModal.svelte";

  interface Props {
    turns: number | "fl";
    onTurnsChange: (turns: number | "fl") => void;
    onMotionTypeChange?: (motionType: MotionType) => void; // For triggering motion type changes
    color: string;
    currentMotionType?: MotionType; // To know current motion type
  }

  let {
    turns,
    onTurnsChange,
    onMotionTypeChange,
    color,
    currentMotionType,
  }: Props = $props();

  // Modal state for Pro/Anti selection
  let showProAntiModal = $state(false);
  let pendingTurnsValue = $state<number>(0);
  let incrementButtonElement = $state<HTMLButtonElement>();

  // Helper functions for display and logic
  let displayValue = $derived(turns === "fl" ? "FL" : turns.toString());
  let numericValue = $derived(turns === "fl" ? -0.5 : turns);
  let canDecrement = $derived(numericValue > -0.5);
  let canIncrement = $derived(numericValue < 10);

  function increment() {
    const currentTurns = turns === "fl" ? -0.5 : turns;
    if (currentTurns < 10) {
      // Reasonable max limit
      // When incrementing from float (-0.5), go to 0, not 0.5
      const newTurns = turns === "fl" ? 0 : currentTurns + 1;

      // If we're moving away from float, show Pro/Anti selection modal
      if (turns === "fl") {
        pendingTurnsValue = newTurns;
        showProAntiModal = true;
      } else {
        // Normal increment
        onTurnsChange(newTurns);
      }
    }
  }

  function decrement() {
    const currentTurns = turns === "fl" ? -0.5 : turns;
    if (currentTurns > -0.5) {
      const newTurns = currentTurns - 1;

      // If we go below 0, switch to float
      if (newTurns < 0) {
        onTurnsChange("fl");
        if (onMotionTypeChange) {
          onMotionTypeChange(MotionType.FLOAT);
        }
      } else {
        onTurnsChange(newTurns);
      }
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "ArrowUp") {
      event.preventDefault();
      increment();
    } else if (event.key === "ArrowDown") {
      event.preventDefault();
      decrement();
    }
  }

  function handleProAntiSelection(motionType: MotionType) {
    // Apply the pending turns value and motion type
    onTurnsChange(pendingTurnsValue);
    if (onMotionTypeChange) {
      onMotionTypeChange(motionType);
    }
    showProAntiModal = false;
  }

  function closeModal() {
    showProAntiModal = false;
    // Don't apply the pending changes - user cancelled
  }
</script>

<div class="turns-control-container">
  <div class="turns-label">Turns</div>
  <div
    class="turns-control"
    style="--accent-color: {color}"
    role="spinbutton"
    aria-label="Number of turns"
    aria-valuenow={numericValue}
    aria-valuemin="-0.5"
    aria-valuemax="10"
    tabindex="0"
    onkeydown={handleKeyDown}
  >
    <button
      class="turns-btn decrement"
      onclick={decrement}
      disabled={!canDecrement}
      aria-label="Decrease turns"
      title="Decrease turns"
    >
      <span class="btn-icon">−</span>
    </button>

    <div class="turns-display">
      <span class="turns-value">{displayValue}</span>
    </div>

    <button
      bind:this={incrementButtonElement}
      class="turns-btn increment"
      onclick={increment}
      disabled={!canIncrement}
      aria-label="Increase turns"
      title="Increase turns"
    >
      <span class="btn-icon">+</span>
    </button>
  </div>
</div>

{#if showProAntiModal}
  <ProAntiSelectionModal
    onMotionTypeSelect={handleProAntiSelection}
    onClose={closeModal}
    {color}
    triggerElement={incrementButtonElement}
  />
{/if}

<style>
  .turns-control-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .turns-label {
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .turns-control {
    display: flex;
    align-items: center;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 2px;
    gap: 2px;
  }

  .turns-control:focus-within {
    border-color: rgba(var(--accent-color), 0.4);
    box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.2);
  }

  .turns-btn {
    width: 36px;
    height: 36px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.7);
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .turns-btn:hover:not(:disabled) {
    background: rgba(var(--accent-color), 0.2);
    border-color: rgba(var(--accent-color), 0.4);
    color: white;
    transform: scale(1.05);
  }

  .turns-btn:active:not(:disabled) {
    transform: scale(0.95);
  }

  .turns-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    transform: none;
  }

  .turns-btn:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.5);
  }

  .btn-icon {
    line-height: 1;
  }

  .turns-display {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 48px;
    height: 36px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 0 12px;
  }

  .turns-value {
    font-size: 16px;
    font-weight: 700;
    color: white;
    line-height: 1;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .turns-btn {
      width: 32px;
      height: 32px;
      font-size: 14px;
    }

    .turns-display {
      min-width: 42px;
      height: 32px;
      padding: 0 8px;
    }

    .turns-value {
      font-size: 14px;
    }
  }
</style>
