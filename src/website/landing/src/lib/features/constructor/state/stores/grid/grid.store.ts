/**
 * Grid Store
 *
 * This store manages the state of the grid in the application.
 */

import { createStore } from '../state/core.js';
import type { GridData, GridMode, GridPoint, Coordinate } from '../components/objects/Grid/types.js';
import { parseGridCoordinates } from '../components/objects/Grid/gridUtils.js';

// Define the store state interface
export interface GridStoreState {
  status: 'idle' | 'loading' | 'loaded' | 'error';
  mode: GridMode;
  data: GridData | null;
  error: Error | null;
  debugMode: boolean;
}

// Initial state
const initialState: GridStoreState = {
  status: 'idle',
  mode: 'diamond',
  data: null,
  error: null,
  debugMode: false
};

// Create the store
export const gridStore = createStore<GridStoreState, {
  setMode: (mode: GridMode) => void;
  loadData: (mode?: GridMode) => Promise<void>;
  setDebugMode: (enabled: boolean) => void;
  findClosestPoint: (
    coords: Coordinate,
    pointType?: 'hand' | 'layer2' | 'outer' | 'all',
    variant?: 'normal' | 'strict'
  ) => GridPoint | null;
  getPointByKey: (key: string) => GridPoint | null;
}>(
  'grid',
  initialState,
  (set, update, get) => {
    return {
      setMode: (mode: GridMode) => {
        update(state => ({
          ...state,
          mode
        }));
      },

      loadData: async (mode?: GridMode) => {
        // Use provided mode or current mode
        const gridMode = mode || get().mode;

        // Update mode if provided
        if (mode) {
          update(state => ({
            ...state,
            mode: gridMode
          }));
        }

        // Set loading state
        update(state => ({
          ...state,
          status: 'loading',
          error: null
        }));

        try {
          // Parse the grid coordinates based on the mode
          const parsedData = parseGridCoordinates(gridMode);

          // Artificial delay for demo purposes (remove in production)
          await new Promise(resolve => setTimeout(resolve, 100));

          // Set loaded state with data
          update(state => ({
            ...state,
            status: 'loaded',
            data: parsedData,
            error: null
          }));
        } catch (error) {
          console.error(`Failed to load grid data for mode ${gridMode}:`, error);

          update(state => ({
            ...state,
            status: 'error',
            error: error instanceof Error ? error : new Error('Unknown error loading grid data')
          }));
        }
      },

      setDebugMode: (enabled: boolean) => {
        update(state => ({
          ...state,
          debugMode: enabled
        }));
      },

      findClosestPoint: (
        coords: Coordinate,
        pointType: 'hand' | 'layer2' | 'outer' | 'all' = 'hand',
        variant: 'normal' | 'strict' = 'normal'
      ): GridPoint | null => {
        const state = get();
        if (state.status !== 'loaded' || !state.data) return null;

        const data = state.data;
        let points: GridPoint[] = [];

        // Collect points based on type
        if (pointType === 'hand' || pointType === 'all') {
          points = [...points, ...Object.values(data.handPoints[variant])];
        }

        if (pointType === 'layer2' || pointType === 'all') {
          points = [...points, ...Object.values(data.layer2Points[variant])];
        }

        if (pointType === 'outer' || pointType === 'all') {
          points = [...points, ...Object.values(data.outerPoints)];
        }

        if (points.length === 0) return null;

        // Find closest point
        let closestPoint = points[0];
        let minDistance = calculateDistance(coords, closestPoint.coordinates);

        for (let i = 1; i < points.length; i++) {
          const distance = calculateDistance(coords, points[i].coordinates);
          if (distance < minDistance) {
            minDistance = distance;
            closestPoint = points[i];
          }
        }

        return closestPoint;
      },

      getPointByKey: (key: string): GridPoint | null => {
        const state = get();
        if (state.status !== 'loaded' || !state.data) return null;

        const data = state.data;

        // Search through all point collections
        for (const variant of ['normal', 'strict'] as const) {
          // Check hand points
          if (data.handPoints[variant][key]) {
            return data.handPoints[variant][key];
          }

          // Check layer2 points
          if (data.layer2Points[variant][key]) {
            return data.layer2Points[variant][key];
          }
        }

        // Check outer points
        if (data.outerPoints[key]) {
          return data.outerPoints[key];
        }

        // Check if it's the center point
        if (key === 'center') {
          return data.centerPoint;
        }

        return null;
      }
    };
  },
  {
    persist: false,
    description: 'Manages the state of the grid in the application'
  }
);

// Helper function to calculate distance between two points
function calculateDistance(point1: Coordinate, point2: Coordinate): number {
  const dx = point1.x - point2.x;
  const dy = point1.y - point2.y;
  return Math.sqrt(dx * dx + dy * dy);
}
