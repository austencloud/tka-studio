import type { IMotionParameterService } from "$contracts";
import type { MotionData } from "$domain";
import {
  createMotionData,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  RotationDirection,
} from "$domain";
import { injectable } from "inversify";

/**
 * Motion Test Parameters - Using proper enums for type safety
 * No more string-based parameters that cause type issues
 */
export interface MotionTestParams {
  startLocation: Location;
  endLocation: Location;
  motionType: MotionType;
  turns: number | "fl"; // Support both numeric turns and float
  rotationDirection: RotationDirection;
  startOrientation: Orientation;
  endOrientation: Orientation;
}

@injectable()
export class MotionParameterService implements IMotionParameterService {
  // Helper function to determine motion type based on start/end locations
  getMotionType(startLocation: Location, endLocation: Location): MotionType {
    if (startLocation === endLocation) {
      return MotionType.STATIC; // Same location = static
    }

    // Check if it's a dash motion (opposite locations)
    const opposites = [
      [Location.NORTH, Location.SOUTH],
      [Location.SOUTH, Location.NORTH],
      [Location.EAST, Location.WEST],
      [Location.WEST, Location.EAST],
      [Location.NORTHEAST, Location.SOUTHWEST],
      [Location.SOUTHWEST, Location.NORTHEAST],
      [Location.NORTHWEST, Location.SOUTHEAST],
      [Location.SOUTHEAST, Location.NORTHWEST],
    ];

    for (const [startOpp, endOpp] of opposites) {
      if (startLocation === startOpp && endLocation === endOpp) {
        return MotionType.DASH;
      }
    }

    // Adjacent locations = shift motion (default to PRO)
    return MotionType.PRO;
  }

  // Helper function to get available motion types for a start/end pair
  getAvailableMotionTypes(
    startLocation: Location,
    endLocation: Location
  ): MotionType[] {
    const motionType = this.getMotionType(startLocation, endLocation);

    if (motionType === MotionType.STATIC) {
      return [MotionType.STATIC];
    } else if (motionType === MotionType.DASH) {
      return [MotionType.DASH];
    } else {
      // Shift motions can be pro, anti, or float
      return [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT];
    }
  }

  // Helper function to calculate rotation direction based on motion type and locations
  calculateRotationDirection(
    motionType: MotionType,
    startLocation: Location,
    endLocation: Location
  ): RotationDirection {
    // Location order for clockwise movement: N -> E -> S -> W -> N
    const locationOrder = [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
    ];
    const startIndex = locationOrder.indexOf(startLocation);
    const endIndex = locationOrder.indexOf(endLocation);

    // For static motions, no rotation
    if (motionType === MotionType.STATIC) {
      return RotationDirection.NO_ROTATION;
    }

    // For dash motions, typically no rotation unless specified
    if (motionType === MotionType.DASH) {
      return RotationDirection.NO_ROTATION;
    }

    // Handle diagonal locations - default to clockwise
    if (startIndex === -1 || endIndex === -1) {
      return RotationDirection.CLOCKWISE;
    }

    // Calculate the hand path direction (clockwise or counterclockwise)
    const clockwiseDistance = (endIndex - startIndex + 4) % 4;
    const counterClockwiseDistance = (startIndex - endIndex + 4) % 4;

    // Determine hand path direction (shorter distance wins)
    const handPathIsClockwise = clockwiseDistance < counterClockwiseDistance;

    // For PRO: prop rotation matches hand path direction
    // For ANTI: prop rotation opposes hand path direction
    let result: RotationDirection;
    if (motionType === MotionType.PRO) {
      result = handPathIsClockwise
        ? RotationDirection.CLOCKWISE
        : RotationDirection.COUNTER_CLOCKWISE;
    } else if (motionType === MotionType.ANTI) {
      result = handPathIsClockwise
        ? RotationDirection.COUNTER_CLOCKWISE
        : RotationDirection.CLOCKWISE;
    } else {
      result = RotationDirection.CLOCKWISE; // Default for other motion types
    }

    console.log(
      `🔄 Rotation direction for ${startLocation}→${endLocation} (${motionType}): ${result}`
    );

    return result;
  }

  // No more string-to-enum mapping needed - we use enums directly!

  // Helper function to convert MotionTestParams to PropAttributes
  convertMotionTestParamsToPropAttributes(params: MotionTestParams) {
    return {
      startLocation: params.startLocation,
      endLocation: params.endLocation,
      motionType: params.motionType as MotionType,
      turns: params.turns,
      rotationDirection: params.rotationDirection as RotationDirection,
      startOrientation: params.startOrientation as Orientation,
      endOrientation: params.endOrientation as Orientation,
    };
  }

  // Create default motion parameters
  createDefaultParams(): MotionTestParams {
    return {
      startLocation: Location.NORTH,
      endLocation: Location.EAST,
      motionType: MotionType.PRO,
      turns: 0,
      rotationDirection: RotationDirection.CLOCKWISE,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
    };
  }

  // Update motion type when locations change
  updateMotionTypeForLocations(params: MotionTestParams): MotionTestParams {
    const availableTypes = this.getAvailableMotionTypes(
      params.startLocation,
      params.endLocation
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

  // Convert MotionTestParams to MotionData - no mapping needed, already enums!
  convertToMotionData(
    params: MotionTestParams,
    color: MotionColor
  ): MotionData {
    return createMotionData({
      motionType: params.motionType,
      rotationDirection: params.rotationDirection,
      startLocation: params.startLocation,
      endLocation: params.endLocation,
      turns: typeof params.turns === "string" ? -0.5 : params.turns, // Handle "fl" float turns
      startOrientation: params.startOrientation,
      endOrientation: params.endOrientation,
      isVisible: true,
      color,
    });
  }
}
