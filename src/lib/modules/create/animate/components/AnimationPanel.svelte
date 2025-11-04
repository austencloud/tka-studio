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
  import GifExportDialog from "$create/animate/components/GifExportDialog.svelte";
  import { Drawer, SheetDragHandle, GridMode, type Letter } from "$shared";
  import type { GifExportProgress } from "$create/animate/services/contracts";
  import type { PropState } from "$create/animate/domain/types/PropState";

  // Props - ALL state comes from parent
  let {
    show = false,
    combinedPanelHeight = 0,
    loading = false,
    error = null,
    speed = 1,
    blueProp = null,
    redProp = null,
    gridVisible = true,
    gridMode = null,
    letter = null,
    showExportDialog = false,
    isExporting = false,
    exportProgress = null,
    onClose = () => {},
    onSpeedChange = () => {},
    onOpenExport = () => {},
    onCloseExport = () => {},
    onExportGif = () => {},
    onCancelExport = () => {},
  }: {
    show?: boolean;
    combinedPanelHeight?: number;
    loading?: boolean;
    error?: string | null;
    speed?: number;
    blueProp?: PropState | null;
    redProp?: PropState | null;
    gridVisible?: boolean;
    gridMode?: GridMode | null | undefined;
    letter?: Letter | null;
    showExportDialog?: boolean;
    isExporting?: boolean;
    exportProgress?: GifExportProgress | null;
    onClose?: () => void;
    onSpeedChange?: (event: Event) => void;
    onOpenExport?: () => void;
    onCloseExport?: () => void;
    onExportGif?: () => void;
    onCancelExport?: () => void;
  } = $props();

  // Derived styles
  const panelHeightStyle = $derived(() => {
    if (combinedPanelHeight > 0) {
      return `height: ${combinedPanelHeight}px;`;
    }
    return "height: 70vh;";
  });
</script>

<Drawer
  isOpen={show}
  on:close={onClose}
  labelledBy="animation-panel-title"
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  showHandle={false}
  class="animation-panel-container glass-surface"
  backdropClass="animation-panel-backdrop"
>
  <div
    class="animation-panel"
    style={panelHeightStyle()}
    role="dialog"
    aria-labelledby="animation-panel-title"
  >
    <SheetDragHandle />
    <button class="close-button" onclick={onClose} aria-label="Close animator">
      <i class="fas fa-times"></i>
    </button>

    <h2 id="animation-panel-title" class="sr-only">Animation Viewer</h2>

    {#if loading}
      <div class="loading-message">Loading animation...</div>
    {:else if error}
      <div class="error-message">{error}</div>
    {:else}
      <div class="canvas-container">
        <AnimatorCanvas
          {blueProp}
          {redProp}
          {gridVisible}
          {gridMode}
          {letter}
        />
      </div>

      <AnimationControls
        {speed}
        onSpeedChange={onSpeedChange}
        onExport={onOpenExport}
      />
    {/if}
  </div>
</Drawer>

<GifExportDialog
  show={showExportDialog}
  {isExporting}
  progress={exportProgress}
  onExport={onExportGif}
  onCancel={onCancelExport}
  onClose={onCloseExport}
/>

<style>
  /* Use unified sheet system variables - transparent backdrop to allow workspace interaction */
  :global(.bottom-sheet.animation-panel-container) {
    --sheet-backdrop-bg: var(--backdrop-transparent);
    --sheet-backdrop-filter: var(--backdrop-blur-none);
    --sheet-backdrop-pointer-events: none;
    --sheet-bg: var(--sheet-bg-transparent);
    --sheet-filter: var(--glass-backdrop-strong);
    --sheet-border: var(--sheet-border-medium);
    --sheet-shadow: none;
    --sheet-pointer-events: auto;
    min-height: 300px;
  }

  :global(.bottom-sheet.animation-panel-container:hover) {
    box-shadow: none;
  }

  .animation-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    padding: 0 24px 24px 24px; /* No top padding - drag handle at top */
    padding-bottom: calc(24px + env(safe-area-inset-bottom));
    /* height set via inline style for reactive sizing */
    width: 100%;
    transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    /* Mesh gradient animation */
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.15) 0%,
      rgba(118, 75, 162, 0.15) 25%,
      rgba(240, 147, 251, 0.15) 50%,
      rgba(245, 87, 108, 0.15) 75%,
      rgba(79, 172, 254, 0.15) 100%
    );
    background-size: 300% 300%;
    animation: meshGradientFlow 15s ease infinite;
  }

  @keyframes meshGradientFlow {
    0%,
    100% {
      background-position: 0% 50%;
    }
    25% {
      background-position: 50% 100%;
    }
    50% {
      background-position: 100% 50%;
    }
    75% {
      background-position: 50% 0%;
    }
  }

  .close-button {
    position: absolute;
    top: 12px;
    right: 16px;
    width: var(--sheet-close-size-default);
    height: var(--sheet-close-size-default);
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    color: rgba(255, 255, 255, 1);
    cursor: pointer;
    transition: all var(--sheet-transition-smooth);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
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

  .close-button:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .canvas-container {
    container-type: size;
    container-name: animator-canvas;
    flex: 1;
    width: 100%;
    max-width: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
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

    .close-button {
      top: 12px;
      right: 12px;
      width: 44px;
      height: 44px;
      font-size: 18px;
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

  /* High contrast mode */
  @media (prefers-contrast: high) {
    :global(.animation-panel-container) {
      background: rgba(0, 0, 0, 0.95);
      border-top: 2px solid white;
    }
  }

  /* Reduced motion - disable gradient animation */
  @media (prefers-reduced-motion: reduce) {
    .animation-panel {
      animation: none;
      background-position: 0% 50%;
    }

    .close-button {
      transition: none;
    }

    .close-button:hover,
    .close-button:active {
      transform: none;
    }

    :global(.bottom-sheet.animation-panel-container) {
      transition: none;
    }
  }
</style>
