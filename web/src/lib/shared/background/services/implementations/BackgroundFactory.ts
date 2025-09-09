// src/lib/services/implementations/background/BackgroundFactory.ts
// Background Factory - Creates background animation systems

import {
  BackgroundType,
  type AccessibilitySettings,
  type BackgroundSystem,
  type QualityLevel,
} from "$shared";

import { AuroraBackgroundSystem } from "./systems/AuroraBackgroundSystem";
import { BubblesBackgroundSystem } from "./systems/BubblesBackgroundSystem";
import { DeepOceanBackgroundSystem } from "./systems/DeepOceanBackgroundSystem";
import { NightSkyBackgroundSystem } from "./systems/NightSkyBackgroundSystem";
import { SnowfallBackgroundSystem } from "./systems/SnowfallBackgroundSystem";

// BackgroundFactoryParams doesn't exist in domain - define locally
interface BackgroundFactoryParams {
  type: BackgroundType;
  quality: QualityLevel;
  initialQuality: QualityLevel;
  accessibility?: Record<string, unknown>;
  settings?: Record<string, unknown>;
}

// detectAppropriateQuality function doesn't exist - define locally
function detectAppropriateQuality(): QualityLevel {
  return "medium";
}

export class BackgroundFactory {
  // Default accessibility settings
  private static readonly defaultAccessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };

  public static createBackgroundSystem(
    options: BackgroundFactoryParams
  ): BackgroundSystem {
    // Quality detection logic
    const quality: QualityLevel =
      options.initialQuality ?? detectAppropriateQuality();

    // Accessibility detection for window environments
    const accessibility: AccessibilitySettings = {
      ...this.defaultAccessibility,
      ...(options.accessibility || {}),
    };

    // Check for reduced motion preference
    if (typeof window !== "undefined" && window.matchMedia) {
      try {
        const prefersReducedMotion = window.matchMedia(
          "(prefers-reduced-motion: reduce)"
        );
        if (prefersReducedMotion.matches) {
          accessibility.reducedMotion = true;
        }
      } catch (error) {
        console.warn("Could not detect reduced motion preference:", error);
      }
    }

    let backgroundSystem: BackgroundSystem;

    // Switch statement for background types
    switch (options.type) {
      case BackgroundType.AURORA:
        backgroundSystem = new AuroraBackgroundSystem();
        break;
      case BackgroundType.SNOWFALL:
        backgroundSystem = new SnowfallBackgroundSystem();
        break;
      case BackgroundType.NIGHT_SKY:
        backgroundSystem = new NightSkyBackgroundSystem();
        break;
      case BackgroundType.BUBBLES:
        backgroundSystem = new BubblesBackgroundSystem();
        break;
      case BackgroundType.DEEP_OCEAN:
        backgroundSystem = new DeepOceanBackgroundSystem();
        break;
      default:
        console.warn(
          `Background type "${options.type}" not implemented. Defaulting to Aurora.`
        );
        backgroundSystem = new AuroraBackgroundSystem();
    }

    // Apply accessibility settings if the background system supports them
    if (backgroundSystem.setAccessibility) {
      backgroundSystem.setAccessibility(accessibility);
    }

    // Set initial quality
    backgroundSystem.setQuality(quality);

    return backgroundSystem;
  }

  public static createOptimalBackgroundSystem(): BackgroundSystem {
    const quality = detectAppropriateQuality();

    // Default to nightSky as the preferred background
    return this.createBackgroundSystem({
      type: BackgroundType.NIGHT_SKY,
      quality,
      initialQuality: quality,
    });
  }

  public static isBackgroundSupported(type: string): boolean {
    const quality = detectAppropriateQuality();

    switch (type) {
      case BackgroundType.SNOWFALL:
      case BackgroundType.NIGHT_SKY:
      case BackgroundType.AURORA:
      case BackgroundType.BUBBLES:
      case BackgroundType.DEEP_OCEAN:
        return quality !== "minimal";
      default:
        return false;
    }
  }

  public static getSupportedBackgroundTypes(): BackgroundType[] {
    return [
      BackgroundType.NIGHT_SKY,
      BackgroundType.SNOWFALL,
      BackgroundType.AURORA,
      BackgroundType.BUBBLES,
      BackgroundType.DEEP_OCEAN,
    ];
  }
}
