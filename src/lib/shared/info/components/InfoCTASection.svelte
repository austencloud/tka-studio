<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  let {
    ctaLabel,
    onEnterStudio = () => {},
  }: {
    ctaLabel: string;
    onEnterStudio?: () => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClick() {
    // Trigger haptic feedback for CTA button
    hapticService?.trigger("selection");
    onEnterStudio();
  }
</script>

<div class="cta-section">
  <button class="cta-button" type="button" onclick={handleClick}>
    <i class="fas fa-rocket"></i>
    {ctaLabel}
  </button>
</div>

<style>
  .cta-section {
    flex-shrink: 0;
    padding: clamp(0.375rem, 1vh, 0.5rem) 0;
    text-align: center;
  }

  .cta-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: clamp(0.625rem, 1.5vh, 0.875rem) clamp(1.25rem, 3.5vw, 2rem);
    width: 100%;
    max-width: 360px;
    min-height: 44px;
    margin: 0 auto;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 1.25rem;
    font-size: clamp(0.9375rem, 3vw, 1.125rem);
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  }

  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(102, 126, 234, 0.6);
  }

  .cta-button:active {
    transform: translateY(0);
  }

  .cta-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  .cta-button i {
    font-size: clamp(1rem, 2.75vw, 1.25rem);
  }

  @media (max-height: 700px) {
    .cta-section {
      padding: 0.375rem 0;
    }

    .cta-button {
      min-height: 44px;
      padding: 0.625rem 1.25rem;
      font-size: clamp(0.875rem, 3vw, 1rem);
      gap: 0.5rem;
    }

    .cta-button i {
      font-size: clamp(0.875rem, 2.5vw, 1rem);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .cta-button:hover,
    .cta-button:active {
      transform: none;
    }
  }
</style>
