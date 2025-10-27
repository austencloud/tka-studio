<!--
ActionSection.svelte - Action buttons for generation operations
Refactored to use config-mapper utility for clean type-safe conversions
Uses consistent spacing via --element-spacing CSS variable from parent
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { GenerationOptions } from "../shared/domain";
  import type { UIGenerationConfig } from "../shared/utils/config-mapper";
  import { uiConfigToGenerationOptions } from "../shared/utils/config-mapper";

  let {
    onGenerateClicked,
    config,
    isGenerating,
  } = $props<{
    onGenerateClicked: (options: GenerationOptions) => Promise<void>;
    config: UIGenerationConfig;
    isGenerating: boolean;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  /**
   * Handle generate button click with proper config conversion
   */
  async function handleGenerateClick() {
    hapticService?.trigger("selection");

    // Use mapper utility for clean, type-safe conversion
    const generationOptions = uiConfigToGenerationOptions(config, "fan");

    await onGenerateClicked(generationOptions);
  }

</script>

<div class="action-section">
  <button
    class="action-button primary"
    onclick={handleGenerateClick}
    disabled={isGenerating}
    type="button"
  >
    {isGenerating ? "Generating..." : "Generate New"}
  </button>
</div>

<style>
  .action-section {
    flex-shrink: 0;
    display: flex;
    gap: var(--element-spacing);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: var(--element-spacing);
    flex-direction: row;
  }

  .action-button {
    flex: 1;
    min-height: var(--min-touch-target);
    padding: 12px 20px;
    border: none;

    /* Modern 16px border-radius */
    border-radius: 16px;

    font-size: 14px;
    font-weight: 600;
    cursor: pointer;

    /* Smooth cubic-bezier transition */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    /* Layered shadows for depth */
    box-shadow:
      0 1px 2px hsl(0deg 0% 0% / 0.12),
      0 2px 4px hsl(0deg 0% 0% / 0.12),
      0 4px 8px hsl(0deg 0% 0% / 0.12);
  }

  .action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .action-button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;

    /* Add pulsing glow animation - moved from CAP card */
    animation: generateButtonGlow 3s ease-in-out infinite;
  }

  .action-button.primary:hover:not(:disabled) {
    filter: brightness(1.15);
    transform: translateY(-3px) scale(1.02);

    /* Enhanced elevation with stronger glow on hover */
    box-shadow:
      0 0 25px rgba(102, 126, 234, 0.8),
      0 0 50px rgba(102, 126, 234, 0.6),
      0 4px 16px rgba(0, 0, 0, 0.2);
  }

  /* Pulsing glow animation - makes Generate button the star of the show */
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

  /* Responsive layouts - spacing controlled by parent's --element-spacing */
  :global(.generate-panel[data-layout="comfortable"]) .action-button {
    min-height: calc(var(--min-touch-target) * 1.1);
    font-size: 16px;
  }

  :global(.generate-panel[data-layout="spacious"]) .action-button {
    min-height: calc(var(--min-touch-target) * 1.3);
    font-size: 16px;
  }

  :global(.generate-panel[data-layout="compact"]) .action-button {
    min-height: var(--min-touch-target);
    font-size: 13px;
    padding: 8px 16px;
  }

  /* High DPI display adjustments */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .action-button {
      border-width: 0.5px;
    }
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .action-section {
      flex-direction: row;
    }

    .action-button {
      min-height: calc(var(--min-touch-target) * 1.1) !important;
      font-size: 16px !important;
    }
  }

  /* 🎯 EXTREME CONSTRAINTS: Ultra-compact mode for landscape mobile */
  /* Matches app's isLandscapeMobile() criteria: aspectRatio > 1.7 AND height < 500px */
  /* This targets devices like Z Fold 5 in horizontal orientation (882x344) */
  /* Excludes portrait mode (344x882) which has aspectRatio 0.39 < 1.7 */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .action-section {
      padding-top: calc(var(--element-spacing) * 0.5);
      gap: calc(var(--element-spacing) * 0.5);
    }

    .action-button {
      min-height: 36px;
      padding: 6px 12px;
      font-size: 12px;
      border-radius: 12px;
    }
  }

  /* When in very narrow landscape (like Z Fold horizontal), stack vertically */
  @media (max-width: 500px) and (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .action-section {
      flex-direction: column;
      gap: calc(var(--element-spacing) * 0.4);
      padding-top: calc(var(--element-spacing) * 0.4);
    }

    .action-button {
      min-height: 32px;
      padding: 6px 10px;
      font-size: 11px;
    }
  }
</style>
