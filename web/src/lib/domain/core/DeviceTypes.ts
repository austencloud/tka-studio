/**
 * Device Detection and Responsive Types
 *
 * Types for device capability detection and responsive design.
 */

export interface DeviceCapabilities {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  hasTouch: boolean;
  screenSize: { width: number; height: number };
  pixelRatio: number;
}

export interface ResponsiveSettings {
  minTouchTarget: number;
  elementSpacing: number;
  preferScrolling: boolean;
  maxContentWidth: number;
}
