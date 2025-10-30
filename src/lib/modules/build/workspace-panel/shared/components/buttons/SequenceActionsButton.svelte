<!--
  SequenceActionsButton.svelte

  Opens a sheet with various sequence actions (Animate, Mirror, Rotate, etc.)
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared/application/services/contracts";
  import { resolve, TYPES } from "$shared/inversify";

  let {
    onclick,
  } = $props<{
    onclick?: () => void;
  }>();

  // Resolve haptic feedback service
  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleClick() {
    hapticService?.trigger("selection");
    onclick?.();
  }
</script>

<button
  class="sequence-actions-button glass-button"
  onclick={handleClick}
  aria-label="Sequence actions"
  title="Sequence actions"
>
  <i class="fas fa-tools"></i>
</button>

<style>
  .sequence-actions-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
    border-radius: 50%;
    color: #ffffff;
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
  }

  .sequence-actions-button:hover {
    background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(6, 182, 212, 0.6);
  }

  .sequence-actions-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .sequence-actions-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  .sequence-actions-button i {
    font-size: 18px;
  }

  /* Mobile responsive - 44px minimum per iOS/Android guidelines */
  @media (max-width: 768px) {
    .sequence-actions-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 480px) {
    .sequence-actions-button {
      width: 44px; /* Maintain 44px minimum */
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 320px) {
    .sequence-actions-button {
      width: 44px; /* NEVER below 44px for accessibility */
      height: 44px;
      font-size: 14px;
    }
  }

  /* Landscape mobile: Maintain 44px minimum */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .sequence-actions-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
    }

    .sequence-actions-button i {
      font-size: 16px;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .sequence-actions-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid rgba(255, 255, 255, 0.5);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .sequence-actions-button {
      transition: none;
    }

    .sequence-actions-button:hover {
      transform: none;
    }

    .sequence-actions-button:active {
      transform: none;
    }
  }
</style>
