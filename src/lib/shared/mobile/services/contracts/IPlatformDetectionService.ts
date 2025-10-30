/**
 * Platform Detection Service Contract
 *
 * Provides centralized platform and browser detection capabilities.
 * Eliminates duplication of detection logic across components.
 */

export type Platform = "ios" | "android" | "desktop";
export type Browser = "chrome" | "safari" | "edge" | "firefox" | "samsung" | "other";

export interface PlatformInfo {
  platform: Platform;
  browser: Browser;
}

export interface IPlatformDetectionService {
  /**
   * Detect the user's platform and browser from user agent
   */
  detectPlatformAndBrowser(): PlatformInfo;

  /**
   * Detect the user's platform (iOS, Android, or Desktop)
   */
  detectPlatform(): Platform;

  /**
   * Detect the user's browser
   */
  detectBrowser(): Browser;

  /**
   * Check if the current platform/browser combination supports PWA installation
   */
  supportsPWAInstall(platform: Platform, browser: Browser): boolean;

  /**
   * Get a user-friendly browser name
   */
  getBrowserDisplayName(browser: Browser): string;

  /**
   * Get a user-friendly platform name
   */
  getPlatformDisplayName(platform: Platform): string;
}
