import { injectable } from "inversify";
import type {
  DeviceCapabilities,
  ResponsiveSettings,
} from "../../domain/models/device-models";
import type { IDeviceDetector } from "../contracts/IDeviceDetector";
import { DeviceType } from "../../domain";

/**
 * Device Detector Implementation
 *
 * Detects device capabilities and characteristics using browser APIs.
 */
@injectable()
export class DeviceDetector implements IDeviceDetector {
  private deviceType: DeviceType | null = null;
  private capabilitiesCallbacks: ((caps: DeviceCapabilities) => void)[] = [];

  detectDeviceType(): DeviceType {
    if (this.deviceType) {
      return this.deviceType;
    }

    const screenWidth = window.screen.width;
    const hasTouch = "ontouchstart" in window;

    // Mobile detection
    if (hasTouch && screenWidth < 768) {
      this.deviceType = DeviceType.MOBILE;
    }
    // Tablet detection
    else if (hasTouch && screenWidth >= 768 && screenWidth < 1024) {
      this.deviceType = DeviceType.TABLET;
    }
    // Desktop detection
    else {
      this.deviceType = DeviceType.DESKTOP;
    }

    console.log(`📱 DeviceDetector: Detected device type: ${this.deviceType}`);
    return this.deviceType!; // Non-null assertion since we just set it above
  }

  isTouchDevice(): boolean {
    return "ontouchstart" in window || navigator.maxTouchPoints > 0;
  }

  isMobile(): boolean {
    return this.detectDeviceType() === DeviceType.MOBILE;
  }

  isTablet(): boolean {
    return this.detectDeviceType() === DeviceType.TABLET;
  }

  isDesktop(): boolean {
    return this.detectDeviceType() === DeviceType.DESKTOP;
  }

  getScreenInfo() {
    return {
      width: window.screen.width,
      height: window.screen.height,
      pixelRatio: window.devicePixelRatio || 1,
    };
  }

  supportsFoldable(): boolean {
    // Basic check for foldable device features
    // This would need to be expanded with actual foldable detection logic
    return "screen" in window && "orientation" in window.screen;
  }

  getCapabilities(): DeviceCapabilities {
    const screenInfo = this.getScreenInfo();
    const deviceType = this.detectDeviceType();
    const hasTouch = this.isTouchDevice();

    return {
      primaryInput: hasTouch ? "touch" : "mouse",
      screenSize: this.getScreenSizeCategory(deviceType),
      hasTouch,
      hasPrecisePointer: !hasTouch,
      hasKeyboard: !this.isMobile(),
      viewport: {
        width: screenInfo.width,
        height: screenInfo.height,
      },
      pixelRatio: screenInfo.pixelRatio,
      colorDepth: window.screen?.colorDepth || 24,
      supportsHDR: false, // Basic implementation
      hardwareConcurrency: navigator.hardwareConcurrency || 4,
    };
  }

  getResponsiveSettings(): ResponsiveSettings {
    const capabilities = this.getCapabilities();
    const isMobile = this.isMobile();
    const isTablet = this.isTablet();
    const isDesktop = this.isDesktop();

    return {
      minTouchTarget: capabilities.hasTouch ? 44 : 32,
      elementSpacing: isMobile ? 12 : isTablet ? 16 : 20,
      allowScrolling: true,
      layoutDensity: isMobile
        ? "compact"
        : isTablet
          ? "comfortable"
          : "spacious",
      fontScaling: isMobile ? 1.1 : 1.0,
      isMobile,
      isTablet,
      isDesktop,
      screenWidth: capabilities.viewport.width,
      screenHeight: capabilities.viewport.height,
      devicePixelRatio: capabilities.pixelRatio,
      touchSupported: capabilities.hasTouch,
      orientation:
        capabilities.viewport.width > capabilities.viewport.height
          ? "landscape"
          : "portrait",
    };
  }

  onCapabilitiesChanged(
    callback: (caps: DeviceCapabilities) => void
  ): () => void {
    this.capabilitiesCallbacks.push(callback);

    // Return cleanup function
    return () => {
      const index = this.capabilitiesCallbacks.indexOf(callback);
      if (index > -1) {
        this.capabilitiesCallbacks.splice(index, 1);
      }
    };
  }

  private getScreenSizeCategory(
    deviceType: DeviceType
  ): "mobile" | "tablet" | "desktop" | "largeDesktop" {
    switch (deviceType) {
      case DeviceType.MOBILE:
        return "mobile";
      case DeviceType.TABLET:
        return "tablet";
      case DeviceType.DESKTOP:
        return window.screen.width > 1440 ? "largeDesktop" : "desktop";
      default:
        return "desktop";
    }
  }
}
