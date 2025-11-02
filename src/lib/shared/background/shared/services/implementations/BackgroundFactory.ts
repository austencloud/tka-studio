// src/lib/services/implementations/background/BackgroundFactory.ts
// Background Factory - Creates background animation systems

import type {
  AccessibilitySettings,
  BackgroundSystem,
  QualityLevel,
} from "../../domain";
import { BackgroundType } from "../../domain/enums/background-enums";

import { AuroraBackgroundSystem } from "../../../aurora/services/AuroraBackgroundSystem";
import { DeepOceanBackgroundOrchestrator } from "../../../deep-ocean/services/DeepOceanBackgroundOrchestrator";
import { NightSkyBackgroundSystem } from "../../../night-sky";
import { SimpleBackgroundSystem } from "../../../simple/services/SimpleBackgroundSystem";
import { SnowfallBackgroundSystem } from "../../../snowfall/services/SnowfallBackgroundSystem";
import { resolve, TYPES } from "$shared";

// BackgroundFactoryParams doesn't exist in domain - define locally
interface BackgroundFactoryParams {
  type: BackgroundType;
  quality: QualityLevel;
  initialQuality: QualityLevel;
  accessibility?: Record<string, unknown>;
  settings?: Record<string, unknown>;
  // Simple background settings
  backgroundColor?: string;
  gradientColors?: string[];
  gradientDirection?: number;
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

  public static async createBackgroundSystem(
    options: BackgroundFactoryParams
  ): Promise<BackgroundSystem> {
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
        backgroundSystem = await NightSkyBackgroundSystem.create();
        break;
      case BackgroundType.DEEP_OCEAN:
        // Use the refactored orchestrator
        backgroundSystem = new DeepOceanBackgroundOrchestrator(
          resolve(TYPES.IBubblePhysics),
          resolve(TYPES.IMarineLifeAnimator),
          resolve(TYPES.IParticleSystem),
          resolve(TYPES.IOceanRenderer),
          resolve(TYPES.ILightRayCalculator)
        );
        break;
      case BackgroundType.SOLID_COLOR:
        backgroundSystem = new SimpleBackgroundSystem({
          type: "solid",
          color: options.backgroundColor || "#1a1a2e",
        });
        break;
      case BackgroundType.LINEAR_GRADIENT:
        backgroundSystem = new SimpleBackgroundSystem({
          type: "gradient",
          colors: options.gradientColors || ["#667eea", "#764ba2"],
          direction: options.gradientDirection || 135,
        });
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

  public static async createOptimalBackgroundSystem(): Promise<BackgroundSystem> {
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
      BackgroundType.DEEP_OCEAN,
      BackgroundType.SOLID_COLOR,
      BackgroundType.LINEAR_GRADIENT,
    ];
  }
}
