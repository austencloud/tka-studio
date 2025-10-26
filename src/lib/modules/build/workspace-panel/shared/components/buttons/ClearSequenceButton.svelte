<!--
  ClearSequencePanelButton.svelte

  Clear sequence button for ButtonPanel (panel-style, not floating).
  Clears the entire sequence when clicked.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  const {
    onclick
  }: {
    onclick?: () => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  function handleClick() {
    hapticService?.trigger("selection");
    onclick?.();
  }
</script>

<button
  class="panel-button clear-button"
  onclick={handleClick}
  aria-label="Clear sequence"
  title="Clear sequence"
>
  <i class="fa-solid fa-broom" aria-hidden="true"></i>
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
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  .clear-button {
    background: rgba(239, 68, 68, 0.8);
    border-color: rgba(248, 113, 113, 0.3);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  .clear-button:hover {
    background: rgba(239, 68, 68, 0.9);
    box-shadow: 0 6px 16px rgba(239, 68, 68, 0.6);
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
      width: 40px;
      height: 40px;
      font-size: 14px;
    }
  }

  @media (max-width: 320px) {
    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 12px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Compact buttons for Z Fold 5 horizontal (882x344) */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 14px;
    }
  }
</style>
