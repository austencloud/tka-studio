<!--
  CreatePanelDrawer.svelte
  
  Centralized drawer wrapper for all Create module panels that need responsive layout behavior:
  - Desktop/Side-by-side: Slides from right, takes up tool panel space
  - Mobile/Portrait: Slides from bottom, full width with dynamic height
  
  This component encapsulates the common drawer positioning logic and styles,
  ensuring consistency across Animation Panel, Edit Panel, and future panels.
  
  Usage:
  Use CreatePanelDrawer with bind:isOpen, provide panel content via children slot
-->
<script lang="ts">
  import { Drawer } from "$shared";
  import { tryGetCreateModuleContext } from "$create/shared/context";
  import type { Snippet } from "svelte";

  let {
    isOpen = $bindable(false),
    panelName,
    combinedPanelHeight = 0,
    fullHeightOnMobile = false,
    showHandle = true,
    closeOnBackdrop = false,
    focusTrap = false,
    lockScroll = false,
    labelledBy,
    ariaLabel,
    onClose,
    onBackdropClick,
    children,
  }: {
    isOpen?: boolean;
    panelName: string; // Used for CSS class names (e.g., "animation", "edit")
    combinedPanelHeight?: number;
    fullHeightOnMobile?: boolean; // If true, panel takes ~95vh on mobile instead of 70vh
    showHandle?: boolean;
    closeOnBackdrop?: boolean;
    focusTrap?: boolean;
    lockScroll?: boolean;
    labelledBy?: string;
    ariaLabel?: string;
    onClose?: () => void;
    onBackdropClick?: (event: MouseEvent) => boolean; // Return true to close, false to keep open
    children: Snippet;
  } = $props();

  // Get layout context
  const createModuleContext = tryGetCreateModuleContext();
  const isSideBySideLayout = $derived.by(() =>
    createModuleContext
      ? createModuleContext.layout.shouldUseSideBySideLayout
      : false
  );

  // Get measured tool panel width for accurate panel sizing
  const toolPanelWidth = $derived.by(() =>
    createModuleContext ? createModuleContext.panelState.toolPanelWidth : 0
  );

  // Drawer handle footprint (height + vertical margins). Keep in sync with SheetDragHandle variables.
  const drawerHandleFootprint = 29;

  // Calculate panel height for mobile/bottom placement
  const panelHeightStyle = $derived.by(() => {
    if (isSideBySideLayout) {
      return "height: 100%;";
    }
    // If fullHeightOnMobile is set, take full viewport height on mobile
    if (fullHeightOnMobile) {
      return "height: 100dvh;";
    }
    // Otherwise use measured height if available
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

  // Determine drawer placement based on layout
  const drawerPlacement = $derived.by(() =>
    isSideBySideLayout ? "right" : "bottom"
  );

  // Generate unique key when layout mode changes to force drawer re-mount
  // This ensures proper positioning when switching between mobile/desktop layouts
  const drawerKey = $derived.by(() =>
    isSideBySideLayout ? `${panelName}-side` : `${panelName}-bottom`
  );

  // Dynamic CSS classes
  const drawerClass = $derived.by(
    () =>
      `${panelName}-panel-container glass-surface${
        isSideBySideLayout ? " side-by-side-layout" : ""
      }`
  );

  const drawerBackdropClass = $derived.by(
    () =>
      `${panelName}-panel-backdrop${
        isSideBySideLayout ? " side-by-side-layout" : ""
      }`
  );

  // Dynamic inline styles for width and z-index
  const drawerStyle = $derived.by(() => {
    let styles = "--sheet-z-index: 150;"; // Ensure panel appears above navigation (z-index: 100)
    if (isSideBySideLayout && toolPanelWidth > 0) {
      styles += ` --measured-panel-width: ${toolPanelWidth}px;`;
    }
    return styles;
  });

  // Handle close event
  function handleClose() {
    // Update the bindable isOpen state
    isOpen = false;
    // Call the optional onClose callback
    onClose?.();
  }

  // Watch for external close (e.g., via vaul-svelte gesture)
  // When isOpen transitions false, ensure onClose is called
  let wasOpen = $state(isOpen);
  $effect(() => {
    if (wasOpen && !isOpen) {
      // Drawer was closed externally (gesture, etc.)
      // Call onClose to notify parent
      onClose?.();
    }
    wasOpen = isOpen;
  });

  // Handle backdrop click with custom logic
  function handleBackdropClickInternal(event: MouseEvent): boolean {
    if (onBackdropClick) {
      const shouldClose = onBackdropClick(event);
      if (shouldClose) {
        handleClose();
      }
      return shouldClose;
    }
    // Default behavior if no custom handler
    if (closeOnBackdrop) {
      handleClose();
      return true;
    }
    return false;
  }
</script>

{#key drawerKey}
  <div style={drawerStyle}>
    <Drawer
      bind:isOpen
      {...labelledBy ? { labelledBy } : {}}
      {...ariaLabel ? { ariaLabel } : {}}
      onclose={handleClose}
      onbackdropclick={handleBackdropClickInternal}
      {closeOnBackdrop}
      {focusTrap}
      {lockScroll}
      {showHandle}
      respectLayoutMode={true}
      placement={drawerPlacement}
      class={drawerClass}
      backdropClass={drawerBackdropClass}
    >
      <div class="panel-content" style={panelHeightStyle}>
        {@render children()}
      </div>
    </Drawer>
  </div>
{/key}

<style>
  /*
   * ============================================================================
   * SHARED DRAWER POSITIONING & STYLING
   * These styles apply to ALL Create module panels for consistency
   * ============================================================================
   */

  /* Base drawer content styling - solid background */
  :global(.drawer-content[class*="-panel-container"]) {
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
    /* Z-index set via --sheet-z-index CSS variable in drawerStyle */
  }

  /*
   * Side-by-side layout (Desktop): Panels slide from right
   * Width uses measured tool panel container width for pixel-perfect alignment
   * Only set positioning - let base Drawer handle transforms and transitions
   */
  :global(
    .drawer-content[class*="-panel-container"].side-by-side-layout[data-placement="right"]
  ) {
    top: var(--create-panel-top, 64px);
    bottom: var(--create-panel-bottom, 0);
    height: auto;
    max-height: calc(100vh - var(--create-panel-top, 64px));
    /* Use measured tool panel width for exact alignment */
    width: var(--measured-panel-width, clamp(360px, 44.44vw, 900px));
    max-width: 100%;
  }

  /*
   * Mobile/Stacked layout: Panels slide from bottom
   * Height determined by combinedPanelHeight prop via .panel-content
   */
  :global(
    .drawer-content[class*="-panel-container"][data-placement="bottom"]:not(
        .side-by-side-layout
      )
  ) {
    /* Let base Drawer handle positioning from bottom */
    /* Width is already set by base Drawer */
    /* Height is controlled by .panel-content below */
  }

  /*
   * Backdrop styling - transparent, gesture-enabled for swipe-to-dismiss
   * Backdrop handles gesture detection but provides no visual overlay
   */
  :global(.drawer-overlay[class*="-panel-backdrop"]) {
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    /* CRITICAL: Keep pointer-events enabled for gesture detection */
    pointer-events: auto !important;
    /* Z-index automatically set to one less than drawer content by base Drawer */
  }

  /* 
   * Backdrop for side-by-side: only covers right side of screen
   * Left side (sequence area) remains interactive
   */
  :global(.drawer-overlay[class*="-panel-backdrop"].side-by-side-layout) {
    top: var(--create-panel-top, 64px);
    bottom: var(--create-panel-bottom, 0);
    left: var(--create-panel-left, 50%);
    right: 0;
  }

  /*
   * ============================================================================
   * PANEL CONTENT WRAPPER
   * ============================================================================
   */

  .panel-content {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    /* height set dynamically via inline style for reactive sizing */
    transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent; /* Background is on drawer-content */
  }

  /*
   * ============================================================================
   * ACCESSIBILITY & MOTION PREFERENCES
   * ============================================================================
   */

  /* Reduced motion preference - disable height transitions */
  @media (prefers-reduced-motion: reduce) {
    .panel-content {
      transition: none;
    }

    /* vaul-svelte respects prefers-reduced-motion automatically */
  }

  /* High contrast mode - stronger borders */
  @media (prefers-contrast: high) {
    :global(.drawer-content[class*="-panel-container"]) {
      border-top: 2px solid white;
    }
  }
</style>
