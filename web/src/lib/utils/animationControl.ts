/**
 * Simple Animation Control
 * Just checks if animations should be enabled
 */

import { getSettings } from "$lib/state/appState.svelte";

/**
 * Check if animations should run based on settings and user preferences
 */
export function shouldAnimate(): boolean {
  // Check user's reduced motion preference
  if (typeof window !== "undefined") {
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReducedMotion) return false;
  }

  // Check app settings
  const settings = getSettings();
  return settings.animationsEnabled !== false;
}

/**
 * Get current settings for use in fade functions
 */
export function getAnimationSettings() {
  return {
    animationsEnabled: shouldAnimate(),
  };
}
