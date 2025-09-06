// src/lib/components/ConstructTab/OptionPicker/utils/transitions.ts
import { cubicOut, quintOut } from 'svelte/easing';
import type { NavigationDirection } from '../store/navigationStore';
import { prefersReducedMotion } from './a11y';
import { get } from 'svelte/store';

type TransitionParams = {
    duration?: number;
    delay?: number;
    easing?: (t: number) => number;
    fadeIn?: boolean;
    fadeOut?: boolean;
};

type DirectionTransitionParams = TransitionParams & {
    direction?: NavigationDirection | 'none';
    distance?: number;
};

/**
 * Enhanced direction-aware transition that slides content based on navigation direction
 * with improved support for exit/entry transitions
 */
export function directionTransition(node: HTMLElement, params: DirectionTransitionParams = {}) {
    const {
        direction = 'initial',
        duration = 300,
        delay = 0,
        easing = cubicOut,
        distance = 30,
        fadeIn = false,
        fadeOut = false
    } = params;

    // Skip animations if user prefers reduced motion
    if (get(prefersReducedMotion)) {
        return {
            duration: 0,
            css: () => 'opacity: 1'
        };
    }

    // Determine the direction of movement
    const dx = direction === 'forward' ? distance :
               direction === 'backward' ? -distance : 0;

    // For fade in/out effects
    const initialOpacity = fadeIn ? 0 : 1;
    const finalOpacity = fadeOut ? 0 : 1;

    return {
        duration,
        delay,
        easing,
        css: (t: number, u: number) => {
            // Calculate opacity based on fade direction
            let opacity;
            if (fadeIn && fadeOut) {
                // Fade in and out (peak at t=0.5)
                opacity = t < 0.5 ? t * 2 : (1 - t) * 2;
            } else if (fadeIn) {
                // Just fade in
                opacity = t;
            } else if (fadeOut) {
                // Just fade out
                opacity = 1 - t;
            } else {
                // No fade
                opacity = 1;
            }

            return `
                opacity: ${opacity};
                transform: translateX(${dx * u}px);
                pointer-events: ${t < 0.5 && fadeOut ? 'none' : 'auto'};
            `;
        }
    };
}

/**
 * Enhanced transition for empty states with subtle scale and blur
 */
export function emptyStateTransition(node: HTMLElement, params: TransitionParams = {}) {
    const {
        duration = 400,
        delay = 0,
        easing = quintOut
    } = params;

    // Skip animations if user prefers reduced motion
    if (get(prefersReducedMotion)) {
        return {
            duration: 0,
            css: () => 'opacity: 1'
        };
    }

    return {
        duration,
        delay,
        easing,
        css: (t: number) => `
            opacity: ${t};
            transform: scale(${0.92 + (0.08 * t)});
            filter: blur(${(1-t) * 2}px);
        `
    };
}

/**
 * Improved staggered grid item transition with natural timing
 * Better for option transitions
 */
export function staggeredItemTransition(node: HTMLElement, params: { index: number; total: number } & TransitionParams) {
    const {
        index,
        total,
        duration = 350,
        easing = quintOut
    } = params;

    // Skip animations if user prefers reduced motion
    if (get(prefersReducedMotion)) {
        return {
            duration: 0,
            css: () => 'opacity: 1'
        };
    }

    // Calculate a more natural stagger delay based on grid position
    // This creates a wave-like effect through the grid
    const rowSize = Math.ceil(Math.sqrt(total));
    const row = Math.floor(index / rowSize);
    const col = index % rowSize;

    // Creates a wave-like stagger pattern
    const baseDelay = (row + col) * 20;
    const maxDelay = 150; // Cap maximum delay
    const delay = Math.min(baseDelay, maxDelay);

    return {
        duration,
        delay,
        easing,
        css: (t: number) => `
            opacity: ${t};
            transform: scale(${0.95 + (0.05 * t)}) translateY(${(1-t) * 5}px);
        `
    };
}

/**
 * Option grid transition - specialized for transitioning pictograph options
 */
export function optionGridTransition(node: HTMLElement, params: TransitionParams & { isEntering?: boolean }) {
    const {
        duration = 300,
        delay = 0,
        easing = cubicOut,
        isEntering = true
    } = params;

    // Skip animations if user prefers reduced motion
    if (get(prefersReducedMotion)) {
        return {
            duration: 0,
            css: () => 'opacity: 1'
        };
    }

    // Entering and exiting have different animations
    if (isEntering) {
        return {
            duration,
            delay,
            easing,
            css: (t: number) => `
                opacity: ${t};
                transform: scale(${0.98 + (0.02 * t)});
                filter: blur(${(1-t) * 1}px);
            `
        };
    } else {
        return {
            duration,
            delay,
            easing,
            css: (t: number) => `
                opacity: ${1-t};
                transform: scale(${1 - (0.02 * (1-t))}) translateY(${(1-t) * 5}px);
                filter: blur(${(1-t) * 1}px);
                pointer-events: none;
            `
        };
    }
}

/**
 * Transition for swipe gesture feedback
 */
export function swipeFeedbackTransition(node: HTMLElement, params: { percent: number; direction: 'left' | 'right' }) {
    const { percent, direction } = params;

    // Skip animations if user prefers reduced motion
    if (get(prefersReducedMotion)) {
        return {
            duration: 0,
            css: () => ''
        };
    }

    const sign = direction === 'left' ? -1 : 1;
    const translateX = sign * percent * 20; // Max 20px movement
    const opacity = 0.2 + (percent * 0.8); // Fade in as swipe progresses

    return {
        duration: 0, // Immediate update
        css: () => `
            opacity: ${opacity};
            transform: translateX(${translateX}px);
        `
    };
}
