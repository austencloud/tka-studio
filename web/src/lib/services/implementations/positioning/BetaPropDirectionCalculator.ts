/**
 * Beta Prop Direction Calculator
 *
 * Calculates movement directions for beta prop positioning based on legacy logic.
 * Ported from legacy_web BetaPropDirectionCalculator.ts
 */

import type { MotionData, PropPlacementData } from "$domain";
import { GridMode, Location, MotionType } from "$domain";

// Direction constants
export const UP = "up";
export const DOWN = "down";
export const LEFT = "left";
export const RIGHT = "right";
export const UPRIGHT = "upright";
export const DOWNRIGHT = "downright";
export const UPLEFT = "upleft";
export const DOWNLEFT = "downleft";

export type Direction =
  | typeof UP
  | typeof DOWN
  | typeof LEFT
  | typeof RIGHT
  | typeof UPRIGHT
  | typeof DOWNRIGHT
  | typeof UPLEFT
  | typeof DOWNLEFT;

// Use domain Location enum string values
type Loc = `${Location}`; // enum string values
type DiamondLoc =
  | Location.NORTH
  | Location.SOUTH
  | Location.EAST
  | Location.WEST;
type BoxLoc =
  | Location.NORTHEAST
  | Location.SOUTHEAST
  | Location.SOUTHWEST
  | Location.NORTHWEST;

// Color constants
export const RED = "red";
export const BLUE = "blue";
export type Color = typeof RED | typeof BLUE;

// Grid mode constants kept local (could import GridMode if needed)
const DIAMOND = GridMode.DIAMOND;
const BOX = GridMode.BOX;

export class BetaPropDirectionCalculator {
  // Diamond grid maps for static/dash motions
  private diamondMapRadial: Record<DiamondLoc, Record<Color, Direction>> = {
    [Location.NORTH]: { [RED]: RIGHT, [BLUE]: LEFT },
    [Location.EAST]: { [RED]: DOWN, [BLUE]: UP },
    [Location.SOUTH]: { [RED]: LEFT, [BLUE]: RIGHT },
    [Location.WEST]: { [RED]: UP, [BLUE]: DOWN },
  };

  private diamondMapNonRadial: Record<DiamondLoc, Record<Color, Direction>> = {
    [Location.NORTH]: { [RED]: UP, [BLUE]: DOWN },
    [Location.EAST]: { [RED]: RIGHT, [BLUE]: LEFT },
    [Location.SOUTH]: { [RED]: DOWN, [BLUE]: UP },
    [Location.WEST]: { [RED]: LEFT, [BLUE]: RIGHT },
  };

  // Box grid maps for static/dash motions
  private boxMapRadial: Record<BoxLoc, Record<Color, Direction>> = {
    [Location.NORTHEAST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
    [Location.SOUTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
    [Location.SOUTHWEST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
    [Location.NORTHWEST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
  };

  private boxMapNonRadial: Record<BoxLoc, Record<Color, Direction>> = {
    [Location.NORTHEAST]: { [RED]: UPLEFT, [BLUE]: DOWNRIGHT },
    [Location.SOUTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
    [Location.SOUTHWEST]: { [RED]: UPLEFT, [BLUE]: DOWNRIGHT },
    [Location.NORTHWEST]: { [RED]: DOWNLEFT, [BLUE]: UPRIGHT },
  };

  // Shift motion direction maps
  private directionMapRadialShift: Record<
    Loc,
    Partial<Record<Loc, Direction>>
  > = {
    [Location.EAST]: { [Location.NORTH]: RIGHT, [Location.SOUTH]: RIGHT },
    [Location.WEST]: { [Location.NORTH]: LEFT, [Location.SOUTH]: LEFT },
    [Location.NORTH]: { [Location.EAST]: UP, [Location.WEST]: UP },
    [Location.SOUTH]: { [Location.EAST]: DOWN, [Location.WEST]: DOWN },
    [Location.NORTHEAST]: {
      [Location.NORTHWEST]: UPRIGHT,
      [Location.SOUTHEAST]: UPRIGHT,
    },
    [Location.SOUTHEAST]: {
      [Location.NORTHEAST]: DOWNRIGHT,
      [Location.SOUTHWEST]: DOWNRIGHT,
    },
    [Location.SOUTHWEST]: {
      [Location.NORTHWEST]: DOWNLEFT,
      [Location.SOUTHEAST]: DOWNLEFT,
    },
    [Location.NORTHWEST]: {
      [Location.NORTHEAST]: UPLEFT,
      [Location.SOUTHWEST]: UPLEFT,
    },
  };

  private directionMapNonRadialShift: Record<
    Loc,
    Partial<Record<Loc, Direction>>
  > = {
    [Location.EAST]: { [Location.NORTH]: UP, [Location.SOUTH]: UP },
    [Location.WEST]: { [Location.NORTH]: DOWN, [Location.SOUTH]: DOWN },
    [Location.NORTH]: { [Location.EAST]: RIGHT, [Location.WEST]: RIGHT },
    [Location.SOUTH]: { [Location.EAST]: LEFT, [Location.WEST]: LEFT },
    [Location.NORTHEAST]: {
      [Location.SOUTHEAST]: UPLEFT,
      [Location.NORTHWEST]: DOWNRIGHT,
    },
    [Location.SOUTHEAST]: {
      [Location.NORTHEAST]: UPRIGHT,
      [Location.SOUTHWEST]: UPRIGHT,
    },
    [Location.SOUTHWEST]: {
      [Location.NORTHWEST]: UPLEFT,
      [Location.SOUTHEAST]: DOWNRIGHT,
    },
    [Location.NORTHWEST]: {
      [Location.NORTHEAST]: DOWNLEFT,
      [Location.SOUTHWEST]: DOWNLEFT,
    },
  };

  constructor(private motionDataSet: { red: MotionData; blue: MotionData }) {}

  /**
   * Get motion data for a prop by matching its context
   * Since we removed prop.color, we need to determine which motion to use
   * This is a transitional approach - ideally services should be passed the specific motion directly
   */
  private getMotionDataForProp(_prop: PropPlacementData): MotionData | null {
    // For now, we'll need to determine this based on how the service is called
    // This is not ideal but maintains functionality during the transition
    // In the future, services should be passed the specific motion data directly

    // Try to match based on prop properties with motion properties
    // This is a heuristic approach during the transition
    const blueMotion = this.motionDataSet.blue;
    const redMotion = this.motionDataSet.red;

    // For now, assume blue if we can't determine otherwise
    // This will need to be fixed by passing proper context to the service
    return blueMotion || redMotion;
  }

  /**
   * Get direction for a prop based on its motion data
   */
  getDirection(prop: PropPlacementData): Direction | null {
    // Get the appropriate motion data for this prop
    const motionData = this.getMotionDataForProp(prop);
    if (!motionData) {
      console.error(`No motion data found for prop`);
      return null;
    }

    return this.getDirectionForMotionData(motionData);
  }

  /**
   * Get direction based on motion data directly (bypasses prop matching)
   */
  getDirectionForMotionData(motionData: MotionData): Direction | null {
    if (!motionData) {
      return null;
    }

    // Handle shift motions (pro, anti, float)
    if (
      [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT].includes(
        motionData.motionType
      )
    ) {
      return this.handleShiftMotionForData(motionData);
    }

    // Handle static/dash motions
    return this.handleStaticDashMotionForData(motionData);
  }

  /**
   * Handle shift motion direction calculation
   */
  private handleShiftMotion(
    _prop: PropPlacementData,
    motionData: MotionData
  ): Direction | null {
    return this.handleShiftMotionForData(motionData);
  }

  /**
   * Handle shift motion direction calculation for motion data directly
   */
  private handleShiftMotionForData(motionData: MotionData): Direction | null {
    const isRadial = this.endsWithRadialOrientation();
    const startLocation =
      (
        motionData as unknown as {
          startLocation?: string;
          start_location?: string;
        }
      ).startLocation ??
      (motionData as unknown as { start_location?: string }).start_location ??
      "";
    const endLocation =
      (motionData as unknown as { endLocation?: string; end_location?: string })
        .endLocation ??
      (motionData as unknown as { end_location?: string }).end_location ??
      "";
    return this.getShiftDirection(isRadial, startLocation, endLocation);
  }

  /**
   * Get shift direction based on start and end locations
   */
  private getShiftDirection(
    isRadial: boolean,
    startLocation: string,
    endLocation: string
  ): Direction | null {
    const map = isRadial
      ? this.directionMapRadialShift
      : this.directionMapNonRadialShift;
    return map[startLocation as Loc]?.[endLocation as Loc] ?? null;
  }

  /**
   * Handle static/dash motion direction calculation
   */
  private handleStaticDashMotion(
    _prop: PropPlacementData,
    motionData: MotionData
  ): Direction | null {
    return this.handleStaticDashMotionForData(motionData);
  }

  /**
   * Handle static/dash motion direction calculation for motion data directly
   */
  private handleStaticDashMotionForData(
    motionData: MotionData
  ): Direction | null {
    const location = motionData.endLocation as Loc;
    const cardinalValues = [
      Location.NORTH,
      Location.SOUTH,
      Location.EAST,
      Location.WEST,
    ] as string[];
    const gridMode = cardinalValues.includes(location) ? DIAMOND : BOX;
    const isRadial = this.endsWithRadialOrientation();

    if (gridMode === DIAMOND) {
      const map = isRadial ? this.diamondMapRadial : this.diamondMapNonRadial;
      return map[location as DiamondLoc]?.[motionData.color as Color] ?? null;
    }

    const map = isRadial ? this.boxMapRadial : this.boxMapNonRadial;
    return map[location as BoxLoc]?.[motionData.color as Color] ?? null;
  }

  /**
   * Get opposite direction
   */
  getOppositeDirection(direction: Direction): Direction {
    const opposites: Record<Direction, Direction> = {
      [UP]: DOWN,
      [DOWN]: UP,
      [LEFT]: RIGHT,
      [RIGHT]: LEFT,
      [UPRIGHT]: DOWNLEFT,
      [DOWNLEFT]: UPRIGHT,
      [UPLEFT]: DOWNRIGHT,
      [DOWNRIGHT]: UPLEFT,
    };
    return opposites[direction];
  }

  /**
   * Check if motion ends with radial orientation
   * This needs to be passed in from the test or determined by context
   */
  private endsWithRadialOrientation(): boolean {
    // ✅ FIXED: Simplified orientation access using MotionData
    const redEndOri = this.motionDataSet.red?.endOrientation;
    const blueEndOri = this.motionDataSet.blue?.endOrientation;
    if (redEndOri === "in" && blueEndOri === "in") return true;
    if (redEndOri === "out" && blueEndOri === "out") return false;
    return true;
  }
}
