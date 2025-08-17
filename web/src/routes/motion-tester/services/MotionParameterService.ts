import {
  MotionType,
  Orientation,
  RotationDirection,
  Location,
} from "$lib/domain/enums";
import type { MotionData } from "$lib/domain/MotionData";
import type { IMotionParameterService } from "./interfaces";

export interface MotionTestParams {
  startLoc: string;
  endLoc: string;
  motionType: string;
  turns: number | "fl"; // Support both numeric turns and float
  rotationDirection: string;
  startOri: string;
  endOri: string;
}

export class MotionParameterService implements IMotionParameterService {
  // Helper function to determine motion type based on start/end locations
  getMotionType(startLoc: string, endLoc: string): string {
    // Normalize to lowercase for case-insensitive comparison
    const start = startLoc.toLowerCase();
    const end = endLoc.toLowerCase();

    if (start === end) {
      return "static"; // Same location = static
    }

    // Check if it's a dash motion (opposite locations)
    const opposites = [
      ["n", "s"],
      ["s", "n"],
      ["e", "w"],
      ["w", "e"],
    ];

    for (const [startOpp, endOpp] of opposites) {
      if (start === startOpp && end === endOpp) {
        return "dash";
      }
    }

    // Adjacent locations = shift motion (pro/anti/float)
    return "pro"; // TODO - fix this so it actually receives the real info required to get the motion type, pro as default is bad
  }

  // Helper function to get available motion types for a start/end pair
  getAvailableMotionTypes(startLoc: string, endLoc: string): string[] {
    const motionType = this.getMotionType(startLoc, endLoc);

    if (motionType === "static") {
      return ["static"];
    } else if (motionType === "dash") {
      return ["dash"];
    } else {
      // Shift motions can be pro, anti, or float
      return ["pro", "anti", "float"];
    }
  }

  // Helper function to calculate rotation direction based on motion type and locations
  calculateRotationDirection(
    motionType: string,
    startLoc: string,
    endLoc: string
  ): string {
    // Location order for clockwise movement: n -> e -> s -> w -> n
    const locationOrder = ["n", "e", "s", "w"];
    const startIndex = locationOrder.indexOf(startLoc.toLowerCase());
    const endIndex = locationOrder.indexOf(endLoc.toLowerCase());

    if (startIndex === -1 || endIndex === -1) {
      return "cw"; // Default to clockwise for unknown locations
    }

    // For static motions, no rotation
    if (motionType === "static") {
      return "no_rot";
    }

    // For dash motions, typically no rotation unless specified
    if (motionType === "dash") {
      return "no_rot";
    }

    // Calculate the hand path direction (clockwise or counterclockwise)
    const clockwiseDistance = (endIndex - startIndex + 4) % 4;
    const counterClockwiseDistance = (startIndex - endIndex + 4) % 4;

    // Determine hand path direction (shorter distance wins)
    const handPathIsClockwise = clockwiseDistance < counterClockwiseDistance;

    // For PRO: prop rotation matches hand path direction
    // For ANTI: prop rotation opposes hand path direction
    let result;
    if (motionType === "pro") {
      result = handPathIsClockwise ? "cw" : "ccw";
    } else if (motionType === "anti") {
      result = handPathIsClockwise ? "ccw" : "cw";
    } else {
      result = "cw"; // Default for other motion types
    }

    console.log(
      `🔄 Rotation direction for ${startLoc}→${endLoc} (${motionType}): ${result}`
    );
    console.log(
      `   handPathIsClockwise: ${handPathIsClockwise}, clockwiseDistance: ${clockwiseDistance}, counterClockwiseDistance: ${counterClockwiseDistance}`
    );

    return result;
  }

  // Helper function to map string values to enum values
  mapMotionTypeToEnum(motionType: string): MotionType {
    switch (motionType.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "static":
        return MotionType.STATIC;
      case "dash":
        return MotionType.DASH;
      case "fl":
      case "float":
        return MotionType.FLOAT;
      default:
        return MotionType.PRO;
    }
  }

  mapOrientationToEnum(orientation: string): Orientation {
    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      case "n":
        return Orientation.IN; // Map cardinal directions to in/out for now
      case "e":
        return Orientation.IN;
      case "s":
        return Orientation.IN;
      case "w":
        return Orientation.IN;
      default:
        return Orientation.IN;
    }
  }

  mapRotationDirectionToEnum(rotDir: string): RotationDirection {
    switch (rotDir.toLowerCase()) {
      case "cw":
      case "clockwise":
        return RotationDirection.CLOCKWISE;
      case "ccw":
      case "counter_clockwise":
      case "counterclockwise":
        return RotationDirection.COUNTER_CLOCKWISE;
      default:
        return RotationDirection.CLOCKWISE;
    }
  }

  mapLocationToEnum(location: string): Location {
    switch (location.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return Location.NORTH;
    }
  }

  // Helper function to convert MotionTestParams to PropAttributes
  convertMotionTestParamsToPropAttributes(params: MotionTestParams) {
    return {
      start_loc: params.startLoc,
      end_loc: params.endLoc,
      motion_type: params.motionType as MotionType,
      turns: params.turns,
      prop_rot_dir: params.rotationDirection as RotationDirection,
      start_ori: params.startOri as Orientation,
      end_ori: params.endOri as Orientation,
    };
  }

  // Create default motion parameters
  createDefaultParams(): MotionTestParams {
    return {
      startLoc: "n",
      endLoc: "e",
      motionType: "pro",
      turns: 0,
      rotationDirection: "cw",
      startOri: "in",
      endOri: "in",
    };
  }

  // Update motion type when locations change
  updateMotionTypeForLocations(params: MotionTestParams): MotionTestParams {
    const availableTypes = this.getAvailableMotionTypes(
      params.startLoc,
      params.endLoc
    );

    // If current motion type is not available, switch to the first available
    if (!availableTypes.includes(params.motionType)) {
      return {
        ...params,
        motionType: availableTypes[0],
      };
    }

    return params;
  }

  // Convert MotionTestParams to MotionData (moved from state layer)
  convertToMotionData(params: MotionTestParams): MotionData {
    return {
      motion_type: this.mapMotionTypeToEnum(params.motionType),
      prop_rot_dir: this.mapRotationDirectionToEnum(params.rotationDirection),
      start_loc: this.mapLocationToEnum(params.startLoc),
      end_loc: this.mapLocationToEnum(params.endLoc),
      turns: params.turns,
      start_ori: this.mapOrientationToEnum(params.startOri),
      end_ori: this.mapOrientationToEnum(params.endOri),
      is_visible: true,
      prefloat_motion_type: null,
      prefloat_prop_rot_dir: null,
    };
  }
}
