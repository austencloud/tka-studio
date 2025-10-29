<!--
  ShareButton.svelte

  Opens the share sheet from the ButtonPanel. Highlights when the sheet is visible.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  const {
    onclick,
    isActive = false,
    disabled = false,
  }: {
    onclick?: () => void;
    isActive?: boolean;
    disabled?: boolean;
  } = $props();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  function handleClick() {
    if (disabled) return;
    hapticService?.trigger(isActive ? "navigation" : "selection");
    onclick?.();
  }
</script>

<button
  class="panel-button share-button"
  class:active={isActive}
  onclick={handleClick}
  aria-pressed={isActive}
  aria-label={isActive ? "Close share panel" : "Open share panel"}
  title="Share"
  disabled={disabled}
>
  <i class="fas fa-share-nodes" aria-hidden="true"></i>
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

    background: linear-gradient(135deg, rgba(139, 92, 246, 0.9), rgba(236, 72, 153, 0.9));
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow:
      0 2px 8px rgba(79, 70, 229, 0.35),
      0 6px 18px rgba(236, 72, 153, 0.25);
  }

  .panel-button:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow:
      0 4px 12px rgba(79, 70, 229, 0.45),
      0 8px 22px rgba(236, 72, 153, 0.35);
  }

  .panel-button:active:not(:disabled) {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .panel-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  .panel-button:disabled {
    opacity: 0.45;
    cursor: not-allowed;
    box-shadow: none;
  }

  .share-button.active {
    background: linear-gradient(135deg, rgba(139, 92, 246, 1), rgba(236, 72, 153, 1));
    box-shadow:
      0 4px 14px rgba(79, 70, 229, 0.55),
      0 10px 26px rgba(236, 72, 153, 0.4);
  }

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

  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .panel-button {
      width: 36px;
      height: 36px;
      font-size: 14px;
    }
  }
</style>
