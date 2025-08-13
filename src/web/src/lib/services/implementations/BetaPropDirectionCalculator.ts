/**
 * Beta Prop Direction Calculator
 *
 * Calculates movement directions for beta prop positioning based on legacy logic.
 * Ported from legacy_web BetaPropDirectionCalculator.ts
 */

import type { MotionData, PropData } from "$lib/domain";
import { Location, MotionType } from "$lib/domain/enums";

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
const DIAMOND = "diamond";
const BOX = "box";

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

  constructor(private motionData: { red: MotionData; blue: MotionData }) {}

  /**
   * Get direction for a prop based on its motion data and color
   */
  getDirection(prop: PropData): Direction | null {
    const motionData =
      prop.color === "red" ? this.motionData.red : this.motionData.blue;
    if (!motionData) {
      console.error(`No motion data found for ${prop.color} prop`);
      return null;
    }

    // Handle shift motions (pro, anti, float)
    if (
      [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT].includes(
        motionData.motion_type,
      )
    ) {
      return this.handleShiftMotion(prop, motionData);
    }

    // Handle static/dash motions
    return this.handleStaticDashMotion(prop);
  }

  /**
   * Handle shift motion direction calculation
   */
  private handleShiftMotion(
    _prop: PropData,
    motionData: MotionData,
  ): Direction | null {
    const isRadial = this.endsWithRadialOrientation();
    const startLoc =
      (motionData as unknown as { start_loc?: string; start_location?: string })
        .start_loc ??
      (motionData as unknown as { start_location?: string }).start_location ??
      "";
    const endLoc =
      (motionData as unknown as { end_loc?: string; end_location?: string })
        .end_loc ??
      (motionData as unknown as { end_location?: string }).end_location ??
      "";
    return this.getShiftDirection(isRadial, startLoc, endLoc);
  }

  /**
   * Get shift direction based on start and end locations
   */
  private getShiftDirection(
    isRadial: boolean,
    startLoc: string,
    endLoc: string,
  ): Direction | null {
    const map = isRadial
      ? this.directionMapRadialShift
      : this.directionMapNonRadialShift;
    return map[startLoc as Loc]?.[endLoc as Loc] ?? null;
  }

  /**
   * Handle static/dash motion direction calculation
   */
  private handleStaticDashMotion(prop: PropData): Direction | null {
    const location = (prop.location || "") as Loc;
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
      return map[location as DiamondLoc]?.[prop.color as Color] ?? null;
    }

    const map = isRadial ? this.boxMapRadial : this.boxMapNonRadial;
    return map[location as BoxLoc]?.[prop.color as Color] ?? null;
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
    const redEndOri =
      (
        this.motionData.red as unknown as {
          end_orientation?: string;
          end_ori?: string;
        }
      ).end_orientation ??
      (this.motionData.red as unknown as { end_ori?: string }).end_ori;
    const blueEndOri =
      (
        this.motionData.blue as unknown as {
          end_orientation?: string;
          end_ori?: string;
        }
      ).end_orientation ??
      (this.motionData.blue as unknown as { end_ori?: string }).end_ori;
    if (redEndOri === "in" && blueEndOri === "in") return true;
    if (redEndOri === "out" && blueEndOri === "out") return false;
    return true;
  }
}
