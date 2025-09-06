<!-- GeneralTab.svelte - General application settings -->
<script lang="ts">
  import type { AppSettings } from "$shared/domain";
  import SettingCard from "../SettingCard.svelte";
  import ToggleSetting from "../ToggleSetting.svelte";

  interface Props {
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }

  let { settings, onUpdate }: Props = $props();

  // General settings state
  let generalSettings = $state({
    theme: settings?.theme || "dark",
    autoSave: settings?.autoSave ?? true,
    showBeatNumbers: settings?.showBeatNumbers ?? true,
    animationsEnabled: settings?.animationsEnabled ?? true,
    developerMode: settings?.developerMode ?? false,
    exportQuality: settings?.exportQuality || "high",
    workbenchColumns: settings?.workbenchColumns || 3,
  });

  function updateGeneralSetting<K extends keyof typeof generalSettings>(
    key: K,
    value: (typeof generalSettings)[K]
  ) {
    generalSettings[key] = value;
    onUpdate?.({ key, value });
  }

  function handleThemeChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateGeneralSetting("theme", target.value as "light" | "dark");
  }

  function handleExportQualityChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    updateGeneralSetting(
      "exportQuality",
      target.value as "low" | "medium" | "high"
    );
  }

  function handleWorkbenchColumnsChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const value = parseInt(target.value, 10);
    if (value >= 1 && value <= 6) {
      updateGeneralSetting("workbenchColumns", value);
    }
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Appearance"
    description="Control the visual appearance of the application"
  >
    <div class="setting-row">
      <label for="theme-select" class="setting-label">Theme</label>
      <select
        id="theme-select"
        class="setting-select"
        value={generalSettings.theme}
        onchange={handleThemeChange}
      >
        <option value="dark">Dark</option>
        <option value="light">Light</option>
      </select>
    </div>

    <ToggleSetting
      label="Enable Animations"
      checked={generalSettings.animationsEnabled}
      helpText="Enable smooth animations and transitions"
      onchange={(checked) => updateGeneralSetting("animationsEnabled", checked)}
    />
  </SettingCard>

  <SettingCard
    title="Workbench"
    description="Configure the sequence construction workspace"
  >
    <ToggleSetting
      label="Show Beat Numbers"
      checked={generalSettings.showBeatNumbers}
      helpText="Display beat numbers in the workbench"
      onchange={(checked) => updateGeneralSetting("showBeatNumbers", checked)}
    />

    <div class="setting-row">
      <label for="columns-input" class="setting-label">Workbench Columns</label>
      <input
        id="columns-input"
        type="number"
        class="setting-input"
        min="1"
        max="6"
        value={generalSettings.workbenchColumns}
        onchange={handleWorkbenchColumnsChange}
      />
    </div>
  </SettingCard>

  <SettingCard
    title="Data & Export"
    description="Configure data handling and export options"
  >
    <ToggleSetting
      label="Auto Save"
      checked={generalSettings.autoSave}
      helpText="Automatically save changes as you work"
      onchange={(checked) => updateGeneralSetting("autoSave", checked)}
    />

    <div class="setting-row">
      <label for="quality-select" class="setting-label">Export Quality</label>
      <select
        id="quality-select"
        class="setting-select"
        value={generalSettings.exportQuality}
        onchange={handleExportQualityChange}
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>
  </SettingCard>

  <SettingCard
    title="Developer"
    description="Advanced settings for developers and power users"
  >
    <ToggleSetting
      label="Developer Mode"
      checked={generalSettings.developerMode}
      helpText="Enable developer features and debugging tools"
      onchange={(checked) => updateGeneralSetting("developerMode", checked)}
    />
  </SettingCard>
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

  .setting-select,
  .setting-input {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: clamp(6px, 0.8vw, 10px) clamp(8px, 1vw, 12px);
    color: rgba(255, 255, 255, 0.9);
    font-size: clamp(11px, 1.1vw, 14px);
    min-width: clamp(80px, 10vw, 120px);
    transition: all var(--transition-fast);
  }

  .setting-select:hover,
  .setting-input:hover {
    border-color: rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.08);
  }

  .setting-select:focus,
  .setting-input:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .setting-input[type="number"] {
    text-align: center;
  }
</style>
