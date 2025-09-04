import type { QualityLevel } from "../BackgroundTypes";
import { NightSkyConfig } from "./nightSky";

/**
 * Snowfall configuration object
 */
export const SnowfallConfig = {
  snowflake: {
    colors: ["#ffffff", "#f0f8ff", "#e6f3ff", "#ddeeff"],
    minSize: 2,
    maxSize: 8,
    minSpeed: 0.5,
    maxSpeed: 2,
    density: 0.0001,
    windChangeInterval: 300,
  },
  shootingStar: {
    colors: ["#ffffff", "#ffff99", "#99ccff", "#ffcc99"],
    minSize: 2,
    maxSize: 4,
    minSpeed: 0.8,
    maxSpeed: 1.5,
    minInterval: 5000,
    maxInterval: 15000,
    tailLength: {
      min: 10,
      max: 20,
    },
  },
};

/**
 * Detects the appropriate quality level based on device capabilities
 * and performance characteristics.
 */
export function detectAppropriateQuality(): QualityLevel {
  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  if (prefersReducedMotion) {
    return "minimal";
  }

  // Check device memory (if available)
  const deviceMemory = (navigator as Navigator & { deviceMemory?: number })
    .deviceMemory;
  if (deviceMemory && deviceMemory < 4) {
    return "low";
  }

  // Check hardware concurrency (CPU cores)
  const hardwareConcurrency = navigator.hardwareConcurrency || 2;
  if (hardwareConcurrency < 4) {
    return "medium";
  }

  // Check connection type (if available)
  const connection = (
    navigator as Navigator & {
      connection?: {
        effectiveType?: string;
      };
    }
  ).connection;
  if (connection) {
    const effectiveType = connection.effectiveType;
    if (effectiveType === "slow-2g" || effectiveType === "2g") {
      return "minimal";
    }
    if (effectiveType === "3g") {
      return "low";
    }
  }

  // Check screen size and pixel density
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const pixelRatio = window.devicePixelRatio || 1;

  // Low resolution or small screens
  if (screenWidth < 1024 || screenHeight < 768) {
    return "medium";
  }

  // Very high pixel density might strain performance
  if (pixelRatio > 2) {
    return "medium";
  }

  // Check if we're on a mobile device
  const isMobile =
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );
  if (isMobile) {
    return "medium";
  }

  // Check battery status (if available)
  const battery = (
    navigator as Navigator & {
      getBattery?: () => Promise<{ level: number }>;
    }
  ).getBattery?.();
  if (battery) {
    battery.then((batteryManager: { level: number }) => {
      if (batteryManager.level < 0.2) {
        return "low";
      }
      return "normal";
    });
  }

  // Default to high quality for desktop devices with good specs
  return "high";
}

/**
 * Quality level configurations
 */
export const QUALITY_CONFIGS = {
  minimal: {
    maxParticles: 20,
    animationFrameRate: 15,
    enableBlur: false,
    enableGlow: false,
    particleSize: 1,
    densityMultiplier: 0.3,
  },
  low: {
    maxParticles: 50,
    animationFrameRate: 30,
    enableBlur: false,
    enableGlow: false,
    particleSize: 2,
    densityMultiplier: 0.5,
  },
  medium: {
    maxParticles: 100,
    animationFrameRate: 45,
    enableBlur: true,
    enableGlow: false,
    particleSize: 3,
    densityMultiplier: 0.75,
  },
  high: {
    maxParticles: 200,
    animationFrameRate: 60,
    enableBlur: true,
    enableGlow: true,
    particleSize: 4,
    densityMultiplier: 1.0,
  },
} as const;

/**
 * Get configuration for a specific quality level
 */
export function getQualityConfig(quality: QualityLevel) {
  return QUALITY_CONFIGS[quality];
}

/**
 * Get optimized configuration for a specific quality level
 * This function provides both the base config and quality-specific settings
 */
export function getOptimizedConfig(quality: QualityLevel) {
  const qualitySettings = getQualityConfig(quality);

  return {
    config: {
      core: {
        background: {
          gradientStops: [
            { position: 0, color: "#1a1a2e" },
            { position: 0.5, color: "#16213e" },
            { position: 1, color: "#0f3460" },
          ],
        },
      },
      nightSky: NightSkyConfig,
    },
    qualitySettings: {
      ...qualitySettings,
      enableShootingStars: quality === "high" || quality === "medium",
    },
  };
}
