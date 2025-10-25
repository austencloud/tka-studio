/**
 * Scroll Lock Utility
 * Manages body scroll locking for modals and overlays
 * Prevents background scrolling while maintaining scrollbar width compensation
 */

export interface ScrollLockState {
  /** Locks the body scroll */
  lock: () => void;
  /** Unlocks the body scroll */
  unlock: () => void;
  /** Whether scroll is currently locked */
  isLocked: () => boolean;
}

/**
 * Gets the current scrollbar width to prevent layout shift
 */
function getScrollbarWidth(): number {
  if (typeof window === "undefined") return 0;
  return window.innerWidth - document.documentElement.clientWidth;
}

/**
 * Creates a scroll lock manager
 * Maintains a reference count to handle nested modals
 */
export function createScrollLock(): ScrollLockState {
  let lockCount = 0;
  let originalOverflow = "";
  let originalPaddingRight = "";

  function lock() {
    if (typeof document === "undefined") return;

    // Only store original values on first lock
    if (lockCount === 0) {
      originalOverflow = document.body.style.overflow;
      originalPaddingRight = document.body.style.paddingRight;

      // Apply scroll lock with scrollbar width compensation
      document.body.style.overflow = "hidden";
      document.body.style.paddingRight = getScrollbarWidth() + "px";
    }

    lockCount++;
  }

  function unlock() {
    if (typeof document === "undefined") return;

    lockCount = Math.max(0, lockCount - 1);

    // Only restore when all locks are released
    if (lockCount === 0) {
      document.body.style.overflow = originalOverflow;
      document.body.style.paddingRight = originalPaddingRight;
    }
  }

  function isLocked(): boolean {
    return lockCount > 0;
  }

  return {
    lock,
    unlock,
    isLocked,
  };
}

/**
 * Global scroll lock instance (singleton pattern)
 * Use this for coordinating multiple modals
 */
export const globalScrollLock = createScrollLock();

/**
 * Svelte effect-friendly scroll lock
 * Returns cleanup function for use in $effect
 */
export function useScrollLock(enabled: boolean = true): () => void {
  if (enabled) {
    globalScrollLock.lock();
  }

  return () => {
    if (enabled) {
      globalScrollLock.unlock();
    }
  };
}
