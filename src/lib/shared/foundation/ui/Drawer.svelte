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
  import { resolve, TYPES } from "$shared/inversify";
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

  // Swipe-to-dismiss state
  let drawerElement = $state<HTMLElement | null>(null);
  let isDragging = $state(false);
  let dragStartX = 0;
  let dragStartY = 0;
  let dragDeltaX = $state(0);
  let dragDeltaY = $state(0);
  let dragStartTime = 0;

  // Initialize layout service if responsive layout is enabled
  onMount(() => {
    mounted = true;
    if (respectLayoutMode) {
      try {
        layoutService = resolve(
          TYPES.IResponsiveLayoutService
        ) as IResponsiveLayoutService;
      } catch (error) {
        console.warn(
          "ResponsiveLayoutService not available, using default layout"
        );
      }
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

      // Emit close event when closing
      if (wasOpen && !isOpen) {
        emitClose("programmatic");
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

  // Compute state attribute for CSS
  const dataState = $derived(isOpen ? "open" : "closed");

  // Compute full class names
  const overlayClasses = $derived(
    `drawer-overlay ${backdropClass} ${respectLayoutMode && isSideBySideLayout ? "side-by-side-layout" : ""}`.trim()
  );

  const contentClasses = $derived(
    `drawer-content ${drawerClass} ${respectLayoutMode && isSideBySideLayout ? "side-by-side-layout" : ""}`.trim()
  );

  // Touch/Mouse drag handlers (based on swipeGesture.ts pattern)
  function handleTouchStart(event: TouchEvent) {
    if (!dismissible) return;

    isDragging = true;
    dragStartX = event.touches[0]!.clientX;
    dragStartY = event.touches[0]!.clientY;
    dragStartTime = Date.now();
    dragDeltaX = 0;
    dragDeltaY = 0;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!isDragging || !dismissible) return;

    const currentX = event.touches[0]!.clientX;
    const currentY = event.touches[0]!.clientY;
    const deltaX = currentX - dragStartX;
    const deltaY = currentY - dragStartY;

    // Apply drag based on placement - only allow correct direction
    if (placement === "right") {
      dragDeltaX = Math.max(0, deltaX); // Only right
    } else if (placement === "bottom") {
      dragDeltaY = Math.max(0, deltaY); // Only down
    } else if (placement === "left") {
      dragDeltaX = Math.min(0, deltaX); // Only left
    } else if (placement === "top") {
      dragDeltaY = Math.min(0, deltaY); // Only up
    }

    // Prevent default if dragging significantly
    const distance = Math.abs(
      placement === "right" || placement === "left" ? dragDeltaX : dragDeltaY
    );
    if (distance > 25) {
      event.preventDefault();
    }
  }

  function handleTouchEnd(event: TouchEvent) {
    if (!isDragging || !dismissible) return;

    const threshold = 100;
    const maxDuration = 500;
    const duration = Date.now() - dragStartTime;
    const distance = Math.abs(
      placement === "right" || placement === "left" ? dragDeltaX : dragDeltaY
    );

    // Dismiss if dragged past threshold or fast swipe
    if (distance > threshold || (distance > 50 && duration < maxDuration)) {
      emitClose("programmatic");
      isOpen = false;
    }

    isDragging = false;
    dragDeltaX = 0;
    dragDeltaY = 0;
  }

  // Mouse handlers for desktop
  function handleMouseDown(event: MouseEvent) {
    if (!dismissible) return;

    isDragging = true;
    dragStartX = event.clientX;
    dragStartY = event.clientY;
    dragStartTime = Date.now();
    dragDeltaX = 0;
    dragDeltaY = 0;
  }

  function handleMouseMove(event: MouseEvent) {
    if (!isDragging || !dismissible) return;

    const deltaX = event.clientX - dragStartX;
    const deltaY = event.clientY - dragStartY;

    // Apply drag based on placement
    if (placement === "right") {
      dragDeltaX = Math.max(0, deltaX);
    } else if (placement === "bottom") {
      dragDeltaY = Math.max(0, deltaY);
    } else if (placement === "left") {
      dragDeltaX = Math.min(0, deltaX);
    } else if (placement === "top") {
      dragDeltaY = Math.min(0, deltaY);
    }
  }

  function handleMouseUp(event: MouseEvent) {
    if (!isDragging || !dismissible) return;

    const threshold = 100;
    const maxDuration = 500;
    const duration = Date.now() - dragStartTime;
    const distance = Math.abs(
      placement === "right" || placement === "left" ? dragDeltaX : dragDeltaY
    );

    if (distance > threshold || (distance > 50 && duration < maxDuration)) {
      emitClose("programmatic");
      isOpen = false;
    }

    isDragging = false;
    dragDeltaX = 0;
    dragDeltaY = 0;
  }

  // Compute transform for dragging
  const dragTransform = $derived(() => {
    if (!isDragging) return "";

    if (placement === "right") {
      return `translate3d(${dragDeltaX}px, 0, 0)`;
    } else if (placement === "bottom") {
      return `translate3d(0, ${dragDeltaY}px, 0)`;
    } else if (placement === "left") {
      return `translate3d(${dragDeltaX}px, 0, 0)`;
    } else if (placement === "top") {
      return `translate3d(0, ${dragDeltaY}px, 0)`;
    }
    return "";
  });
</script>

<svelte:window onkeydown={handleKeydown} />

{#if mounted && isOpen}
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
    style:transform={isDragging ? dragTransform() : ""}
    style:transition={isDragging ? "none" : ""}
    ontouchstart={handleTouchStart}
    ontouchmove={handleTouchMove}
    ontouchend={handleTouchEnd}
    onmousedown={handleMouseDown}
    onmousemove={handleMouseMove}
    onmouseup={handleMouseUp}
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
    background: var(
      --sheet-backdrop-bg,
      var(--backdrop-medium, rgba(0, 0, 0, 0.5))
    );
    backdrop-filter: var(
      --sheet-backdrop-filter,
      var(--backdrop-blur-medium, blur(8px))
    );
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

    /* Default styling */
    background: var(--sheet-bg, var(--sheet-bg-glass, rgba(20, 25, 35, 0.95)));
    backdrop-filter: var(
      --sheet-filter,
      var(--glass-backdrop-strong, blur(24px))
    );
    border: var(
      --sheet-border,
      var(--sheet-border-subtle, 1px solid rgba(255, 255, 255, 0.1))
    );
    box-shadow: var(
      --sheet-shadow,
      var(--sheet-shadow-bottom, 0 -4px 24px rgba(0, 0, 0, 0.3))
    );

    /* Smooth CSS transitions - THIS IS THE MAGIC */
    transition:
      transform 350ms cubic-bezier(0.32, 0.72, 0, 1),
      opacity 350ms cubic-bezier(0.32, 0.72, 0, 1);
    will-change: transform;

    /* Enable swipe-to-dismiss without browser interference */
    touch-action: none;
    user-select: none;
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

  /* Handle */
  .drawer-handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 10px auto 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
  }

  /* Inner content container */
  .drawer-inner {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  /* Scrollbar styling */
  .drawer-inner::-webkit-scrollbar {
    width: 8px;
  }

  .drawer-inner::-webkit-scrollbar-track {
    background: transparent;
  }

  .drawer-inner::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
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
