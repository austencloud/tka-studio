// background-config.ts - Background metadata configuration
import { BackgroundType } from "$domain";

export interface BackgroundMetadata {
  type: BackgroundType;
  name: string;
  description: string;
  icon: string;
  gradient: string;
  animation: string;
}

/**
 * Available backgrounds with their metadata and animation configurations
 */
export const backgroundsConfig: BackgroundMetadata[] = [
  {
    type: BackgroundType.AURORA,
    name: "Aurora",
    description: "Colorful flowing aurora with animated blobs",
    icon: "🌌",
    gradient:
      "linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)",
    animation: "aurora-flow",
  },
  {
    type: BackgroundType.SNOWFALL,
    name: "Snowfall",
    description: "Gentle falling snowflakes with shooting stars",
    icon: "❄️",
    gradient: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
    animation: "snow-fall",
  },
  {
    type: BackgroundType.NIGHT_SKY,
    name: "Night Sky",
    description: "Starry night with twinkling celestial bodies",
    icon: "🌙",
    gradient: "linear-gradient(135deg, #0a0e2c 0%, #1a2040 50%, #2a3060 100%)",
    animation: "star-twinkle",
  },
  {
    type: BackgroundType.BUBBLES,
    name: "Bubbles",
    description: "Underwater scene with floating bubbles",
    icon: "🫧",
    gradient: "linear-gradient(135deg, #143250 0%, #0a1e3c 50%, #050f28 100%)",
    animation: "bubble-float",
  },
];

/**
 * Get background metadata by type
 */
export function getBackgroundConfig(
  type: BackgroundType
): BackgroundMetadata | undefined {
  return backgroundsConfig.find((bg) => bg.type === type);
}

/**
 * Get all available background types
 */
export function getAvailableBackgroundTypes(): BackgroundType[] {
  return backgroundsConfig.map((bg) => bg.type);
}
