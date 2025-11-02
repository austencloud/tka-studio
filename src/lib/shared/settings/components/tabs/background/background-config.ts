// background-config.ts - Background metadata configuration
import { BackgroundType } from "$shared/background/shared/domain/enums/background-enums";

export interface BackgroundMetadata {
  type: BackgroundType;
  name: string;
  description: string;
  icon: string;
}

/**
 * Available backgrounds with their metadata and animation configurations
 */
export const backgroundsConfig: BackgroundMetadata[] = [
  {
    type: BackgroundType.AURORA,
    name: "Aurora",
    description: "Colorful flowing aurora with lens flare",
    icon: '<i class="fas fa-star"></i>',
  },
  {
    type: BackgroundType.SNOWFALL,
    name: "Snowfall",
    description: "Gentle falling snowflakes with shooting stars",
    icon: '<i class="fas fa-snowflake"></i>',
  },
  {
    type: BackgroundType.NIGHT_SKY,
    name: "Night Sky",
    description: "Starry night with twinkling celestial bodies",
    icon: '<i class="fas fa-moon"></i>',
  },
  {
    type: BackgroundType.DEEP_OCEAN,
    name: "Deep Ocean",
    description:
      "Immersive underwater scene with marine life and floating bubbles",
    icon: '<i class="fas fa-water"></i>',
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
