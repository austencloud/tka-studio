/**
 * Device Detector Service Interface
 *
 * Service contract for device detection and responsive settings management.
 */

import type { DeviceCapabilities, ResponsiveSettings } from "$domain";

// ============================================================================
// SERVICE CONTRACT (Behavioral Interface)
// ============================================================================

export interface IDeviceDetector {
  /**
   * Get current device capabilities
   */
  getCapabilities(): DeviceCapabilities;

  /**
   * Get responsive settings
   */
  getResponsiveSettings(): ResponsiveSettings;

  /**
   * Check if touch is the primary input method
   */
  isTouchPrimary(): boolean;

  /**
   * Check if interface should be optimized for touch
   */
  shouldOptimizeForTouch(): boolean;

  /**
   * Get current responsive breakpoint
   */
  getCurrentBreakpoint(): "mobile" | "tablet" | "desktop" | "large-desktop";

  /**
   * Add listener for capability changes
   */
  addCapabilityListener(
    callback: (capabilities: DeviceCapabilities) => void
  ): void;

  /**
   * Remove capability change listener
   */
  removeCapabilityListener(
    callback: (capabilities: DeviceCapabilities) => void
  ): void;

  /**
   * Add listener for capability changes with cleanup function
   */
  onCapabilitiesChanged(
    callback: (capabilities: DeviceCapabilities) => void
  ): () => void;

  /**
   * Cleanup resources
   */
  dispose(): void;
}
