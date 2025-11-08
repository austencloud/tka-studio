<!--
  AnimationExportDialog.svelte

  Modal dialog for animation export with progress tracking.
  Supports multiple output formats (GIF + WebP).
-->
<script lang="ts">
  import type {
    AnimationExportFormat,
    GifExportProgress,
  } from "$create/animate/services/contracts";

  // Props
  let {
    show = false,
    isExporting = false,
    progress = null,
    onExport = () => {},
    onCancel = () => {},
    onClose = () => {},
  }: {
    show?: boolean;
    isExporting?: boolean;
    progress?: GifExportProgress | null;
    onExport?: (format: AnimationExportFormat) => void;
    onCancel?: () => void;
    onClose?: () => void;
  } = $props();

  let selectedFormat = $state<AnimationExportFormat>("gif");

  const formatCopy: Record<AnimationExportFormat, string> = {
    gif: "Maximum compatibility",
    webp: "Smaller files, modern browsers",
  };

  function handleBackdropClick() {
    if (!isExporting) {
      onClose();
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && !isExporting) {
      onClose();
    }
  }

  function startExport() {
    onExport(selectedFormat);
  }
</script>

{#if show}
  <div
    class="export-dialog-backdrop"
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="button"
    tabindex="0"
    aria-label="Close export dialog"
  >
    <div
      class="export-dialog"
      onclick={(e) => e.stopPropagation()}
      onkeydown={(e) => e.stopPropagation()}
      role="dialog"
      aria-modal="true"
      aria-labelledby="export-dialog-title"
      tabindex="-1"
    >
      <h3 id="export-dialog-title">Export Animation</h3>

      {#if !isExporting && !progress}
        <p>
          Select an output format. WebP offers smaller files while GIF maximizes
          compatibility.
        </p>
        <div class="export-options">
          <label class="export-option">
            <input
              type="radio"
              name="export-format"
              value="gif"
              bind:group={selectedFormat}
            />
            <div>
              <strong>GIF (Legacy)</strong>
              <p>{formatCopy.gif}</p>
            </div>
          </label>
          <label class="export-option">
            <input
              type="radio"
              name="export-format"
              value="webp"
              bind:group={selectedFormat}
            />
            <div>
              <strong>WebP (High Efficiency)</strong>
              <p>{formatCopy.webp}</p>
            </div>
          </label>
        </div>
        <div class="export-actions">
          <button
            class="export-action-button export-action-button--primary"
            onclick={startExport}
          >
            <i class="fas fa-file-export"></i>
            Start Export
          </button>
          <button class="export-action-button" onclick={onClose}>
            Cancel
          </button>
        </div>
      {:else if progress}
        <div class="export-progress">
          {#if progress.stage === "capturing"}
            <p>
              Capturing frames... ({progress.currentFrame}/{progress.totalFrames})
            </p>
            <div class="progress-bar">
              <div
                class="progress-fill"
                style="width: {progress.progress * 100}%"
              ></div>
            </div>
          {:else if progress.stage === "encoding"}
            <p>Encoding frames...</p>
            <div class="progress-bar">
              <div class="progress-fill progress-fill--indeterminate"></div>
            </div>
          {:else if progress.stage === "transcoding"}
            <p>Optimizing for WebP...</p>
            <div class="progress-bar">
              <div class="progress-fill progress-fill--indeterminate"></div>
            </div>
          {:else if progress.stage === "complete"}
            <p class="export-success">
              <i class="fas fa-check-circle"></i>
              Export complete! Your file is downloading.
            </p>
          {:else if progress.stage === "error"}
            <p class="export-error">
              <i class="fas fa-exclamation-circle"></i>
              Error: {progress.error}
            </p>
            <button class="export-action-button" onclick={onClose}>
              Close
            </button>
          {/if}

          {#if isExporting && progress.stage !== "complete" && progress.stage !== "error"}
            <button
              class="export-action-button export-action-button--danger"
              onclick={onCancel}
            >
              Cancel Export
            </button>
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .export-dialog-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    padding: 20px;
  }

  .export-dialog {
    background: linear-gradient(
      135deg,
      rgba(30, 30, 40, 0.95),
      rgba(20, 20, 30, 0.95)
    );
    backdrop-filter: blur(20px);
    border-radius: 16px;
    padding: 24px;
    max-width: 400px;
    width: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .export-dialog h3 {
    margin: 0 0 16px 0;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
  }

  .export-dialog p {
    margin: 0 0 16px 0;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
  }

  .export-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
  }

  .export-option {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.2);
  }

  .export-option strong {
    color: rgba(255, 255, 255, 1);
    display: block;
  }

  .export-option input {
    margin-top: 4px;
  }

  .export-option p {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .export-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }

  .export-action-button {
    flex: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 120px;
  }

  .export-action-button--primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }

  .export-action-button--primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  .export-action-button--danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  }

  .export-action-button--danger:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  .export-action-button:not(.export-action-button--primary):not(
      .export-action-button--danger
    ) {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
  }

  .export-action-button:not(.export-action-button--primary):not(
      .export-action-button--danger
    ):hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .export-action-button i {
    margin-right: 6px;
  }

  .export-progress {
    text-align: center;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin: 16px 0;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    transition: width 0.3s ease;
    border-radius: 4px;
  }

  .progress-fill--indeterminate {
    width: 40%;
    animation: indeterminate 1.5s ease-in-out infinite;
  }

  @keyframes indeterminate {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(350%);
    }
  }

  .export-success {
    color: #10b981;
    font-weight: 600;
  }

  .export-success i {
    font-size: 24px;
    display: block;
    margin-bottom: 8px;
  }

  .export-error {
    color: #ef4444;
    font-weight: 600;
  }

  .export-error i {
    font-size: 24px;
    display: block;
    margin-bottom: 8px;
  }
</style>
