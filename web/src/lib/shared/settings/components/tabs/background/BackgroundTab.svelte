<!-- BackgroundTab.svelte - Background settings and configuration -->
<script lang="ts">
  import type { AppSettings } from "$shared";
  import { BackgroundType } from "$shared";
  import SettingCard from "../../SettingCard.svelte";
  import ToggleSetting from "../../ToggleSetting.svelte";
  import BackgroundSelector from "./BackgroundSelector.svelte";
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

  function handleBackgroundSelect(selectedType: BackgroundType) {
    updateBackgroundSetting("backgroundType", selectedType);
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
      description="Choose your preferred animated background style"
    >
      <BackgroundSelector
        selectedBackground={backgroundSettings.backgroundType}
        onBackgroundSelect={handleBackgroundSelect}
      />

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
