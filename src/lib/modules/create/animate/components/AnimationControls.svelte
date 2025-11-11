<!--
  AnimationControls.svelte

  Reusable animation controls component with speed controls.
-->
<script lang="ts">
  // Constants - All in BPM (beats per minute)
  const DEFAULT_BPM = 60; // Base tempo
  const MIN_BPM = 15; // Minimum speed
  const MAX_BPM = 150; // Maximum speed
  const BPM_INCREMENT = 5; // Increment/decrement by 5 BPM per button click

  // Internal conversion factors (system uses multipliers internally)
  const MIN_SPEED = MIN_BPM / DEFAULT_BPM; // 0.25
  const MAX_SPEED = MAX_BPM / DEFAULT_BPM; // 2.5
  const SPEED_INCREMENT = BPM_INCREMENT / DEFAULT_BPM; // ~0.0833

  // Props
  let {
    speed = 1,
    onSpeedChange = () => {},
  }: {
    speed?: number;
    onSpeedChange?: (newSpeed: number) => void;
  } = $props();

  // State for editing
  let isEditing = $state(false);
  let editValue = $state("");

  // Derived: Convert speed multiplier to BPM
  let bpm = $derived(Math.round(speed * DEFAULT_BPM));

  // Handlers
  function decreaseSpeed() {
    const newSpeed = Math.max(MIN_SPEED, speed - SPEED_INCREMENT);
    onSpeedChange(newSpeed);
  }

  function increaseSpeed() {
    const newSpeed = Math.min(MAX_SPEED, speed + SPEED_INCREMENT);
    onSpeedChange(newSpeed);
  }

  function startEditing() {
    isEditing = true;
    editValue = bpm.toString();
  }

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    editValue = target.value;
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      submitEdit();
    } else if (event.key === "Escape") {
      cancelEdit();
    }
  }

  function submitEdit() {
    const newBpm = parseInt(editValue, 10);
    if (!isNaN(newBpm)) {
      // Convert BPM to speed multiplier
      const newSpeed = newBpm / DEFAULT_BPM;
      // Clamp to min/max range
      const clampedSpeed = Math.max(MIN_SPEED, Math.min(MAX_SPEED, newSpeed));
      onSpeedChange(clampedSpeed);
    }
    isEditing = false;
  }

  function cancelEdit() {
    isEditing = false;
    editValue = "";
  }

  function handleBlur() {
    submitEdit();
  }
</script>

<div class="controls-container">
  <div class="speed-control">
    <div class="speed-label" role="heading" aria-level="3">Speed</div>

    <div class="speed-buttons">
      <button
        class="speed-btn"
        onclick={decreaseSpeed}
        disabled={speed <= MIN_SPEED}
        aria-label="Decrease speed"
        type="button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>

      {#if isEditing}
        <input
          type="number"
          class="speed-input"
          value={editValue}
          oninput={handleInput}
          onkeydown={handleKeyDown}
          onblur={handleBlur}
          min={Math.round(MIN_SPEED * DEFAULT_BPM)}
          max={Math.round(MAX_SPEED * DEFAULT_BPM)}
          step={BPM_INCREMENT}
          aria-label="Enter BPM"
        />
      {:else}
        <button
          class="speed-value"
          onclick={startEditing}
          aria-label="Click to edit BPM"
          type="button"
        >
          {bpm} BPM
        </button>
      {/if}

      <button
        class="speed-btn"
        onclick={increaseSpeed}
        disabled={speed >= MAX_SPEED}
        aria-label="Increase speed"
        type="button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    </div>
  </div>
</div>

<style>
  .controls-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-shrink: 0;
    padding: 0 clamp(12px, 3vw, 24px);
    box-sizing: border-box;
  }

  .speed-control {
    display: flex;
    align-items: center;
    gap: clamp(12px, 3vw, 20px);
    padding: clamp(10px, 2.5vw, 16px) clamp(12px, 3vw, 20px);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: clamp(12px, 3vw, 16px);
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    box-sizing: border-box;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
    -webkit-tap-highlight-color: transparent;
  }

  /* Only apply hover effects on devices with hover capability (not touch) */
  @media (hover: hover) and (pointer: fine) {
    .speed-control:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
    }
  }

  .speed-control:active {
    background: rgba(255, 255, 255, 0.1);
  }

  .speed-label {
    font-size: clamp(10px, 2.5vw, 12px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .speed-buttons {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(12px, 3vw, 16px);
  }

  .speed-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(36px, 9vw, 44px);
    height: clamp(36px, 9vw, 44px);
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    -webkit-tap-highlight-color: transparent;
  }

  .speed-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    background: rgba(255, 255, 255, 0.1);
  }

  @media (hover: hover) and (pointer: fine) {
    .speed-btn:not(:disabled):hover {
      transform: scale(1.1);
      box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.3),
        0 0 0 4px rgba(59, 130, 246, 0.2);
    }
  }

  .speed-btn:not(:disabled):active {
    transform: scale(0.95);
  }

  .speed-value {
    font-size: clamp(14px, 3.5vw, 16px);
    font-weight: 700;
    color: #ffffff;
    min-width: clamp(60px, 15vw, 80px);
    text-align: center;
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 8px;
    transition: all 0.2s ease;
    -webkit-tap-highlight-color: transparent;
  }

  @media (hover: hover) and (pointer: fine) {
    .speed-value:hover {
      background: rgba(255, 255, 255, 0.1);
      transform: scale(1.05);
    }
  }

  .speed-value:active {
    transform: scale(0.98);
    background: rgba(255, 255, 255, 0.15);
  }

  .speed-input {
    font-size: clamp(14px, 3.5vw, 16px);
    font-weight: 700;
    color: #ffffff;
    min-width: clamp(60px, 15vw, 80px);
    width: clamp(60px, 15vw, 80px);
    text-align: center;
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
    background: rgba(59, 130, 246, 0.2);
    border: 2px solid #3b82f6;
    border-radius: 8px;
    padding: 4px 8px;
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    transition: all 0.2s ease;
  }

  .speed-input:focus {
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
    border-color: #2563eb;
  }

  /* Hide number input spinners */
  .speed-input::-webkit-outer-spin-button,
  .speed-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .speed-input[type="number"] {
    -moz-appearance: textfield;
    appearance: textfield;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .controls-container {
      padding: 0 16px;
    }
  }

  @media (max-width: 480px) {
    .controls-container {
      padding: 0 12px;
    }

    .speed-control {
      gap: clamp(8px, 2vw, 12px);
    }
  }

  /* Very narrow viewports */
  @media (max-width: 360px) {
    .speed-label {
      font-size: 9px;
      letter-spacing: 0.3px;
    }

    .speed-value {
      font-size: 12px;
      min-width: 55px;
    }

    .speed-btn {
      width: 32px;
      height: 32px;
    }

    .speed-btn svg {
      width: 16px;
      height: 16px;
    }
  }

  /* Landscape mobile: More compact */
  @media (max-height: 500px) and (orientation: landscape) {
    .speed-control {
      padding: 8px 12px;
      gap: 8px;
    }

    .speed-btn {
      width: 32px;
      height: 32px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .speed-control,
    .speed-btn {
      transition: none;
    }

    .speed-btn:not(:disabled):hover,
    .speed-btn:not(:disabled):active {
      transform: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .speed-control {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.4);
    }

    .speed-label,
    .speed-value {
      color: #ffffff;
    }

    .speed-btn:not(:disabled) {
      border: 2px solid rgba(255, 255, 255, 0.3);
    }
  }
</style>
