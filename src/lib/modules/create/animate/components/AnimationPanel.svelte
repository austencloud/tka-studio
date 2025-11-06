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
  import { Drawer, GridMode, type Letter } from "$shared";
  import { tryGetCreateModuleContext } from "../../shared/context";
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

  // Track drag state for manual swipe-to-dismiss
  let dragState = $state<{
    isDragging: boolean;
    startY: number;
    currentY: number;
    startX: number;
    currentX: number;
  }>({
    isDragging: false,
    startY: 0,
    currentY: 0,
    startX: 0,
    currentX: 0,
  });

  // Derived styles
  const createModuleContext = tryGetCreateModuleContext();
  const isSideBySideLayout = $derived.by(() =>
    createModuleContext
      ? createModuleContext.layout.shouldUseSideBySideLayout
      : false
  );

  // Drawer handle footprint (height + vertical margins). Keep in sync with SheetDragHandle variables.
  const drawerHandleFootprint = 29;

  const panelHeightStyle = $derived.by(() => {
    if (isSideBySideLayout) {
      return "height: 100%;";
    }
    if (combinedPanelHeight > 0) {
      const adjustedHeight = Math.max(
        combinedPanelHeight - drawerHandleFootprint,
        0
      );
      return `height: ${adjustedHeight}px;`;
    }
    // Fallback while measurements resolve
    return "height: 70vh;";
  });
  const drawerPlacement = $derived.by(() =>
    isSideBySideLayout ? "right" : "bottom"
  );
  const drawerClass = $derived.by(() =>
    `animation-panel-container glass-surface${
      isSideBySideLayout ? " side-by-side-layout" : ""
    }`
  );
  const drawerBackdropClass = $derived.by(() =>
    `animation-panel-backdrop${
      isSideBySideLayout ? " side-by-side-layout" : ""
    }`
  );

  function handlePanelPointerDown(event: PointerEvent) {
    // Don't start drag if clicking on interactive elements (buttons)
    const target = event.target as HTMLElement;
    if (
      target.closest("button") ||
      target.closest("input") ||
      target.closest("a")
    ) {
      return;
    }

    // Start tracking drag from anywhere on the panel
    dragState.isDragging = true;
    dragState.startY = event.clientY;
    dragState.currentY = event.clientY;
    dragState.startX = event.clientX;
    dragState.currentX = event.clientX;
    (event.currentTarget as HTMLElement).setPointerCapture(event.pointerId);
  }

  function handlePanelPointerMove(event: PointerEvent) {
    if (!dragState.isDragging) return;

    dragState.currentY = event.clientY;
    dragState.currentX = event.clientX;

    const panel = event.currentTarget as HTMLElement;
    const drawerContent = panel.closest(".drawer-content") as HTMLElement | null;
    if (!drawerContent) return;

    if (isSideBySideLayout) {
      const deltaX = dragState.currentX - dragState.startX;
      if (deltaX > 0) {
        drawerContent.style.transform = `translateX(${deltaX}px)`;
        drawerContent.style.transition = "none";
      }
    } else {
      const deltaY = dragState.currentY - dragState.startY;
      if (deltaY > 0) {
        drawerContent.style.transform = `translateY(${deltaY}px)`;
        drawerContent.style.transition = "none";
      }
    }
  }

  function handlePanelPointerUp(event: PointerEvent) {
    if (!dragState.isDragging) return;

    const deltaY = dragState.currentY - dragState.startY;
    const deltaX = dragState.currentX - dragState.startX;
    const panel = event.currentTarget as HTMLElement;
    const drawerContent = panel.closest(".drawer-content") as HTMLElement;

    if (isSideBySideLayout) {
      if (deltaX > 150) {
        onClose();
      } else if (drawerContent) {
        drawerContent.style.transform = "";
        drawerContent.style.transition =
          "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)";
      }
    } else if (deltaY > 150) {
      onClose();
    } else if (drawerContent) {
      drawerContent.style.transform = "";
      drawerContent.style.transition =
        "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)";
    }

    dragState.isDragging = false;
    (event.currentTarget as HTMLElement).releasePointerCapture(event.pointerId);
  }
</script>

<Drawer
  isOpen={show}
  onclose={onClose}
  labelledBy="animation-panel-title"
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  showHandle={true}
  respectLayoutMode={false}
  placement={drawerPlacement}
  class={drawerClass}
  backdropClass={drawerBackdropClass}
>
  <div
    class="animation-panel"
    class:desktop-layout={isSideBySideLayout}
    style={panelHeightStyle}
    role="dialog"
    aria-labelledby="animation-panel-title"
    onpointerdown={handlePanelPointerDown}
    onpointermove={handlePanelPointerMove}
    onpointerup={handlePanelPointerUp}
    onpointercancel={handlePanelPointerUp}
  >
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

      <AnimationControls {speed} {onSpeedChange} onExport={onOpenExport} />
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
  /* Drawer content styling - opaque background to match animation-panel */
  :global(.drawer-content.animation-panel-container) {
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    ) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.5),
      0 -2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
  }

  :global(
      .drawer-content.animation-panel-container.side-by-side-layout[data-placement="right"]
    ) {
    top: var(--create-panel-top, 64px);
    bottom: var(--create-panel-bottom, 0);
    right: var(--create-panel-inset-right, 0);
    width: var(
      --create-panel-width,
      clamp(360px, 32vw, 520px)
    );
    max-width: min(600px, 100%);
    height: auto;
    max-height: calc(100vh - var(--create-panel-top, 64px));
    transform: translateX(100%);
    transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
  }

  :global(
      .drawer-content.animation-panel-container.side-by-side-layout[data-placement="right"][data-state="open"]
    ) {
    transform: translateX(0);
  }

  :global(
      .drawer-content.animation-panel-container.side-by-side-layout[data-placement="right"][data-state="closed"]
    ) {
    transform: translateX(100%);
  }

  :global(
      .drawer-content.animation-panel-container[data-placement="bottom"]:not(
        .side-by-side-layout
      )
    ) {
    left: 0;
    right: 0;
    width: 100%;
    max-width: 100%;
    margin: 0;
  }

  :global(.bottom-sheet.animation-panel-container:hover) {
    box-shadow: none;
  }

  /* Backdrop - ensure no blur on the overlay behind the drawer */
  :global(.drawer-overlay.animation-panel-backdrop) {
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    pointer-events: none !important;
  }

  :global(
      .drawer-content.animation-panel-container.side-by-side-layout .drawer-handle
    ) {
    position: absolute;
    top: 50%;
    left: 18px;
    width: 4px;
    height: 48px;
    margin: 0;
    border-radius: 999px;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.35);
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
    /* Background is now on drawer-content, so make this transparent */
    background: transparent;
  }

  .animation-panel.desktop-layout {
    padding-bottom: 24px;
    height: 100%;
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
    .animation-panel {
      background: rgba(0, 0, 0, 0.98);
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      border-top: 2px solid white;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .animation-panel {
      transition: none;
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

  :global(
      .drawer-overlay.animation-panel-backdrop.side-by-side-layout
    ) {
    top: var(--create-panel-top, 64px);
    bottom: var(--create-panel-bottom, 0);
    left: var(--create-panel-left, 50%);
    right: 0;
  }
</style>
