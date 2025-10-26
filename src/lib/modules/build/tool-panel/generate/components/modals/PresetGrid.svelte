<!--
PresetGrid.svelte - Grid layout for preset cards
Displays a list of presets in a scrollable grid layout
-->
<script lang="ts">
  import type { GenerationPreset } from "../../state/preset.svelte";
  import PresetCard from "./PresetCard.svelte";

  let {
    presets,
    onPresetSelect,
    onPresetEdit,
    onPresetDelete
  } = $props<{
    presets: GenerationPreset[];
    onPresetSelect: (preset: GenerationPreset) => void;
    onPresetEdit: (preset: GenerationPreset) => void;
    onPresetDelete: (presetId: string) => void;
  }>();
</script>

{#if presets.length === 0}
  <div class="empty-state">
    <div class="empty-icon">📋</div>
    <div class="empty-text">No saved presets yet</div>
    <div class="empty-hint">Save your current settings to create a preset</div>
  </div>
{:else}
  <div class="preset-list">
    {#each presets as preset (preset.id)}
      <PresetCard
        {preset}
        onSelect={onPresetSelect}
        onEdit={onPresetEdit}
        onDelete={onPresetDelete}
      />
    {/each}
  </div>
{/if}

<style>
  .preset-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px 24px;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
  }

  /* Scrollbar styling */
  .preset-list::-webkit-scrollbar {
    width: 8px;
  }

  .preset-list::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
  }

  .preset-list::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .preset-list::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 24px;
    text-align: center;
    color: white;
  }

  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.5;
  }

  .empty-text {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
    color: rgba(255, 255, 255, 0.9);
  }

  .empty-hint {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
  }

  @media (max-width: 640px) {
    .preset-list {
      padding: 16px;
      gap: 10px;
    }

    .empty-state {
      padding: 40px 16px;
    }

    .empty-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    .empty-text {
      font-size: 18px;
    }

    .empty-hint {
      font-size: 13px;
    }
  }

  /* Optimize for very narrow devices (Z Fold, narrow foldables) */
  @media (max-width: 380px) {
    .preset-list {
      padding: 12px;
      gap: 8px;
    }

    .preset-list::-webkit-scrollbar {
      width: 6px;
    }

    .empty-state {
      padding: 32px 12px;
    }

    .empty-icon {
      font-size: 40px;
      margin-bottom: 10px;
    }

    .empty-text {
      font-size: 16px;
    }

    .empty-hint {
      font-size: 12px;
    }
  }
</style>
