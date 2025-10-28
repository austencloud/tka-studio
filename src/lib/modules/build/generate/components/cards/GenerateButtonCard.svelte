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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;

    /* Pulsing glow animation */
    animation: generateButtonGlow 3s ease-in-out infinite;

    /* Layered shadows for depth */
    box-shadow:
      0 1px 2px hsl(0deg 0% 0% / 0.12),
      0 2px 4px hsl(0deg 0% 0% / 0.12),
      0 4px 8px hsl(0deg 0% 0% / 0.12);
  }

  .button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .generate-button-card:hover:not(:disabled) {
    filter: brightness(1.15);
    transform: translateY(-3px) scale(1.02);
    box-shadow:
      0 0 25px rgba(102, 126, 234, 0.8),
      0 0 50px rgba(102, 126, 234, 0.6),
      0 4px 16px rgba(0, 0, 0, 0.2);
  }

  .generate-button-card:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  @keyframes generateButtonGlow {
    0%, 100% {
      box-shadow:
        0 0 15px rgba(102, 126, 234, 0.5),
        0 0 30px rgba(102, 126, 234, 0.3),
        0 2px 8px rgba(0, 0, 0, 0.15);
    }
    50% {
      box-shadow:
        0 0 25px rgba(118, 75, 162, 0.7),
        0 0 50px rgba(118, 75, 162, 0.5),
        0 4px 12px rgba(0, 0, 0, 0.2);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .generate-button-card {
      animation: none;
    }
  }
</style>
