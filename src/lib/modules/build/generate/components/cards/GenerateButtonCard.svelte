<!--
GenerateButtonCard.svelte - Generate button as a card in the grid
Integrates the "Generate New" button into the card grid layout so it scales with other cards
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import { uiConfigToGenerationOptions } from "../../shared/utils/config-mapper";
  import type { UIGenerationConfig } from "../../state/generate-config.svelte";

  let {
    isGenerating,
    onGenerateClicked,
    config,
  } = $props<{
    isGenerating: boolean;
    onGenerateClicked: (options: any) => Promise<void>;
    config: UIGenerationConfig;
  }>();

  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  async function handleClick() {
    hapticService?.trigger("selection");
    const generationOptions = uiConfigToGenerationOptions(config, "fan");
    await onGenerateClicked(generationOptions);
  }
</script>

<button
  class="generate-button-card"
  onclick={handleClick}
  disabled={isGenerating}
  type="button"
  aria-label={isGenerating ? "Generating..." : "Generate New"}
>
  <div class="button-content">
    {isGenerating ? "Generating..." : "Generate New"}
  </div>
</button>

<style>
  .generate-button-card {
    width: 100%;
    height: 100%;
    padding: 0;
    border: none;

    /* 🟢 PURE GREEN MONOCHROMATIC: Green = GO psychology (no gold/yellow distraction) */
    background: linear-gradient(135deg,
      #059669 0%,      /* Emerald 600 - Deep green */
      #10b981 25%,     /* Emerald 500 - Main green */
      #34d399 50%,     /* Emerald 400 - Bright green */
      #10b981 75%,     /* Emerald 500 - Main green */
      #059669 100%     /* Emerald 600 - Deep green */
    );
    background-size: 300% 300%;

    /* Flowing gradient animation + subtle pulse (NO glow animation to prevent overlay) */
    animation:
      meshGradientFlow 8s ease infinite,
      subtlePulse 2s ease-in-out infinite;

    border: 3px solid rgba(255, 255, 255, 0.4);
    color: white;
    border-radius: 20px;

    /* 🎯 BIGGER TEXT - scales with container, no uppercase */
    font-size: clamp(20px, 5cqi, 40px);
    font-weight: 800;
    letter-spacing: 0.3px;
    text-shadow:
      0 2px 6px rgba(0, 0, 0, 0.5),
      0 0 20px rgba(255, 255, 255, 0.2);

    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;

    /* 🔥 CONTAINED glow - stays within button boundaries */
    box-shadow:
      0 4px 12px rgba(5, 150, 105, 0.4),
      0 2px 6px rgba(0, 0, 0, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.3),
      inset 0 -1px 0 rgba(0, 0, 0, 0.2);
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .generate-button-card:hover:not(:disabled) {
    filter: brightness(1.2) saturate(1.15);
    transform: translateY(-4px) scale(1.03);

    /* 🌟 ENHANCED but CONTAINED glow - no overlay on other cards */
    box-shadow:
      0 8px 20px rgba(5, 150, 105, 0.6),
      0 4px 12px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.4),
      inset 0 -1px 0 rgba(0, 0, 0, 0.3);

    /* Enhance text glow on hover */
    text-shadow:
      0 2px 6px rgba(0, 0, 0, 0.6),
      0 0 25px rgba(255, 255, 255, 0.4);

    /* Speed up animations on hover for urgency */
    animation-duration: 6s, 1.5s;
  }

  .generate-button-card:active:not(:disabled) {
    transform: scale(0.98);
    transition: all 0.1s ease;
  }

  .generate-button-card:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    animation: none;
    filter: grayscale(0.5);
  }

  /* Mobile: Disable Y-axis translation, use only press effect */
  @media (max-width: 768px) {
    .generate-button-card:hover:not(:disabled) {
      transform: none;
      filter: none;
    }

    .generate-button-card:focus:not(:disabled) {
      transform: none;
    }
  }

  /* 🌈 Mesh Gradient Flow - Organic flowing green colors */
  @keyframes meshGradientFlow {
    0%, 100% {
      background-position: 0% 50%;
    }
    25% {
      background-position: 50% 100%;
    }
    50% {
      background-position: 100% 50%;
    }
    75% {
      background-position: 50% 0%;
    }
  }

  /* 💓 Subtle Pulse - Mimics heartbeat for subconscious urgency */
  @keyframes subtlePulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.015);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .generate-button-card {
      animation: meshGradientFlow 8s ease infinite;
    }
  }
</style>
