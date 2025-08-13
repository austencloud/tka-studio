/**
 * Fold Animation System - Smooth Transitions Between Landing & App
 *
 * Creates a sophisticated fold-over effect that makes the transition
 * between landing page and app interface feel seamless and professional.
 */

import { cubicOut } from "svelte/easing";

export interface FoldTransitionParams {
  duration?: number;
  direction?: "fold-in" | "fold-out";
  axis?: "x" | "y";
  easing?: (t: number) => number;
}

export interface TransitionReturn {
  delay?: number;
  duration: number;
  easing?: (t: number) => number;
  css?: (t: number) => string;
  tick?: (t: number) => void;
}

/**
 * Main fold transition - creates the signature "folding" effect
 */
export function foldTransition(
  node: Element,
  params: FoldTransitionParams = {},
): TransitionReturn {
  const {
    duration = 600,
    direction = "fold-in",
    axis = "y",
    easing = cubicOut,
  } = params;

  const isFoldIn = direction === "fold-in";
  const isYAxis = axis === "y";

  return {
    duration,
    easing,
    css: (t: number) => {
      const progress = isFoldIn ? t : 1 - t;
      const angle = (1 - progress) * 90;
      const opacity = Math.max(0, progress - 0.1); // Slight delay on opacity
      const scale = 0.9 + progress * 0.1; // Subtle scale effect

      // Different fold directions
      const transform = isYAxis
        ? `rotateX(${angle}deg) scale(${scale})`
        : `rotateY(${angle}deg) scale(${scale})`;

      const transformOrigin = isYAxis ? "center top" : "left center";

      return `
                transform: ${transform};
                transform-origin: ${transformOrigin};
                opacity: ${opacity};
                backface-visibility: hidden;
                perspective: 1000px;
            `;
    },
  };
}

/**
 * Slide transition for secondary elements
 */
export function slideTransition(
  node: Element,
  params: {
    direction?: "up" | "down" | "left" | "right";
    duration?: number;
    delay?: number;
  } = {},
): TransitionReturn {
  const { direction = "up", duration = 400, delay = 0 } = params;

  const getTransform = (progress: number) => {
    const distance = 50; // pixels
    const movement = (1 - progress) * distance;

    switch (direction) {
      case "up":
        return `translateY(${movement}px)`;
      case "down":
        return `translateY(-${movement}px)`;
      case "left":
        return `translateX(${movement}px)`;
      case "right":
        return `translateX(-${movement}px)`;
      default:
        return `translateY(${movement}px)`;
    }
  };

  return {
    delay,
    duration,
    css: (t: number) => `
            transform: ${getTransform(t)};
            opacity: ${t};
        `,
  };
}

/**
 * Advanced 3D flip transition
 */
export function flipTransition(
  node: Element,
  params: { duration?: number; axis?: "x" | "y" } = {},
): TransitionReturn {
  const { duration = 600, axis = "y" } = params;

  return {
    duration,
    css: (t: number) => {
      const angle = (1 - t) * 180;
      const transform =
        axis === "y" ? `rotateY(${angle}deg)` : `rotateX(${angle}deg)`;

      return `
                transform: ${transform};
                transform-style: preserve-3d;
                backface-visibility: hidden;
                perspective: 1000px;
            `;
    },
  };
}

/**
 * Staggered entrance animations for multiple elements
 */
export function staggeredEntrance(
  index: number,
  total: number,
  baseDuration: number = 300,
): TransitionReturn {
  const delay = (index / total) * 200; // Stagger delay

  return {
    delay,
    duration: baseDuration,
    css: (t: number) => `
            transform: translateY(${(1 - t) * 30}px);
            opacity: ${t};
        `,
  };
}

/**
 * Glassmorphism reveal effect
 */
export function glassReveal(
  node: Element,
  params: { duration?: number; blur?: number } = {},
): TransitionReturn {
  const { duration = 500, blur = 20 } = params;

  return {
    duration,
    css: (t: number) => {
      const blurAmount = blur * (1 - t);
      const opacity = t;
      const scale = 0.95 + t * 0.05;

      return `
                filter: blur(${blurAmount}px);
                opacity: ${opacity};
                transform: scale(${scale});
                backdrop-filter: blur(${10 + blurAmount}px);
            `;
    },
  };
}

/**
 * Mode transition coordinator - orchestrates the complete transition
 */
export class ModeTransitionOrchestrator {
  private isTransitioning = false;

  async orchestrateLandingToApp(): Promise<void> {
    if (this.isTransitioning) return;

    this.isTransitioning = true;

    // Phase 1: Fade out landing content
    await this.fadeOutLandingElements();

    // Phase 2: Fold transition
    await this.executeFoldTransition("fold-in");

    // Phase 3: Fade in app content
    await this.fadeInAppElements();

    this.isTransitioning = false;
  }

  async orchestrateAppToLanding(): Promise<void> {
    if (this.isTransitioning) return;

    this.isTransitioning = true;

    // Phase 1: Fade out app content
    await this.fadeOutAppElements();

    // Phase 2: Fold transition
    await this.executeFoldTransition("fold-out");

    // Phase 3: Fade in landing content
    await this.fadeInLandingElements();

    this.isTransitioning = false;
  }

  private async fadeOutLandingElements(): Promise<void> {
    // Implementation would coordinate with actual DOM elements
    return new Promise((resolve) => setTimeout(resolve, 200));
  }

  private async fadeInLandingElements(): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 200));
  }

  private async fadeOutAppElements(): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 200));
  }

  private async fadeInAppElements(): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 200));
  }

  private async executeFoldTransition(
    direction: "fold-in" | "fold-out",
  ): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, 600));
  }
}

// Export singleton orchestrator
export const transitionOrchestrator = new ModeTransitionOrchestrator();

/**
 * Reduced motion support
 */
export function getReducedMotionTransition(): TransitionReturn {
  return {
    duration: 100,
    css: () => "opacity: 1;",
  };
}

/**
 * Transition utilities
 */
export const transitionUtils = {
  /**
   * Detects if user prefers reduced motion
   */
  prefersReducedMotion(): boolean {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  },

  /**
   * Gets appropriate transition based on user preferences
   */
  getAccessibleTransition(
    defaultTransition: () => TransitionReturn,
    reducedTransition?: () => TransitionReturn,
  ): TransitionReturn {
    if (this.prefersReducedMotion()) {
      return reducedTransition
        ? reducedTransition()
        : getReducedMotionTransition();
    }
    return defaultTransition();
  },
};
