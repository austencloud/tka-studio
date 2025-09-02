/**
 * Responsive Layout Service Interfaces
 *
 * Interfaces for responsive UI layout calculations, grid configuration,
 * and option picker layout management.
 */

// Import missing types
import type {
  LayoutCalculationParams,
  LayoutCalculationResult,
  OptionPickerGridConfiguration,
  ResponsiveLayoutConfig,
} from "$domain";

// ============================================================================
// LAYOUT TYPES
// ============================================================================

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IResponsiveLayoutService {
  /** Calculate optimal layout for given parameters */
  calculateLayout(params: LayoutCalculationParams): LayoutCalculationResult;

  /** Get grid configuration for specific dimensions */
  getGridConfiguration(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): OptionPickerGridConfiguration;

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
