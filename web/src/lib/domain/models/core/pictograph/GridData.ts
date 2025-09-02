/**
 * Grid Domain Model
 *
 * Immutable data for the pictograph grid system.
 * Based on modern desktop app's gridData.py
 */

import { GridMode, type GridPointData } from "$domain";

export interface GridData {
  readonly gridMode: GridMode;
  readonly centerX: number;
  readonly centerY: number;
  readonly radius: number;
  readonly gridPointData: GridPointData; //
}

export function createGridData(data: Partial<GridData> = {}): GridData {
  return {
    gridMode: data.gridMode ?? GridMode.DIAMOND,
    centerX: data.centerX ?? 0.0,
    centerY: data.centerY ?? 0.0,
    radius: data.radius ?? 100.0,
    gridPointData: data.gridPointData ?? {
      allHandPointsStrict: {},
      allHandPointsNormal: {},
      allLayer2PointsStrict: {},
      allLayer2PointsNormal: {},
      allOuterPoints: {},
      centerPoint: { coordinates: { x: 0, y: 0 } },
    },
  };
}

export function updateGridData(
  grid: GridData,
  updates: Partial<GridData>
): GridData {
  return {
    ...grid,
    ...updates,
  };
}

export function gridDataToObject(grid: GridData): Record<string, unknown> {
  return {
    gridMode: grid.gridMode,
    centerX: grid.centerX,
    centerY: grid.centerY,
    radius: grid.radius,
    gridPoints: grid.gridPointData,
  };
}

export function gridDataFromObject(data: Record<string, unknown>): GridData {
  const gridData: Record<string, unknown> = {};

  if (data.gridMode !== undefined) {
    gridData.gridMode = data.gridMode;
  }
  if (data.centerX !== undefined) {
    gridData.centerX = data.centerX;
  }
  if (data.centerY !== undefined) {
    gridData.centerY = data.centerY;
  }
  if (data.radius !== undefined) {
    gridData.radius = data.radius;
  }
  if (data.gridPoints !== undefined) {
    gridData.gridPoints = data.gridPoints;
  }

  return createGridData(gridData as Partial<GridData>);
}

// Canvas-based grid drawing options (for BeatGridService)
export interface GridDrawOptions {
  size?: number; // Grid size for canvas drawing
  opacity?: number; // Grid opacity (0-1)
  lineWidth?: number; // Line width for grid lines
  strokeStyle?: string; // Line color/style
  padding?: number; // Padding around grid
}

// Combined grid options for overlay rendering
export interface CombinedGridOptions {
  primaryGridMode: GridMode; // Primary grid type
  overlayGridMode?: GridMode; // Optional overlay grid type
  primaryOpacity?: number; // Primary grid opacity
  overlayOpacity?: number; // Overlay grid opacity
}

// Legacy generic grid display options (kept for backward compatibility)
export interface GenericGridDisplayOptions {
  showGrid: boolean;
  gridColor: string;
  gridOpacity: number;
  showLabels: boolean;
  labelColor: string;
  labelSize: number;
}

export interface GridValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}
