import type { MotionData } from "$shared/domain";
import {
  createMotionData,
  GridLocation,
  MotionColor,
  MotionType,
  Orientation,
  RotationDirection,
} from "$shared/domain";
import { injectable } from "inversify";
import type { AnimatedMotionParams } from "../../domain";
import type { IMotionParameterService } from "../contracts";

/**
 * Motion Parameter Service
 * Handles motion parameter calculations and conversions
 */

@injectable()
export class MotionParameterService implements IMotionParameterService {
  // Helper function to determine motion type based on start/end locations
  getMotionType(
    startLocation: GridLocation,
    endLocation: GridLocation
  ): MotionType {
    if (startLocation === endLocation) {
      return MotionType.STATIC; // Same location = static
    }

    // Check if it's a dash motion (opposite locations)
    const opposites = [
      [GridLocation.NORTH, GridLocation.SOUTH],
      [GridLocation.SOUTH, GridLocation.NORTH],
      [GridLocation.EAST, GridLocation.WEST],
      [GridLocation.WEST, GridLocation.EAST],
      [GridLocation.NORTHEAST, GridLocation.SOUTHWEST],
      [GridLocation.SOUTHWEST, GridLocation.NORTHEAST],
      [GridLocation.NORTHWEST, GridLocation.SOUTHEAST],
      [GridLocation.SOUTHEAST, GridLocation.NORTHWEST],
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
    startLocation: GridLocation,
    endLocation: GridLocation
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
    startLocation: GridLocation,
    endLocation: GridLocation
  ): RotationDirection {
    // GridLocation order for clockwise movement: N -> E -> S -> W -> N
    const locationOrder = [
      GridLocation.NORTH,
      GridLocation.EAST,
      GridLocation.SOUTH,
      GridLocation.WEST,
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

  // Helper function to convert AnimatedMotionParams to PropAttributes
  convertAnimatedMotionParamsToPropAttributes(params: AnimatedMotionParams) {
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
  createDefaultParams(): AnimatedMotionParams {
    return {
      startLocation: GridLocation.NORTH,
      endLocation: GridLocation.EAST,
      motionType: MotionType.PRO,
      turns: 0,
      rotationDirection: RotationDirection.CLOCKWISE,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
    };
  }

  // Update motion type when locations change
  updateMotionTypeForLocations(
    params: AnimatedMotionParams
  ): AnimatedMotionParams {
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

  // Convert AnimatedMotionParams to MotionData - no mapping needed, already enums!
  convertToMotionData(
    params: AnimatedMotionParams,
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
