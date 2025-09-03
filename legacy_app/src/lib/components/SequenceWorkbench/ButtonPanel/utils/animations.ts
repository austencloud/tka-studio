import type { LayoutOrientation } from "../types";

/**
 * Animation timing constants
 */
export const ANIMATION_DURATIONS = {
  TOGGLE_OUT: 400,     // Time for panel hide animation (match CSS)
  TOGGLE_IN: 500,      // Time for panel show animation (match CSS)
  BUTTON_STAGGER: 50,  // Time between each button animation in ms (match CSS calc)
  PULSE_STOP_DELAY: 3000 // Duration before initial pulse animation stops
};

/**
 * Get the correct CSS animation name based on the layout orientation
 * and whether the animation is entering or exiting.
 * These names must match the @keyframes defined in the component CSS.
 */
export function getAnimationName(
  layout: LayoutOrientation,
  isEntering: boolean
): string {
  if (layout === 'vertical') {
    return isEntering ? 'flyInVertical' : 'flyOutVertical';
  } else {
    return isEntering ? 'flyInHorizontal' : 'flyOutHorizontal';
  }
}

/**
 * Get toggle handle icon based on layout orientation.
 * Uses grip icons for a handle-like appearance.
 */
export function getToggleHandleIcon(layout: LayoutOrientation): string {
  return layout === 'vertical' ? 'fa-grip-lines' : 'fa-grip-lines-vertical';
}

/**
 * Get toggle indicator icon (chevron) based on layout orientation and visibility state.
 */
export function getToggleIndicatorIcon(
  layout: LayoutOrientation,
  isVisible: boolean
): string {
  if (layout === 'vertical') {
    return isVisible ? 'fa-chevron-up' : 'fa-chevron-down';
  } else {
    return isVisible ? 'fa-chevron-left' : 'fa-chevron-right';
  }
}

/**
 * Calculate toggle handle dimensions based on layout and button size.
 * Aims for a visually balanced handle relative to the buttons.
 */
export function calculateToggleHandleDimensions(
  layout: LayoutOrientation,
  buttonSize: number
): { width: number; height: number } {
  // Make handle slightly larger than button for vertical layout width
  // and slightly taller for horizontal layout height for better grab area.
  // Keep the other dimension smaller for a pill/handle shape.
  return layout === 'vertical'
    ? { width: buttonSize * 1.2, height: buttonSize * 0.6 }
    : { width: buttonSize * 0.6, height: buttonSize * 1.2 };
}

/**
 * Helper to generate animation delay CSS value for buttons.
 * Matches the calculation used in ActionButton.svelte CSS.
 */
export function getButtonAnimationDelayValue(index: number): string {
 const delayFactor = 0.05; // Corresponds to 50ms stagger
 return `calc(${delayFactor}s * ${index})`;
}
