/**
 * Background configuration for landing project
 */

export type QualityLevel = "high" | "medium" | "low" | "minimal";

/**
 * Detects the appropriate quality level based on device capabilities
 */
export function detectAppropriateQuality(): QualityLevel {
  // Fallback for server-side rendering
  if (typeof window === "undefined") {
    return "medium";
  }

  try {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (prefersReducedMotion) {
      return "minimal";
    }

    // Check device memory (if available)
    const deviceMemory = (navigator as Navigator & { deviceMemory?: number })
      .deviceMemory;
    if (deviceMemory && deviceMemory < 4) {
      return "low";
    }

    // Check hardware concurrency (CPU cores)
    const hardwareConcurrency = navigator.hardwareConcurrency || 2;
    if (hardwareConcurrency < 2) {
      return "low";
    }

    // Check screen size - smaller screens get lower quality
    const screenSize = window.screen.width * window.screen.height;
    if (screenSize < 1280 * 720) {
      return "low";
    }

    // Check if mobile device
    const isMobile =
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      );
    if (isMobile) {
      return "medium";
    }

    // Default to medium quality for most devices
    return "medium";
  } catch (error) {
    console.warn("Failed to detect appropriate quality level:", error);
    return "medium";
  }
}
