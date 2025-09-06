// src/lib/components/backgrounds/config/nightSky.ts
import type { QualityLevel } from "../BackgroundTypes";

// ============================================================================
// CONFIGURATION INTERFACES
// ============================================================================

export interface CometConfig {
  size: number;
  speed: number;
  color: string;
  tailLength: number;
  interval: number;
  enabledOnQuality: QualityLevel[];
}

// ============================================================================
// NIGHT SKY CONFIGURATION
// ============================================================================

export const NightSkyConfig = {
  stars: {
    count: 200,
    minSize: 1,
    maxSize: 3,
    colors: ["#ffffff", "#f0f8ff", "#e6f3ff", "#ddeeff", "#ffff99"],
    twinkleSpeed: 0.02,
    parallaxLayers: 3,
    baseOpacityMin: 0.4,
    baseOpacityMax: 1.0,
    minTwinkleSpeed: 0.01,
    maxTwinkleSpeed: 0.05,
    twinkleChance: 0.7,
  },
  parallax: {
    far: {
      density: 0.00008,
      drift: 0.00002,
    },
    mid: {
      density: 0.00006,
      drift: 0.00004,
    },
    near: {
      density: 0.00004,
      drift: 0.00006,
    },
  },
  nebula: {
    count: 3,
    minRadius: 80,
    maxRadius: 150,
    colors: [
      "rgba(128, 0, 255, 0.1)",
      "rgba(255, 0, 128, 0.1)",
      "rgba(0, 128, 255, 0.1)",
    ],
    pulseSpeed: {
      min: 0.005,
      max: 0.02,
    },
    enabledOnQuality: ["high", "medium"] as (
      | "high"
      | "medium"
      | "low"
      | "minimal"
    )[],
  },
  constellations: {
    maxLines: 8,
    opacity: 0.3,
    twinkleSpeed: 0.01,
    enabledOnQuality: ["high", "medium"] as (
      | "high"
      | "medium"
      | "low"
      | "minimal"
    )[],
  },
  Moon: {
    radiusPercent: 0.04,
    maxRadiusPx: 60,
    color: "#f5f5dc",
    position: {
      x: 0.8,
      y: 0.2,
    },
    driftSpeed: 0.00001,
    enabledOnQuality: ["high", "medium", "low"] as (
      | "high"
      | "medium"
      | "low"
      | "minimal"
    )[],
  },
  celestialBodies: {
    moon: {
      size: 60,
      color: "#f5f5dc",
      glowRadius: 20,
      enabled: true,
    },
    planets: {
      count: 2,
      minSize: 3,
      maxSize: 8,
      colors: ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"],
    },
  },
  shootingStars: {
    frequency: 0.001,
    minSpeed: 2,
    maxSpeed: 5,
    colors: ["#ffffff", "#ffff99", "#99ccff", "#ffcc99"],
    tailLength: 15,
  },
  spaceship: {
    size: 12,
    speed: 1.5,
    color: "#silver",
    blinkInterval: 2000,
    enabled: false, // Easter egg
    speedPercent: 0.001,
    enabledOnQuality: ["high"] as ("high" | "medium" | "low" | "minimal")[],
  },
  comet: {
    size: 8,
    speed: 0.8,
    tailLength: 30,
    color: "#87ceeb",
    enabled: false, // Easter egg
    interval: 45000,
    enabledOnQuality: ["high"] as ("high" | "medium" | "low" | "minimal")[],
  },
  background: {
    gradientStops: [
      { position: 0, color: "#0c0c1e" },
      { position: 0.3, color: "#1a1a2e" },
      { position: 0.7, color: "#16213e" },
      { position: 1, color: "#0f3460" },
    ],
  },
  animation: {
    starDriftSpeed: 0.1,
    MoonDriftSpeed: 0.05,
    parallaxMultiplier: 0.3,
  },
};

export type NightSkyConfigType = typeof NightSkyConfig;
