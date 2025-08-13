/**
 * Device Detection Service Implementation
 * Uses modern detection methods based on research from W3C, Material Design, and iOS guidelines
 */

import type {
  DeviceCapabilities,
  IDeviceDetectionService,
  ResponsiveSettings,
} from "../interfaces";

export class DeviceDetectionService implements IDeviceDetectionService {
  private capabilities: DeviceCapabilities | null = null;
  private listeners: Array<(capabilities: DeviceCapabilities) => void> = [];
  private resizeObserver: ResizeObserver | null = null;

  constructor() {
    this.detectCapabilities();
    this.setupListeners();
  }

  getCapabilities(): DeviceCapabilities {
    if (!this.capabilities) {
      this.detectCapabilities();
    }
    if (!this.capabilities) {
      throw new Error("Failed to detect device capabilities");
    }
    return this.capabilities;
  }

  getResponsiveSettings(): ResponsiveSettings {
    const caps = this.getCapabilities();

    // Based on research: mobile needs 44-48px, desktop can be smaller
    const minTouchTarget = caps.primaryInput === "touch" ? 48 : 32;
    const elementSpacing = caps.primaryInput === "touch" ? 16 : 8;

    // Mobile users expect scrolling, desktop should fit when possible
    const allowScrolling =
      caps.screenSize === "mobile" || caps.screenSize === "tablet";

    // Layout density based on screen real estate and input method
    let layoutDensity: "compact" | "comfortable" | "spacious" = "comfortable";
    if (caps.screenSize === "mobile") {
      layoutDensity = "comfortable"; // Mobile needs space for touch
    } else if (caps.screenSize === "desktop" && caps.primaryInput === "mouse") {
      layoutDensity = "compact"; // Desktop with mouse can be denser
    } else {
      layoutDensity = "spacious"; // Hybrid devices get spacious
    }

    const fontScaling = caps.screenSize === "mobile" ? 1.1 : 1.0;

    return {
      minTouchTarget,
      elementSpacing,
      allowScrolling,
      layoutDensity,
      fontScaling,
    };
  }

  isTouchPrimary(): boolean {
    return this.getCapabilities().primaryInput === "touch";
  }

  shouldOptimizeForTouch(): boolean {
    const caps = this.getCapabilities();
    return caps.primaryInput === "touch" || caps.primaryInput === "hybrid";
  }

  getCurrentBreakpoint(): "mobile" | "tablet" | "desktop" | "large-desktop" {
    const { width } = this.getCapabilities().viewport;

    // Standard breakpoints based on research
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    if (width < 1440) return "desktop";
    return "large-desktop";
  }

  onCapabilitiesChanged(
    callback: (capabilities: DeviceCapabilities) => void,
  ): () => void {
    this.listeners.push(callback);

    // Return cleanup function
    return () => {
      const index = this.listeners.indexOf(callback);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private detectCapabilities(): void {
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight,
    };

    // Touch detection using multiple methods for reliability
    const hasTouch = this.detectTouch();

    // Precise pointer detection (mouse/trackpad)
    const hasPrecisePointer = this.detectPrecisePointer();

    // Keyboard detection (best effort)
    const hasKeyboard = this.detectKeyboard();

    // Screen size category
    const screenSize = this.determineScreenSize(viewport.width);

    // Primary input method determination
    const primaryInput = this.determinePrimaryInput(
      hasTouch,
      hasPrecisePointer,
      screenSize,
    );

    this.capabilities = {
      primaryInput,
      screenSize,
      hasTouch,
      hasPrecisePointer,
      hasKeyboard,
      viewport,
      pixelRatio: window.devicePixelRatio || 1,
      colorDepth: screen.colorDepth || 24,
      supportsHDR: this.detectHDRSupport(),
      hardwareConcurrency: navigator.hardwareConcurrency || 4,
      memoryEstimate: this.estimateMemory(),
      connectionSpeed: this.detectConnectionSpeed(),
    };

    // Update CSS custom properties
    this.updateCSSProperties();
  }

  private detectTouch(): boolean {
    // Multi-method approach based on research
    return (
      "ontouchstart" in window ||
      navigator.maxTouchPoints > 0 ||
      // Legacy IE support
      ((navigator as Navigator & { msMaxTouchPoints?: number })
        .msMaxTouchPoints ?? 0) > 0
    );
  }

  private detectPrecisePointer(): boolean {
    // Use CSS media query for precise pointer detection
    return window.matchMedia("(pointer: fine)").matches;
  }

  private detectKeyboard(): boolean {
    // This is hard to detect reliably without user interaction
    // For now, assume desktop/laptop devices have keyboards
    // Could be enhanced with actual key event detection
    return window.matchMedia("(pointer: fine)").matches;
  }

  private determineScreenSize(width: number): "mobile" | "tablet" | "desktop" {
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    return "desktop";
  }

  private determinePrimaryInput(
    hasTouch: boolean,
    hasPrecisePointer: boolean,
    screenSize: "mobile" | "tablet" | "desktop",
  ): "touch" | "mouse" | "hybrid" {
    // Mobile devices are primarily touch
    if (screenSize === "mobile") return "touch";

    // Desktop without touch is mouse
    if (screenSize === "desktop" && !hasTouch) return "mouse";

    // Desktop with touch capabilities (Windows tablets, touchscreen laptops)
    if (screenSize === "desktop" && hasTouch && hasPrecisePointer)
      return "hybrid";

    // Tablet logic
    if (screenSize === "tablet") {
      return hasPrecisePointer ? "hybrid" : "touch";
    }

    // Fallback
    return hasTouch ? "touch" : "mouse";
  }

  private updateCSSProperties(): void {
    if (!this.capabilities) return;

    const settings = this.getResponsiveSettings();

    // Update CSS custom properties for global use
    document.documentElement.style.setProperty(
      "--min-touch-target",
      `${settings.minTouchTarget}px`,
    );
    document.documentElement.style.setProperty(
      "--element-spacing",
      `${settings.elementSpacing}px`,
    );
    document.documentElement.style.setProperty(
      "--font-scaling",
      settings.fontScaling.toString(),
    );

    // Set data attributes for CSS targeting
    document.documentElement.setAttribute(
      "data-device-type",
      this.capabilities.primaryInput,
    );
    document.documentElement.setAttribute(
      "data-screen-size",
      this.capabilities.screenSize,
    );
    document.documentElement.setAttribute(
      "data-layout-density",
      settings.layoutDensity,
    );
  }

  private setupListeners(): void {
    // Listen for viewport changes
    const handleResize = () => {
      const oldCapabilities = this.capabilities;
      this.detectCapabilities();

      // Only notify if capabilities actually changed
      if (this.hasCapabilitiesChanged(oldCapabilities, this.capabilities)) {
        this.notifyListeners();
      }
    };

    // Listen for orientation changes on mobile
    const handleOrientationChange = () => {
      // Small delay to ensure viewport is updated
      setTimeout(handleResize, 100);
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("orientationchange", handleOrientationChange);

    // Modern ResizeObserver for more responsive updates
    if ("ResizeObserver" in window) {
      this.resizeObserver = new ResizeObserver(handleResize);
      this.resizeObserver.observe(document.documentElement);
    }

    // Detect if user switches from touch to mouse (or vice versa)
    let hasDetectedMouse = false;
    const handleMouseMove = () => {
      if (!hasDetectedMouse) {
        hasDetectedMouse = true;
        // Re-evaluate capabilities if we detect mouse on a touch device
        const oldCapabilities = this.capabilities;
        this.detectCapabilities();
        if (this.hasCapabilitiesChanged(oldCapabilities, this.capabilities)) {
          this.notifyListeners();
        }
      }
    };

    window.addEventListener("mousemove", handleMouseMove, { once: true });
  }

  private hasCapabilitiesChanged(
    old: DeviceCapabilities | null,
    current: DeviceCapabilities | null,
  ): boolean {
    if (!old || !current) return true;

    return (
      old.primaryInput !== current.primaryInput ||
      old.screenSize !== current.screenSize ||
      old.viewport.width !== current.viewport.width ||
      old.viewport.height !== current.viewport.height
    );
  }

  private notifyListeners(): void {
    if (this.capabilities) {
      const capabilities = this.capabilities; // Capture for closure
      this.listeners.forEach((callback) => callback(capabilities));
    }
  }

  // Cleanup method for proper disposal
  public dispose(): void {
    this.listeners = [];
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
  }

  private detectHDRSupport(): boolean {
    // Check for HDR support using media queries
    if (typeof window !== "undefined" && window.matchMedia) {
      return (
        window.matchMedia("(dynamic-range: high)").matches ||
        window.matchMedia("(color-gamut: p3)").matches
      );
    }
    return false;
  }

  private estimateMemory(): number | undefined {
    // Use navigator.deviceMemory if available (Chrome)
    if ("deviceMemory" in navigator) {
      return (navigator as any).deviceMemory * 1024; // Convert GB to MB
    }

    // Fallback estimation based on other factors
    const hardwareConcurrency = navigator.hardwareConcurrency || 4;
    if (hardwareConcurrency >= 8) return 8192; // 8GB
    if (hardwareConcurrency >= 4) return 4096; // 4GB
    return 2048; // 2GB fallback
  }

  private detectConnectionSpeed(): "slow" | "medium" | "fast" | undefined {
    // Use navigator.connection if available
    if ("connection" in navigator) {
      const connection = (navigator as any).connection;
      if (connection.effectiveType) {
        switch (connection.effectiveType) {
          case "slow-2g":
          case "2g":
            return "slow";
          case "3g":
            return "medium";
          case "4g":
          default:
            return "fast";
        }
      }
    }
    return undefined;
  }
}
