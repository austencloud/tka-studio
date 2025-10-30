<!--
  RemoveBeatButton.svelte

  Remove beat button for ButtonPanel.
  Removes the selected beat and all following beats.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  const {
    beatNumber,
    onclick
  }: {
    beatNumber: number;
    onclick?: () => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  function handleClick() {
    hapticService?.trigger("warning");
    onclick?.();
  }
</script>

<button
  class="panel-button remove-beat-button"
  onclick={handleClick}
  aria-label="Remove Beat {beatNumber} and all following beats"
  title="Remove Beat {beatNumber} and all following beats"
>
  <i class="fa-solid fa-trash" aria-hidden="true"></i>
</button>

<style>
  .panel-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
    font-size: 18px;
    color: #ffffff;

    /* Base button styling */
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .panel-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .panel-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .panel-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  .remove-beat-button {
    background: linear-gradient(135deg, #ff9800 0%, #ff6b00 100%);
    border-color: rgba(255, 152, 0, 0.3);
    box-shadow: 0 4px 12px rgba(255, 152, 0, 0.4);
  }

  .remove-beat-button:hover {
    background: linear-gradient(135deg, #ff6b00 0%, #ff5500 100%);
    box-shadow: 0 6px 16px rgba(255, 152, 0, 0.6);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .panel-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 480px) {
    .panel-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
      font-size: 14px;
    }
  }

  @media (max-width: 320px) {
    .panel-button {
      width: 44px; /* NEVER below 44px for accessibility */
      height: 44px;
      font-size: 12px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Maintain 44px minimum for accessibility */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .panel-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
      font-size: 14px;
    }
  }
</style>
