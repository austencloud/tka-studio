// src/lib/components/MainWidget/utils/transitions.ts
import { fly, fade, type TransitionConfig } from 'svelte/transition';
import { cubicInOut } from 'svelte/easing';

/**
 * Transition configuration options
 */
export interface TransitionOptions {
  duration?: number;
  delay?: number;
}

/**
 * Direction for transitions
 */
export type TransitionDirection = 'left' | 'right' | 'up' | 'down';

/**
 * Creates a consistent fly transition based on direction
 */
export function createTabTransition(
  direction: TransitionDirection,
  options: TransitionOptions = {}
): (node: Element) => TransitionConfig {
  const { duration = 300, delay = 0 } = options;

  const distance = 50;

  return (node: Element) => {
    const getCoordinates = () => {
      switch (direction) {
        case 'left':
          return { x: -distance, y: 0 };
        case 'right':
          return { x: distance, y: 0 };
        case 'up':
          return { x: 0, y: -distance };
        case 'down':
          return { x: 0, y: distance };
      }
    };

    const { x, y } = getCoordinates();

    // Use fly transition function directly
    return fly(node, {
      duration,
      delay,
      easing: cubicInOut,
      x,
      y
    });
  };
}

/**
 * Determines transition direction based on tab indices
 */
export function getTabTransitionDirection(
  currentIndex: number,
  previousIndex: number
): TransitionDirection {
  return currentIndex > previousIndex ? 'right' : 'left';
}

/**
 * Creates a consistent crossfade transition for content swapping
 */
export function createContentFade(
  options: TransitionOptions = {}
): (node: Element) => TransitionConfig {
  const { duration = 200, delay = 0 } = options;

  return (node: Element) => {
    return fade(node, {
      duration,
      delay,
      easing: cubicInOut
    });
  };
}
