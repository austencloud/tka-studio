import { OrientationCalculationService } from "$lib/services/implementations/OrientationCalculationService";
import {
  MotionType,
  Orientation,
  RotationDirection,
  Location,
} from "$lib/domain/enums";
import type { MotionTestParams } from "./MotionParameterService";

export class OrientationAutoCalculationService {
  private orientationService: OrientationCalculationService;

  constructor() {
    this.orientationService = new OrientationCalculationService();
  }

  // Calculate end orientation automatically
  calculateEndOrientation(params: MotionTestParams): string {
    try {
      const motionData = {
        motion_type: this.mapMotionTypeToEnum(params.motionType),
        prop_rot_dir: this.mapRotationDirectionToEnum(params.propRotDir),
        start_loc: this.mapLocationToEnum(params.startLoc),
        end_loc: this.mapLocationToEnum(params.endLoc),
        turns: params.turns,
        start_ori: this.mapOrientationToEnum(params.startOri),
        end_ori: this.mapOrientationToEnum(params.endOri), // Will be overwritten
        is_visible: true,
        prefloat_motion_type: null,
        prefloat_prop_rot_dir: null,
      };

      const calculatedEndOri =
        this.orientationService.calculateEndOrientation(motionData);

      // Map back to string
      return this.mapOrientationFromEnum(calculatedEndOri);
    } catch (error) {
      console.warn("Failed to calculate end orientation:", error);
      return params.startOri; // Fallback to start orientation
    }
  }

  // Map string to enum
  private mapMotionTypeToEnum(motionType: string): MotionType {
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

  private mapOrientationToEnum(orientation: string): Orientation {
    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      default:
        return Orientation.IN;
    }
  }

  private mapRotationDirectionToEnum(rotDir: string): RotationDirection {
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

  private mapLocationToEnum(location: string): Location {
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

  // Map enum back to string
  private mapOrientationFromEnum(orientation: Orientation): string {
    switch (orientation) {
      case Orientation.IN:
        return "in";
      case Orientation.OUT:
        return "out";
      case Orientation.CLOCK:
        return "clock";
      case Orientation.COUNTER:
        return "counter";
      default:
        return "in";
    }
  }
}
