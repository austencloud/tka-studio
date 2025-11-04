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
  let scrollableElement = $state<HTMLElement | null>(null); // Track the scrollable element for this gesture
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
      if (first && (active === first || !sheetElement.contains(active))) {
        event.preventDefault();
        last?.focus({ preventScroll: true });
      }
    } else {
      if (first && active === last) {
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

  // Helper to find the scrollable ancestor element
  function findScrollableAncestor(target: HTMLElement): HTMLElement | null {
    let element: HTMLElement | null = target;
    while (element && element !== sheetElement) {
      const styles = window.getComputedStyle(element);
      const overflowY = styles.overflowY;

      if ((overflowY === 'auto' || overflowY === 'scroll') && element.scrollHeight > element.clientHeight) {
        // This is a scrollable area with actual scrollable content
        return element;
      }

      element = element.parentElement;
    }
    return null;
  }

  // Helper to check if we should allow dismiss gesture from a scrollable area
  function shouldAllowDismissFromScroll(scrollableElement: HTMLElement | null, deltaY: number): boolean {
    if (!scrollableElement) return true; // Not in a scrollable area, allow dismiss

    // If scrolled to the top and swiping down, allow dismiss
    if (scrollableElement.scrollTop === 0 && deltaY > 0) {
      return true;
    }

    // Otherwise, let the scroll area handle the gesture
    return false;
  }

  // Swipe to dismiss handlers
  function handlePointerDown(event: PointerEvent) {
    // Only handle bottom placement for now
    if (placement !== "bottom") return;

    // Check if the pointer down is on an interactive element (button, input, etc.)
    // If so, don't interfere with the click - let it through
    const target = event.target as HTMLElement;
    const isInteractive =
      target.closest(
        'button, a, input, select, textarea, [role="button"], [onclick]'
      ) !== null;

    if (isInteractive) {
      // Don't start drag tracking for interactive elements - let the click work
      return;
    }

    // Find if we're in a scrollable area and store the reference
    scrollableElement = findScrollableAncestor(target);

    // Start tracking potential drag from anywhere on the sheet
    isDragging = true;
    isDismissGesture = false; // Will determine this once user moves
    dragStartY = event.clientY;
    currentDragY = event.clientY;

    // DON'T capture pointer yet - let scrolling work normally
    // We'll capture only if we determine this is a dismiss gesture
  }

  function handlePointerMove(event: PointerEvent) {
    if (!isDragging) return;

    currentDragY = event.clientY;
    const deltaY = currentDragY - dragStartY;

    // If we haven't committed to a gesture type yet, decide now
    if (!isDismissGesture && Math.abs(deltaY) > VERTICAL_DRAG_THRESHOLD) {
      if (deltaY > 0) {
        // Dragging down - check if we should allow dismiss from scroll area
        if (shouldAllowDismissFromScroll(scrollableElement, deltaY)) {
          // Either not in a scroll area, or at the top and swiping down
          // NOW we capture the pointer since this is a dismiss gesture
          isDismissGesture = true;
          if (sheetElement) {
            sheetElement.setPointerCapture(event.pointerId);
          }
        } else {
          // In a scroll area that should handle the gesture
          // Reset drag state and let the scroll happen
          isDragging = false;
          dragStartY = 0;
          currentDragY = 0;
          scrollableElement = null;
          return;
        }
      } else {
        // Dragging up - not a dismiss gesture, allow scrolling
        isDragging = false;
        dragStartY = 0;
        currentDragY = 0;
        scrollableElement = null;
        return;
      }
    }

    // If this is a dismiss gesture, update the translation
    if (isDismissGesture && deltaY > 0) {
      dragTranslateY = deltaY;
    }
  }

  function handlePointerUp(event: PointerEvent) {
    if (!isDragging && !isDismissGesture) return;

    const deltaY = currentDragY - dragStartY;

    // Release pointer capture only if we captured it
    if (isDismissGesture && sheetElement) {
      try {
        sheetElement.releasePointerCapture(event.pointerId);
      } catch (e) {
        // Ignore errors if pointer wasn't captured
      }
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
    scrollableElement = null;
  }

  function handlePointerCancel(event: PointerEvent) {
    // Release pointer capture only if we captured it
    if (isDismissGesture && sheetElement) {
      try {
        sheetElement.releasePointerCapture(event.pointerId);
      } catch (e) {
        // Ignore errors if pointer wasn't captured
      }
    }

    // Reset on cancel (e.g., if another gesture takes over like browser scroll)
    isDragging = false;
    isDismissGesture = false;
    dragStartY = 0;
    currentDragY = 0;
    dragTranslateY = 0;
    scrollableElement = null;
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
    if (!backdropElement || !isOpen) return;

    // Add touchstart listener with passive: false so we can preventDefault
    // This prevents the browser from canceling our pointer capture
    const touchStartHandler = (e: TouchEvent) => {
      // Check if the touch is on an interactive element
      const target = e.target as HTMLElement;
      const isInteractive =
        target.closest(
          'button, a, input, select, textarea, [role="button"], [onclick]'
        ) !== null;

      if (isInteractive) {
        // Don't prevent default for interactive elements - let the touch/click work
        return;
      }

      // We no longer skip scrollable areas here - the gesture logic handles it
      // This allows us to detect when we're at the top of a scroll area
      // Don't prevent default - let browser handle scrolling normally
    };

    // Add touchmove listener with passive: false so we can preventDefault
    // This prevents pull-to-refresh and other browser gestures
    const touchMoveHandler = (e: TouchEvent) => {
      // Prevent pull-to-refresh on the backdrop
      if (e.target === backdropElement) {
        e.preventDefault();
        return;
      }

      // Prevent default if we're actively dragging to dismiss
      if (isDragging && isDismissGesture) {
        e.preventDefault();
      }
    };

    backdropElement.addEventListener("touchstart", touchStartHandler, {
      passive: false,
      capture: false,
    });

    backdropElement.addEventListener("touchmove", touchMoveHandler, {
      passive: false,
      capture: false,
    });

    return () => {
      backdropElement?.removeEventListener("touchstart", touchStartHandler);
      backdropElement?.removeEventListener("touchmove", touchMoveHandler);
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
      style={dragTranslateY > 0
        ? `transform: translateY(${dragTranslateY}px);`
        : ""}
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
    z-index: var(--sheet-z-index, var(--sheet-z-base));
    background: var(--sheet-backdrop-bg, var(--backdrop-medium));
    backdrop-filter: var(--sheet-backdrop-filter, var(--backdrop-blur-medium));
    pointer-events: var(--sheet-backdrop-pointer-events, auto);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    /* Prevent pull-to-refresh on mobile */
    overscroll-behavior: contain;
    touch-action: none;
  }

  /* Edit panel backdrop - completely transparent and non-interactive */
  .bottom-sheet-backdrop.edit-panel-backdrop {
    background: transparent !important;
    backdrop-filter: none !important;
    pointer-events: none !important;
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
    width: var(--sheet-width, min(720px, 100%));
    max-height: var(
      --sheet-max-height,
      min(95vh, var(--modal-max-height, 95vh))
    );
    background: var(--sheet-bg, var(--sheet-bg-glass));
    backdrop-filter: var(
      --sheet-filter,
      var(--glass-backdrop-strong, blur(24px))
    );
    border-top-left-radius: var(
      --sheet-border-radius-top-left,
      var(--sheet-radius-large)
    );
    border-top-right-radius: var(
      --sheet-border-radius-top-right,
      var(--sheet-radius-large)
    );
    border: var(--sheet-border, var(--sheet-border-subtle));
    box-shadow: var(--sheet-shadow, var(--sheet-shadow-bottom));
    pointer-events: var(--sheet-pointer-events, auto);
    overflow: hidden;
    outline: none;
    display: flex;
    flex-direction: column;
    /* Allow taps and pans but prevent double-tap zoom and other browser gestures */
    touch-action: manipulation;
    /* Smooth transition when not dragging */
    transition: transform
      var(--sheet-transition, var(--sheet-transition-smooth));
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
      border-top-left-radius: var(
        --sheet-border-radius-top-left,
        var(--sheet-radius-medium)
      );
      border-top-right-radius: var(
        --sheet-border-radius-top-right,
        var(--sheet-radius-medium)
      );
    }
  }
</style>
