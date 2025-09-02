// src/lib/components/backgrounds/systems/nightSky/NightSkyUtils.ts
import type { AccessibilitySettings, Dimensions, Star } from "$domain";

export interface StarConfig {
  minSize: number;
  maxSize: number;
  colors: string[];
  baseOpacityMin: number;
  baseOpacityMax: number;
  minTwinkleSpeed: number;
  maxTwinkleSpeed: number;
  twinkleChance: number;
}

export class NightSkyUtils {
  /**
   * Generate a random float between min and max
   */
  static randFloat(min: number, max: number): number {
    return Math.random() * (max - min) + min;
  }

  /**
   * Generate a random integer between min and max (inclusive)
   */
  static randInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  /**
   * Pick a random item from an array
   */
  static randItem<T>(arr: T[]): T {
    if (arr.length === 0) throw new Error("randItem called with empty array");
    return arr[Math.floor(Math.random() * arr.length)] as T;
  }

  /**
   * Create a star with randomized properties
   */
  static makeStar(
    dim: Dimensions,
    config: StarConfig,
    a11y: AccessibilitySettings
  ): Star {
    const r =
      NightSkyUtils.randFloat(config.minSize, config.maxSize) *
      (a11y.visibleParticleSize > 2 ? 1.5 : 1);
    const tw = Math.random() < config.twinkleChance;

    return {
      x: Math.random() * dim.width,
      y: Math.random() * dim.height,
      radius: r,
      baseOpacity: NightSkyUtils.randFloat(
        config.baseOpacityMin,
        config.baseOpacityMax
      ),
      currentOpacity: 1, // Will be set during updates
      twinkleSpeed: tw
        ? NightSkyUtils.randFloat(
            config.minTwinkleSpeed,
            config.maxTwinkleSpeed
          )
        : 0,
      twinklePhase: Math.random() * Math.PI * 2,
      isTwinkling: tw,
      color: a11y.highContrast
        ? "#FFFFFF"
        : NightSkyUtils.randItem(config.colors),
    };
  }

  /**
   * Simple moon phase calculation without external dependencies
   */
  static getMoonIllumination(date: Date) {
    // Simple lunar phase calculation - basic approximation
    const msPerLunarCycle = 29.53058868 * 24 * 60 * 60 * 1000; // ~29.5 days in ms
    const knownNewMoon = new Date("2024-01-11T11:57:00Z").getTime(); // A known new moon
    const currentTime = date.getTime();

    const timeSinceNewMoon = currentTime - knownNewMoon;
    const cyclePosition = (timeSinceNewMoon / msPerLunarCycle) % 1;

    // Calculate illuminated fraction (0 = new moon, 0.5 = full moon)
    let fraction;
    if (cyclePosition < 0.5) {
      // Waxing
      fraction = cyclePosition * 2;
    } else {
      // Waning
      fraction = 2 - cyclePosition * 2;
    }

    return {
      fraction: Math.abs(fraction),
      phase: cyclePosition,
      angle: 0, // Simplified - no angle calculation
    };
  }
}
