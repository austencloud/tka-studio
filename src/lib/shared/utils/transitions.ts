/**
 * Shared transition utilities for consistent animations across the app
 *
 * Provides reusable transition functions for Svelte components
 */

import type { TransitionConfig } from "svelte/transition";

export interface SlideTransitionOptions {
  /**
   * Duration in milliseconds
   * @default 350
   */
  duration?: number;

  /**
   * Direction to slide from
   * @default 'bottom'
   */
  direction?: "top" | "bottom" | "left" | "right";

  /**
   * Easing function
   * @default 'cubic'
   */
  easing?: "cubic" | "linear";
}

export interface FadeTransitionOptions {
  /**
   * Duration in milliseconds
   * @default 250
   */
  duration?: number;

  /**
   * Delay before starting in milliseconds
   * @default 0
   */
  delay?: number;
}

/**
 * Custom cubic easing out: 1 - (1-t)^3
 */
function cubicOut(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

/**
 * Slide transition with configurable direction and easing
 * Perfect for bottom sheets, side panels, and slide-in menus
 */
export function slideTransition(
  node: Element,
  options: SlideTransitionOptions = {}
): TransitionConfig {
  const { duration = 350, direction = "bottom", easing = "cubic" } = options;

  const computedStyle = getComputedStyle(node);
  const opacity = parseFloat(computedStyle.opacity);

  // Determine transform based on direction
  const getTransform = (t: number) => {
    const easedT = easing === "cubic" ? cubicOut(t) : t;

    switch (direction) {
      case "bottom":
        return `translateY(${(1 - easedT) * 100}%)`;
      case "top":
        return `translateY(${(easedT - 1) * 100}%)`;
      case "right":
        return `translateX(${(1 - easedT) * 100}%)`;
      case "left":
        return `translateX(${(easedT - 1) * 100}%)`;
      default:
        return `translateY(${(1 - easedT) * 100}%)`;
    }
  };

  return {
    duration,
    css: (t: number) => {
      return `
        transform: ${getTransform(t)};
        opacity: ${t * opacity};
      `;
    },
  };
}

/**
 * Fade transition with optional delay
 * Perfect for backdrops and overlays
 */
export function fadeTransition(
  node: Element,
  options: FadeTransitionOptions = {}
): TransitionConfig {
  const { duration = 250, delay = 0 } = options;

  return {
    duration,
    delay,
    css: (t: number) => `opacity: ${t}`,
  };
}

/**
 * Scale transition with fade
 * Perfect for modals and dialogs
 */
export function scaleTransition(
  node: Element,
  options: { duration?: number; start?: number } = {}
): TransitionConfig {
  const { duration = 300, start = 0.95 } = options;

  return {
    duration,
    css: (t: number) => {
      const easedT = cubicOut(t);
      const scale = start + (1 - start) * easedT;
      return `
        transform: scale(${scale});
        opacity: ${t};
      `;
    },
  };
}

/**
 * Fly transition with configurable direction
 * Perfect for notifications and toasts
 */
export function flyTransition(
  node: Element,
  options: { duration?: number; x?: number; y?: number } = {}
): TransitionConfig {
  const { duration = 400, x = 0, y = 0 } = options;

  return {
    duration,
    css: (t: number) => {
      const easedT = cubicOut(t);
      return `
        transform: translate(${(1 - easedT) * x}px, ${(1 - easedT) * y}px);
        opacity: ${t};
      `;
    },
  };
}

/**
 * DEPRECATED: springScaleTransition has been replaced by the unified animation system
 *
 * The old springScaleTransition used hardcoded spring physics approximations (40+ lines).
 * It has been migrated to use PresenceAnimation from $shared/animation which provides:
 * - Real spring physics via Svelte 5's native Spring class
 * - Consistent animation behavior across the app
 * - Configurable spring presets (gentle, snappy, wobbly, etc.)
 *
 * Migration example:
 * ```svelte
 * // Old:
 * import { springScaleTransition } from "$lib/shared/utils/transitions.js";
 * <div transition:springScaleTransition>...</div>
 *
 * // New:
 * import { PresenceAnimation } from "$shared/animation";
 * function presenceTransition(node, { duration = 550, delay = 0 } = {}) {
 *   const animation = new PresenceAnimation('snappy');
 *   animation.enter();
 *   return { duration, delay, css: (t) => `transform: scale(${0.95 + 0.05 * t}); opacity: ${t};` };
 * }
 * <div transition:presenceTransition>...</div>
 * ```
 *
 * See: src/lib/shared/animation/ for the unified animation system
 * See: ANIMATION_SYSTEM.md for migration guide
 */
