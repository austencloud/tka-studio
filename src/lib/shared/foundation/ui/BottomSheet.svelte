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
  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

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
  let previouslyFocused: HTMLElement | null = null;
  let lastOpenState = false;

  function lockBodyScroll() {
    if (!lockScroll || typeof document === "undefined") {
      return;
    }

    const state: ScrollLockState =
      (globalThis as any)[SCROLL_LOCK_KEY] ?? { count: 0, overflow: null };

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

    return Array.from(root.querySelectorAll<HTMLElement>(selectors.join(","))).filter(
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
    data-placement={placement}
    role="presentation"
    transition:fade|local={{ duration: 180 }}
    onclick={handleBackdropClick}
  >
    <div
      class={`bottom-sheet ${sheetClass}`.trim()}
      bind:this={sheetElement}
      data-placement={placement}
      role={role}
      aria-modal="true"
      aria-labelledby={labelledBy}
      aria-label={ariaLabel}
      tabindex="-1"
      onclick={(e) => e.stopPropagation()}
      transition:slideTransition
    >
      {#if showHandle}
        <div class="bottom-sheet__handle" aria-hidden="true"></div>
      {/if}
      <div class="bottom-sheet__content">
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
    max-height: min(80vh, var(--modal-max-height, 80vh));
    background: rgba(24, 24, 24, 0.92);
    backdrop-filter: var(--glass-backdrop-strong, blur(24px));
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 -12px 32px rgba(0, 0, 0, 0.35);
    overflow: hidden;
    padding-bottom: env(safe-area-inset-bottom, 16px);
    outline: none;
    display: flex;
    flex-direction: column;
  }

  .bottom-sheet[data-placement="right"],
  .bottom-sheet[data-placement="left"] {
    height: 100vh;
    max-height: 100vh;
  }

  .bottom-sheet__handle {
    position: relative;
    width: 48px;
    height: 5px;
    margin: 12px auto 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.4);
  }

  .bottom-sheet__content {
    flex: 1;
    overflow-y: auto;
    width: 100%;
    padding: 0 16px 16px;
    box-sizing: border-box;
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
    .bottom-sheet__content {
      padding-left: 12px;
      padding-right: 12px;
    }
  }
</style>
