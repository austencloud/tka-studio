/**
 * Scroll layout metrics calculator for option picker
 */

export interface DeviceInfo {
  type: "mobile" | "tablet" | "desktop";
  deviceType: "mobile" | "tablet" | "desktop"; // Add for compatibility
  width: number;
  height: number;
  isFoldable: boolean;
}

export interface LayoutMetrics {
  itemSize: number;
  columns: number;
  rows: number;
  gap: number;
  padding: number;
  aspectRatio?: number;
  isLandscape?: boolean;
  shouldUseMobileLayout?: boolean;
  contentPadding?: number;
}

export interface ScrollBehaviorConfig {
  smoothScrolling: boolean;
  scrollThreshold: number;
  debounceMs: number;
}

export interface ScrollLayoutMetrics {
  containerHeight: number;
  itemHeight: number;
  visibleRows: number;
  totalRows: number;
  scrollableHeight: number;
}

/**
 * Create layout metrics calculator
 */
export function createLayoutMetricsCalculator() {
  return {
    // Add missing properties
    metrics: {} as LayoutMetrics,
    scrollBehavior: {} as ScrollBehaviorConfig,
    cssProperties: {} as Record<string, string>,
    cssClasses: {} as Record<string, string>,

    calculateScrollMetrics(
      itemCount: number,
      layout: LayoutMetrics,
      containerHeight: number
    ): ScrollLayoutMetrics {
      const totalRows = Math.ceil(itemCount / layout.columns);
      const itemHeight = layout.itemSize + layout.gap;
      const visibleRows = Math.floor(containerHeight / itemHeight);
      const scrollableHeight = Math.max(
        0,
        totalRows * itemHeight - containerHeight
      );

      return {
        containerHeight,
        itemHeight,
        visibleRows,
        totalRows,
        scrollableHeight,
      };
    },

    calculateOptimalLayout(
      deviceInfo: DeviceInfo,
      containerWidth: number,
      containerHeight: number
    ): LayoutMetrics {
      let columns = 2;
      let itemSize = 120;
      let gap = 8;
      let padding = 16;

      // Adjust based on device type
      switch (deviceInfo.type) {
        case "desktop":
          columns = 4;
          itemSize = 160;
          gap = 16;
          padding = 24;
          break;
        case "tablet":
          columns = 3;
          itemSize = 140;
          gap = 12;
          padding = 20;
          break;
        case "mobile":
        default:
          columns = 2;
          itemSize = 120;
          gap = 8;
          padding = 16;
          break;
      }

      // Adjust for container width
      const availableWidth = containerWidth - padding * 2 - gap * (columns - 1);
      const calculatedItemSize = Math.floor(availableWidth / columns);

      if (calculatedItemSize < itemSize) {
        itemSize = calculatedItemSize;
      }

      const rows = Math.ceil(100 / columns); // Assume 100 items for calculation

      return {
        itemSize,
        columns,
        rows,
        gap,
        padding,
      };
    },
  };
}
