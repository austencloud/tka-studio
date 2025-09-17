import type { BeatData, GridMode, PictographData } from "$shared";
import {
  createMotionData,
  createPictographData,
  GridLocation,
  GridPosition,
  Letter,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection
} from "$shared";
import { injectable } from "inversify";
import type { IStartPositionService } from "../contracts";

@injectable()
export class StartPositionService implements IStartPositionService {
  constructor() {}

  async getStartPositions(gridMode: GridMode): Promise<PictographData[]> {
    return await this.getDefaultStartPositions(gridMode);
  }

  async getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]> {
    // Define start position locations based on grid mode (like legacy)
    const startPositionKeys = gridMode === 'diamond'
      ? [
          { position: GridPosition.ALPHA1, letter: Letter.ALPHA },
          { position: GridPosition.BETA5, letter: Letter.BETA },
          { position: GridPosition.GAMMA11, letter: Letter.GAMMA }
        ]
      : [
          { position: GridPosition.ALPHA2, letter: Letter.ALPHA },
          { position: GridPosition.BETA4, letter: Letter.BETA },
          { position: GridPosition.GAMMA12, letter: Letter.GAMMA }
        ];

    const pictographData: PictographData[] = startPositionKeys.map((pos) => {
      // Get the hand locations for this position (blue and red hand locations)
      const [blueLocation, redLocation] = this.getHandLocationsForPosition(pos.position);

      // Create proper motion data using factory functions (like the original working implementation)
      const blueMotion = createMotionData({
        motionType: MotionType.STATIC,
        startLocation: blueLocation,
        endLocation: blueLocation, // Start positions: start === end
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.NO_ROTATION,
        turns: 0,
        color: MotionColor.BLUE,
        isVisible: true,
        propType: PropType.STAFF,
        arrowLocation: blueLocation
      });

      const redMotion = createMotionData({
        motionType: MotionType.STATIC,
        startLocation: redLocation,
        endLocation: redLocation, // Start positions: start === end
        startOrientation: Orientation.IN,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.NO_ROTATION,
        turns: 0,
        color: MotionColor.RED,
        isVisible: true,
        propType: PropType.STAFF,
        arrowLocation: redLocation
      });

      // Create proper pictograph data using factory function (like the original working implementation)
      return createPictographData({
        id: `start-${pos.position}`, // Use the position enum as the unique identifier
        letter: pos.letter,
        startPosition: pos.position,
        endPosition: pos.position,
        motions: {
          [MotionColor.BLUE]: blueMotion,
          [MotionColor.RED]: redMotion
        }
      });
    });

    return pictographData;
  }

  private getHandLocationsForPosition(position: GridPosition): [GridLocation, GridLocation] {
    // Map GridPosition to hand locations (blue, red) based on legacy pattern generator
    switch (position) {
      case GridPosition.ALPHA1: return [GridLocation.SOUTH, GridLocation.NORTH];
      case GridPosition.ALPHA2: return [GridLocation.SOUTHWEST, GridLocation.NORTHEAST];
      case GridPosition.BETA4: return [GridLocation.EAST, GridLocation.EAST];
      case GridPosition.BETA5: return [GridLocation.SOUTH, GridLocation.SOUTH];
      case GridPosition.GAMMA11: return [GridLocation.SOUTH, GridLocation.EAST];
      case GridPosition.GAMMA12: return [GridLocation.SOUTHWEST, GridLocation.SOUTHEAST];
      default: return [GridLocation.SOUTH, GridLocation.NORTH]; // Default to alpha1
    }
  }

  async selectStartPosition(position: any): Promise<void> {
    try {
      const startPosCopy = { ...position, isStartPosition: true };
      localStorage.setItem('startPosition', JSON.stringify(startPosCopy));

      const customEvent = new CustomEvent('start-position-selected', {
        detail: { startPosition: startPosCopy },
        bubbles: true
      });
      document.dispatchEvent(customEvent);
    } catch (error) {
      console.error("Error selecting start position:", error);
      throw new Error(`Failed to select start position: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  async setStartPosition(startPosition: BeatData): Promise<void> {
    try {
      // Store the start position for the sequence
      localStorage.setItem('sequenceStartPosition', JSON.stringify(startPosition));
    } catch (error) {
      console.error("Error setting start position:", error);
      throw new Error(`Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }
}
