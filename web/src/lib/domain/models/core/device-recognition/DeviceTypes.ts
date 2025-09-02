/**
 * Device Detection and Responsive Types
 *
 * Types for device capability detection and responsive design.
 */

export interface DeviceCapabilities {
  // Primary input method
  primaryInput: "touch" | "mouse" | "hybrid";

  // Screen characteristics
  screenSize: "mobile" | "tablet" | "desktop" | "largeDesktop";

  // Device features
  hasTouch: boolean;
  hasPrecisePointer: boolean;
  hasKeyboard: boolean;

  // Viewport information
  viewport: {
    width: number;
    height: number;
  };

  // Display characteristics
  pixelRatio: number;
  colorDepth: number;
  supportsHDR: boolean;

  // Performance indicators
  memoryEstimate?: number; // MB
  hardwareConcurrency: number;
  connectionSpeed?: "slow" | "medium" | "fast";
}

export interface ResponsiveSettings {
  // Touch and interaction
  minTouchTarget: number;
  elementSpacing: number;
  allowScrolling: boolean;
  layoutDensity: "compact" | "comfortable" | "spacious";
  fontScaling: number;

  // Device detection data
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  screenWidth: number;
  screenHeight: number;
  devicePixelRatio: number;
  touchSupported: boolean;
  orientation: "portrait" | "landscape";
}
