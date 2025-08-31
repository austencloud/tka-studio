/**
 * Layout Domain Types
 *
 * Types for responsive UI layout calculations, grid configuration,
 * and layout management.
 */

export interface LayoutDimensions {
  width: number;
  height: number;
}

export interface GridConfiguration {
  columns: number;
  gap: string;
  itemSize: number;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

export interface LayoutCalculationParams {
  count: number;
  containerWidth: number;
  containerHeight: number;
  windowWidth?: number;
  windowHeight?: number;
  isMobileUserAgent?: boolean;
}
