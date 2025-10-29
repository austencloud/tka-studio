<!--
  BottomSheet.svelte

  Shared bottom sheet component that provides:
    - Accessible slide-up panel pattern with backdrop
    - Centralized escape key and backdrop dismissal
    - Focus trapping and restoration when the sheet closes
    - Optional scroll locking with safe-area padding
    - Pluggable styling via `class`/`backdropClass` props and slots
-->
<script lang="ts">
  import { createEventDispatcher, onDestroy, tick } from "svelte";
  import { cubicOut } from "svelte/easing";
  import { fade } from "svelte/transition";

  type CloseReason = "backdrop" | "escape" | "programmatic";

  let {
    isOpen = false,
    closeOnBackdrop = true,
    closeOnEscape = true,
    focusTrap = true,
    lockScroll = true,
    labelledBy,
    ariaLabel,
    role = "dialog",
    showHandle = true,
    class: sheetClass = "",
    backdropClass = "",
    initialFocusSelector,
    children,
    placement = "bottom",
  } = $props<{
    isOpen?: boolean;
    closeOnBackdrop?: boolean;
    closeOnEscape?: boolean;
    focusTrap?: boolean;
    lockScroll?: boolean;
    labelledBy?: string;
    ariaLabel?: string;
    role?: "dialog" | "menu" | "listbox" | "alertdialog";
    showHandle?: boolean;
    class?: string;
    backdropClass?: string;
    initialFocusSelector?: string;
    children?: () => unknown;
    placement?: "bottom" | "top" | "right" | "left";
  }>();

  const dispatch = createEventDispatcher<{
    close: { reason: CloseReason };
  }>();

  const SCROLL_LOCK_KEY = "__tka_bottom_sheet_lock__";

  type ScrollLockState = {
    count: number;
    overflow: string | null;
  };

  let sheetElement = $state<HTMLElement | null>(null);
  let backdropElement = $state<HTMLElement | null>(null);
  let contentElement = $state<HTMLElement | null>(null);
  let previouslyFocused: HTMLElement | null = null;
  let lastOpenState = false;

  // Swipe to dismiss state
  let isDragging = $state(false);
  let isDismissGesture = $state(false); // Track if this gesture is for dismissing
  let dragStartY = $state(0);
  let currentDragY = $state(0);
  let dragTranslateY = $state(0);
  const DISMISS_THRESHOLD = 100; // pixels to drag down before dismissing
  const VERTICAL_DRAG_THRESHOLD = 10; // pixels to move before committing to vertical drag

  function lockBodyScroll() {
    if (!lockScroll || typeof document === "undefined") {
      return;
    }

    const state: ScrollLockState = (globalThis as any)[SCROLL_LOCK_KEY] ?? {
      count: 0,
      overflow: null,
    };

    if (state.count === 0) {
      state.overflow = document.body.style.overflow || null;
      document.body.style.overflow = "hidden";
    }

    state.count += 1;
    (globalThis as any)[SCROLL_LOCK_KEY] = state;
  }

  function unlockBodyScroll() {
    if (!lockScroll || typeof document === "undefined") {
      return;
    }

    const state: ScrollLockState | undefined = (globalThis as any)[
      SCROLL_LOCK_KEY
    ];

    if (!state) {
      return;
    }

    state.count = Math.max(0, state.count - 1);

    if (state.count === 0) {
      document.body.style.overflow = state.overflow ?? "";
      (globalThis as any)[SCROLL_LOCK_KEY] = undefined;
    } else {
      (globalThis as any)[SCROLL_LOCK_KEY] = state;
    }
  }

  function emitClose(reason: CloseReason) {
    dispatch("close", { reason });
  }

  function requestClose(reason: CloseReason) {
    emitClose(reason);
  }

  function handleBackdropClick() {
    if (!closeOnBackdrop) {
      return;
    }
    requestClose("backdrop");
  }

  function focusFirstElement() {
    if (!sheetElement) {
      return;
    }

    const target =
      (initialFocusSelector &&
        sheetElement.querySelector<HTMLElement>(initialFocusSelector)) ||
      sheetElement;

    target.focus({ preventScroll: true });
  }

  function getFocusableElements(root: HTMLElement): HTMLElement[] {
    const selectors = [
      "a[href]",
      "button:not([disabled])",
      "input:not([disabled]):not([type='hidden'])",
      "select:not([disabled])",
      "textarea:not([disabled])",
      "[tabindex]:not([tabindex='-1'])",
    ];

    return Array.from(
      root.querySelectorAll<HTMLElement>(selectors.join(","))
    ).filter(
      (el) => !el.hasAttribute("disabled") && !el.getAttribute("aria-hidden")
    );
  }

  function handleTabKey(event: KeyboardEvent) {
    if (!focusTrap || !sheetElement) {
      return;
    }

    const focusable = getFocusableElements(sheetElement);

    if (focusable.length === 0) {
      event.preventDefault();
      sheetElement.focus({ preventScroll: true });
      return;
    }

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const active = document.activeElement as HTMLElement | null;

    if (event.shiftKey) {
      if (active === first || !sheetElement.contains(active)) {
        event.preventDefault();
        last.focus({ preventScroll: true });
      }
    } else {
      if (active === last) {
        event.preventDefault();
        first.focus({ preventScroll: true });
      }
    }
  }

  function handleWindowKeydown(event: KeyboardEvent) {
    if (!isOpen) {
      return;
    }

    if (event.key === "Escape" && closeOnEscape) {
      event.preventDefault();
      requestClose("escape");
      return;
    }

    if (event.key === "Tab") {
      handleTabKey(event);
    }
  }

  // Swipe to dismiss handlers
  function handlePointerDown(event: PointerEvent) {
    // Only handle bottom placement for now
    if (placement !== "bottom") return;

    // Check if the pointer down is on an interactive element (button, input, etc.)
    // If so, don't interfere with the click - let it through
    const target = event.target as HTMLElement;
    const isInteractive =
      target.closest('button, a, input, select, textarea, [role="button"], [onclick]') !== null;

    if (isInteractive) {
      // Don't start drag tracking for interactive elements - let the click work
      return;
    }

    // Start tracking potential drag from anywhere on the sheet
    isDragging = true;
    isDismissGesture = false; // Will determine this once user moves
    dragStartY = event.clientY;
    currentDragY = event.clientY;

    // Capture pointer to continue receiving events even if pointer moves outside element
    if (sheetElement) {
      sheetElement.setPointerCapture(event.pointerId);
    }
  }

  function handlePointerMove(event: PointerEvent) {
    if (!isDragging) return;

    currentDragY = event.clientY;
    const deltaY = currentDragY - dragStartY;

    // If we haven't committed to a gesture type yet, decide now
    if (!isDismissGesture && Math.abs(deltaY) > VERTICAL_DRAG_THRESHOLD) {
      if (deltaY > 0) {
        // Dragging down - this is a dismiss gesture
        isDismissGesture = true;
      }
      // Note: If dragging up (deltaY < 0), we just do nothing
      // No scrolling in this sheet, so upward drags are ignored
    }

    // If this is a dismiss gesture, update the translation
    if (isDismissGesture && deltaY > 0) {
      dragTranslateY = deltaY;
    }
  }

  function handlePointerUp(event: PointerEvent) {
    if (!isDragging) return;

    const deltaY = currentDragY - dragStartY;

    // Release pointer capture
    if (sheetElement) {
      sheetElement.releasePointerCapture(event.pointerId);
    }

    // If this was a dismiss gesture and dragged far enough, dismiss
    if (isDismissGesture && deltaY > DISMISS_THRESHOLD) {
      requestClose("backdrop");
    }

    // Reset drag state
    isDragging = false;
    isDismissGesture = false;
    dragStartY = 0;
    currentDragY = 0;
    dragTranslateY = 0;
  }

  function handlePointerCancel(event: PointerEvent) {
    // Reset on cancel (e.g., if another gesture takes over)
    isDragging = false;
    isDismissGesture = false;
    dragStartY = 0;
    currentDragY = 0;
    dragTranslateY = 0;

    if (sheetElement) {
      sheetElement.releasePointerCapture(event.pointerId);
    }
  }

  // Prevent pull-to-refresh on mobile when touching the backdrop
  function handleTouchMove(event: TouchEvent) {
    // Prevent pull-to-refresh on the backdrop
    if (event.target === backdropElement) {
      event.preventDefault();
      return;
    }

    // Also prevent default if we're actively dragging to dismiss
    if (isDragging && isDismissGesture) {
      event.preventDefault();
    }
  }

  // Prevent default touch handling on the sheet to avoid browser gesture conflicts
  function handleTouchStart(event: TouchEvent) {
    // Check if the touch is on an interactive element
    const target = event.target as HTMLElement;
    const isInteractive =
      target.closest('button, a, input, select, textarea, [role="button"], [onclick]') !== null;

    if (isInteractive) {
      // Don't prevent default for interactive elements - let the touch/click work
      return;
    }

    // This is critical: prevent the browser from starting its default pan/scroll gestures
    // which would cancel our pointer capture and cause the "snap back" behavior
    if (placement === "bottom") {
      event.preventDefault();
    }
  }

  $effect(() => {
    if (typeof window === "undefined") {
      return;
    }

    if (isOpen) {
      if (!lastOpenState && document.activeElement instanceof HTMLElement) {
        previouslyFocused = document.activeElement;
      }

      lockBodyScroll();

      tick().then(() => {
        focusFirstElement();
      });
    } else if (lastOpenState) {
      unlockBodyScroll();
      if (previouslyFocused && typeof previouslyFocused.focus === "function") {
        previouslyFocused.focus({ preventScroll: true });
      }
      previouslyFocused = null;
    }

    lastOpenState = isOpen;

    return () => {
      if (lastOpenState) {
        unlockBodyScroll();
      }
    };
  });

  // Register non-passive touch event listeners to prevent browser gestures
  $effect(() => {
    if (!sheetElement || !isOpen) return;

    // Add touchstart listener with passive: false so we can preventDefault
    // This prevents the browser from canceling our pointer capture
    const touchStartHandler = (e: TouchEvent) => {
      // Check if the touch is on an interactive element
      const target = e.target as HTMLElement;
      const isInteractive =
        target.closest('button, a, input, select, textarea, [role="button"], [onclick]') !== null;

      if (isInteractive) {
        // Don't prevent default for interactive elements - let the touch/click work
        return;
      }

      if (placement === "bottom") {
        // Prevent browser's default pan/scroll gesture handling
        e.preventDefault();
      }
    };

    sheetElement.addEventListener("touchstart", touchStartHandler, {
      passive: false,
      capture: false,
    });

    return () => {
      sheetElement?.removeEventListener("touchstart", touchStartHandler);
    };
  });

  onDestroy(() => {
    if (lastOpenState) {
      unlockBodyScroll();
    }
  });

  const slideTransition = (node: Element, { duration = 300 } = {}) => {
    return {
      duration,
      easing: cubicOut,
      css: (t: number) => {
        const offset = (1 - t) * 100;
        switch (placement) {
          case "top":
            return `transform: translateY(-${offset}%);`;
          case "right":
            return `transform: translateX(${offset}%);`;
          case "left":
            return `transform: translateX(-${offset}%);`;
          case "bottom":
          default:
            return `transform: translateY(${offset}%);`;
        }
      },
    };
  };
</script>

<svelte:window on:keydown={handleWindowKeydown} />

{#if isOpen}
  <div
    class={`bottom-sheet-backdrop ${backdropClass}`.trim()}
    bind:this={backdropElement}
    data-placement={placement}
    role="presentation"
    transition:fade|local={{ duration: 180 }}
    onclick={handleBackdropClick}
    ontouchmove={handleTouchMove}
  >
    <div
      class={`bottom-sheet ${sheetClass}`.trim()}
      class:is-dragging={isDragging}
      bind:this={sheetElement}
      data-placement={placement}
      {role}
      aria-modal="true"
      aria-labelledby={labelledBy}
      aria-label={ariaLabel}
      tabindex="-1"
      style={dragTranslateY > 0 ? `transform: translateY(${dragTranslateY}px);` : ''}
      onclick={(e) => e.stopPropagation()}
      onpointerdown={handlePointerDown}
      onpointermove={handlePointerMove}
      onpointerup={handlePointerUp}
      onpointercancel={handlePointerCancel}
      transition:slideTransition
    >
      {#if showHandle}
        <div class="bottom-sheet__handle" aria-hidden="true"></div>
      {/if}
      <div class="bottom-sheet__content" bind:this={contentElement}>
        {@render children?.()}
      </div>
    </div>
  </div>
{/if}

<style>
  .bottom-sheet-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1000;
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    /* Prevent pull-to-refresh on mobile */
    overscroll-behavior: contain;
    touch-action: none;
  }

  .bottom-sheet-backdrop[data-placement="top"] {
    align-items: flex-start;
  }

  .bottom-sheet-backdrop[data-placement="right"] {
    justify-content: flex-end;
    align-items: stretch;
  }

  .bottom-sheet-backdrop[data-placement="left"] {
    justify-content: flex-start;
    align-items: stretch;
  }

  .bottom-sheet {
    position: relative;
    width: min(720px, 100%);
    max-height: min(95vh, var(--modal-max-height, 95vh));
    background: rgba(24, 24, 24, 0.92);
    backdrop-filter: var(--glass-backdrop-strong, blur(24px));
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 -12px 32px rgba(0, 0, 0, 0.35);
    overflow: hidden;
    outline: none;
    display: flex;
    flex-direction: column;
    /* Allow taps and pans but prevent double-tap zoom and other browser gestures */
    touch-action: manipulation;
    /* Smooth transition when not dragging */
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .bottom-sheet.is-dragging {
    /* Disable transition while dragging for immediate feedback */
    transition: none;
  }

  .bottom-sheet[data-placement="right"],
  .bottom-sheet[data-placement="left"] {
    height: 100vh;
    max-height: 100vh;
  }

  .bottom-sheet__handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 10px auto 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.3);
    cursor: grab;
  }

  .is-dragging .bottom-sheet__handle {
    cursor: grabbing;
  }

  .bottom-sheet__content {
    flex: 1;
    overflow-y: auto;
    width: 100%;
    box-sizing: border-box;
    /* Prevent overscroll from propagating to parent (pull-to-refresh) */
    overscroll-behavior-y: contain;
    /* Allow pointer events to bubble up for swipe-to-dismiss */
    touch-action: inherit;
  }

  @media (prefers-contrast: high) {
    .bottom-sheet {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .bottom-sheet__handle {
      background: rgba(255, 255, 255, 0.8);
    }
  }

  @media (max-width: 480px) {
    .bottom-sheet {
      border-top-left-radius: 20px;
      border-top-right-radius: 20px;
    }
  }
</style>
