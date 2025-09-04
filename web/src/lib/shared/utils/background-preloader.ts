/**
 * Background Preloader Utility
 *
 * Handles immediate body background updates when background settings change.
 * Ensures smooth transitions without showing the default gradient.
 */

import type { BackgroundType } from "../domain/ui/backgrounds/BackgroundTypes";

// Background gradients mapping - mirrors background-config.ts
export const BACKGROUND_GRADIENTS: Record<string, string> = {
  aurora:
    "linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)",
  snowfall: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
  nightSky: "linear-gradient(135deg, #0a0e2c 0%, #1a2040 50%, #2a3060 100%)",
  bubbles: "linear-gradient(135deg, #143250 0%, #0a1e3c 50%, #050f28 100%)",
  deepOcean: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
};

/**
 * Updates the body background immediately by setting the --gradient-cosmic CSS variable
 */
export function updateBodyBackground(backgroundType: BackgroundType): void {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return; // SSR safety
  }

  try {
    const gradient =
      BACKGROUND_GRADIENTS[backgroundType] || BACKGROUND_GRADIENTS.nightSky;

    // Update the CSS custom property that controls the body background
    document.documentElement.style.setProperty("--gradient-cosmic", gradient);

    console.log(`🎨 Body background updated to: ${backgroundType}`);
  } catch (error) {
    console.warn("Failed to update body background:", error);
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
      console.log("🎨 Background preloaded from storage:", backgroundType);
    } else {
      console.log("🎨 No saved background found, using default");
    }
  } catch (error) {
    console.warn("Failed to preload background:", error);
  }
}
