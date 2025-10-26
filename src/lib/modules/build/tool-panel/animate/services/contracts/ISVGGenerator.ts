/**
 * SVG Generator Service Contract
 *
 * Handles generation of SVG strings for grid and prop staffs.
 */

import type { GridMode } from "$shared";

export interface PropSvgData {
  svg: string;
  width: number;
  height: number;
}

export interface ISVGGenerator {
  /**
   * Generate grid SVG
   * @param gridMode - Type of grid to generate (GridMode.DIAMOND or GridMode.BOX)
   */
  generateGridSvg(gridMode?: GridMode): string;

  /**
   * Generate blue prop SVG with dynamic prop type
   * @param propType - Type of prop to generate (default: "staff")
   * @returns PropSvgData with SVG string and viewBox dimensions
   */
  generateBluePropSvg(propType?: string): Promise<PropSvgData>;

  /**
   * Generate red prop SVG with dynamic prop type
   * @param propType - Type of prop to generate (default: "staff")
   * @returns PropSvgData with SVG string and viewBox dimensions
   */
  generateRedPropSvg(propType?: string): Promise<PropSvgData>;

  /**
   * Generate blue staff SVG
   * @deprecated Use generateBluePropSvg instead
   */
  generateBlueStaffSvg(): string;

  /**
   * Generate red staff SVG
   * @deprecated Use generateRedPropSvg instead
   */
  generateRedStaffSvg(): string;
}
