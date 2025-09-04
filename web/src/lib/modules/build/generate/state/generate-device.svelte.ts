/**
 * Simple device state management for GeneratePanel
 *
 * Just extracts the device detection logic without over-engineering
 */

import type { DeviceCapabilities, ResponsiveSettings } from "$domain";

/**
 * Creates simple reactive state for device integration
 */
export function createDeviceState() {
  // Simple device state (matches your original)
  let deviceCapabilities = $state<DeviceCapabilities | null>(null);
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // Derived values (matches your original logic exactly)
  const layoutMode = $derived(() => {
    if (!responsiveSettings) return "comfortable";
    return responsiveSettings.layoutDensity;
  });

  const shouldAllowScrolling = $derived(() => {
    return responsiveSettings?.allowScrolling ?? true;
  });

  const minTouchTarget = $derived(() => {
    return responsiveSettings?.minTouchTarget ?? 44;
  });

  const elementSpacing = $derived(() => {
    return responsiveSettings?.elementSpacing ?? 16;
  });

  // Compatibility properties for older code
  const isMobile = $derived(() => {
    return deviceCapabilities?.screenSize === "mobile";
  });

  const isTablet = $derived(() => {
    return deviceCapabilities?.screenSize === "tablet";
  });

  const isDesktop = $derived(() => {
    return deviceCapabilities?.screenSize === "desktop";
  });

  // Simple initialization function (matches your original onMount logic)
  function initializeDevice(deviceService: {
    getCapabilities(): DeviceCapabilities;
    getResponsiveSettings(): ResponsiveSettings;
    onCapabilitiesChanged(
      callback: (caps: DeviceCapabilities) => void
    ): () => void;
  }) {
    try {
      deviceCapabilities = deviceService.getCapabilities();
      responsiveSettings = deviceService.getResponsiveSettings();

      console.log(
        "🔍 Device capabilities:",
        $state.snapshot(deviceCapabilities)
      );
      console.log(
        "📱 Responsive settings:",
        $state.snapshot(responsiveSettings)
      );

      // Listen for device changes
      const cleanup = deviceService.onCapabilitiesChanged(
        (caps: DeviceCapabilities) => {
          deviceCapabilities = caps;
          responsiveSettings = deviceService.getResponsiveSettings();
        }
      );

      return cleanup;
    } catch (error) {
      console.warn(
        "DeviceDetectionService not available, using defaults:",
        error
      );
      // Fallback defaults (matches your original)
      responsiveSettings = {
        minTouchTarget: 44,
        elementSpacing: 16,
        allowScrolling: true,
        layoutDensity: "comfortable",
        fontScaling: 1.0,
      } as ResponsiveSettings;
      // Return empty cleanup function for fallback
      return () => {};
    }
  }

  return {
    // State
    get deviceCapabilities() {
      return deviceCapabilities;
    },
    get responsiveSettings() {
      return responsiveSettings;
    },

    // Derived values
    get layoutMode() {
      return layoutMode;
    },
    get shouldAllowScrolling() {
      return shouldAllowScrolling;
    },
    get minTouchTarget() {
      return minTouchTarget;
    },
    get elementSpacing() {
      return elementSpacing;
    },

    // Compatibility properties
    get isMobile() {
      return isMobile;
    },
    get isTablet() {
      return isTablet;
    },
    get isDesktop() {
      return isDesktop;
    },

    // Actions
    initializeDevice,
  };
}
