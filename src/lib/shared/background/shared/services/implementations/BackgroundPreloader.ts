import { injectable } from "inversify";
import { BACKGROUND_GRADIENTS } from "../../domain";
import type { BackgroundType } from "../../domain/enums/background-enums";
import type { IBackgroundPreloader } from "../contracts/IBackgroundPreloader";

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

@injectable()
export class BackgroundPreLoader implements IBackgroundPreloader {
  /**
   * Updates the body background with smooth transition using ::before overlay technique
   * This works because CSS CAN transition opacity, even though gradients cannot be transitioned directly
   */
  updateBodyBackground(backgroundType: BackgroundType): void {
    console.log(
      "🔵 [Service] updateBodyBackground called with:",
      backgroundType
    );

    if (typeof window === "undefined" || typeof document === "undefined") {
      console.log("⚠️ [Service] Window or document undefined (SSR)");
      return; // SSR safety
    }

    try {
      const newGradient =
        BACKGROUND_GRADIENTS[backgroundType] || BACKGROUND_GRADIENTS.nightSky;
      const newAnimation =
        BACKGROUND_ANIMATIONS[backgroundType] || BACKGROUND_ANIMATIONS.nightSky;

      console.log(
        "🎨 [Service] New gradient:",
        newGradient.substring(0, 50) + "..."
      );
      console.log("🎨 [Service] New animation:", newAnimation);

      // Get current gradient
      const currentGradient =
        document.documentElement.style.getPropertyValue("--gradient-cosmic");

      console.log(
        "🎨 [Service] Current gradient:",
        currentGradient.substring(0, 50) + "..."
      );

      // Skip if already set to this gradient
      if (currentGradient === newGradient) {
        console.log("⏭️ [Service] Skipping - already showing this gradient");
        return;
      }

      if (isTransitioning) {
        console.log("⏭️ [Service] Skipping - transition already in progress");
        return;
      }

      console.log("✅ [Service] Starting transition...");
      isTransitioning = true;
      const body = document.body;

      // Update body animation class immediately
      console.log(
        "📝 [Service] Updating body animation class to:",
        newAnimation
      );
      body.classList.remove(
        "aurora-flow",
        "snow-fall",
        "star-twinkle",
        "deep-ocean-flow"
      );
      body.classList.add(newAnimation);

      // Step 1: Set the ::before overlay to the NEW gradient (separate CSS variable)
      console.log("📝 [Service] Step 1: Setting --gradient-next");
      document.documentElement.style.setProperty(
        "--gradient-next",
        newGradient
      );

      // Step 2: Fade in the ::before overlay (showing NEW gradient on top of OLD)
      console.log("📝 [Service] Step 2: Adding background-transitioning class");
      requestAnimationFrame(() => {
        body.classList.add("background-transitioning");
        console.log(
          "✨ [Service] Class added, opacity should be transitioning now"
        );
      });

      // Step 3: After transition completes, swap the gradients
      setTimeout(() => {
        console.log("📝 [Service] Step 3: Swapping gradients after 1.5s");
        document.documentElement.style.setProperty(
          "--gradient-cosmic",
          newGradient
        );
        body.classList.remove("background-transitioning");
        isTransitioning = false;
        console.log(
          `🎨 [Service] Body background transitioned to: ${backgroundType}`
        );
      }, 1500);
    } catch (error) {
      console.warn("[Service] Failed to update body background:", error);
      isTransitioning = false;
    }
  }

  /**
   * Preloads the background from localStorage on app startup
   * This is called by the inline script in app.html
   */
  preloadBackgroundFromStorage(): void {
    if (typeof window === "undefined" || typeof localStorage === "undefined") {
      return; // SSR safety
    }

    try {
      const settingsKey = "tka-modern-web-settings";
      const stored = localStorage.getItem(settingsKey);

      if (stored) {
        const settings = JSON.parse(stored);
        const backgroundType = settings.backgroundType || "nightSky";
        this.updateBodyBackground(backgroundType as BackgroundType);
      }
    } catch (error) {
      console.warn("Failed to preload background:", error);
    }
  }
}
