/**
 * Responsive Layout Service Interfaces
 *
 * Interfaces for responsive UI layout calculations, grid configuration,
 * and option picker layout management.
 */

// ============================================================================
// LAYOUT TYPES
// ============================================================================

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

export interface ResponsiveLayoutConfig {
  gridColumns: string;
  optionSize: string;
  gridGap: string;
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

export interface LayoutCalculationResult {
  optionsPerRow: number;
  optionSize: number;
  gridGap: string;
  gridColumns: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
  deviceType: string;
  containerAspect: string;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  layoutConfig: ResponsiveLayoutConfig;
}

// ============================================================================
// RESPONSIVE LAYOUT SERVICE
// ============================================================================

/**
 * Service for calculating responsive layouts for option pickers and grids
 */
export interface IResponsiveLayoutService {
  /** Calculate optimal layout for given parameters */
  calculateLayout(params: LayoutCalculationParams): LayoutCalculationResult;

  /** Get grid configuration for specific dimensions */
  getGridConfiguration(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): GridConfiguration;

  /** Calculate optimal item size for container */
  calculateOptimalItemSize(
    count: number,
    containerWidth: number,
    containerHeight: number,
    targetColumns?: number
  ): number;

  /** Get responsive layout configuration */
  getResponsiveConfig(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): ResponsiveLayoutConfig;

  /** Check if mobile layout should be used */
  shouldUseMobileLayout(
    containerWidth: number,
    isMobileUserAgent?: boolean
  ): boolean;
}
