/**
 * ScrollLayoutMetricsUtil - Advanced layout metrics calculation for scroll containers
 *
 * Extracted from OptionPickerScroll.svelte to provide reusable layout calculation logic.
 * Handles sophisticated device detection, foldable devices, and responsive layout calculations.
 */

import type { ResponsiveLayoutConfig } from "../config";
import type { FoldableDetectionResult } from "./deviceDetection";

// ===== Types =====
export interface LayoutMetrics {
  shouldUseCompactLayout: boolean;
  shouldUseMobileLayout: boolean;
  shouldUseTabletLayout: boolean;
  isFoldableDevice: boolean;
  isUnfoldedFoldable: boolean;
  shouldAdjustForFoldable: boolean;
  aspectRatio: number;
  isLandscape: boolean;
  isPortrait: boolean;
  effectiveScaleFactor: number;
  contentPadding: number;
  sectionSpacing: number;
}

export interface ScrollBehaviorConfig {
  smoothScrolling: boolean;
  scrollbarWidth: string;
  scrollbarOpacity: number;
}

export interface DeviceInfo {
  deviceType: string;
  isFoldable: boolean;
  foldableInfo: FoldableDetectionResult;
}

// ===== Main Utility Class =====
export class ScrollLayoutMetricsUtil {
  /**
   * Calculates sophisticated layout metrics based on container dimensions and device info
   */
  static calculateLayoutMetrics(
    containerWidth: number,
    containerHeight: number,
    deviceInfo: DeviceInfo,
    foldableInfo: FoldableDetectionResult,
    layoutConfig: ResponsiveLayoutConfig,
  ): LayoutMetrics {
    const metrics: LayoutMetrics = {
      shouldUseCompactLayout: containerHeight < 400,
      shouldUseMobileLayout:
        deviceInfo.deviceType === "mobile" ||
        deviceInfo.deviceType === "smallMobile",
      shouldUseTabletLayout: deviceInfo.deviceType === "tablet",
      isFoldableDevice: foldableInfo.isFoldable,
      isUnfoldedFoldable: foldableInfo.isFoldable && foldableInfo.isUnfolded,
      shouldAdjustForFoldable:
        foldableInfo.isFoldable && foldableInfo.foldableType === "zfold",
      aspectRatio: containerWidth / containerHeight,
      isLandscape: containerWidth > containerHeight,
      isPortrait: containerHeight > containerWidth,
      effectiveScaleFactor: layoutConfig.scaleFactor,
      contentPadding: 8,
      sectionSpacing: 12,
    };

    // Adjust metrics for foldable devices
    if (metrics.shouldAdjustForFoldable) {
      metrics.contentPadding = metrics.isUnfoldedFoldable ? 12 : 6;
      metrics.sectionSpacing = metrics.isUnfoldedFoldable ? 16 : 8;
    }

    // Adjust for mobile devices
    if (metrics.shouldUseMobileLayout) {
      metrics.contentPadding = 6;
      metrics.sectionSpacing = 8;
    }

    return metrics;
  }

  /**
   * Calculates scroll behavior configuration based on layout metrics
   */
  static calculateScrollBehavior(
    layoutMetrics: LayoutMetrics,
    foldableInfo: FoldableDetectionResult,
  ): ScrollBehaviorConfig {
    return {
      smoothScrolling:
        !layoutMetrics.shouldUseMobileLayout || foldableInfo.isUnfolded,
      scrollbarWidth: layoutMetrics.shouldUseMobileLayout ? "4px" : "8px",
      scrollbarOpacity: foldableInfo.isFoldable ? 0.3 : 0.2,
    };
  }

  /**
   * Generates CSS custom properties for layout metrics
   */
  static generateCSSProperties(
    layoutMetrics: LayoutMetrics,
    scrollBehavior: ScrollBehaviorConfig,
  ): Record<string, string | number> {
    return {
      "--scroll-width": scrollBehavior.scrollbarWidth,
      "--scroll-opacity": scrollBehavior.scrollbarOpacity,
      "--content-padding": `${layoutMetrics.contentPadding}px`,
      "--section-spacing": `${layoutMetrics.sectionSpacing}px`,
      "--scale-factor": layoutMetrics.effectiveScaleFactor,
    };
  }

  /**
   * Generates CSS classes based on layout metrics
   */
  static generateCSSClasses(
    layoutMetrics: LayoutMetrics,
    _foldableInfo: FoldableDetectionResult,
  ): string[] {
    const classes: string[] = [];

    if (layoutMetrics.shouldUseMobileLayout) classes.push("mobile");
    if (layoutMetrics.shouldUseTabletLayout) classes.push("tablet");
    if (layoutMetrics.isFoldableDevice) classes.push("foldable");
    if (layoutMetrics.isUnfoldedFoldable) classes.push("unfolded");
    if (layoutMetrics.shouldUseCompactLayout) classes.push("compact");
    if (layoutMetrics.isLandscape) classes.push("landscape");
    if (layoutMetrics.isPortrait) classes.push("portrait");

    return classes;
  }

  /**
   * Provides responsive breakpoint checks for advanced layouts
   */
  static getResponsiveBreakpoints(
    containerWidth: number,
    containerHeight: number,
  ): {
    isSmallMobile: boolean;
    isMobile: boolean;
    isTablet: boolean;
    isDesktop: boolean;
    isLargeDesktop: boolean;
    isVeryTall: boolean;
    isVeryWide: boolean;
  } {
    return {
      isSmallMobile: containerWidth <= 375,
      isMobile: containerWidth <= 480,
      isTablet: containerWidth <= 768,
      isDesktop: containerWidth <= 1280,
      isLargeDesktop: containerWidth > 1280,
      isVeryTall: containerHeight > containerWidth * 1.5,
      isVeryWide: containerWidth > containerHeight * 2,
    };
  }

  /**
   * Validates container dimensions and provides warnings for edge cases
   */
  static validateContainerDimensions(
    containerWidth: number,
    containerHeight: number,
  ): {
    isValid: boolean;
    warnings: string[];
    recommendations: string[];
  } {
    const warnings: string[] = [];
    const recommendations: string[] = [];
    let isValid = true;

    if (containerWidth <= 0 || containerHeight <= 0) {
      warnings.push("Container dimensions are not positive values");
      isValid = false;
    }

    if (containerWidth < 200) {
      warnings.push("Container width is very narrow");
      recommendations.push("Consider minimum width of 200px for usability");
    }

    if (containerHeight < 300) {
      warnings.push("Container height is very short");
      recommendations.push(
        "Consider minimum height of 300px for content visibility",
      );
    }

    if (containerWidth > 2000) {
      warnings.push("Container width is extremely wide");
      recommendations.push(
        "Consider maximum width constraints for optimal layout",
      );
    }

    const aspectRatio = containerWidth / containerHeight;
    if (aspectRatio > 3 || aspectRatio < 0.3) {
      warnings.push("Container has extreme aspect ratio");
      recommendations.push(
        "Consider more balanced aspect ratio for better user experience",
      );
    }

    return { isValid, warnings, recommendations };
  }
}

// ===== Convenience Functions =====

/**
 * Quick layout metrics calculation for simple use cases
 */
export function calculateQuickLayoutMetrics(
  containerWidth: number,
  containerHeight: number,
  deviceInfo: DeviceInfo,
  layoutConfig: ResponsiveLayoutConfig = {
    gridColumns: "repeat(4, minmax(0, 1fr))",
    optionSize: "100px",
    gridGap: "8px",
    gridClass: "",
    aspectClass: "",
    scaleFactor: 1.0,
  },
): {
  metrics: LayoutMetrics;
  scrollBehavior: ScrollBehaviorConfig;
  cssProperties: Record<string, string | number>;
  cssClasses: string[];
} {
  const metrics = ScrollLayoutMetricsUtil.calculateLayoutMetrics(
    containerWidth,
    containerHeight,
    deviceInfo,
    deviceInfo.foldableInfo,
    layoutConfig,
  );

  const scrollBehavior = ScrollLayoutMetricsUtil.calculateScrollBehavior(
    metrics,
    deviceInfo.foldableInfo,
  );

  const cssProperties = ScrollLayoutMetricsUtil.generateCSSProperties(
    metrics,
    scrollBehavior,
  );
  const cssClasses = ScrollLayoutMetricsUtil.generateCSSClasses(
    metrics,
    deviceInfo.foldableInfo,
  );

  return {
    metrics,
    scrollBehavior,
    cssProperties,
    cssClasses,
  };
}

/**
 * Creates a reactive layout metrics calculator using Svelte runes
 */
export function createLayoutMetricsCalculator(
  containerWidth: () => number,
  containerHeight: () => number,
  deviceInfo: () => DeviceInfo,
  layoutConfig: () => ResponsiveLayoutConfig,
) {
  return {
    get metrics() {
      return ScrollLayoutMetricsUtil.calculateLayoutMetrics(
        containerWidth(),
        containerHeight(),
        deviceInfo(),
        deviceInfo().foldableInfo,
        layoutConfig(),
      );
    },
    get scrollBehavior() {
      const metrics = ScrollLayoutMetricsUtil.calculateLayoutMetrics(
        containerWidth(),
        containerHeight(),
        deviceInfo(),
        deviceInfo().foldableInfo,
        layoutConfig(),
      );
      return ScrollLayoutMetricsUtil.calculateScrollBehavior(
        metrics,
        deviceInfo().foldableInfo,
      );
    },
    get cssProperties() {
      const metrics = ScrollLayoutMetricsUtil.calculateLayoutMetrics(
        containerWidth(),
        containerHeight(),
        deviceInfo(),
        deviceInfo().foldableInfo,
        layoutConfig(),
      );
      const scrollBehavior = ScrollLayoutMetricsUtil.calculateScrollBehavior(
        metrics,
        deviceInfo().foldableInfo,
      );
      return ScrollLayoutMetricsUtil.generateCSSProperties(
        metrics,
        scrollBehavior,
      );
    },
    get cssClasses() {
      const metrics = ScrollLayoutMetricsUtil.calculateLayoutMetrics(
        containerWidth(),
        containerHeight(),
        deviceInfo(),
        deviceInfo().foldableInfo,
        layoutConfig(),
      );
      return ScrollLayoutMetricsUtil.generateCSSClasses(
        metrics,
        deviceInfo().foldableInfo,
      );
    },
  };
}
