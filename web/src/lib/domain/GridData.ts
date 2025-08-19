/**
 * Grid Domain Model
 *
 * Immutable data for the pictograph grid system.
 * Based on modern desktop app's gridData.py
 */

import { GridMode } from "./enums";

export interface GridData {
  readonly gridMode: GridMode;
  readonly center_x: number;
  readonly center_y: number;
  readonly radius: number;
  readonly grid_points: Record<string, [number, number]>; // [x, y] coordinates
}

export function createGridData(data: Partial<GridData> = {}): GridData {
  return {
    gridMode: data.gridMode ?? GridMode.DIAMOND,
    center_x: data.center_x ?? 0.0,
    center_y: data.center_y ?? 0.0,
    radius: data.radius ?? 100.0,
    grid_points: data.grid_points ?? {},
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
    center_x: grid.center_x,
    center_y: grid.center_y,
    radius: grid.radius,
    grid_points: grid.grid_points,
  };
}

export function gridDataFromObject(data: Record<string, unknown>): GridData {
  const gridData: Record<string, unknown> = {};

  if (data.gridMode !== undefined) {
    gridData.gridMode = data.gridMode;
  }
  if (data.center_x !== undefined) {
    gridData.center_x = data.center_x;
  }
  if (data.center_y !== undefined) {
    gridData.center_y = data.center_y;
  }
  if (data.radius !== undefined) {
    gridData.radius = data.radius;
  }
  if (data.grid_points !== undefined) {
    gridData.grid_points = data.grid_points;
  }

  return createGridData(gridData as Partial<GridData>);
}
