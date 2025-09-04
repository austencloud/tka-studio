<!--
ModeSpecificSection.svelte - Mode-specific configuration settings
Shows different options based on generation mode (freeform vs circular)
-->
<script lang="ts">
  import type { GenerationConfig } from "$lib/state/build/generate/generate-config.svelte";
  import CAPTypeSelector from "../selectors/CAPTypeSelector.svelte";
  import LetterTypeSelector from "../selectors/LetterTypeSelector.svelte";
  import SliceSizeSelector from "../selectors/SliceSizeSelector.svelte";

  interface Props {
    config: GenerationConfig;
    isFreeformMode: boolean;
  }

  let { config, isFreeformMode }: Props = $props();
</script>

<section class="settings-section mode-specific-section">
  {#if isFreeformMode}
    <h4 class="section-title">Filter Options</h4>
    <div class="settings-grid">
      <div class="setting-item full-width">
        <LetterTypeSelector initialValue={config.letterTypes} />
      </div>
    </div>
  {:else}
    <h4 class="section-title">Circular Mode Options</h4>
    <div class="settings-grid">
      <div class="setting-item">
        <SliceSizeSelector initialValue={config.sliceSize} />
      </div>
      <div class="setting-item">
        <CAPTypeSelector initialValue={config.capType} />
      </div>
    </div>
  {/if}
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
    transition: grid-template-rows 0.2s ease-out;
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

  .setting-item.full-width {
    grid-column: 1 / -1;
  }

  /* Ensure consistent height for mode-specific section */
  .mode-specific-section {
    min-height: 120px; /* Reserve space to prevent layout shift */
    transition: height 0.2s ease-out;
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

  /* Large desktop optimization - only for sections without full-width items */
  @media (min-width: 1440px) {
    :global(.generate-panel[data-layout="compact"])
      .settings-section:not(:has(.full-width))
      .settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    :global(.generate-panel[data-layout="spacious"])
      .settings-section:not(:has(.full-width))
      .settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .settings-grid {
      grid-template-columns: 1fr !important;
    }
  }
</style>
