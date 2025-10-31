/**
 * Background Preloader Utility
 *
 * Handles immediate body background updates when background settings change.
 * Uses CSS ::before pseudo-element with opacity transition for smooth gradient changes.
 */

import { BACKGROUND_GRADIENTS } from "./domain";
import type { BackgroundType } from "./domain/enums/background-enums";

let isTransitioning = false;

// Background animation mapping - same as app.html
const BACKGROUND_ANIMATIONS: Record<BackgroundType, string> = {
  aurora: "aurora-flow",
  snowfall: "snow-fall",
  nightSky: "star-twinkle",
  deepOcean: "deep-ocean-flow",
  solidColor: "", // No animation for solid colors
  linearGradient: "", // No animation for gradients
};

/**
 * Updates the body background with smooth transition using ::before overlay technique
 * This works because CSS CAN transition opacity, even though gradients cannot be transitioned directly
 */
export function updateBodyBackground(backgroundType: BackgroundType): void {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return; // SSR safety
  }

  try {
    const newGradient =
      BACKGROUND_GRADIENTS[backgroundType] || BACKGROUND_GRADIENTS.nightSky;
    const newAnimation =
      BACKGROUND_ANIMATIONS[backgroundType] || BACKGROUND_ANIMATIONS.nightSky;

    // Get current gradient
    const currentGradient =
      document.documentElement.style.getPropertyValue("--gradient-cosmic");

    // Skip if already set to this gradient
    if (currentGradient === newGradient) {
      return;
    }

    if (isTransitioning) {
      return;
    }

    isTransitioning = true;
    const body = document.body;

    // Update body animation class immediately
    body.classList.remove(
      "aurora-flow",
      "snow-fall",
      "star-twinkle",
      "deep-ocean-flow"
    );
    body.classList.add(newAnimation);

    // Step 1: Set the ::before overlay to the NEW gradient (separate CSS variable)
    document.documentElement.style.setProperty("--gradient-next", newGradient);

    // Step 2: Fade in the ::before overlay (showing NEW gradient on top of OLD)
    requestAnimationFrame(() => {
      body.classList.add("background-transitioning");
    });

    // Step 3: After transition completes, swap the gradients
    setTimeout(() => {
      document.documentElement.style.setProperty(
        "--gradient-cosmic",
        newGradient
      );
      body.classList.remove("background-transitioning");
      isTransitioning = false;
    }, 1500);
  } catch (error) {
    console.warn("Failed to update body background:", error);
    isTransitioning = false;
  }
}

/**
 * Preloads the background from localStorage on app startup
 * This is called by the inline script in app.html
 */
export function preloadBackgroundFromStorage(): void {
  if (typeof window === "undefined" || typeof localStorage === "undefined") {
    return; // SSR safety
  }

  try {
    const settingsKey = "tka-modern-web-settings";
    const stored = localStorage.getItem(settingsKey);

    if (stored) {
      const settings = JSON.parse(stored);
      const backgroundType = settings.backgroundType || "nightSky";
      updateBodyBackground(backgroundType as BackgroundType);
    }
  } catch (error) {
    console.warn("Failed to preload background:", error);
  }
}
