/**
 * Custom popIn transition for Svelte components
 * Combines scale and opacity for a smooth pop-in effect
 */
import { cubicOut } from 'svelte/easing';
import type { TransitionConfig } from 'svelte/transition';

interface PopInParams {
  delay?: number;
  duration?: number;
  easing?: (t: number) => number;
  start?: number;
  opacity?: number;
}

/**
 * Creates a pop-in transition effect that combines scaling and opacity
 * for a smooth, professional animation
 */
export function popIn(
  node: Element,
  {
    delay = 0,
    duration = 200,
    easing = cubicOut,
    start = 0.85,
    opacity = 0.2
  }: PopInParams = {}
): TransitionConfig {
  const style = getComputedStyle(node);
  const targetOpacity = +style.opacity;
  const transform = style.transform === 'none' ? '' : style.transform;

  return {
    delay,
    duration,
    easing,
    css: (t, u) => `
      transform: ${transform} scale(${start + (1 - start) * t});
      opacity: ${opacity + (targetOpacity - opacity) * t};
    `
  };
}
