<!-- CodexExporterTab.svelte - Export settings and configuration -->
<script lang="ts">
  import type { AppSettings } from "$shared/domain";
  import SettingCard from "../SettingCard.svelte";
  import ToggleSetting from "../ToggleSetting.svelte";

  interface Props {
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }

  let { settings, onUpdate }: Props = $props();

  // Export settings state
  let exportSettings = $state({
    includeStartPosition: settings?.imageExport?.includeStartPosition ?? true,
    addReversalSymbols: settings?.imageExport?.addReversalSymbols ?? true,
    addBeatNumbers: settings?.imageExport?.addBeatNumbers ?? true,
    addDifficultyLevel: settings?.imageExport?.addDifficultyLevel ?? true,
    addWord: settings?.imageExport?.addWord ?? true,
    addInfo: settings?.imageExport?.addInfo ?? true,
    addUserInfo: settings?.imageExport?.addUserInfo ?? false,
  });

  function updateExportSetting<K extends keyof typeof exportSettings>(
    key: K,
    value: (typeof exportSettings)[K]
  ) {
    exportSettings[key] = value;
    // Update the nested imageExport object
    onUpdate?.({ key: `imageExport.${key}`, value });
  }

  function handleExportSequence() {
    console.log("🚀 Export sequence requested with settings:", exportSettings);
    // TODO: Implement actual export functionality
    alert("Export functionality will be implemented soon!");
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Export Content"
    description="Choose what information to include in exported images"
  >
    <ToggleSetting
      label="Include Start Position"
      checked={exportSettings.includeStartPosition}
      helpText="Show the starting position for the sequence"
      onchange={(checked) =>
        updateExportSetting("includeStartPosition", checked)}
    />

    <ToggleSetting
      label="Add Beat Numbers"
      checked={exportSettings.addBeatNumbers}
      helpText="Display beat numbers on each pictograph"
      onchange={(checked) => updateExportSetting("addBeatNumbers", checked)}
    />

    <ToggleSetting
      label="Add Reversal Symbols"
      checked={exportSettings.addReversalSymbols}
      helpText="Include symbols indicating direction reversals"
      onchange={(checked) => updateExportSetting("addReversalSymbols", checked)}
    />

    <ToggleSetting
      label="Add Difficulty Level"
      checked={exportSettings.addDifficultyLevel}
      helpText="Show the difficulty rating of the sequence"
      onchange={(checked) => updateExportSetting("addDifficultyLevel", checked)}
    />
  </SettingCard>

  <SettingCard
    title="Sequence Information"
    description="Include sequence metadata in the export"
  >
    <ToggleSetting
      label="Add Sequence Name"
      checked={exportSettings.addWord}
      helpText="Include the name/title of the sequence"
      onchange={(checked) => updateExportSetting("addWord", checked)}
    />

    <ToggleSetting
      label="Add Sequence Info"
      checked={exportSettings.addInfo}
      helpText="Include description and additional sequence details"
      onchange={(checked) => updateExportSetting("addInfo", checked)}
    />

    <ToggleSetting
      label="Add User Information"
      checked={exportSettings.addUserInfo}
      helpText="Include creator/author information in the export"
      onchange={(checked) => updateExportSetting("addUserInfo", checked)}
    />
  </SettingCard>

  <SettingCard
    title="Export Actions"
    description="Export your sequences with the current settings"
  >
    <div class="export-actions">
      <button
        class="export-button primary"
        onclick={handleExportSequence}
        type="button"
      >
        📤 Export Current Sequence
      </button>

      <div class="export-info">
        <p class="export-description">
          Export the current sequence as an image with your selected settings.
          The exported image will include all enabled options above.
        </p>
      </div>
    </div>
  </SettingCard>
</div>

<style>
  .tab-content {
    width: 100%;
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    container-type: inline-size;
  }

  .export-actions {
    display: flex;
    flex-direction: column;
    gap: clamp(12px, 1.5vw, 20px);
  }

  .export-button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: none;
    border-radius: 8px;
    padding: clamp(12px, 1.5vw, 16px) clamp(20px, 2.5vw, 32px);
    color: white;
    font-size: clamp(13px, 1.3vw, 16px);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1vw, 12px);
    min-height: clamp(40px, 5vw, 48px);
  }

  .export-button:hover {
    background: linear-gradient(135deg, #5855eb 0%, #7c3aed 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  .export-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
  }

  .export-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.4);
  }

  .export-info {
    padding: clamp(12px, 1.5vw, 16px);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
  }

  .export-description {
    font-size: clamp(11px, 1.1vw, 14px);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.5;
  }
</style>
