/**
 * Coordinate type representing a point in 2D space
 */
export interface Coordinate {
    x: number;
    y: number;
  }

  /**
   * Grid point with additional metadata
   */
  export interface GridPoint {
    coordinates: Coordinate;
    id: string;
    type: 'hand' | 'layer2' | 'outer' | 'center';
    variant: 'normal' | 'strict' | 'none';
  }

  /**
   * Type of grid layout
   */
  export type GridMode = 'diamond' | 'box';

  /**
   * Grid data representing all points in a grid
   */
  export interface GridData {
    handPoints: {
      normal: Record<string, GridPoint>;
      strict: Record<string, GridPoint>;
    };
    layer2Points: {
      normal: Record<string, GridPoint>;
      strict: Record<string, GridPoint>;
    };
    outerPoints: Record<string, GridPoint>;
    centerPoint: GridPoint;
    mode: GridMode;
  }

  /**
   * Loading states for grid data
   */
  export type GridLoadingState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'error'; error: Error }
    | { status: 'loaded'; data: GridData };

  /**
   * Point finder function result
   */
  export interface PointFinderResult {
    point: GridPoint | null;
    distance: number;
    key: string | null;
  }
