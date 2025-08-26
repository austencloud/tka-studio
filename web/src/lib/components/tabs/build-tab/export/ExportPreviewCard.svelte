<!-- ExportPreviewCard.svelte - Real TKA Image Export Preview -->
<script lang="ts">
  import type { SequenceData } from "$services/interfaces/domain-types";

  interface Props {
    currentSequence: SequenceData | null;
    exportSettings: {
      include_start_position: boolean;
      add_beatNumbers: boolean;
      add_reversal_symbols: boolean;
      add_user_info: boolean;
      add_word: boolean;
      use_last_save_directory: boolean;
      export_format: string;
      export_quality: string;
      user_name: string;
      custom_note: string;
    };
    // Real preview state from image export service
    previewImageUrl?: string | null;
    isGeneratingPreview?: boolean;
    previewError?: string | null;
    validationErrors?: string[];
  }

  let {
    currentSequence,
    exportSettings,
    previewImageUrl = null,
    isGeneratingPreview = false,
    previewError = null,
    validationErrors = [],
  }: Props = $props();

  // Preview info derived from current sequence and settings
  let previewInfo = $derived(() => {
    if (!currentSequence) return null;

    const enabledOptions = Object.entries(exportSettings).filter(
      ([_key, value]) => typeof value === "boolean" && value
    ).length;

    return {
      sequenceName:
        currentSequence.name || currentSequence.word || "Untitled Sequence",
      beatCount: currentSequence.beats?.length || 0,
      format: exportSettings.export_format,
      quality: exportSettings.export_quality,
      enabledOptions,
      hasStartPosition: !!currentSequence.startPosition,
      isEmpty: (currentSequence.beats?.length || 0) === 0,
    };
  });

  // Status message based on current state
  let statusMessage = $derived(() => {
    if (isGeneratingPreview) return "Generating preview...";
    if (previewError) return `Error: ${previewError}`;
    if (validationErrors && validationErrors.length > 0) {
      return `Validation errors: ${validationErrors.join(", ")}`;
    }
    if (!currentSequence) {
      return "Create a sequence to see preview";
    }

    const info = previewInfo();
    if (info) {
      if (info.isEmpty && !exportSettings.include_start_position) {
        return "Empty sequence - enable start position to preview";
      }
      if (info.isEmpty && exportSettings.include_start_position) {
        return "Start position only preview";
      }
      return `Preview: ${info.format} • ${info.quality} • ${info.enabledOptions} options enabled`;
    }
    return "Preview ready";
  });

  // Sequence details for display
  let sequenceDetails = $derived(() => {
    const info = previewInfo();
    if (!info) return null;

    return [
      { label: "Sequence", value: info.sequenceName },
      { label: "Beats", value: info.beatCount.toString() },
      { label: "Format", value: info.format },
      { label: "Quality", value: info.quality },
      { label: "Start Position", value: info.hasStartPosition ? "Yes" : "No" },
    ];
  });

  function handleRefreshPreview() {
    // Preview refresh is handled automatically by the parent component
    // This button exists for user feedback but the actual refresh happens
    // in ExportPanel when sequence or settings change
    console.log("🔄 [PREVIEW-CARD] Manual refresh requested");
  }

  // Helper to determine preview display state
  let previewDisplayState = $derived(() => {
    if (isGeneratingPreview) return "loading";
    if (previewError) return "error";
    if (validationErrors && validationErrors.length > 0)
      return "validation-error";
    if (previewImageUrl) return "image";
    if (!currentSequence) return "no-sequence";
    return "placeholder";
  });
</script>

<div class="export-preview-card">
  <div class="preview-header">
    <h3 class="card-title">Export Preview</h3>
    <button
      class="refresh-button"
      onclick={handleRefreshPreview}
      disabled={isGeneratingPreview}
      title="Refresh preview"
    >
      <span class="refresh-icon" class:spinning={isGeneratingPreview}>🔄</span>
    </button>
  </div>

  <div class="preview-content">
    {#if previewDisplayState() === "loading"}
      <div class="preview-loading">
        <div class="loading-spinner"></div>
        <p>Generating preview...</p>
        <span class="loading-hint">Creating image from sequence...</span>
      </div>
    {:else if previewDisplayState() === "error"}
      <div class="preview-error">
        <div class="error-icon">❌</div>
        <p>Preview generation failed</p>
        <span class="error-details">{previewError}</span>
      </div>
    {:else if previewDisplayState() === "validation-error"}
      <div class="preview-error">
        <div class="error-icon">⚠️</div>
        <p>Validation errors</p>
        <div class="validation-errors">
          {#each validationErrors as error}
            <span class="validation-error">{error}</span>
          {/each}
        </div>
      </div>
    {:else if previewDisplayState() === "image"}
      <div class="preview-image-container">
        <img src={previewImageUrl} alt="Export preview" class="preview-image" />
        <div class="image-overlay">
          <div class="image-info">
            {#if previewInfo()}
              {@const info = previewInfo()}
              <span class="image-size">{info?.format}</span>
              <span class="image-beats">{info?.beatCount} beats</span>
            {/if}
          </div>
        </div>
      </div>
    {:else if previewDisplayState() === "no-sequence"}
      <div class="preview-placeholder">
        <div class="placeholder-icon">📄</div>
        <p>No sequence selected</p>
        <span class="placeholder-hint">
          Create or select a sequence in the Construct tab to see preview
        </span>
      </div>
    {:else}
      <div class="preview-placeholder">
        <div class="placeholder-icon">📝</div>
        <p>Ready to preview</p>
        <span class="placeholder-hint">
          Preview will update automatically when settings change
        </span>
      </div>
    {/if}
  </div>

  <div class="preview-footer">
    <div class="status-bar">
      <span class="status-text">{statusMessage()}</span>
    </div>

    {#if sequenceDetails()}
      {@const details = sequenceDetails()}
      {#if details}
        <div class="preview-details">
          {#each details as detail}
            <div class="detail-item">
              <span class="detail-label">{detail.label}:</span>
              <span class="detail-value">{detail.value}</span>
            </div>
          {/each}
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  .export-preview-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .preview-header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .card-title {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .refresh-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: var(--spacing-xs);
    cursor: pointer;
    transition: all var(--transition-fast);
    color: rgba(255, 255, 255, 0.8);
  }

  .refresh-button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    color: rgba(255, 255, 255, 1);
  }

  .refresh-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .refresh-icon {
    display: inline-block;
    transition: transform 0.3s ease;
  }

  .refresh-icon.spinning {
    animation: spin 1s linear infinite;
  }

  .preview-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    min-height: 200px;
    position: relative;
  }

  .preview-loading,
  .preview-error,
  .preview-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    max-width: 300px;
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .error-icon,
  .placeholder-icon {
    font-size: 2rem;
    opacity: 0.7;
  }

  .error-details,
  .placeholder-hint,
  .loading-hint {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.5);
    max-width: 250px;
    line-height: 1.4;
  }

  .validation-errors {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    max-width: 250px;
  }

  .validation-error {
    font-size: var(--font-size-xs);
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
    padding: var(--spacing-xs);
    border-radius: 4px;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  .preview-image-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .preview-image {
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    background: white;
  }

  .image-overlay {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 6px;
    padding: var(--spacing-xs);
    backdrop-filter: blur(4px);
  }

  .image-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: var(--font-size-xs);
    color: white;
  }

  .image-size,
  .image-beats {
    font-weight: 500;
  }

  .preview-footer {
    flex-shrink: 0;
    padding: var(--spacing-md) var(--spacing-lg);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
  }

  .status-bar {
    margin-bottom: var(--spacing-sm);
  }

  .status-text {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.6);
  }

  .preview-details {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
  }

  .detail-item {
    display: flex;
    gap: var(--spacing-xs);
    font-size: var(--font-size-xs);
  }

  .detail-label {
    color: rgba(255, 255, 255, 0.5);
  }

  .detail-value {
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .preview-header,
    .preview-footer {
      padding: var(--spacing-md);
    }

    .preview-content {
      padding: var(--spacing-md);
      min-height: 150px;
    }

    .preview-details {
      flex-direction: column;
      gap: var(--spacing-xs);
    }

    .image-overlay {
      position: static;
      margin-top: var(--spacing-sm);
      background: rgba(0, 0, 0, 0.5);
    }

    .image-info {
      flex-direction: row;
      gap: var(--spacing-sm);
      justify-content: center;
    }
  }
</style>
