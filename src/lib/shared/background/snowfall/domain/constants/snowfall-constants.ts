// src/lib/components/backgrounds/snowfall/constants.ts

export const backgroundGradient = [
  { stop: 0, color: "#0a0e1a" }, // Deep midnight blue
  { stop: 0.2, color: "#1a1d3a" }, // Rich indigo
  { stop: 0.4, color: "#2d2560" }, // Deep purple-blue
  { stop: 0.65, color: "#1e2a4a" }, // Winter evening blue
  { stop: 0.85, color: "#0f1c3d" }, // Deep ocean blue
  { stop: 1, color: "#041426" }, // Deepest night
];

export const performanceThresholds = {
  minRenderFps: 30,
  lowPerformanceThreshold: 45,
  criticalPerformanceThreshold: 30,
};

export const qualitySettings = {
  high: {
    densityMultiplier: 1.0,
    enableShootingStars: true,
    enableSeasonal: true,
  },
  medium: {
    densityMultiplier: 0.75,
    enableShootingStars: true,
    enableSeasonal: true,
  },
  low: {
    densityMultiplier: 0.5,
    enableShootingStars: false,
    enableSeasonal: false,
  },
};

export const resizeConfig = {
  qualityRestoreDelay: 500,
  resizeQuality: "low" as "high" | "medium" | "low",
};
