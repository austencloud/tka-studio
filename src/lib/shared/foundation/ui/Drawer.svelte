<!--
  Drawer.svelte - Minimal, reliable drawer with pure CSS animations

  NO MORE VAUL-SVELTE. Just clean, predictable CSS transforms.

  Features:
  - Slides from right, left, top, or bottom based on placement
  - Smooth CSS transitions that actually work
  - Backdrop support
  - Escape key to close
  - Same API as before so nothing breaks
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { tryResolve, TYPES } from "$shared/inversify";
  import type { IResponsiveLayoutService } from "$lib/modules/create/shared/services/contracts/IResponsiveLayoutService";

  type CloseReason = "backdrop" | "escape" | "programmatic";

  let {
    isOpen = $bindable(false),
    closeOnBackdrop = true,
    closeOnEscape = true,
    dismissible = true,
    focusTrap = true,
    lockScroll = true,
    labelledBy,
    ariaLabel,
    role = "dialog",
    showHandle = true,
    class: drawerClass = "",
    backdropClass = "",
    placement = "bottom",
    respectLayoutMode = false,
    onclose,
    onOpenChange,
    onbackdropclick,
    children,
  } = $props<{
    isOpen?: boolean;
    closeOnBackdrop?: boolean;
    closeOnEscape?: boolean;
    dismissible?: boolean;
    focusTrap?: boolean;
    lockScroll?: boolean;
    labelledBy?: string;
    ariaLabel?: string;
    role?: "dialog" | "menu" | "listbox" | "alertdialog";
    showHandle?: boolean;
    class?: string;
    backdropClass?: string;
    placement?: "bottom" | "top" | "right" | "left";
    respectLayoutMode?: boolean;
    onclose?: (event: CustomEvent<{ reason: CloseReason }>) => void;
    onOpenChange?: (open: boolean) => void;
    onbackdropclick?: (event: MouseEvent) => boolean;
    children?: () => unknown;
  }>();

  let layoutService: IResponsiveLayoutService | null = null;
  let isSideBySideLayout = $state(false);
  let mounted = $state(false);
  let wasOpen = $state(false);
  let shouldRender = $state(false);
  let isAnimatedOpen = $state(false); // Controls visual state for animations

  // Swipe-to-dismiss state
  let drawerElement = $state<HTMLElement | null>(null);
  let isDragging = $state(false);
  let startY = 0;
  let currentY = $state(0); // Must be reactive to update transform in real-time
  let startTime = 0;

  // Initialize layout service if responsive layout is enabled
  onMount(() => {
    mounted = true;
    if (respectLayoutMode) {
      // Try to resolve layout service (optional dependency)
      // Will be null if create module hasn't loaded yet
      layoutService = tryResolve<IResponsiveLayoutService>(
        TYPES.IResponsiveLayoutService
      );
    }
  });

  // Reactive layout detection
  $effect(() => {
    if (respectLayoutMode && layoutService) {
      isSideBySideLayout = layoutService.shouldUseSideBySideLayout();
    }
  });

  // Track open state changes and notify parent
  $effect(() => {
    if (isOpen !== wasOpen) {
      onOpenChange?.(isOpen);

      // When opening, add to DOM in closed state, then animate open
      if (isOpen) {
        shouldRender = true;
        isAnimatedOpen = false; // Start closed
        isDragging = false; // Reset drag state when opening
        // Force browser to render the closed state first using RAF for reliability
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            isAnimatedOpen = true; // Then transition to open
          });
        });
      }

      // When closing, animate to closed state, then remove from DOM
      if (wasOpen && !isOpen) {
        emitClose("programmatic");
        isAnimatedOpen = false; // Trigger close animation
        isDragging = false; // Reset drag state when closing
        // Keep in DOM during closing animation (350ms), then remove
        setTimeout(() => {
          shouldRender = false;
        }, 400); // 350ms transition + 50ms buffer
      }

      wasOpen = isOpen;
    }
  });

  function emitClose(reason: CloseReason) {
    if (onclose) {
      onclose(new CustomEvent("close", { detail: { reason } }));
    }
  }

  function handleBackdropClick(event: MouseEvent) {
    // If custom handler provided, use it to determine whether to close
    if (onbackdropclick) {
      const shouldClose = onbackdropclick(event);
      if (shouldClose) {
        emitClose("backdrop");
        isOpen = false;
      }
      return;
    }

    // Default behavior
    if (closeOnBackdrop) {
      emitClose("backdrop");
      isOpen = false;
    }
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && closeOnEscape && isOpen) {
      event.preventDefault();
      emitClose("escape");
      isOpen = false;
    }
  }

  // Compute state attribute for CSS - use animated state for visual transitions
  const dataState = $derived(isAnimatedOpen ? "open" : "closed");

  // Compute full class names
  const overlayClasses = $derived(
    `drawer-overlay ${backdropClass} ${respectLayoutMode && isSideBySideLayout ? "side-by-side-layout" : ""}`.trim()
  );

  const contentClasses = $derived(
    `drawer-content ${drawerClass} ${respectLayoutMode && isSideBySideLayout ? "side-by-side-layout" : ""}`.trim()
  );

  // Simple touch handlers for swipe-to-dismiss
  function handleTouchStart(event: TouchEvent) {
    if (!dismissible || placement !== "bottom") return;

    startY = event.touches[0]!.clientY;
    startTime = Date.now();
    isDragging = true;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging || !dismissible || placement !== "bottom") return;

    currentY = event.touches[0]!.clientY;
    const deltaY = currentY - startY;

    // Only allow downward drag
    if (deltaY > 0) {
      // Prevent page scroll/bounce while dragging
      event.preventDefault();
    }
  }

  function handleTouchEnd(event: TouchEvent) {
    if (!isDragging || !dismissible || placement !== "bottom") return;

    const deltaY = currentY - startY;
    const duration = Date.now() - startTime;

    // Reset drag state first
    isDragging = false;
    const wasAboveThreshold = deltaY > 100 || (deltaY > 50 && duration < 500);
    startY = 0;
    currentY = 0;

    // Dismiss if dragged down >100px or fast swipe (>50px in <500ms)
    if (wasAboveThreshold) {
      // Setting isOpen to false will trigger the $effect which calls emitClose
      isOpen = false;
    }
  }

  // Compute drag offset
  const dragOffset = $derived(() => {
    if (!isDragging || placement !== "bottom") return 0;
    const delta = currentY - startY;
    return Math.max(0, delta); // Only allow downward
  });

  // Add passive: false touchmove listener to allow preventDefault
  $effect(() => {
    if (!drawerElement) return;

    const handleMove = (e: TouchEvent) => handleTouchMove(e);
    drawerElement.addEventListener('touchmove', handleMove, { passive: false });

    return () => {
      drawerElement?.removeEventListener('touchmove', handleMove);
    };
  });
</script>

<svelte:window onkeydown={handleKeydown} />

{#if mounted && shouldRender}
  <!-- Backdrop -->
  <div
    class={overlayClasses}
    data-state={dataState}
    onclick={handleBackdropClick}
    aria-hidden="true"
  ></div>

  <!-- Drawer content -->
  <div
    bind:this={drawerElement}
    class={contentClasses}
    data-placement={placement}
    data-state={dataState}
    {role}
    aria-modal="true"
    aria-labelledby={labelledBy}
    aria-label={ariaLabel}
    style:transform={isDragging && dragOffset() > 0 ? `translateY(${dragOffset()}px)` : ""}
    style:transition={isDragging ? "none" : ""}
    ontouchstart={handleTouchStart}
    ontouchend={handleTouchEnd}
  >
    {#if showHandle}
      <div class="drawer-handle" aria-hidden="true"></div>
    {/if}
    <div class="drawer-inner">
      {@render children?.()}
    </div>
  </div>
{/if}

<style>
  /* Overlay (backdrop) */
  .drawer-overlay {
    position: fixed;
    inset: 0;
    z-index: calc(var(--sheet-z-index, var(--sheet-z-base, 50)) - 1);

    pointer-events: var(--sheet-backdrop-pointer-events, auto);
    transition: opacity 350ms cubic-bezier(0.32, 0.72, 0, 1);
    opacity: 0;
  }

  .drawer-overlay[data-state="open"] {
    opacity: 1;
  }

  .drawer-overlay[data-state="closed"] {
    opacity: 0;
    pointer-events: none;
  }

  /* Edit panel backdrop - completely transparent and non-interactive */
  .drawer-overlay.edit-panel-backdrop {
    background: transparent !important;
    backdrop-filter: none !important;
    pointer-events: none !important;
  }

  /* Sequence Actions sheet backdrop - completely transparent to show beats behind */
  .drawer-overlay.actions-sheet-backdrop {
    background: transparent !important;
    backdrop-filter: none !important;
    pointer-events: auto !important;
  }

  /* Side-by-side layout: Constrain backdrop to right half of viewport */
  .drawer-overlay.side-by-side-layout {
    left: var(--create-panel-left, 50%);
    right: 0;
    top: var(--create-panel-top, 0);
    bottom: var(--create-panel-bottom, 0);
  }

  /* Drawer content container */
  .drawer-content {
    position: fixed;
    z-index: var(--sheet-z-index, var(--sheet-z-base, 50));
    display: flex;
    flex-direction: column;
    outline: none;
/* Background with fallback */    background: var(--sheet-bg, rgba(26, 26, 46, 0.95));    backdrop-filter: var(--sheet-filter, blur(24px));    -webkit-backdrop-filter: var(--sheet-filter, blur(24px));

    border: var(
      --sheet-border,
      var(--sheet-border-subtle, 1px solid rgba(255, 255, 255, 0.1))
    );

    /* Smooth CSS transitions */
    transition:
      transform 350ms cubic-bezier(0.32, 0.72, 0, 1),
      opacity 350ms cubic-bezier(0.32, 0.72, 0, 1);
    will-change: transform;

    /* Prevent pull-to-refresh ONLY on this drawer, not globally */
    overscroll-behavior-y: contain;
    /* Allow touch manipulation without disabling all gestures */
    touch-action: pan-y;
  }

  .drawer-content[data-state="closed"] {
    pointer-events: none;
  }

  /* Bottom placement - default (mobile) */
  .drawer-content[data-placement="bottom"]:not(.side-by-side-layout) {
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    max-width: 100%;
    max-height: var(
      --sheet-max-height,
      min(95vh, var(--modal-max-height, 95vh))
    );
    margin: 0;
    border-top-left-radius: var(
      --sheet-border-radius-top-left,
      var(--sheet-radius-large, 20px)
    );
    border-top-right-radius: var(
      --sheet-border-radius-top-right,
      var(--sheet-radius-large, 20px)
    );
    border-bottom: none;
  }

  .drawer-content[data-placement="bottom"][data-state="closed"] {
    transform: translate3d(0, 100%, 0);
  }

  .drawer-content[data-placement="bottom"][data-state="open"] {
    transform: translate3d(0, 0, 0);
  }

  /* Top placement */
  .drawer-content[data-placement="top"] {
    top: 0;
    left: 0;
    right: 0;
    width: var(--sheet-width, min(720px, 100%));
    max-height: var(
      --sheet-max-height,
      min(95vh, var(--modal-max-height, 95vh))
    );
    margin: 0 auto;
    border-bottom-left-radius: var(--sheet-radius-large, 20px);
    border-bottom-right-radius: var(--sheet-radius-large, 20px);
    border-top: none;
  }

  .drawer-content[data-placement="top"][data-state="closed"] {
    transform: translate3d(0, -100%, 0);
  }

  .drawer-content[data-placement="top"][data-state="open"] {
    transform: translate3d(0, 0, 0);
  }

  /* Right placement */
  .drawer-content[data-placement="right"] {
    top: 0;
    right: 0;
    bottom: 0;
    height: 100vh;
    width: var(--sheet-width, min(600px, 90vw));
    border-left: var(
      --sheet-border-strong,
      2px solid rgba(255, 255, 255, 0.15)
    );
    border-right: none;
    border-top-left-radius: var(--sheet-radius-large, 20px);
    border-bottom-left-radius: var(--sheet-radius-large, 20px);
  }

  .drawer-content[data-placement="right"][data-state="closed"] {
    transform: translate3d(100%, 0, 0);
  }

  .drawer-content[data-placement="right"][data-state="open"] {
    transform: translate3d(0, 0, 0);
  }

  /* Right placement in side-by-side mode - use tracked width */
  .drawer-content[data-placement="right"].side-by-side-layout {
    top: var(--create-panel-top, 0);
    bottom: var(--create-panel-bottom, 0);
    height: auto;
    max-height: none;
    width: var(--create-panel-width, clamp(360px, 32vw, 520px));
    max-width: 100%;
  }

  /* Left placement */
  .drawer-content[data-placement="left"] {
    top: 0;
    left: 0;
    bottom: 0;
    height: 100vh;
    width: var(--sheet-width, min(600px, 90vw));
    border-right: var(
      --sheet-border-strong,
      2px solid rgba(255, 255, 255, 0.15)
    );
    border-left: none;
    border-top-right-radius: var(--sheet-radius-large, 20px);
    border-bottom-right-radius: var(--sheet-radius-large, 20px);
  }

  .drawer-content[data-placement="left"][data-state="closed"] {
    transform: translate3d(-100%, 0, 0);
  }

  .drawer-content[data-placement="left"][data-state="open"] {
    transform: translate3d(0, 0, 0);
  }

  /* Handle - fully self-contained styling */
  /* 
   * The drawer handle is now fully self-contained within this component.
   * All styling variations (placement, layout mode) are handled here.
   * External components should NOT override these styles.
   * 
   * Handle adapts automatically to:
   * - Bottom placement (mobile): horizontal bar at top
   * - Right placement + side-by-side: vertical bar on left edge
   * - Left placement: vertical bar on right edge
   * - Top placement: horizontal bar at bottom
   */
  .drawer-handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 10px auto 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
  }

  /* Handle for right placement in side-by-side mode - vertical on left edge */
  .drawer-content[data-placement="right"].side-by-side-layout .drawer-handle {
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

  /* Handle for left placement - vertical on right edge */
  .drawer-content[data-placement="left"] .drawer-handle {
    position: absolute;
    top: 50%;
    right: 18px;
    width: 4px;
    height: 48px;
    margin: 0;
    border-radius: 999px;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.35);
  }

  /* Handle for top placement - horizontal on bottom edge */
  .drawer-content[data-placement="top"] .drawer-handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 8px auto 10px;
    order: 1; /* Place below content */
  }

  /* Handle for bottom placement - stays at top (default) */
  .drawer-content[data-placement="bottom"]:not(.side-by-side-layout)
    .drawer-handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 10px auto 8px;
  }

  /* Inner content container */
  .drawer-inner {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;

    /* Contain scroll - don't chain to parent */
    overscroll-behavior-y: contain;
  }

  /* Scrollbar styling */
  .drawer-inner::-webkit-scrollbar {
    width: 8px;
  }

  .drawer-inner::-webkit-scrollbar-track {
    background: transparent;
  }

  .drawer-inner::-webkit-scrollbar-thumb {
    border-radius: 4px;
  }

  .drawer-inner::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Mobile adjustments */
  @media (max-width: 480px) {
    .drawer-content[data-placement="bottom"] {
      border-top-left-radius: var(--sheet-radius-medium, 16px);
      border-top-right-radius: var(--sheet-radius-medium, 16px);
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .drawer-content {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .drawer-handle {
      background: rgba(255, 255, 255, 0.8);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .drawer-content,
    .drawer-overlay {
      transition: none;
    }
  }
</style>
