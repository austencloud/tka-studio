/**
 * Arrow Grid Coordinate Service
 *
 * Uses the grid module's coordinate system instead of duplicating data.
 * Provides arrow-specific coordinate functionality using the authoritative grid data.
 */

import { GridLocation, GridMode, type MotionData } from "$shared";
import { Point } from "fabric";
import { injectable } from "inversify";
import { createGridPointData } from "../../../../grid/utils/grid-coordinate-utils";

export interface IArrowGridCoordinateService {
  getInitialPosition(motion: MotionData, location: GridLocation): Point;
  getSceneCenter(): Point;
  getSceneDimensions(): [number, number];
  validateCoordinates(point: Point): boolean;
  getAllHandPoints(gridMode?: GridMode): Partial<Record<GridLocation, Point>>;
  getAllLayer2Points(gridMode?: GridMode): Partial<Record<GridLocation, Point>>;
  getSupportedLocations(): GridLocation[];
}

@injectable()
export class ArrowGridCoordinateService implements IArrowGridCoordinateService {
  // Scene dimensions from grid module
  private readonly SCENE_SIZE = 950;
  private readonly CENTER_X = 475.0;
  private readonly CENTER_Y = 475.0;

  getInitialPosition(motion: MotionData, location: GridLocation): Point {
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
    return new Point(this.CENTER_X, this.CENTER_Y);
  }

  getSceneDimensions(): [number, number] {
    return [this.SCENE_SIZE, this.SCENE_SIZE];
  }

  validateCoordinates(point: Point): boolean {
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

  getAllHandPoints(gridMode: GridMode = GridMode.DIAMOND): Partial<Record<GridLocation, Point>> {
    const gridData = createGridPointData(gridMode);
    const handPoints: Partial<Record<GridLocation, Point>> = {};

    // Map grid coordinate keys to GridLocation enum
    const locationMap: Record<string, GridLocation> = {
      'n_diamond_hand_point': GridLocation.NORTH,
      'e_diamond_hand_point': GridLocation.EAST,
      's_diamond_hand_point': GridLocation.SOUTH,
      'w_diamond_hand_point': GridLocation.WEST,
      'ne_box_hand_point': GridLocation.NORTHEAST,
      'se_box_hand_point': GridLocation.SOUTHEAST,
      'sw_box_hand_point': GridLocation.SOUTHWEST,
      'nw_box_hand_point': GridLocation.NORTHWEST,
    };

    // Extract hand points from grid data
    Object.entries(gridData.allHandPointsNormal).forEach(([key, value]) => {
      const location = locationMap[key];
      if (location && value.coordinates) {
        handPoints[location] = new Point(value.coordinates.x, value.coordinates.y);
      }
    });

    return handPoints;
  }

  getAllLayer2Points(gridMode: GridMode = GridMode.DIAMOND): Partial<Record<GridLocation, Point>> {
    const gridData = createGridPointData(gridMode);
    const layer2Points: Partial<Record<GridLocation, Point>> = {};

    // For diamond mode, layer2 points are diagonal positions
    if (gridMode === GridMode.DIAMOND) {
      // Diamond layer2 points map to diagonal positions
      layer2Points[GridLocation.NORTHEAST] = new Point(618.1, 331.9);
      layer2Points[GridLocation.SOUTHEAST] = new Point(618.1, 618.1);
      layer2Points[GridLocation.SOUTHWEST] = new Point(331.9, 618.1);
      layer2Points[GridLocation.NORTHWEST] = new Point(331.9, 331.9);
      
      // For cardinal directions, map to nearest diagonal
      layer2Points[GridLocation.NORTH] = layer2Points[GridLocation.NORTHEAST];
      layer2Points[GridLocation.EAST] = layer2Points[GridLocation.SOUTHEAST];
      layer2Points[GridLocation.SOUTH] = layer2Points[GridLocation.SOUTHWEST];
      layer2Points[GridLocation.WEST] = layer2Points[GridLocation.NORTHWEST];
    } else {
      // For box mode, use actual layer2 points from grid data
      const locationMap: Record<string, GridLocation> = {
        'n_box_layer2_point': GridLocation.NORTH,
        'e_box_layer2_point': GridLocation.EAST,
        's_box_layer2_point': GridLocation.SOUTH,
        'w_box_layer2_point': GridLocation.WEST,
      };

      Object.entries(gridData.allLayer2PointsNormal).forEach(([key, value]) => {
        const location = locationMap[key];
        if (location && value.coordinates) {
          layer2Points[location] = new Point(value.coordinates.x, value.coordinates.y);
        }
      });
    }

    return layer2Points;
  }

  getSupportedLocations(): GridLocation[] {
    return [
      GridLocation.NORTH,
      GridLocation.EAST,
      GridLocation.SOUTH,
      GridLocation.WEST,
      GridLocation.NORTHEAST,
      GridLocation.SOUTHEAST,
      GridLocation.SOUTHWEST,
      GridLocation.NORTHWEST,
    ];
  }

  private getLayer2Coords(location: GridLocation): Point {
    const layer2Points = this.getAllLayer2Points();
    const coords = layer2Points[location];
    if (!coords) {
      console.warn(`No layer2 coordinates for location: ${location}, using center`);
      return this.getSceneCenter();
    }
    return coords;
  }

  private getHandPointCoords(location: GridLocation): Point {
    const handPoints = this.getAllHandPoints();
    const coords = handPoints[location];
    if (!coords) {
      console.warn(`No hand point coordinates for location: ${location}, using center`);
      return this.getSceneCenter();
    }
    return coords;
  }
}
