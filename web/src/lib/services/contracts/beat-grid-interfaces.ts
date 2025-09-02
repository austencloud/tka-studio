/**
 * Beat Grid Service Interfaces
 *
 * Service contracts for handling grid drawing and grid mode operations.
 * Consolidates grid-related logic that was duplicated across
 * BeatRenderingService, GridOverlayService, and other services.
 */
import type {
  CombinedGridOptions,
  GridDrawOptions,
  GridMode,
  GridValidationResult,
} from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IBeatGridService {
  /**
   * Draw a single grid on canvas context
   * Consolidated from BeatRenderingService grid drawing logic
   */
  drawGrid(
    ctx: CanvasRenderingContext2D,
    gridMode: GridMode,
    options: GridDrawOptions
  ): void;

  /**
   * Apply combined grids to a canvas
   * Draws primary grid + overlay grid with different opacities
   */
  applyCombinedGrids(
    canvas: HTMLCanvasElement,
    options: CombinedGridOptions
  ): HTMLCanvasElement;

  /**
   * Get the opposite grid mode for combined grids
   * Diamond -> Box, Box -> Diamond
   */
  getOppositeGridMode(currentMode: GridMode): GridMode;

  /**
   * Determine grid mode from beat data
   * Analyzes beat content to determine appropriate grid
   */
  getGridModeForBeat(beatData: unknown): GridMode;

  /**
   * Draw grid points/intersections
   * For more advanced grid visualizations
   */
  drawGridPoints(
    ctx: CanvasRenderingContext2D,
    gridMode: GridMode,
    options: GridDrawOptions
  ): void;

  /**
   * Validate grid mode and options
   */
  validateGridOptions(
    gridMode: GridMode,
    options: GridDrawOptions
  ): GridValidationResult;

  /**
   * Get grid dimensions and calculations
   * Returns spacing, points, etc. for a grid
   */
  getGridMetrics(
    gridMode: GridMode,
    size: number
  ): {
    spacing: number;
    points: Array<{ x: number; y: number }>;
    lines: Array<{
      start: { x: number; y: number };
      end: { x: number; y: number };
    }>;
  };

  /**
   * Create grid as SVG string
   * For when you need SVG instead of canvas
   */
  createGridSVG(
    gridMode: GridMode,
    size: number,
    options?: GridDrawOptions
  ): string;

  /**
   * Get default grid options for mode
   */
  getDefaultGridOptions(gridMode: GridMode): GridDrawOptions;

  /**
   * Check if two grid modes are compatible for overlay
   */
  areGridModesCompatible(primary: GridMode, overlay: GridMode): boolean;
}
