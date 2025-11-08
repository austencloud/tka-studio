<!--
  AnimationExportSheet.svelte

  Bottom sheet for animation export with progress tracking.
  Supports multiple output formats (GIF + WebP).
  Non-blocking: can be minimized during export.
-->
<script lang="ts">
  import { Drawer } from "$shared";
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

  function handleOpenChange(open: boolean) {
    if (!open && !isExporting) {
      onClose();
    }
  }

  function startExport() {
    onExport(selectedFormat);
  }

  function handleClose() {
    if (!isExporting) {
      onClose();
    }
  }
</script>

<Drawer
  isOpen={show}
  onOpenChange={handleOpenChange}
  placement="bottom"
  closeOnBackdrop={!isExporting}
  closeOnEscape={!isExporting}
  labelledBy="export-sheet-title"
  showHandle={true}
  class="export-sheet"
>
  <div class="export-sheet-content">
    <div class="sheet-header">
      <h3 id="export-sheet-title">Export Animation</h3>
      <button
        class="close-button"
        onclick={handleClose}
        aria-label="Close"
        disabled={isExporting}
      >
        <i class="fas fa-times"></i>
      </button>
    </div>

    {#if !isExporting && !progress}
      <div class="sheet-body">
        <p class="format-description">
          Select an output format. WebP offers smaller files while GIF maximizes
          compatibility.
        </p>
        <div class="export-options">
          <label
            class="export-option"
            class:selected={selectedFormat === "gif"}
          >
            <input
              type="radio"
              name="export-format"
              value="gif"
              bind:group={selectedFormat}
            />
            <div class="option-content">
              <div class="option-icon">
                <i class="fas fa-file-image"></i>
              </div>
              <div class="option-text">
                <strong>GIF (Legacy)</strong>
                <p>{formatCopy.gif}</p>
              </div>
            </div>
          </label>
          <label
            class="export-option"
            class:selected={selectedFormat === "webp"}
          >
            <input
              type="radio"
              name="export-format"
              value="webp"
              bind:group={selectedFormat}
            />
            <div class="option-content">
              <div class="option-icon">
                <i class="fas fa-file-code"></i>
              </div>
              <div class="option-text">
                <strong>WebP (High Efficiency)</strong>
                <p>{formatCopy.webp}</p>
              </div>
            </div>
          </label>
        </div>
        <div class="export-actions">
          <button
            class="export-button export-button--primary"
            onclick={startExport}
          >
            <i class="fas fa-file-export"></i>
            Start Export
          </button>
          <button class="export-button" onclick={handleClose}> Cancel </button>
        </div>
      </div>
    {:else if progress}
      <div class="sheet-body">
        <div class="export-progress">
          {#if progress.stage === "capturing"}
            <div class="progress-info">
              <i class="fas fa-camera progress-icon"></i>
              <p class="progress-text">Capturing frames...</p>
              <p class="progress-detail">
                ({progress.currentFrame}/{progress.totalFrames})
              </p>
            </div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                style="width: {progress.progress * 100}%"
              ></div>
            </div>
          {:else if progress.stage === "encoding"}
            <div class="progress-info">
              <i class="fas fa-cog fa-spin progress-icon"></i>
              <p class="progress-text">Encoding frames...</p>
            </div>
            <div class="progress-bar">
              <div class="progress-fill progress-fill--indeterminate"></div>
            </div>
          {:else if progress.stage === "transcoding"}
            <div class="progress-info">
              <i class="fas fa-sync fa-spin progress-icon"></i>
              <p class="progress-text">Optimizing for WebP...</p>
            </div>
            <div class="progress-bar">
              <div class="progress-fill progress-fill--indeterminate"></div>
            </div>
          {:else if progress.stage === "complete"}
            <div class="export-success">
              <i class="fas fa-check-circle"></i>
              <p>Export complete! Your file is downloading.</p>
            </div>
          {:else if progress.stage === "error"}
            <div class="export-error">
              <i class="fas fa-exclamation-circle"></i>
              <p>Error: {progress.error}</p>
            </div>
            <button class="export-button" onclick={handleClose}> Close </button>
          {/if}

          {#if isExporting && progress.stage !== "complete" && progress.stage !== "error"}
            <button
              class="export-button export-button--danger"
              onclick={onCancel}
            >
              <i class="fas fa-ban"></i>
              Cancel Export
            </button>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</Drawer>

<style>
  .export-sheet-content {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 80vh;
  }

  .sheet-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .sheet-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .close-button {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }

  .close-button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
  }

  .close-button:active:not(:disabled) {
    transform: scale(0.95);
  }

  .close-button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .sheet-body {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
  }

  .format-description {
    margin: 0 0 20px 0;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
    font-size: 14px;
  }

  .export-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 24px;
  }

  .export-option {
    display: flex;
    cursor: pointer;
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    padding: 16px;
    transition: all 0.2s ease;
    position: relative;
  }

  .export-option:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .export-option.selected {
    background: rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.5);
  }

  .export-option input[type="radio"] {
    position: absolute;
    opacity: 0;
    pointer-events: none;
  }

  .option-content {
    display: flex;
    gap: 12px;
    align-items: center;
    width: 100%;
  }

  .option-icon {
    font-size: 24px;
    color: rgba(59, 130, 246, 0.9);
    flex-shrink: 0;
  }

  .option-text {
    flex: 1;
  }

  .option-text strong {
    display: block;
    color: rgba(255, 255, 255, 0.95);
    font-size: 15px;
    margin-bottom: 4px;
  }

  .option-text p {
    margin: 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .export-actions {
    display: flex;
    gap: 12px;
  }

  .export-button {
    flex: 1;
    padding: 14px 20px;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .export-button--primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .export-button--primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .export-button--danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    width: 100%;
  }

  .export-button--danger:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  .export-button:not(.export-button--primary):not(.export-button--danger) {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
  }

  .export-button:not(.export-button--primary):not(
      .export-button--danger
    ):hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .export-button:active {
    transform: translateY(0);
  }

  .export-progress {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .progress-info {
    text-align: center;
  }

  .progress-icon {
    font-size: 32px;
    color: rgba(59, 130, 246, 0.9);
    margin-bottom: 12px;
    display: block;
  }

  .progress-text {
    margin: 0 0 4px 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 16px;
    font-weight: 500;
  }

  .progress-detail {
    margin: 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
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

  .export-success,
  .export-error {
    text-align: center;
    padding: 20px;
  }

  .export-success i,
  .export-error i {
    font-size: 48px;
    display: block;
    margin-bottom: 12px;
  }

  .export-success {
    color: #10b981;
  }

  .export-success i {
    color: #10b981;
  }

  .export-error {
    color: #ef4444;
  }

  .export-error i {
    color: #ef4444;
  }

  .export-success p,
  .export-error p {
    margin: 0;
    font-weight: 500;
    font-size: 16px;
  }

  /* Mobile adjustments */
  @media (max-width: 480px) {
    .sheet-header {
      padding: 16px 20px 12px;
    }

    .sheet-header h3 {
      font-size: 18px;
    }

    .sheet-body {
      padding: 20px;
    }

    .export-options {
      gap: 10px;
    }

    .export-option {
      padding: 14px;
    }

    .option-icon {
      font-size: 20px;
    }

    .export-actions {
      flex-direction: column;
    }

    .export-button {
      width: 100%;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .export-option,
    .export-button,
    .close-button {
      transition: none;
    }

    .export-option:hover,
    .export-button:hover,
    .close-button:hover {
      transform: none;
    }

    .progress-fill--indeterminate {
      animation: none;
    }
  }
</style>
