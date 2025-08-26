<!-- ExportPanel.svelte - Construct Tab Export Panel with Real TKA Image Export -->
<script lang="ts">
  import { browser } from "$app/environment";
  import { resolve } from "$services/bootstrap";
  import { createImageExportState } from "$lib/state/image-export-state.svelte";
  import type { SequenceData } from "$lib/domain";
  import type { ITKAImageExportService } from "$services/interfaces/image-export-interfaces";
  import { ITKAImageExportServiceInterface } from "$services/di/interfaces/image-export-interfaces";
  import ExportActionsCard from "./ExportActionsCard.svelte";
  import ExportPreviewCard from "./ExportPreviewCard.svelte";
  import ExportSettingsCard from "./ExportSettingsCard.svelte";

  interface Props {
    // Current sequence from construct tab
    currentSequence?: SequenceData | null;
    // Legacy event handlers for backward compatibility
    onsettingchanged?: (data: { setting: string; value: any }) => void;
    onpreviewupdaterequested?: (settings: any) => void;
    onexportrequested?: (data: { type: string; config: any }) => void;
  }

  let {
    currentSequence = null,
    onsettingchanged,
    onpreviewupdaterequested,
    onexportrequested,
  }: Props = $props();

  // Get the real TKA image export service
  const imageExportService = browser
    ? (resolve(
        ITKAImageExportServiceInterface
      ) as ITKAImageExportService | null)
    : null;

  // Create image export state with real service
  const exportState =
    browser && imageExportService
      ? createImageExportState(imageExportService)
      : null;

  // Auto-generate preview when current sequence changes
  $effect(() => {
    if (exportState && currentSequence) {
      console.log(
        "🖼️ [EXPORT-PANEL] Current sequence changed, generating preview...",
        {
          sequenceId: currentSequence.id,
          beatCount: currentSequence.beats.length,
          word: currentSequence.word,
        }
      );
      exportState.generatePreview(currentSequence);
    } else if (exportState && !currentSequence) {
      console.log("🖼️ [EXPORT-PANEL] No current sequence, clearing preview");
      exportState.clearPreview();
    }
  });

  // Auto-regenerate preview when export options change
  $effect(() => {
    if (exportState && currentSequence && exportState.exportOptions) {
      // Debounce to avoid excessive regeneration
      const timeoutId = setTimeout(() => {
        console.log(
          "🖼️ [EXPORT-PANEL] Export options changed, regenerating preview..."
        );
        exportState.generatePreview(currentSequence);
      }, 300);

      return () => clearTimeout(timeoutId);
    }
  });

  // Convert TKA export options to legacy format for settings card
  let legacyExportSettings = $derived(() => {
    if (!exportState) {
      return {
        include_start_position: true,
        add_beatNumbers: true,
        add_reversal_symbols: true,
        add_user_info: true,
        add_word: true,
        use_last_save_directory: true,
        export_format: "PNG",
        export_quality: "300 DPI",
        user_name: "Default User",
        custom_note: "",
      };
    }

    const options = exportState.exportOptions;
    return {
      include_start_position: options.includeStartPosition,
      add_beatNumbers: options.addBeatNumbers,
      add_reversal_symbols: options.addReversalSymbols,
      add_user_info: options.addUserInfo,
      add_word: options.addWord,
      use_last_save_directory: true, // Not in TKA options, legacy setting
      export_format: options.format,
      export_quality: "300 DPI", // Simplified for UI
      user_name: options.userName,
      custom_note: options.notes,
    };
  });

  // Handle setting changes from legacy components
  function handleSettingChanged(data: { setting: string; value: any }) {
    if (!exportState) return;

    const { setting, value } = data;
    console.log("🔧 [EXPORT-PANEL] Setting changed:", setting, "=", value);

    // Convert legacy setting names to TKA option names
    const settingMap: Record<string, string> = {
      include_start_position: "includeStartPosition",
      add_beatNumbers: "addBeatNumbers",
      add_reversal_symbols: "addReversalSymbols",
      add_user_info: "addUserInfo",
      add_word: "addWord",
      export_format: "format",
      user_name: "userName",
      custom_note: "notes",
    };

    const tkaSettingName = settingMap[setting] || setting;

    // Update TKA export options
    exportState.updateOptions({ [tkaSettingName]: value });

    // Emit to parent for backward compatibility
    onsettingchanged?.({ setting, value });
    onpreviewupdaterequested?.(legacyExportSettings());
  }

  // Handle export current sequence using real service
  async function handleExportCurrent() {
    if (!exportState || !currentSequence) {
      console.warn("🚫 [EXPORT-PANEL] Cannot export: no service or sequence");
      return;
    }

    if (!currentSequence.beats || currentSequence.beats.length === 0) {
      console.warn("🚫 [EXPORT-PANEL] Cannot export: sequence has no beats");
      return;
    }

    console.log("📤 [EXPORT-PANEL] Exporting current sequence...", {
      sequenceId: currentSequence.id,
      word: currentSequence.word,
      beatCount: currentSequence.beats.length,
    });

    try {
      await exportState.exportSequence(currentSequence);
      console.log("✅ [EXPORT-PANEL] Export completed successfully");
    } catch (error) {
      console.error("❌ [EXPORT-PANEL] Export failed:", error);
    }

    // Legacy event emission
    const exportConfig = {
      sequence: currentSequence,
      settings: legacyExportSettings(),
    };
    onexportrequested?.({ type: "current", config: exportConfig });
  }

  // Handle export all sequences (legacy handler)
  function handleExportAll() {
    console.log("📤 [EXPORT-PANEL] Export all requested (legacy handler)");

    const exportConfig = {
      settings: legacyExportSettings(),
    };
    onexportrequested?.({ type: "all", config: exportConfig });
  }

  let sequenceInfo = $derived(() => {
    if (!currentSequence) {
      return "No sequence selected";
    }

    const beatCount = currentSequence.beats?.length || 0;
    const word = currentSequence.word || "Untitled";

    if (beatCount === 0) {
      return `Sequence "${word}" is empty`;
    }

    return `Sequence "${word}" (${beatCount} beats)`;
  });
</script>

<div class="export-panel">
  <!-- Header with current sequence info -->
  <div class="export-header">
    <h2 class="export-title">Export</h2>
    <p class="export-description">
      {sequenceInfo()}
    </p>
    {#if !browser}
      <p class="export-status">⚠️ Export requires JavaScript</p>
    {:else if !exportState}
      <p class="export-status">⚠️ Export service not available</p>
    {:else if exportState.isExporting}
      <p class="export-status">📤 Exporting...</p>
    {:else if exportState.exportError}
      <p class="export-status error">❌ {exportState.exportError}</p>
    {:else if exportState.lastExportedFile}
      <p class="export-status success">
        ✅ Exported: {exportState.lastExportedFile}
      </p>
    {/if}
  </div>

  <!-- Main content: Settings and Preview side by side -->
  <div class="export-content">
    <!-- Left: Settings column -->
    <div class="settings-column">
      <!-- Actions should always be visible; place first and keep out of scroll -->
      <ExportActionsCard
        {currentSequence}
        canExport={exportState?.canExport || false}
        isExporting={exportState?.isExporting || false}
        onexportcurrent={handleExportCurrent}
        onexportall={handleExportAll}
      />

      <!-- Scroll only the settings, not the actions -->
      <div class="settings-scroll">
        <ExportSettingsCard
          exportSettings={legacyExportSettings()}
          onsettingchanged={handleSettingChanged}
        />
      </div>
    </div>

    <!-- Right: Preview column -->
    <div class="preview-column">
      <ExportPreviewCard
        {currentSequence}
        exportSettings={legacyExportSettings()}
        previewImageUrl={exportState?.previewImageUrl || null}
        isGeneratingPreview={exportState?.isGeneratingPreview || false}
        previewError={exportState?.previewError || null}
        validationErrors={exportState?.validationErrors || []}
      />
    </div>
  </div>
</div>

<style>
  .export-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
    overflow: hidden;
  }

  .export-header {
    flex-shrink: 0;
    text-align: left;
  }

  .export-title {
    margin: 0 0 2px 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .export-description {
    margin: 0 0 4px 0;
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
  }

  .export-status {
    margin: 0;
    font-size: var(--font-size-xs);
    font-weight: 500;
    padding: 2px 0;
  }

  .export-status.error {
    color: #ef4444;
  }

  .export-status.success {
    color: #10b981;
  }

  .export-content {
    flex: 1;
    display: flex;
    gap: var(--spacing-sm);
    overflow: hidden;
    min-height: 0;
  }

  .settings-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    min-width: 0;
  }

  /* Only settings should scroll; keep actions visible */
  .settings-scroll {
    flex: 1;
    overflow-y: auto;
    min-height: 0;
  }

  .preview-column {
    flex: 2;
    display: flex;
    flex-direction: column;
    min-width: 0;
    overflow: hidden;
  }

  /* Responsive layout */
  @media (max-width: 1024px) {
    .export-content {
      flex-direction: column;
    }

    .settings-column,
    .preview-column {
      flex: none;
    }

    .settings-column {
      height: auto;
      max-height: 50vh;
    }

    .preview-column {
      flex: 1;
      min-height: 300px;
    }
  }

  @media (max-width: 768px) {
    .export-panel {
      padding: var(--spacing-sm);
    }

    .export-content {
      gap: var(--spacing-sm);
    }

    .settings-column {
      gap: var(--spacing-sm);
    }
  }
</style>
