/**
 * Device detection utilities for option picker
 */

import type { DeviceType } from "../config";
import { BREAKPOINTS } from "../config";

export interface FoldableDetectionResult {
  isFoldable: boolean;
  isUnfolded: boolean;
  screenSpanning: boolean;
  foldableType?: string; // Add for compatibility
  confidence?: number; // Add for compatibility
}

export interface DeviceCapabilities {
  touchSupport: boolean;
  hoverSupport: boolean;
  keyboardSupport: boolean;
  screenSize: DeviceType;
}

/**
 * Detect device type based on screen width
 */
export function detectDeviceType(): DeviceType {
  if (typeof window === "undefined") return "desktop";

  const width = window.innerWidth;

  if (width < BREAKPOINTS.mobile) return "mobile";
  if (width < BREAKPOINTS.tablet) return "tablet";
  return "desktop";
}

/**
 * Detect foldable device characteristics
 */
export function detectFoldableDevice(): FoldableDetectionResult {
  if (typeof window === "undefined") {
    return {
      isFoldable: false,
      isUnfolded: false,
      screenSpanning: false,
      foldableType: "unknown",
      confidence: 0,
    };
  }

  // Use proper foldable detection logic based on the existing comprehensive system
  const ua = navigator.userAgent;
  const windowW = window.innerWidth;
  const windowH = window.innerHeight;
  const aspectRatio = windowW / windowH;
  const pixelRatio = window.devicePixelRatio || 1;

  // Check for screen spanning API (most reliable)
  const isScreenSpanning =
    window.matchMedia("(screen-spanning: single-fold-vertical)").matches ||
    window.matchMedia("(screen-spanning: single-fold-horizontal)").matches;

  // Check for window segments API
  const hasSegments =
    "getWindowSegments" in navigator &&
    typeof (navigator as Navigator & { getWindowSegments?: () => unknown })
      .getWindowSegments === "function";

  if (isScreenSpanning || hasSegments) {
    return {
      isFoldable: true,
      isUnfolded: aspectRatio > 0.8 && aspectRatio < 1.3,
      screenSpanning: isScreenSpanning,
      foldableType: /galaxy z/i.test(ua) ? "zfold" : "other",
      confidence: 0.8,
    };
  }

  // Dimension heuristic for high-end devices (fallback)
  if (
    windowW > 600 &&
    aspectRatio > 0.8 &&
    aspectRatio < 1.3 &&
    pixelRatio > 1.5
  ) {
    return {
      isFoldable: true,
      isUnfolded: true,
      screenSpanning: false,
      foldableType: /galaxy z/i.test(ua) ? "zfold" : "other",
      confidence: 0.5,
    };
  }

  // Default fallback
  return {
    isFoldable: false,
    isUnfolded: false,
    screenSpanning: false,
    foldableType: "unknown",
    confidence: 0,
  };
}

/**
 * Detect device capabilities
 */
export function detectDeviceCapabilities(): DeviceCapabilities {
  if (typeof window === "undefined") {
    return {
      touchSupport: false,
      hoverSupport: true,
      keyboardSupport: true,
      screenSize: "desktop",
    };
  }

  return {
    touchSupport: "ontouchstart" in window,
    hoverSupport: window.matchMedia("(hover: hover)").matches,
    keyboardSupport: true, // Assume keyboard support
    screenSize: detectDeviceType(),
  };
}

/**
 * Check if device is in landscape orientation
 */
export function isLandscapeOrientation(): boolean {
  if (typeof window === "undefined") return true;
  return window.innerWidth > window.innerHeight;
}
