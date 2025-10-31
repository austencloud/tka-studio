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
 * Spring easing function that creates natural overshoot and settle
 * Mimics physics-based spring animation
 */
function springEasing(t: number): number {
  // Custom cubic-bezier approximation: cubic-bezier(0.34, 1.56, 0.64, 1)
  // This creates the signature spring overshoot effect
  const c1 = 0.34;
  const c2 = 1.56;
  const c3 = 0.64;
  const c4 = 1;

  return (
    3 * Math.pow(1 - t, 2) * t * c1 +
    3 * (1 - t) * Math.pow(t, 2) * c2 +
    Math.pow(t, 3) * c4 +
    3 * Math.pow(1 - t, 2) * t * (c2 - c1) * t
  );
}

/**
 * Spring scale transition with natural overshoot and settle
 * Perfect for button panel items that appear/disappear
 * Creates a delightful, physics-based animation that encourages interaction
 *
 * Based on 2025 UX trends for micro-interactions
 *
 * @param node - The element to animate
 * @param options - Configuration options
 * @param options.duration - Animation duration in ms (default: 550)
 * @param options.delay - Delay before animation starts in ms (default: 0)
 */
export function springScaleTransition(
  node: Element,
  options: { duration?: number; delay?: number } = {}
): TransitionConfig {
  const { duration = 550, delay = 0 } = options;

  return {
    duration,
    delay,
    css: (t: number) => {
      // Create enhanced spring scale curve with more pronounced overshoot
      let scale: number;

      if (t < 0.45) {
        // First phase: grow from 0 to 1.2 (more overshoot)
        scale = (t / 0.45) * 1.2;
      } else if (t < 0.7) {
        // Second phase: settle from 1.2 to 0.92 (deeper undershoot)
        const phase = (t - 0.45) / 0.25;
        scale = 1.2 - phase * 0.28;
      } else if (t < 0.85) {
        // Third phase: bounce back from 0.92 to 1.04 (subtle bounce)
        const phase = (t - 0.7) / 0.15;
        scale = 0.92 + phase * 0.12;
      } else {
        // Final phase: settle to 1.0
        const phase = (t - 0.85) / 0.15;
        scale = 1.04 - phase * 0.04;
      }

      return `
        transform: scale(${scale});
        opacity: ${t};
      `;
    },
    easing: springEasing,
  };
}
