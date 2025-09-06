<!--
SettingsContainer.svelte - Container for all settings controls
Handles the responsive layout and scrolling behavior
All individual controls are evenly spaced throughout the container
-->
<script lang="ts">
  import { DifficultyLevel, GenerationMode } from "$shared/domain";
  import type { GenerationConfig } from "../state/generate-config.svelte";
  import CAPTypeSelector from "./selectors/CAPTypeSelector.svelte";
  import GenerationModeToggle from "./selectors/GenerationModeToggle.svelte";
  import GridModeSelector from "./selectors/GridModeSelector.svelte";
  import LengthSelector from "./selectors/LengthSelector.svelte";
  import LetterTypeSelector from "./selectors/LetterTypeSelector.svelte";
  import LevelSelector from "./selectors/LevelSelector.svelte";
  import PropContinuityToggle from "./selectors/PropContinuityToggle.svelte";
  import SliceSizeSelector from "./selectors/SliceSizeSelector.svelte";
  import TurnIntensitySelector from "./selectors/TurnIntensitySelector.svelte";

  interface Props {
    config: GenerationConfig;
    isFreeformMode: boolean;
  }

  let { config, isFreeformMode }: Props = $props();

  // Convert number level to DifficultyLevel enum
  function levelToDifficulty(level: number): DifficultyLevel {
    switch (level) {
      case 1: return DifficultyLevel.BEGINNER;
      case 2: return DifficultyLevel.INTERMEDIATE;
      case 3: return DifficultyLevel.ADVANCED;
      default: return DifficultyLevel.INTERMEDIATE;
    }
  }
</script>

<div class="settings-container">
  <!-- Core Sequence Settings -->
  <div class="setting-item">
    <LevelSelector initialValue={levelToDifficulty(config.level)} />
  </div>

  <div class="setting-item">
    <LengthSelector initialValue={config.length} />
  </div>

  <div class="setting-item">
    <TurnIntensitySelector initialValue={config.turnIntensity} />
  </div>

  <!-- Mode & Layout Settings -->
  <div class="setting-item">
    <GridModeSelector initialMode={config.gridMode} />
  </div>

  <div class="setting-item">
    <GenerationModeToggle
      initialMode={config.mode === GenerationMode.FREEFORM
        ? GenerationMode.FREEFORM
        : GenerationMode.CIRCULAR}
    />
  </div>

  <div class="setting-item">
    <PropContinuityToggle initialValue={config.propContinuity} />
  </div>

  <!-- Mode-Specific Settings -->
  {#if isFreeformMode}
    <div class="setting-item">
      <LetterTypeSelector initialValue={config.letterTypes} />
    </div>
  {:else}
    <div class="setting-item">
      <SliceSizeSelector initialValue={config.sliceSize} />
    </div>

    <div class="setting-item">
      <CAPTypeSelector initialValue={config.capType} />
    </div>
  {/if}
</div>

<style>
  .settings-container {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    min-height: 0; /* Allow proper overflow handling */
    padding: calc(var(--element-spacing) * 1.5);

    /* Single glassmorphism card for the entire container */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.05),
      rgba(255, 255, 255, 0.02)
    );
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .setting-item {
    /* Simple centered row - no individual cards */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: var(--min-touch-target, 44px);
    transition: opacity 0.2s ease;
  }

  .setting-item:hover {
    opacity: 0.8;
  }

  /* Responsive layouts */
  :global(.generate-panel[data-layout="spacious"]) .settings-container {
    padding: calc(var(--element-spacing) * 2);
  }

  :global(.generate-panel[data-layout="compact"]) .settings-container {
    padding: var(--element-spacing);
  }

  /* Ensure no scrolling is forced when not appropriate */
  :global(.generate-panel[data-allow-scroll="false"]) .settings-container {
    overflow: hidden;
    flex: 1;
    min-height: 0;
    /* Ensure flex doesn't expand beyond container */
    max-height: 100%;
  }
</style>
