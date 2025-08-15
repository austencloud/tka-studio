/**
 * Device Detection State - Pure Svelte 5 Runes
 *
 * Handles device detection, window dimensions, and mobile/tablet detection
 */

import { BREAKPOINTS, type DeviceType } from "../config";
import {
  detectFoldableDevice,
  type FoldableDetectionResult,
} from "../utils/deviceDetection";
import { getEnhancedDeviceType } from "../utils/layoutUtils";

export interface DeviceState {
  windowWidth: number;
  windowHeight: number;
  deviceType: DeviceType;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  foldableInfo: FoldableDetectionResult;
}

export function createDeviceState() {
  // Window dimensions state using runes
  let windowWidth = $state(
    typeof window !== "undefined" ? window.innerWidth : BREAKPOINTS.desktop
  );
  let windowHeight = $state(
    typeof window !== "undefined" ? window.innerHeight : 768
  );

  // Derived device information using runes
  const foldableInfo = $derived(() => detectFoldableDevice());

  const enhancedDeviceInfo = $derived(() => {
    const isMobileUserAgent =
      typeof navigator !== "undefined" &&
      /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    return getEnhancedDeviceType(windowWidth, isMobileUserAgent);
  });

  const deviceType = $derived(() => enhancedDeviceInfo().deviceType);
  const isMobile = $derived(
    () => deviceType() === "smallMobile" || deviceType() === "mobile"
  );
  const isTablet = $derived(() => deviceType() === "tablet");
  const isPortrait = $derived(() => windowHeight > windowWidth);

  // Window resize handler
  function updateWindowDimensions() {
    if (typeof window !== "undefined") {
      windowWidth = window.innerWidth;
      windowHeight = window.innerHeight;
    }
  }

  // Setup window resize listener (call this in onMount)
  function initializeWindowListener() {
    if (typeof window !== "undefined") {
      window.addEventListener("resize", updateWindowDimensions);
      updateWindowDimensions(); // Initial update
    }
  }

  // Cleanup function
  function destroyWindowListener() {
    if (typeof window !== "undefined") {
      window.removeEventListener("resize", updateWindowDimensions);
    }
  }

  return {
    // State accessors
    get windowWidth() {
      return windowWidth;
    },
    get windowHeight() {
      return windowHeight;
    },
    get deviceType() {
      return deviceType();
    },
    get isMobile() {
      return isMobile();
    },
    get isTablet() {
      return isTablet();
    },
    get isPortrait() {
      return isPortrait();
    },
    get foldableInfo() {
      return foldableInfo();
    },

    // Actions
    updateWindowDimensions,
    initializeWindowListener,
    destroyWindowListener,

    // Derived state object
    get state(): DeviceState {
      return {
        windowWidth,
        windowHeight,
        deviceType: deviceType(),
        isMobile: isMobile(),
        isTablet: isTablet(),
        isPortrait: isPortrait(),
        foldableInfo: foldableInfo(),
      };
    },
  };
}
