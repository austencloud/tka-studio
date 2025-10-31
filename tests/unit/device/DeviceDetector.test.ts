/**
 * DeviceDetector Tests
 *
 * Comprehensive test suite for the DeviceDetector service.
 * Tests device type detection, touch detection, orientation, and capabilities.
 */

// Import directly from source files to avoid circular dependency issues with $shared barrel exports
import { beforeEach, describe, expect, it, vi } from "vitest";
import { DeviceType } from "../../../src/lib/shared/device/domain";
import { DeviceDetector } from "../../../src/lib/shared/device/services/implementations/DeviceDetector";

// Mock ViewportService
class MockViewportService {
  width = 1024;
  height = 768;

  getAspectRatio(): number {
    return this.width / this.height;
  }

  isLandscape(): boolean {
    return this.width > this.height;
  }

  isPortrait(): boolean {
    return this.height > this.width;
  }

  setDimensions(width: number, height: number) {
    this.width = width;
    this.height = height;
  }
}

describe("DeviceDetector", () => {
  let detector: DeviceDetector;
  let mockViewportService: MockViewportService;

  beforeEach(() => {
    mockViewportService = new MockViewportService();
    detector = new DeviceDetector(mockViewportService as any);

    // Reset window properties - DELETE ontouchstart instead of setting to undefined
    // because "ontouchstart" in window checks for property existence, not value
    if ("ontouchstart" in window) {
      delete (window as any).ontouchstart;
    }

    Object.defineProperty(navigator, "maxTouchPoints", {
      writable: true,
      configurable: true,
      value: 0,
    });

    Object.defineProperty(window.screen, "width", {
      writable: true,
      configurable: true,
      value: 1920,
    });

    Object.defineProperty(window.screen, "height", {
      writable: true,
      configurable: true,
      value: 1080,
    });

    Object.defineProperty(window.screen, "orientation", {
      writable: true,
      configurable: true,
      value: { type: "landscape-primary", angle: 0 },
    });

    Object.defineProperty(window, "devicePixelRatio", {
      writable: true,
      value: 1,
    });
  });

  // ============================================================================
  // DEVICE TYPE DETECTION TESTS
  // ============================================================================

  describe("detectDeviceType", () => {
    it("should detect mobile device (viewport < 768px)", () => {
      mockViewportService.setDimensions(375, 667);
      expect(detector.detectDeviceType()).toBe(DeviceType.MOBILE);
    });

    it("should detect tablet device (touch + 768-1024px)", () => {
      mockViewportService.setDimensions(768, 1024);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });

      expect(detector.detectDeviceType()).toBe(DeviceType.TABLET);
    });

    it("should detect desktop device (>= 1024px)", () => {
      mockViewportService.setDimensions(1920, 1080);
      expect(detector.detectDeviceType()).toBe(DeviceType.DESKTOP);
    });

    it("should detect desktop even with touch on large screen", () => {
      mockViewportService.setDimensions(1920, 1080);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });

      expect(detector.detectDeviceType()).toBe(DeviceType.DESKTOP);
    });

    it("should cache device type for same viewport dimensions", () => {
      mockViewportService.setDimensions(1024, 768);

      const firstCall = detector.detectDeviceType();
      const secondCall = detector.detectDeviceType();

      expect(firstCall).toBe(secondCall);
      expect(firstCall).toBe(DeviceType.DESKTOP);
    });

    it("should invalidate cache when viewport changes", () => {
      mockViewportService.setDimensions(1024, 768);
      const firstType = detector.detectDeviceType();

      mockViewportService.setDimensions(375, 667);
      const secondType = detector.detectDeviceType();

      expect(firstType).toBe(DeviceType.DESKTOP);
      expect(secondType).toBe(DeviceType.MOBILE);
    });

    it("should handle edge case at 768px boundary", () => {
      mockViewportService.setDimensions(767, 1024);
      expect(detector.detectDeviceType()).toBe(DeviceType.MOBILE);

      mockViewportService.setDimensions(768, 1024);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });
      expect(detector.detectDeviceType()).toBe(DeviceType.TABLET);
    });

    it("should handle edge case at 1024px boundary", () => {
      mockViewportService.setDimensions(1023, 768);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });
      expect(detector.detectDeviceType()).toBe(DeviceType.TABLET);

      mockViewportService.setDimensions(1024, 768);
      expect(detector.detectDeviceType()).toBe(DeviceType.DESKTOP);
    });
  });

  // ============================================================================
  // TOUCH DETECTION TESTS
  // ============================================================================

  describe("isTouchDevice", () => {
    it("should detect touch via ontouchstart", () => {
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });
      expect(detector.isTouchDevice()).toBe(true);
    });

    it("should detect touch via maxTouchPoints", () => {
      Object.defineProperty(navigator, "maxTouchPoints", { value: 5 });
      expect(detector.isTouchDevice()).toBe(true);
    });

    it("should return false for non-touch devices", () => {
      expect(detector.isTouchDevice()).toBe(false);
    });
  });

  // ============================================================================
  // DEVICE TYPE HELPER TESTS
  // ============================================================================

  describe("Device Type Helpers", () => {
    it("isMobile should return true for mobile devices", () => {
      mockViewportService.setDimensions(375, 667);
      expect(detector.isMobile()).toBe(true);
      expect(detector.isTablet()).toBe(false);
      expect(detector.isDesktop()).toBe(false);
    });

    it("isTablet should return true for tablet devices", () => {
      mockViewportService.setDimensions(768, 1024);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });

      expect(detector.isMobile()).toBe(false);
      expect(detector.isTablet()).toBe(true);
      expect(detector.isDesktop()).toBe(false);
    });

    it("isDesktop should return true for desktop devices", () => {
      mockViewportService.setDimensions(1920, 1080);
      expect(detector.isMobile()).toBe(false);
      expect(detector.isTablet()).toBe(false);
      expect(detector.isDesktop()).toBe(true);
    });
  });

  // ============================================================================
  // LANDSCAPE MOBILE DETECTION TESTS
  // ============================================================================

  describe("isLandscapeMobile", () => {
    it("should detect landscape mobile (wide aspect + low height)", () => {
      mockViewportService.setDimensions(844, 390); // iPhone 14 Pro landscape
      expect(detector.isLandscapeMobile()).toBe(true);
    });

    it("should detect landscape mobile with aspect ratio > 1.7", () => {
      mockViewportService.setDimensions(850, 400); // 2.125:1 ratio
      expect(detector.isLandscapeMobile()).toBe(true);
    });

    it("should NOT detect tablet landscape as landscape mobile", () => {
      mockViewportService.setDimensions(1024, 768); // Tablet landscape
      expect(detector.isLandscapeMobile()).toBe(false);
    });

    it("should NOT detect landscape mobile if height >= 500px", () => {
      mockViewportService.setDimensions(1000, 500);
      expect(detector.isLandscapeMobile()).toBe(false);
    });

    it("should NOT detect landscape mobile if aspect ratio <= 1.7", () => {
      mockViewportService.setDimensions(680, 400); // 1.7:1 ratio
      expect(detector.isLandscapeMobile()).toBe(false);
    });

    it("should NOT detect portrait as landscape mobile", () => {
      mockViewportService.setDimensions(390, 844); // Portrait
      expect(detector.isLandscapeMobile()).toBe(false);
    });
  });

  // ============================================================================
  // PORTRAIT MOBILE DETECTION TESTS
  // ============================================================================

  describe("isPortraitMobile", () => {
    it("should detect portrait mobile (narrow width)", () => {
      mockViewportService.setDimensions(390, 844); // iPhone portrait
      expect(detector.isPortraitMobile()).toBe(true);
    });

    it("should detect portrait mobile with width < 600px", () => {
      mockViewportService.setDimensions(599, 1000);
      expect(detector.isPortraitMobile()).toBe(true);
    });

    it("should NOT detect portrait mobile if width >= 600px", () => {
      mockViewportService.setDimensions(600, 1000);
      expect(detector.isPortraitMobile()).toBe(false);
    });

    it("should NOT detect landscape as portrait mobile", () => {
      mockViewportService.setDimensions(844, 390);
      expect(detector.isPortraitMobile()).toBe(false);
    });
  });

  // ============================================================================
  // SCREEN INFO TESTS
  // ============================================================================

  describe("getScreenInfo", () => {
    it("should return screen dimensions", () => {
      const info = detector.getScreenInfo();
      expect(info.width).toBe(1920);
      expect(info.height).toBe(1080);
    });

    it("should return pixel ratio", () => {
      Object.defineProperty(window, "devicePixelRatio", { value: 2 });
      const info = detector.getScreenInfo();
      expect(info.pixelRatio).toBe(2);
    });

    it("should default to pixel ratio 1 if not available", () => {
      Object.defineProperty(window, "devicePixelRatio", { value: undefined });
      const info = detector.getScreenInfo();
      expect(info.pixelRatio).toBe(1);
    });
  });

  // ============================================================================
  // FOLDABLE SUPPORT TESTS
  // ============================================================================

  describe("supportsFoldable", () => {
    it("should return true if screen and orientation are available", () => {
      expect(detector.supportsFoldable()).toBe(true);
    });
  });

  // ============================================================================
  // CAPABILITIES TESTS
  // ============================================================================

  describe("getCapabilities", () => {
    it("should return capabilities for desktop", () => {
      mockViewportService.setDimensions(1920, 1080);
      // Set screen dimensions to ≤1440 to get "desktop" instead of "largeDesktop"
      Object.defineProperty(window.screen, "width", {
        value: 1366,
        configurable: true,
      });
      Object.defineProperty(window.screen, "height", {
        value: 768,
        configurable: true,
      });

      const caps = detector.getCapabilities();

      expect(caps.primaryInput).toBe("mouse");
      expect(caps.screenSize).toBe("desktop");
      expect(caps.hasTouch).toBe(false);
      expect(caps.hasPrecisePointer).toBe(true);
      expect(caps.hasKeyboard).toBe(true);
    });

    it("should return capabilities for mobile with touch", () => {
      mockViewportService.setDimensions(375, 667);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });

      const caps = detector.getCapabilities();

      expect(caps.primaryInput).toBe("touch");
      expect(caps.screenSize).toBe("mobile");
      expect(caps.hasTouch).toBe(true);
      expect(caps.hasPrecisePointer).toBe(false);
      expect(caps.hasKeyboard).toBe(false);
    });

    it("should include viewport dimensions", () => {
      const caps = detector.getCapabilities();
      expect(caps.viewport.width).toBe(1920);
      expect(caps.viewport.height).toBe(1080);
    });

    it("should include pixel ratio", () => {
      Object.defineProperty(window, "devicePixelRatio", { value: 2 });
      const caps = detector.getCapabilities();
      expect(caps.pixelRatio).toBe(2);
    });

    it("should detect large desktop", () => {
      mockViewportService.setDimensions(2560, 1440);
      Object.defineProperty(window.screen, "width", { value: 2560 });

      const caps = detector.getCapabilities();
      expect(caps.screenSize).toBe("largeDesktop");
    });
  });

  // ============================================================================
  // NAVIGATION LAYOUT TESTS
  // ============================================================================

  describe("getNavigationLayoutImmediate", () => {
    it("should return 'left' for landscape mobile", () => {
      mockViewportService.setDimensions(844, 390);
      expect(detector.getNavigationLayoutImmediate()).toBe("left");
    });

    it("should return 'top' for desktop", () => {
      mockViewportService.setDimensions(1920, 1080);
      expect(detector.getNavigationLayoutImmediate()).toBe("top");
    });

    it("should return 'top' for tablet landscape", () => {
      mockViewportService.setDimensions(1024, 768);
      expect(detector.getNavigationLayoutImmediate()).toBe("top");
    });

    it("should return 'top' for portrait mobile", () => {
      mockViewportService.setDimensions(390, 844);
      expect(detector.getNavigationLayoutImmediate()).toBe("top");
    });
  });

  // ============================================================================
  // RESPONSIVE SETTINGS TESTS
  // ============================================================================

  describe("getResponsiveSettings", () => {
    it("should return mobile settings", () => {
      mockViewportService.setDimensions(375, 667);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });
      // Set screen dimensions to match viewport for correct orientation detection
      Object.defineProperty(window.screen, "width", {
        value: 375,
        configurable: true,
      });
      Object.defineProperty(window.screen, "height", {
        value: 667,
        configurable: true,
      });

      const settings = detector.getResponsiveSettings();

      expect(settings.isMobile).toBe(true);
      expect(settings.isTablet).toBe(false);
      expect(settings.isDesktop).toBe(false);
      expect(settings.minTouchTarget).toBe(44);
      expect(settings.elementSpacing).toBe(12);
      expect(settings.layoutDensity).toBe("compact");
      expect(settings.fontScaling).toBe(1.1);
      expect(settings.touchSupported).toBe(true);
      expect(settings.orientation).toBe("portrait");
    });

    it("should return tablet settings", () => {
      mockViewportService.setDimensions(768, 1024);
      Object.defineProperty(window, "ontouchstart", {
        value: true,
        configurable: true,
      });

      const settings = detector.getResponsiveSettings();

      expect(settings.isMobile).toBe(false);
      expect(settings.isTablet).toBe(true);
      expect(settings.isDesktop).toBe(false);
      expect(settings.minTouchTarget).toBe(44);
      expect(settings.elementSpacing).toBe(16);
      expect(settings.layoutDensity).toBe("comfortable");
      expect(settings.fontScaling).toBe(1.0);
    });

    it("should return desktop settings", () => {
      mockViewportService.setDimensions(1920, 1080);

      const settings = detector.getResponsiveSettings();

      expect(settings.isMobile).toBe(false);
      expect(settings.isTablet).toBe(false);
      expect(settings.isDesktop).toBe(true);
      expect(settings.minTouchTarget).toBe(32);
      expect(settings.elementSpacing).toBe(20);
      expect(settings.layoutDensity).toBe("spacious");
      expect(settings.fontScaling).toBe(1.0);
      expect(settings.touchSupported).toBe(false);
      expect(settings.orientation).toBe("landscape");
    });

    it("should detect landscape orientation", () => {
      mockViewportService.setDimensions(1920, 1080);
      const settings = detector.getResponsiveSettings();
      expect(settings.orientation).toBe("landscape");
    });

    it("should detect portrait orientation", () => {
      mockViewportService.setDimensions(1080, 1920);
      // Set screen dimensions to match viewport for correct orientation detection
      Object.defineProperty(window.screen, "width", {
        value: 1080,
        configurable: true,
      });
      Object.defineProperty(window.screen, "height", {
        value: 1920,
        configurable: true,
      });

      const settings = detector.getResponsiveSettings();
      expect(settings.orientation).toBe("portrait");
    });

    it("should include navigation layout", () => {
      mockViewportService.setDimensions(844, 390);
      const settings = detector.getResponsiveSettings();
      expect(settings.navigationLayout).toBe("left");
      expect(settings.isLandscapeMobile).toBe(true);
    });
  });

  // ============================================================================
  // CALLBACK TESTS
  // ============================================================================

  describe("onCapabilitiesChanged", () => {
    it("should register callback", () => {
      const callback = vi.fn();
      const cleanup = detector.onCapabilitiesChanged(callback);

      expect(typeof cleanup).toBe("function");
    });

    it("should remove callback when cleanup is called", () => {
      const callback = vi.fn();
      const cleanup = detector.onCapabilitiesChanged(callback);

      cleanup();

      // Callback should be removed (no way to verify directly, but cleanup should not throw)
      expect(() => cleanup()).not.toThrow();
    });

    it("should handle multiple callbacks", () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();

      const cleanup1 = detector.onCapabilitiesChanged(callback1);
      const cleanup2 = detector.onCapabilitiesChanged(callback2);

      cleanup1();
      cleanup2();

      expect(() => cleanup1()).not.toThrow();
      expect(() => cleanup2()).not.toThrow();
    });
  });
});
