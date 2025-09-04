/**
 * App Mode State - Svelte 5 Runes
 *
 * Manages application mode transitions and landing page state.
 * Handles the transition between landing page and main app.
 */

import { browser } from "$app/environment";

// ============================================================================
// TYPES
// ============================================================================

type LandingBackground = "deepOcean" | "snowfall" | "nightSky";
type AppMode = "landing" | "app";

// ============================================================================
// STATE
// ============================================================================

const LANDING_BACKGROUND_KEY = "tka-landing-background";
const APP_MODE_KEY = "tka-app-mode";

// Default values
const DEFAULT_LANDING_BACKGROUND: LandingBackground = "nightSky";
const DEFAULT_APP_MODE: AppMode = "landing";

// Load from localStorage
function loadLandingBackground(): LandingBackground {
  if (!browser) return DEFAULT_LANDING_BACKGROUND;

  try {
    const stored = localStorage.getItem(LANDING_BACKGROUND_KEY);
    if (stored && ["deepOcean", "snowfall", "nightSky"].includes(stored)) {
      return stored as LandingBackground;
    }
  } catch (error) {
    console.warn("Failed to load landing background from localStorage:", error);
  }

  return DEFAULT_LANDING_BACKGROUND;
}

function loadAppMode(): AppMode {
  if (!browser) return DEFAULT_APP_MODE;

  try {
    const stored = localStorage.getItem(APP_MODE_KEY);
    if (stored && ["landing", "app"].includes(stored)) {
      return stored as AppMode;
    }
  } catch (error) {
    console.warn("Failed to load app mode from localStorage:", error);
  }

  return DEFAULT_APP_MODE;
}

// Reactive state
const appModeState = $state({
  currentMode: loadAppMode(),
  landingBackground: loadLandingBackground(),
  isTransitioning: false,
});

// ============================================================================
// ACTIONS
// ============================================================================

/**
 * Set the landing page background
 */
export function setLandingBackground(background: LandingBackground): void {
  appModeState.landingBackground = background;

  if (browser) {
    try {
      localStorage.setItem(LANDING_BACKGROUND_KEY, background);
    } catch (error) {
      console.warn("Failed to save landing background to localStorage:", error);
    }
  }
}

/**
 * Get the current landing background
 */
export function getLandingBackground(): LandingBackground {
  return appModeState.landingBackground;
}

/**
 * Enter the main application mode
 */
export async function enterAppMode(): Promise<void> {
  if (appModeState.currentMode === "app") {
    return; // Already in app mode
  }

  appModeState.isTransitioning = true;

  try {
    // Simulate transition delay
    await new Promise((resolve) => setTimeout(resolve, 300));

    appModeState.currentMode = "app";

    if (browser) {
      try {
        localStorage.setItem(APP_MODE_KEY, "app");
      } catch (error) {
        console.warn("Failed to save app mode to localStorage:", error);
      }
    }
  } finally {
    appModeState.isTransitioning = false;
  }
}

/**
 * Return to landing page mode
 */
export async function exitAppMode(): Promise<void> {
  if (appModeState.currentMode === "landing") {
    return; // Already in landing mode
  }

  appModeState.isTransitioning = true;

  try {
    // Simulate transition delay
    await new Promise((resolve) => setTimeout(resolve, 300));

    appModeState.currentMode = "landing";

    if (browser) {
      try {
        localStorage.setItem(APP_MODE_KEY, "landing");
      } catch (error) {
        console.warn("Failed to save app mode to localStorage:", error);
      }
    }
  } finally {
    appModeState.isTransitioning = false;
  }
}

/**
 * Get the current app mode
 */
export function getCurrentAppMode(): AppMode {
  return appModeState.currentMode;
}

/**
 * Check if currently transitioning between modes
 */
export function isTransitioning(): boolean {
  return appModeState.isTransitioning;
}

/**
 * Check if in app mode
 */
export function isInAppMode(): boolean {
  return appModeState.currentMode === "app";
}

/**
 * Check if in landing mode
 */
export function isInLandingMode(): boolean {
  return appModeState.currentMode === "landing";
}
