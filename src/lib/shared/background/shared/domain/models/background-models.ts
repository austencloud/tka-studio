// Clean Shared Background Models - Only truly shared interfaces

import type {
  Dimensions,
  PerformanceMetrics,
  QualityLevel,
} from "../types/background-types";

export interface GradientStop {
  position: number;
  color: string;
}

export interface AccessibilitySettings {
  reducedMotion: boolean;
  highContrast: boolean;
  visibleParticleSize: number;
}

export interface AnimationComponent {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
  update: (dimensions: Dimensions) => void;
  draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
  cleanup: () => void;
  setQuality: (quality: QualityLevel) => void;
  setAccessibility?: (settings: AccessibilitySettings) => void;
}

export interface AnimationSystem<T> {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => T;
  update: (state: T, dimensions: Dimensions) => T;
  draw: (
    state: T,
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ) => void;
  cleanup?: () => void;
  setQuality?: (quality: QualityLevel) => void;
  adjustToResize?: (
    state: T,
    oldDimensions: Dimensions,
    newDimensions: Dimensions,
    quality: QualityLevel
  ) => T;
  setAccessibility?: (settings: AccessibilitySettings) => void;
}

export interface BackgroundSystem {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
  update: (dimensions: Dimensions, frameMultiplier?: number) => void;
  draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
  setQuality: (quality: QualityLevel) => void;
  cleanup: () => void;
  handleResize?: (oldDimensions: Dimensions, newDimensions: Dimensions) => void;
  setAccessibility?: (settings: AccessibilitySettings) => void;
  getMetrics?: () => PerformanceMetrics;
}

export interface QualityConfig {
  maxParticles: number;
  animationFrameRate: number;
  enableBlur: boolean;
  enableGlow: boolean;
  particleSize: number;
  densityMultiplier: number;
}

export interface QualitySettings {
  densityMultiplier: number;
  enableShootingStars: boolean;
  enableSeasonal: boolean;
  particleComplexity: "high" | "medium" | "low" | "minimal";
  enableBloom: boolean;
  enableReflections: boolean;
}
export interface GradientStop {
  position: number;
  color: string;
}

export interface AccessibilitySettings {
  reducedMotion: boolean;
  highContrast: boolean;
  visibleParticleSize: number;
}

export interface AnimationComponent {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
  update: (dimensions: Dimensions) => void;
  draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
  cleanup: () => void;
  setQuality: (quality: QualityLevel) => void;
  setAccessibility?: (settings: AccessibilitySettings) => void;
}

export interface AnimationSystem<T> {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => T;
  update: (state: T, dimensions: Dimensions) => T;
  draw: (
    state: T,
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ) => void;
  cleanup?: () => void;
  setQuality?: (quality: QualityLevel) => void;
  adjustToResize?: (
    state: T,
    oldDimensions: Dimensions,
    newDimensions: Dimensions,
    quality: QualityLevel
  ) => T;
  setAccessibility?: (settings: AccessibilitySettings) => void;
}

export interface BackgroundSystem {
  initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
  update: (dimensions: Dimensions, frameMultiplier?: number) => void;
  draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
  setQuality: (quality: QualityLevel) => void;
  cleanup: () => void;
  handleResize?: (oldDimensions: Dimensions, newDimensions: Dimensions) => void;
  setAccessibility?: (settings: AccessibilitySettings) => void;
  getMetrics?: () => PerformanceMetrics;
}
