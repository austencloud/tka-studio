/**
 * Arrow Coordinate System Service
 *
 * Pure service for managing coordinate systems and initial position calculations.
 * Direct TypeScript port of the Python ArrowCoordinateSystemService.
 *
 * This service handles:
 * - Scene coordinate system management (950x950 scene with center at 475,475)
 * - Hand point coordinates (for STATIC/DASH arrows)
 * - Layer2 point coordinates (for PRO/ANTI/FLOAT arrows)
 * - Initial position computation based on motion type
 *
 * No UI dependencies, completely testable in isolation.
 */

import type { MotionData } from "$lib/domain";
import { Location } from "$lib/domain";
import type { Point } from "../../types";
import { injectable } from "inversify";

export interface IArrowCoordinateSystemService {
  getInitialPosition(motion: MotionData, location: Location): Point;
  getSceneCenter(): Point;
  getSceneDimensions(): [number, number];
  getCoordinateInfo(location: Location): Record<string, unknown>;
  validateCoordinates(point: Point): boolean;
  getAllHandPoints(): Record<Location, Point>;
  getAllLayer2Points(): Record<Location, Point>;
  getSupportedLocations(): Location[];
}

@injectable()
export class ArrowCoordinateSystemService
  implements IArrowCoordinateSystemService
{
  /**
   * Pure service for coordinate system management and initial position calculation.
   *
   * Manages the TKA coordinate systems without any UI dependencies.
   * Provides precise coordinate mappings for different arrow types.
   */

  // Scene dimensions: 950x950 scene with center at (475, 475)
  private readonly SCENE_SIZE = 950;
  private readonly CENTER_X = 475.0;
  private readonly CENTER_Y = 475.0;

  // Hand point coordinates (for STATIC/DASH arrows)
  // These are the inner grid positions where props are placed
  private readonly HAND_POINTS: Record<Location, Point> = {
    [Location.NORTH]: { x: 475.0, y: 331.9 },
    [Location.EAST]: { x: 618.1, y: 475.0 },
    [Location.SOUTH]: { x: 475.0, y: 618.1 },
    [Location.WEST]: { x: 331.9, y: 475.0 },
    // Diagonal hand points (calculated from radius)
    [Location.NORTHEAST]: { x: 618.1, y: 331.9 },
    [Location.SOUTHEAST]: { x: 618.1, y: 618.1 },
    [Location.SOUTHWEST]: { x: 331.9, y: 618.1 },
    [Location.NORTHWEST]: { x: 331.9, y: 331.9 },
  };

  // Layer2 point coordinates (for PRO/ANTI/FLOAT arrows)
  // Using DIAMOND layer2 points from circle_coords.json
  private readonly LAYER2_POINTS: Record<Location, Point> = {
    // Diamond layer2 points are diagonal positions
    [Location.NORTHEAST]: { x: 618.1, y: 331.9 },
    [Location.SOUTHEAST]: { x: 618.1, y: 618.1 },
    [Location.SOUTHWEST]: { x: 331.9, y: 618.1 },
    [Location.NORTHWEST]: { x: 331.9, y: 331.9 },
    // For cardinal directions, map to nearest diagonal
    [Location.NORTH]: { x: 618.1, y: 331.9 }, // Maps to NE
    [Location.EAST]: { x: 618.1, y: 618.1 }, // Maps to SE
    [Location.SOUTH]: { x: 331.9, y: 618.1 }, // Maps to SW
    [Location.WEST]: { x: 331.9, y: 331.9 }, // Maps to NW
  };

  getInitialPosition(motion: MotionData, location: Location): Point {
    /**
     * Get initial position coordinates based on motion type and location.
     *
     * Args:
     *     motion: Motion data to determine coordinate system (hand points vs layer2)
     *     location: Arrow location
     *
     * Returns:
     *     Point representing the initial position coordinates
     */
    const motionType = motion.motionType?.toLowerCase();

    if (["pro", "anti", "float"].includes(motionType || "")) {
      // Shift arrows use layer2 points
      return this.getLayer2Coords(location);
    } else if (["static", "dash"].includes(motionType || "")) {
      // Static/dash arrows use hand points
      return this.getHandPointCoords(location);
    } else {
      // Default fallback
      console.warn(`Unknown motion type: ${motionType}, using scene center`);
      return this.getSceneCenter();
    }
  }

  getSceneCenter(): Point {
    /**Get the center point of the scene coordinate system.*/
    return { x: this.CENTER_X, y: this.CENTER_Y };
  }

  private getLayer2Coords(location: Location): Point {
    /**Get layer2 point coordinates for shift arrows.*/
    const coords = this.LAYER2_POINTS[location];
    if (!coords) {
      console.warn(
        `No layer2 coordinates for location: ${location}, using center`
      );
      return this.getSceneCenter();
    }
    return coords;
  }

  private getHandPointCoords(location: Location): Point {
    /**Get hand point coordinates for static/dash arrows.*/
    const coords = this.HAND_POINTS[location];
    if (!coords) {
      console.warn(
        `No hand point coordinates for location: ${location}, using center`
      );
      return this.getSceneCenter();
    }
    return coords;
  }

  getSceneDimensions(): [number, number] {
    /**
     * Get the scene dimensions.
     *
     * Returns:
     *     Tuple of [width, height] for the scene
     */
    return [this.SCENE_SIZE, this.SCENE_SIZE];
  }

  getCoordinateInfo(location: Location): Record<string, unknown> {
    /**
     * Get detailed coordinate information for debugging.
     *
     * Args:
     *     location: Location to get coordinate info for
     *
     * Returns:
     *     Dictionary with coordinate details
     */
    const handPoint = this.HAND_POINTS[location];
    const layer2Point = this.LAYER2_POINTS[location];

    return {
      location: location,
      hand_point: {
        x: handPoint?.x || null,
        y: handPoint?.y || null,
      },
      layer2_point: {
        x: layer2Point?.x || null,
        y: layer2Point?.y || null,
      },
      scene_center: { x: this.CENTER_X, y: this.CENTER_Y },
      scene_size: this.SCENE_SIZE,
    };
  }

  validateCoordinates(point: Point): boolean {
    /**
     * Validate that coordinates are within scene bounds.
     *
     * Args:
     *     point: Point to validate
     *
     * Returns:
     *     True if point is within scene bounds
     */
    return (
      point &&
      typeof point.x === "number" &&
      typeof point.y === "number" &&
      point.x >= 0 &&
      point.x <= this.SCENE_SIZE &&
      point.y >= 0 &&
      point.y <= this.SCENE_SIZE
    );
  }

  getAllHandPoints(): Record<Location, Point> {
    /**Get all hand point coordinates.*/
    return { ...this.HAND_POINTS };
  }

  getAllLayer2Points(): Record<Location, Point> {
    /**Get all layer2 point coordinates.*/
    return { ...this.LAYER2_POINTS };
  }

  getSupportedLocations(): Location[] {
    /**Get list of supported location values.*/
    return [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
      Location.NORTHEAST,
      Location.SOUTHEAST,
      Location.SOUTHWEST,
      Location.NORTHWEST,
    ];
  }
}
