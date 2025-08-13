import {
  MotionType,
  Orientation,
  RotationDirection,
  Location,
} from "$lib/domain/enums";

export interface MotionTestParams {
  startLoc: string;
  endLoc: string;
  motionType: string;
  turns: number;
  propRotDir: string;
  startOri: string;
  endOri: string;
}

export class MotionParameterService {
  // Helper function to determine motion type based on start/end locations
  getMotionType(startLoc: string, endLoc: string): string {
    if (startLoc === endLoc) {
      return "static"; // Same location = static
    }

    // Check if it's a dash motion (opposite locations)
    const opposites = [
      ["n", "s"],
      ["s", "n"],
      ["e", "w"],
      ["w", "e"],
    ];

    for (const [start, end] of opposites) {
      if (startLoc === start && endLoc === end) {
        return "dash";
      }
    }

    // Adjacent locations = shift motion (pro/anti/float)
    return "pro"; // Default to pro for shift motions
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
    endLoc: string,
  ): string {
    // Location order for clockwise movement: n -> e -> s -> w -> n
    const locationOrder = ["n", "e", "s", "w"];
    const startIndex = locationOrder.indexOf(startLoc);
    const endIndex = locationOrder.indexOf(endLoc);

    if (startIndex === -1 || endIndex === -1) {
      return "cw"; // Default to clockwise for unknown locations
    }

    // Calculate the direction of movement
    let clockwiseDistance = (endIndex - startIndex + 4) % 4;
    let counterClockwiseDistance = (startIndex - endIndex + 4) % 4;

    // For static motions, no rotation
    if (motionType === "static") {
      return "no_rot";
    }

    // For dash motions, typically no rotation unless specified
    if (motionType === "dash") {
      return "no_rot";
    }

    // For pro motions: follow natural circular progression
    // For anti motions: go opposite to natural progression
    if (clockwiseDistance <= counterClockwiseDistance) {
      return motionType === "pro" ? "cw" : "ccw";
    } else {
      return motionType === "pro" ? "ccw" : "cw";
    }
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
      motion_type: params.motionType as any,
      turns: params.turns,
      prop_rot_dir: params.propRotDir as any,
      start_ori: params.startOri as any,
      end_ori: params.endOri as any,
    };
  }

  // Create default motion parameters
  createDefaultParams(): MotionTestParams {
    return {
      startLoc: "n",
      endLoc: "e",
      motionType: "pro",
      turns: 0,
      propRotDir: "cw",
      startOri: "in",
      endOri: "in",
    };
  }

  // Update motion type when locations change
  updateMotionTypeForLocations(params: MotionTestParams): MotionTestParams {
    const newMotionType = this.getMotionType(params.startLoc, params.endLoc);
    const availableTypes = this.getAvailableMotionTypes(
      params.startLoc,
      params.endLoc,
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
}
