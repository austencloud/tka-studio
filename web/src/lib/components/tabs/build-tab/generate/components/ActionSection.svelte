<!--
ActionSection.svelte - Action buttons for generation operations
Updated to convert config format and handle real generation
-->
<script lang="ts">
  import type { GenerationConfig } from "$lib/state/generate/generate-config.svelte";
  import type { GenerationConfig as ActionsGenerationConfig } from "$lib/state/generate/generate-actions.svelte";
  import {
    GridMode,
    DifficultyLevel,
    PropContinuity,
    GenerationMode,
    LetterType,
  } from "$lib/domain/enums";

  interface Props {
    onAutoCompleteClicked: () => void;
    onGenerateClicked: (config: ActionsGenerationConfig) => Promise<void>;
    config: GenerationConfig;
    isGenerating: boolean;
  }

  let {
    onAutoCompleteClicked,
    onGenerateClicked,
    config,
    isGenerating,
  }: Props = $props();

  /**
   * Convert GenerationConfig to ActionsGenerationConfig format
   */
  function convertConfig(config: GenerationConfig): ActionsGenerationConfig {
    // Convert letter types from Set<LetterType> to string[]
    const letterTypes: string[] = [];
    config.letterTypes.forEach((type) => {
      switch (type) {
        case LetterType.TYPE1:
          letterTypes.push("Dual-Shift");
          break;
        case LetterType.TYPE2:
          letterTypes.push("Shift");
          break;
        case LetterType.TYPE3:
          letterTypes.push("Cross-Shift");
          break;
        case LetterType.TYPE4:
          letterTypes.push("Dash");
          break;
        case LetterType.TYPE5:
          letterTypes.push("Dual-Dash");
          break;
        case LetterType.TYPE6:
          letterTypes.push("Static");
          break;
      }
    });

    // Convert difficulty level to string
    let difficulty: "beginner" | "intermediate" | "advanced";
    switch (config.level) {
      case 1:
        difficulty = "beginner";
        break;
      case 2:
        difficulty = "intermediate";
        break;
      case 3:
        difficulty = "advanced";
        break;
      default:
        difficulty = "intermediate";
    }

    return {
      mode: GenerationMode.FREEFORM, // Default to freeform mode
      length: config.length,
      gridMode:
        config.gridMode === GridMode.DIAMOND ? GridMode.DIAMOND : GridMode.BOX,
      propType: "fan", // Default prop type
      difficulty: difficulty as DifficultyLevel,
      propContinuity:
        config.propContinuity.toLowerCase() === "continuous"
          ? PropContinuity.CONTINUOUS
          : PropContinuity.RANDOM,
      turnIntensity: config.turnIntensity,
      letterTypes,
    };
  }

  /**
   * Handle generate button click with proper config conversion
   */
  async function handleGenerateClick() {
    const convertedConfig = convertConfig(config);
    console.log("🔄 Converting config:", {
      original: config,
      converted: convertedConfig,
    });
    await onGenerateClicked(convertedConfig);
  }
</script>

<div class="action-section">
  <button
    class="action-button secondary"
    onclick={() => onAutoCompleteClicked()}
    disabled={isGenerating}
    type="button"
  >
    Auto-Complete
  </button>

  <button
    class="action-button primary"
    onclick={handleGenerateClick}
    disabled={isGenerating}
    type="button"
  >
    {isGenerating ? "Generating..." : "Generate New"}
  </button>
</div>

<!-- Error display if generation fails -->
{#if config && !isGenerating}
  <div class="config-summary">
    <small>
      {config.length} beats • {config.gridMode.toLowerCase()} • Level {config.level}
      • {config.letterTypes.size} types selected
    </small>
  </div>
{/if}

<style>
  .action-section {
    flex-shrink: 0;
    display: flex;
    gap: var(--element-spacing);
    padding-top: var(--element-spacing);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-direction: column;
  }

  .action-button {
    flex: 1;
    min-height: var(--min-touch-target);
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .action-button.secondary {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.9);
  }

  .action-button.secondary:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .action-button.primary {
    background: rgba(70, 130, 255, 0.8);
    border: 1px solid rgba(70, 130, 255, 0.9);
    color: white;
  }

  .action-button.primary:hover:not(:disabled) {
    background: rgba(80, 140, 255, 0.9);
    border-color: rgba(80, 140, 255, 1);
  }

  .config-summary {
    padding: 8px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    text-align: center;
  }

  .config-summary small {
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
  }

  /* Responsive layouts */
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
      flex-direction: column;
    }

    .action-button {
      min-height: calc(var(--min-touch-target) * 1.1) !important;
      font-size: 16px !important;
    }
  }
</style>
