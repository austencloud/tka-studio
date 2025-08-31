<!-- ExportActionsCard.svelte - Real TKA Image Export Actions -->
<script lang="ts">
  import type { SequenceData } from "$domain";

  interface Props {
    currentSequence: SequenceData | null;
    canExport?: boolean;
    isExporting?: boolean;
    onexportcurrent?: () => void;
    onexportall?: () => void;
  }

  let {
    currentSequence,
    canExport = false,
    isExporting = false,
    onexportcurrent,
    onexportall,
  }: Props = $props();

  // Loading states for batch operations
  let isExportingAll = $state(false);

  // Derived state for button availability
  let canExportCurrent = $derived(() => {
    // Use the provided canExport prop if available, otherwise fall back to sequence check
    if (canExport !== undefined) {
      return canExport && currentSequence !== null;
    }

    return (
      currentSequence &&
      currentSequence.beats &&
      currentSequence.beats.length > 0
    );
  });

  // Handle export current sequence
  async function handleExportCurrent() {
    if (!canExportCurrent || isExporting) return;

    console.log("📤 [ACTIONS-CARD] Triggering current sequence export");
    onexportcurrent?.();
  }

  // Handle export all sequences
  async function handleExportAll() {
    if (isExportingAll) return;

    try {
      isExportingAll = true;
      console.log("📤 [ACTIONS-CARD] Triggering batch export");
      onexportall?.();
    } catch (error) {
      console.error("Export all failed:", error);
    } finally {
      // Allow manual reset, actual state managed by parent
      setTimeout(() => {
        isExportingAll = false;
      }, 1000);
    }
  }

  // Get current sequence info for display
  let sequenceInfo = $derived(() => {
    if (!currentSequence) return null;

    const beatCount = currentSequence.beats?.length || 0;
    const word = currentSequence.word || currentSequence.name || "Untitled";

    return {
      name: word,
      beatCount,
      isEmpty: beatCount === 0,
      hasStartPosition: !!currentSequence.startPosition,
    };
  });

  // Export button text based on current state
  let exportButtonText = $derived(() => {
    if (isExporting) {
      return "Exporting...";
    }

    const info = sequenceInfo();
    if (!info) {
      return "No Sequence to Export";
    }

    if (info.isEmpty && !info.hasStartPosition) {
      return "Empty Sequence";
    }

    if (info.isEmpty && info.hasStartPosition) {
      return "Export Start Position";
    }

    return "Export Current Sequence";
  });

  // Status message for user feedback
  let sequenceStatus = $derived(() => {
    const info = sequenceInfo();
    if (!info) {
      return "Create a sequence in the Construct tab";
    }

    if (info.isEmpty && !info.hasStartPosition) {
      return "Add beats or set start position to export";
    }

    if (info.isEmpty && info.hasStartPosition) {
      return "Start position only";
    }

    return `${info.beatCount} beats ready to export`;
  });
</script>

<div class="export-actions-card">
  <h3 class="card-title">Export Actions</h3>

  <!-- Current Sequence Export -->
  <div class="action-section">
    <div class="action-header">
      <h4 class="action-title">Current Sequence</h4>
      {#if sequenceInfo()}
        {@const info = sequenceInfo()}
        {#if info}
          <div class="sequence-info">
            <span class="sequence-name">{info.name}</span>
            <div class="sequence-metadata">
              {#if info.beatCount > 0}
                <span class="beat-count">{info.beatCount} beats</span>
              {/if}
              {#if info.hasStartPosition}
                <span class="start-pos-indicator">📍 Start Position</span>
              {/if}
              {#if info.isEmpty && !info.hasStartPosition}
                <span class="empty-indicator">⚠️ Empty</span>
              {/if}
            </div>
          </div>
        {/if}
        <div class="sequence-status">
          <span class="status-text">{sequenceStatus()}</span>
        </div>
      {:else}
        <div class="no-sequence">
          <span class="no-sequence-text">No sequence loaded</span>
          <span class="status-text">{sequenceStatus()}</span>
        </div>
      {/if}
    </div>

    <button
      class="export-button primary"
      class:disabled={!canExportCurrent || isExporting}
      onclick={handleExportCurrent}
      disabled={!canExportCurrent || isExporting}
    >
      {#if isExporting}
        <span class="loading-spinner"></span>
        {exportButtonText()}
      {:else}
        <span class="button-icon">🔤</span>
        {exportButtonText()}
      {/if}
    </button>
  </div>

  <!-- All Sequences Export -->
  <div class="action-section">
    <div class="action-header">
      <h4 class="action-title">Batch Export</h4>
      <div class="all-sequences-info">
        <span class="info-text">Export all sequences in your library</span>
        <span class="status-text">(Feature coming soon)</span>
      </div>
    </div>

    <button
      class="export-button secondary"
      class:disabled={isExportingAll}
      onclick={handleExportAll}
      disabled={isExportingAll}
    >
      {#if isExportingAll}
        <span class="loading-spinner"></span>
        Preparing Batch...
      {:else}
        <span class="button-icon">📚</span>
        Export All Sequences
      {/if}
    </button>
  </div>
</div>

<style>
  .export-actions-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: var(--spacing-sm);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    position: sticky;
    top: 0;
    z-index: 1;
  }

  .card-title {
    margin: 0;
    font-size: var(--font-size-md);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .action-section {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs);
    background: rgba(255, 255, 255, 0.02);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .action-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .action-title {
    margin: 0;
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  .sequence-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .sequence-name {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
  }

  .sequence-metadata {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    flex-wrap: wrap;
  }

  .beat-count {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
    padding: 1px 6px;
    background: rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    white-space: nowrap;
  }

  .start-pos-indicator {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
    padding: 1px 6px;
    background: rgba(16, 185, 129, 0.3);
    border-radius: 8px;
    white-space: nowrap;
  }

  .empty-indicator {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
    padding: 1px 6px;
    background: rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    white-space: nowrap;
  }

  .sequence-status,
  .no-sequence {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .no-sequence-text {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
  }

  .status-text {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.5);
    font-style: italic;
    line-height: 1.2;
  }

  .all-sequences-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .info-text {
    font-size: var(--font-size-xs);
    color: rgba(255, 255, 255, 0.7);
  }

  .export-button {
    padding: var(--spacing-sm);
    border-radius: 6px;
    font-size: var(--font-size-xs);
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
    border: 1px solid transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xs);
    min-height: 36px;
  }

  .export-button.primary {
    background: linear-gradient(135deg, #6366f1 0%, #5855eb 100%);
    color: white;
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  .export-button.primary:hover:not(.disabled) {
    background: linear-gradient(135deg, #5855eb 0%, #4f46e5 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
  }

  .export-button.secondary {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .export-button.secondary:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .export-button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }

  .button-icon {
    font-size: var(--font-size-sm);
  }

  .loading-spinner {
    width: 12px;
    height: 12px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
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
    .export-actions-card {
      padding: var(--spacing-md);
    }

    .export-button {
      padding: var(--spacing-sm) var(--spacing-md);
      font-size: var(--font-size-xs);
    }

    .sequence-metadata {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
