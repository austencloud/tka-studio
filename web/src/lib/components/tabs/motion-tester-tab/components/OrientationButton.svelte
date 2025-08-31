<!--
OrientationButton.svelte - Button-style orientation selector with modal

Shows a button that opens a modal for orientation selection when clicked.
Matches the visual style of the calculated end orientation for consistency.
-->
<script lang="ts">
  import type { Orientation } from "$domain";
  import OrientationModal from "./OrientationModal.svelte";

  interface Props {
    selectedOrientation: Orientation;
    onOrientationChange: (orientation: Orientation) => void;
    label: string;
    color: string;
    disabled?: boolean;
  }

  let {
    selectedOrientation,
    onOrientationChange,
    label,
    color,
    disabled = false,
  }: Props = $props();

  let showModal = $state(false);
  let buttonElement = $state<HTMLButtonElement>();

  function openModal() {
    if (disabled) return;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (disabled) return;

    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openModal();
    }
  }
</script>

<div class="orientation-button-container">
  <div class="orientation-label">{label}</div>
  <button
    bind:this={buttonElement}
    class="orientation-button"
    class:disabled
    class:interactive={!disabled}
    style="--accent-color: {color}"
    onclick={openModal}
    onkeydown={handleKeyDown}
    {disabled}
    aria-label={disabled
      ? `${label} orientation: ${selectedOrientation.toUpperCase()}`
      : `Click to select ${label} orientation. Current: ${selectedOrientation.toUpperCase()}`}
    title={disabled
      ? `${selectedOrientation.toUpperCase()} (calculated)`
      : `Click to select orientation. Current: ${selectedOrientation.toUpperCase()}`}
  >
    <span class="orientation-value">{selectedOrientation.toUpperCase()}</span>
  </button>
</div>

{#if showModal && !disabled}
  <OrientationModal
    {selectedOrientation}
    {onOrientationChange}
    onClose={closeModal}
    {color}
    triggerElement={buttonElement}
  />
{/if}

<style>
  .orientation-button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .orientation-label {
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .orientation-button {
    background: rgba(var(--accent-color), 0.1);
    border: 1px solid rgba(var(--accent-color), 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12px;
    font-weight: 600;
    color: rgba(var(--accent-color), 0.9);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    min-width: 80px;
    text-align: center;
    transition: all 0.2s ease;
    cursor: default;
  }

  .orientation-button.interactive {
    cursor: pointer;
    background: rgba(var(--accent-color), 0.15);
    border-color: rgba(var(--accent-color), 0.4);
  }

  .orientation-button.interactive:hover {
    background: rgba(var(--accent-color), 0.25);
    border-color: rgba(var(--accent-color), 0.6);
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(var(--accent-color), 0.3);
  }

  .orientation-button.interactive:active {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(var(--accent-color), 0.2);
  }

  .orientation-button.disabled {
    opacity: 0.7;
    background: rgba(var(--accent-color), 0.05);
    border-color: rgba(var(--accent-color), 0.2);
    color: rgba(var(--accent-color), 0.6);
    cursor: not-allowed;
  }

  .orientation-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.5);
  }

  .orientation-value {
    line-height: 1;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .orientation-button {
      padding: 10px 14px;
      font-size: 11px;
      min-width: 70px;
    }
  }

  @media (max-width: 480px) {
    .orientation-button {
      padding: 8px 12px;
      font-size: 10px;
      min-width: 60px;
    }
  }
</style>
