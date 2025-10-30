import { injectable } from "inversify";
import type { IPlatformDetectionService, Platform, Browser, PlatformInfo } from "../contracts/IPlatformDetectionService";

/**
 * Platform Detection Service Implementation
 *
 * Provides centralized platform and browser detection capabilities.
 */
@injectable()
export class PlatformDetectionService implements IPlatformDetectionService {

  detectPlatformAndBrowser(): PlatformInfo {
    return {
      platform: this.detectPlatform(),
      browser: this.detectBrowser(),
    };
  }

  detectPlatform(): Platform {
    if (typeof navigator === "undefined") return "desktop";

    const ua = navigator.userAgent.toLowerCase();

    if (/iphone|ipad|ipod/.test(ua)) {
      return "ios";
    }

    if (/android/.test(ua)) {
      return "android";
    }

    return "desktop";
  }

  detectBrowser(): Browser {
    if (typeof navigator === "undefined") return "other";

    const ua = navigator.userAgent.toLowerCase();

    // Check for Samsung Internet first (most specific)
    if (ua.includes("samsungbrowser")) {
      return "samsung";
    }

    // Check for Edge (before Chrome, as Edge UA contains "chrome")
    if (ua.includes("edg/")) {
      return "edge";
    }

    // Check for Firefox
    if (ua.includes("firefox") || ua.includes("fxios")) {
      return "firefox";
    }

    // Check for Chrome (excludes Edge and Samsung)
    if (ua.includes("chrome") || ua.includes("crios")) {
      return "chrome";
    }

    // Check for Safari (must be after Chrome/Edge/Firefox checks)
    if (ua.includes("safari")) {
      return "safari";
    }

    return "other";
  }

  supportsPWAInstall(platform: Platform, browser: Browser): boolean {
    // iOS only supports Safari
    if (platform === "ios") {
      return browser === "safari";
    }

    // Android supports Chrome, Edge, and Samsung Internet
    if (platform === "android") {
      return ["chrome", "edge", "samsung"].includes(browser);
    }

    // Desktop supports Chrome and Edge
    if (platform === "desktop") {
      return ["chrome", "edge"].includes(browser);
    }

    return false;
  }

  getBrowserDisplayName(browser: Browser): string {
    const names: Record<Browser, string> = {
      chrome: "Chrome",
      safari: "Safari",
      edge: "Edge",
      firefox: "Firefox",
      samsung: "Samsung Internet",
      other: "Unknown Browser",
    };

    return names[browser];
  }

  getPlatformDisplayName(platform: Platform): string {
    const names: Record<Platform, string> = {
      ios: "iOS",
      android: "Android",
      desktop: "Desktop",
    };

    return names[platform];
  }
}
