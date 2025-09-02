<!--
ModeLayoutSection.svelte - Mode and layout configuration settings
Contains Grid Mode, Generation Mode, and Prop Continuity selectors
-->
<script lang="ts">
  import { GenerationMode } from "$domain";
  import type { GenerationConfig } from "$state";
  import GenerationModeToggle from "../selectors/GenerationModeToggle.svelte";
  import GridModeSelector from "../selectors/GridModeSelector.svelte";
  import PropContinuityToggle from "../selectors/PropContinuityToggle.svelte";

  interface Props {
    config: GenerationConfig;
  }

  let { config }: Props = $props();
</script>

<section class="settings-section">
  <h4 class="section-title">Mode & Layout</h4>
  <div class="settings-grid">
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
  </div>
</section>

<style>
  .settings-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-height: auto;
  }

  .section-title {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 6px;
  }

  .settings-grid {
    display: grid;
    gap: var(--element-spacing);
    grid-template-columns: 1fr;
    align-content: start;
  }

  .setting-item {
    border-radius: 6px;
    padding: var(--element-spacing);
    transition: background-color 0.2s ease;
    min-height: var(--min-touch-target);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .setting-item:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  /* Responsive layouts */
  :global(.generate-panel[data-layout="comfortable"]) .settings-grid {
    grid-template-columns: 1fr;
    gap: calc(var(--element-spacing) * 1.25);
  }

  :global(.generate-panel[data-layout="comfortable"]) .setting-item {
    padding: calc(var(--element-spacing) * 1.25);
    min-height: calc(var(--min-touch-target) * 1.2);
  }

  :global(.generate-panel[data-layout="spacious"]) .settings-grid {
    grid-template-columns: 1fr;
    gap: calc(var(--element-spacing) * 1.5);
  }

  :global(.generate-panel[data-layout="spacious"]) .setting-item {
    padding: calc(var(--element-spacing) * 1.5);
    min-height: calc(var(--min-touch-target) * 1.4);
  }

  :global(.generate-panel[data-layout="compact"]) .settings-grid {
    grid-template-columns: 1fr;
    gap: calc(var(--element-spacing) * 0.75);
  }

  :global(.generate-panel[data-layout="compact"]) .setting-item {
    padding: calc(var(--element-spacing) * 0.75);
    min-height: calc(var(--min-touch-target) * 0.8);
  }

  /* Large desktop optimization */
  @media (min-width: 1440px) {
    :global(.generate-panel[data-layout="compact"]) .settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    :global(.generate-panel[data-layout="spacious"]) .settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .settings-grid {
      grid-template-columns: 1fr !important;
    }
  }

  /* Child component styling */
  .setting-item :global(.grid-mode-selector) {
    width: 100%;
  }

  .setting-item :global(.level-button) {
    min-height: calc(var(--min-touch-target) * 0.8);
    min-width: calc(var(--min-touch-target) * 0.8);
  }

  .setting-item :global(.value-display) {
    min-height: calc(var(--min-touch-target) * 0.6);
    min-width: calc(var(--min-touch-target) * 0.8);
  }
</style>
