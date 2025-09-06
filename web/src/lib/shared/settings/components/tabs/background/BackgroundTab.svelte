<!-- BackgroundTab.svelte - Background settings and configuration -->
<script lang="ts">
  import type { AppSettings } from "$shared/domain";
  import { BackgroundType } from "$shared/domain/ui/backgrounds/BackgroundTypes";
  import SettingCard from "../../SettingCard.svelte";
  import ToggleSetting from "../../ToggleSetting.svelte";
  import { backgroundsConfig } from "./background-config";

  interface Props {
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }

  let { settings, onUpdate }: Props = $props();

  // Background settings state
  let backgroundSettings = $state({
    backgroundEnabled: settings?.backgroundEnabled ?? true,
    backgroundType: settings?.backgroundType || BackgroundType.NIGHT_SKY,
    backgroundQuality: settings?.backgroundQuality || "medium",
  });

  function updateBackgroundSetting<K extends keyof typeof backgroundSettings>(
    key: K,
    value: (typeof backgroundSettings)[K]
  ) {
    backgroundSettings[key] = value;
    onUpdate?.({ key, value });
  }

  function handleBackgroundTypeChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateBackgroundSetting("backgroundType", target.value as BackgroundType);
  }

  function handleQualityChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateBackgroundSetting(
      "backgroundQuality",
      target.value as "low" | "medium" | "high"
    );
  }

  // Get background info for display
  const currentBackgroundInfo = $derived(() => {
    return backgroundsConfig.find(
      (bg) => bg.type === backgroundSettings.backgroundType
    );
  });
</script>

<div class="tab-content">
  <SettingCard
    title="Background Display"
    description="Control whether background effects are shown"
  >
    <ToggleSetting
      label="Enable Background"
      checked={backgroundSettings.backgroundEnabled}
      helpText="Show animated background effects behind the interface"
      onchange={(checked) =>
        updateBackgroundSetting("backgroundEnabled", checked)}
    />
  </SettingCard>

  {#if backgroundSettings.backgroundEnabled}
    <SettingCard
      title="Background Type"
      description="Choose the visual style for the background"
    >
      <div class="setting-row">
        <label for="background-select" class="setting-label"
          >Background Style</label
        >
        <select
          id="background-select"
          class="setting-select"
          value={backgroundSettings.backgroundType}
          onchange={handleBackgroundTypeChange}
        >
          {#each backgroundsConfig as background}
            <option value={background.type}>{background.name}</option>
          {/each}
        </select>
      </div>

      {#if currentBackgroundInfo()}
        {@const bgInfo = currentBackgroundInfo()!}
        <div class="background-info">
          <div class="background-preview">
            <span class="background-icon">{bgInfo.icon}</span>
            <div class="background-details">
              <h4 class="background-name">{bgInfo.name}</h4>
              <p class="background-description">
                {bgInfo.description}
              </p>
            </div>
          </div>
        </div>
      {/if}
    </SettingCard>

    <SettingCard
      title="Performance"
      description="Adjust background quality for optimal performance"
    >
      <div class="setting-row">
        <label for="quality-select" class="setting-label"
          >Rendering Quality</label
        >
        <select
          id="quality-select"
          class="setting-select"
          value={backgroundSettings.backgroundQuality}
          onchange={handleQualityChange}
        >
          <option value="low">Low (Better Performance)</option>
          <option value="medium">Medium (Balanced)</option>
          <option value="high">High (Best Quality)</option>
        </select>
      </div>

      <div class="quality-info">
        <p class="quality-description">
          {#if backgroundSettings.backgroundQuality === "low"}
            Reduced particle count and simplified effects for maximum
            performance.
          {:else if backgroundSettings.backgroundQuality === "medium"}
            Balanced quality and performance - recommended for most devices.
          {:else}
            Full quality effects with maximum visual detail.
          {/if}
        </p>
      </div>
    </SettingCard>
  {/if}
</div>

<style>
  .tab-content {
    width: 100%;
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    container-type: inline-size;
  }

  .setting-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: clamp(12px, 1.5vw, 24px);
    padding: clamp(8px, 1vw, 16px) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .setting-row:last-child {
    border-bottom: none;
  }

  .setting-label {
    font-size: clamp(12px, 1.2vw, 16px);
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    flex: 1;
  }

  .setting-select {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: clamp(6px, 0.8vw, 10px) clamp(8px, 1vw, 12px);
    color: rgba(255, 255, 255, 0.9);
    font-size: clamp(11px, 1.1vw, 14px);
    min-width: clamp(120px, 15vw, 180px);
    transition: all var(--transition-fast);
  }

  .setting-select:hover {
    border-color: rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.08);
  }

  .setting-select:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .background-info {
    margin-top: clamp(12px, 1.5vw, 20px);
    padding: clamp(12px, 1.5vw, 20px);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
  }

  .background-preview {
    display: flex;
    align-items: center;
    gap: clamp(12px, 1.5vw, 16px);
  }

  .background-icon {
    font-size: clamp(20px, 2.5vw, 32px);
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(40px, 5vw, 60px);
    height: clamp(40px, 5vw, 60px);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .background-details {
    flex: 1;
  }

  .background-name {
    font-size: clamp(14px, 1.4vw, 18px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 clamp(4px, 0.5vw, 8px) 0;
  }

  .background-description {
    font-size: clamp(11px, 1.1vw, 14px);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.4;
  }

  .quality-info {
    margin-top: clamp(8px, 1vw, 12px);
  }

  .quality-description {
    font-size: clamp(11px, 1.1vw, 13px);
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    line-height: 1.4;
    font-style: italic;
  }
</style>
