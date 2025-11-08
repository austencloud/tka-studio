<!--
  AnimationPanel.svelte

  Pure presentation component for animation display.
  All business logic lives in AnimationCoordinator.

  This component:
  - Receives all state as props
  - Displays UI based on props
  - Emits events when user interacts
  - Has ZERO business logic
-->
<script lang="ts">
  import AnimatorCanvas from "$create/animate/components/AnimatorCanvas.svelte";
  import AnimationControls from "$create/animate/components/AnimationControls.svelte";
  import ExportProgressIndicator from "$create/animate/components/ExportProgressIndicator.svelte";
  import ExportToast from "$create/animate/components/ExportToast.svelte";
  import { CreatePanelDrawer } from "$create/shared/components";
  import PanelHeader from "$create/shared/components/PanelHeader.svelte";
  import { GridMode, type Letter, type BeatData } from "$shared";
  import type {
    AnimationExportFormat,
    GifExportProgress,
  } from "$create/animate/services/contracts";
  import type { PropState } from "$create/animate/domain/types/PropState";

  // Props - ALL state comes from parent
  let {
    show = false,
    combinedPanelHeight = 0,
    isSideBySideLayout = false,
    loading = false,
    error = null,
    speed = 1,
    blueProp = null,
    redProp = null,
    gridVisible = true,
    gridMode = null,
    letter = null,
    beatData = null,
    showExportSheet = false,
    isExporting = false,
    exportProgress = null,
    showExportToast = false,
    exportToastType = "success",
    exportToastMessage = "",
    onClose = () => {},
    onSpeedChange = () => {},
    onOpenExport = () => {},
    onCloseExport = () => {},
    onExport = () => {},
    onCancelExport = () => {},
    onCanvasReady = () => {},
    onDismissToast = () => {},
  }: {
    show?: boolean;
    combinedPanelHeight?: number;
    isSideBySideLayout?: boolean;
    loading?: boolean;
    error?: string | null;
    speed?: number;
    blueProp?: PropState | null;
    redProp?: PropState | null;
    gridVisible?: boolean;
    gridMode?: GridMode | null | undefined;
    letter?: Letter | null;
    beatData?: BeatData | null;
    showExportSheet?: boolean;
    isExporting?: boolean;
    exportProgress?: GifExportProgress | null;
    showExportToast?: boolean;
    exportToastType?: "success" | "error";
    exportToastMessage?: string;
    onClose?: () => void;
    onSpeedChange?: (event: Event) => void;
    onOpenExport?: () => void;
    onCloseExport?: () => void;
    onExport?: (format: AnimationExportFormat) => void;
    onCancelExport?: () => void;
    onCanvasReady?: (canvas: HTMLCanvasElement | null) => void;
    onDismissToast?: () => void;
  } = $props();

  // Track if export sheet is minimized
  let isExportMinimized = $state(false);

  // Selected export format
  let selectedFormat = $state<AnimationExportFormat>("gif");

  // Auto-minimize export sheet when export starts
  $effect(() => {
    if (isExporting && showExportSheet && !isExportMinimized) {
      // Wait a brief moment before minimizing to show initial progress
      const timeout = setTimeout(() => {
        isExportMinimized = true;
      }, 1500);

      return () => clearTimeout(timeout);
    }
    return undefined;
  });

  // Reset minimized state when sheet is closed or export completes
  $effect(() => {
    if (!showExportSheet || !isExporting) {
      isExportMinimized = false;
    }
  });

  function handleExpandExport() {
    isExportMinimized = false;
  }
</script>

{#snippet actionButtons()}
  <button
    class="action-button export-button"
    onclickcapture={onOpenExport}
    aria-label="Export animation as GIF"
  >
    <i class="fas fa-file-export"></i>
  </button>
{/snippet}

<CreatePanelDrawer
  isOpen={show}
  panelName="animation"
  {combinedPanelHeight}
  showHandle={true}
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  labelledBy="animation-panel-title"
  {onClose}
>
  <div
    class="animation-panel"
    role="dialog"
    aria-labelledby="animation-panel-title"
  >
    <PanelHeader
      title="Animation Viewer"
      isMobile={!isSideBySideLayout}
      {onClose}
      {actionButtons}
    />

    <h2 id="animation-panel-title" class="sr-only">Animation Viewer</h2>

    {#if loading}
      <div class="loading-message">Loading animation...</div>
    {:else if error}
      <div class="error-message">{error}</div>
    {:else if showExportSheet && !isExportMinimized}
      <!-- Export UI - Inline within panel when export mode is active -->
      <div class="export-section" class:exporting={isExporting}>
        {#if !isExporting && !exportProgress}
          <!-- Format Selection -->
          <div class="export-format-selection">
            <p class="export-description">
              Select output format. WebP offers smaller files while GIF
              maximizes compatibility.
            </p>

            <div class="format-options">
              <button
                class="format-option"
                class:selected={selectedFormat === "gif"}
                onclick={() => (selectedFormat = "gif")}
              >
                <div class="format-icon">
                  <i class="fas fa-file-image"></i>
                </div>
                <div class="format-info">
                  <strong>GIF</strong>
                  <span>Maximum compatibility</span>
                </div>
              </button>

              <button
                class="format-option"
                class:selected={selectedFormat === "webp"}
                onclick={() => (selectedFormat = "webp")}
              >
                <div class="format-icon">
                  <i class="fas fa-file-code"></i>
                </div>
                <div class="format-info">
                  <strong>WebP</strong>
                  <span>Smaller files, modern browsers</span>
                </div>
              </button>
            </div>

            <div class="export-actions">
              <button
                class="export-btn export-btn--primary"
                onclick={() => onExport(selectedFormat)}
              >
                <i class="fas fa-file-export"></i>
                Start Export
              </button>
              <button class="export-btn" onclick={onCloseExport}>
                Cancel
              </button>
            </div>
          </div>
        {:else if exportProgress}
          <!-- Export Progress -->
          <div class="export-progress-section">
            {#if exportProgress.stage === "capturing"}
              <div class="progress-content">
                <i class="fas fa-camera progress-icon"></i>
                <p class="progress-text">Capturing frames...</p>
                <p class="progress-detail">
                  ({exportProgress.currentFrame}/{exportProgress.totalFrames})
                </p>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    style="width: {exportProgress.progress * 100}%"
                  ></div>
                </div>
              </div>
            {:else if exportProgress.stage === "encoding"}
              <div class="progress-content">
                <i class="fas fa-cog fa-spin progress-icon"></i>
                <p class="progress-text">Encoding frames...</p>
                <div class="progress-bar">
                  <div class="progress-fill progress-fill--indeterminate"></div>
                </div>
              </div>
            {:else if exportProgress.stage === "transcoding"}
              <div class="progress-content">
                <i class="fas fa-sync fa-spin progress-icon"></i>
                <p class="progress-text">Optimizing for WebP...</p>
                <div class="progress-bar">
                  <div class="progress-fill progress-fill--indeterminate"></div>
                </div>
              </div>
            {:else if exportProgress.stage === "error"}
              <div class="progress-content error">
                <i class="fas fa-exclamation-circle progress-icon"></i>
                <p class="progress-text">Error: {exportProgress.error}</p>
                <button class="export-btn" onclick={onCloseExport}>Close</button
                >
              </div>
            {/if}

            {#if isExporting && exportProgress.stage !== "complete" && exportProgress.stage !== "error"}
              <div class="progress-actions">
                <button
                  class="minimize-btn"
                  onclick={() => (isExportMinimized = true)}
                >
                  <i class="fas fa-minus"></i>
                  Minimize
                </button>
                <button
                  class="export-btn export-btn--danger"
                  onclick={onCancelExport}
                >
                  <i class="fas fa-ban"></i>
                  Cancel
                </button>
              </div>
            {/if}
          </div>
        {/if}
      </div>
    {:else}
      <!-- Animation Viewer - Normal mode -->
      <div class="canvas-container">
        <AnimatorCanvas
          {blueProp}
          {redProp}
          {gridVisible}
          {gridMode}
          {letter}
          {beatData}
          {onCanvasReady}
        />
      </div>

      <AnimationControls {speed} {onSpeedChange} />
    {/if}
  </div>
</CreatePanelDrawer>

<!-- Export Progress Indicator - Minimized background indicator -->
<ExportProgressIndicator
  show={isExporting && isExportMinimized}
  progress={exportProgress}
  onExpand={handleExpandExport}
  onCancel={onCancelExport}
/>

<!-- Export Toast - Success/error notification -->
<ExportToast
  show={showExportToast}
  type={exportToastType}
  message={exportToastMessage}
  onDismiss={onDismissToast}
/>

<style>
  .animation-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align to top for header */
    gap: 16px;
    padding: 0; /* No padding - PanelHeader handles its own spacing */
    padding-bottom: calc(24px + env(safe-area-inset-bottom));
    width: 100%;
    height: 100%;
    /* Background is on CreatePanelDrawer */
    background: transparent;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* Action button in header - icon-only with 44px touch target */
  /* NOTE: Button styles have been moved to PanelHeader.svelte for consistency */

  .canvas-container {
    container-type: size;
    container-name: animator-canvas;
    flex: 1;
    width: 100%;
    max-width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
    padding: 0 24px; /* Horizontal padding for canvas */
  }

  .loading-message,
  .error-message {
    padding: 2rem;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }

  .error-message {
    color: rgba(255, 100, 100, 0.9);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .animation-panel {
      padding: 0 16px 16px 16px;
      padding-bottom: calc(16px + env(safe-area-inset-bottom));
      gap: 12px;
    }
  }

  @media (max-width: 480px) {
    .animation-panel {
      padding: 0 12px 12px 12px;
      padding-bottom: calc(12px + env(safe-area-inset-bottom));
      gap: 8px;
    }
  }

  /* Landscape mobile: Adjust spacing */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .animation-panel {
      padding: 0 12px 12px 12px;
      gap: 8px;
    }

    .canvas-container {
      max-width: 500px;
    }
  }

  /* Export Section - Inline export UI */
  .export-section {
    flex: 1;
    width: 100%;
    max-width: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 24px;
  }

  .export-format-selection,
  .export-progress-section {
    width: 100%;
  }

  .export-description {
    margin: 0 0 24px 0;
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    line-height: 1.5;
    text-align: center;
  }

  .format-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 24px;
  }

  .format-option {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    text-align: left;
  }

  .format-option:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .format-option.selected {
    background: rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .format-icon {
    font-size: 28px;
    color: rgba(59, 130, 246, 0.9);
    flex-shrink: 0;
  }

  .format-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .format-info strong {
    color: rgba(255, 255, 255, 0.95);
    font-size: 16px;
  }

  .format-info span {
    color: rgba(255, 255, 255, 0.6);
    font-size: 13px;
  }

  .export-actions {
    display: flex;
    gap: 12px;
  }

  .export-btn {
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
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
  }

  .export-btn--primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  }

  .export-btn--primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  .export-btn--danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  }

  .export-btn--danger:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  .export-btn:not(.export-btn--primary):not(.export-btn--danger):hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .export-btn:active {
    transform: translateY(0);
  }

  /* Export Progress */
  .export-progress-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .progress-content {
    text-align: center;
    padding: 20px;
  }

  .progress-content.error {
    color: #ef4444;
  }

  .progress-icon {
    font-size: 48px;
    color: rgba(59, 130, 246, 0.9);
    margin-bottom: 16px;
    display: block;
  }

  .progress-content.error .progress-icon {
    color: #ef4444;
  }

  .progress-text {
    margin: 0 0 8px 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 16px;
    font-weight: 500;
  }

  .progress-detail {
    margin: 0 0 16px 0;
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin: 0 auto;
    max-width: 300px;
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

  .progress-actions {
    display: flex;
    gap: 12px;
  }

  .minimize-btn {
    flex: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
  }

  .minimize-btn:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
  }

  .minimize-btn:active {
    transform: translateY(0);
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .export-section {
      padding: 0 20px;
    }

    .format-options {
      gap: 10px;
    }

    .format-option {
      padding: 14px 16px;
    }

    .format-icon {
      font-size: 24px;
    }

    .export-actions {
      flex-direction: column;
    }

    .export-btn {
      width: 100%;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .format-option,
    .export-btn,
    .minimize-btn {
      transition: none;
    }

    .format-option:hover,
    .export-btn:hover,
    .minimize-btn:hover {
      transform: none;
    }

    .progress-fill--indeterminate {
      animation: none;
    }
  }
</style>
