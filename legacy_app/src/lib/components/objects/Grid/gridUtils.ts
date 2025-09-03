/**
 * Grid Utilities
 *
 * This file contains utility functions for working with grids.
 */

import type { GridData, GridMode, GridPoint, Coordinate } from './types';

/**
 * Parse grid coordinates based on the specified mode
 *
 * @param mode The grid mode to parse coordinates for
 * @returns The parsed grid data
 */
export function parseGridCoordinates(mode: GridMode): GridData {
  // This is a simplified implementation
  // In a real application, this would parse actual grid data

  // Create a grid with points based on the mode
  const centerPoint: GridPoint = {
    coordinates: { x: 0, y: 0 },
    id: 'center',
    type: 'center',
    variant: 'none'
  };

  const handPoints: Record<'normal' | 'strict', Record<string, GridPoint>> = {
    normal: {},
    strict: {}
  };

  const layer2Points: Record<'normal' | 'strict', Record<string, GridPoint>> = {
    normal: {},
    strict: {}
  };

  const outerPoints: Record<string, GridPoint> = {};

  // Generate points based on mode
  if (mode === 'diamond') {
    // Diamond grid has points at 45, 135, 225, and 315 degrees
    handPoints.normal['top_right'] = createGridPoint(100, -100, 'top_right', 'hand', 'normal');
    handPoints.normal['bottom_right'] = createGridPoint(100, 100, 'bottom_right', 'hand', 'normal');
    handPoints.normal['bottom_left'] = createGridPoint(-100, 100, 'bottom_left', 'hand', 'normal');
    handPoints.normal['top_left'] = createGridPoint(-100, -100, 'top_left', 'hand', 'normal');

    // Strict points are slightly offset
    handPoints.strict['top_right'] = createGridPoint(90, -90, 'top_right', 'hand', 'strict');
    handPoints.strict['bottom_right'] = createGridPoint(90, 90, 'bottom_right', 'hand', 'strict');
    handPoints.strict['bottom_left'] = createGridPoint(-90, 90, 'bottom_left', 'hand', 'strict');
    handPoints.strict['top_left'] = createGridPoint(-90, -90, 'top_left', 'hand', 'strict');

    // Layer 2 points
    layer2Points.normal['far_right'] = createGridPoint(150, 0, 'far_right', 'layer2', 'normal');
    layer2Points.normal['far_bottom'] = createGridPoint(0, 150, 'far_bottom', 'layer2', 'normal');
    layer2Points.normal['far_left'] = createGridPoint(-150, 0, 'far_left', 'layer2', 'normal');
    layer2Points.normal['far_top'] = createGridPoint(0, -150, 'far_top', 'layer2', 'normal');

    // Outer points
    outerPoints['outer_right'] = createGridPoint(200, 0, 'outer_right', 'outer', 'none');
    outerPoints['outer_bottom'] = createGridPoint(0, 200, 'outer_bottom', 'outer', 'none');
    outerPoints['outer_left'] = createGridPoint(-200, 0, 'outer_left', 'outer', 'none');
    outerPoints['outer_top'] = createGridPoint(0, -200, 'outer_top', 'outer', 'none');
  } else {
    // Box grid has points at 0, 90, 180, and 270 degrees
    handPoints.normal['right'] = createGridPoint(100, 0, 'right', 'hand', 'normal');
    handPoints.normal['bottom'] = createGridPoint(0, 100, 'bottom', 'hand', 'normal');
    handPoints.normal['left'] = createGridPoint(-100, 0, 'left', 'hand', 'normal');
    handPoints.normal['top'] = createGridPoint(0, -100, 'top', 'hand', 'normal');

    // Strict points are slightly offset
    handPoints.strict['right'] = createGridPoint(90, 0, 'right', 'hand', 'strict');
    handPoints.strict['bottom'] = createGridPoint(0, 90, 'bottom', 'hand', 'strict');
    handPoints.strict['left'] = createGridPoint(-90, 0, 'left', 'hand', 'strict');
    handPoints.strict['top'] = createGridPoint(0, -90, 'top', 'hand', 'strict');

    // Layer 2 points
    layer2Points.normal['top_right'] = createGridPoint(100, -100, 'top_right', 'layer2', 'normal');
    layer2Points.normal['bottom_right'] = createGridPoint(100, 100, 'bottom_right', 'layer2', 'normal');
    layer2Points.normal['bottom_left'] = createGridPoint(-100, 100, 'bottom_left', 'layer2', 'normal');
    layer2Points.normal['top_left'] = createGridPoint(-100, -100, 'top_left', 'layer2', 'normal');

    // Outer points
    outerPoints['outer_right'] = createGridPoint(200, 0, 'outer_right', 'outer', 'none');
    outerPoints['outer_bottom'] = createGridPoint(0, 200, 'outer_bottom', 'outer', 'none');
    outerPoints['outer_left'] = createGridPoint(-200, 0, 'outer_left', 'outer', 'none');
    outerPoints['outer_top'] = createGridPoint(0, -200, 'outer_top', 'outer', 'none');
  }

  return {
    handPoints,
    layer2Points,
    outerPoints,
    centerPoint,
    mode
  };
}

/**
 * Create a grid point
 *
 * @param x X coordinate
 * @param y Y coordinate
 * @param id Point identifier
 * @param type Point type
 * @param variant Point variant
 * @returns A grid point
 */
function createGridPoint(
  x: number,
  y: number,
  id: string,
  type: 'hand' | 'layer2' | 'outer' | 'center',
  variant: 'normal' | 'strict' | 'none'
): GridPoint {
  return {
    coordinates: { x, y },
    id,
    type,
    variant
  };
}
