/**
 * Device Detection Service Interfaces
 *
 * Interfaces for device capability detection, responsive design,
 * and platform-specific optimizations.
 */

import type { DeviceCapabilities } from "../../domain-types";

// ============================================================================
// RESPONSIVE SETTINGS
// ============================================================================

export interface ResponsiveSettings {
  /** Minimum touch target size in pixels */
  minTouchTarget: number;

  /** Preferred spacing between interactive elements */
  elementSpacing: number;

  /** Whether scrolling is acceptable in current context */
  allowScrolling: boolean;

  /** Layout density preference */
  layoutDensity: "compact" | "comfortable" | "spacious";

  /** Font size scaling factor */
  fontScaling: number;
}

// ============================================================================
// DEVICE DETECTION SERVICE
// ============================================================================

/**
 * Service for detecting device capabilities and optimizing UI accordingly
 */
export interface IDeviceDetectionService {
  /** Get current device capabilities */
  getCapabilities(): DeviceCapabilities;

  /** Get responsive settings based on device */
  getResponsiveSettings(): ResponsiveSettings;

  /** Check if device is primarily touch-based */
  isTouchPrimary(): boolean;

  /** Check if layout should prioritize touch targets */
  shouldOptimizeForTouch(): boolean;

  /** Listen for device capability changes (screen rotation, etc.) */
  onCapabilitiesChanged(
    callback: (capabilities: DeviceCapabilities) => void
  ): () => void;

  /** Get breakpoint for current viewport */
  getCurrentBreakpoint(): "mobile" | "tablet" | "desktop" | "large-desktop";
}
