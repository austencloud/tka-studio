import type { BeatData, GridMode, IGridPositionDeriver, PictographData } from "$shared";
import { createMotionData, createPictographData, GridLocation, GridPosition, Letter, MotionColor, MotionType, Orientation, PropType, RotationDirection } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IStartPositionService } from "../contracts";

@injectable()
export class StartPositionService implements IStartPositionService {
  constructor(
    @inject(TYPES.IGridPositionDeriver) private gridPositionDeriver: IGridPositionDeriver
  ) {}

  async getStartPositions(gridMode: GridMode): Promise<PictographData[]> {
    return await this.getDefaultStartPositions(gridMode);
  }

  async getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]> {
    // Define start position locations based on grid mode
    const startPositionKeys = gridMode === "diamond"
      ? [
          { position: GridPosition.ALPHA1, letter: Letter.ALPHA },
          { position: GridPosition.GAMMA11, letter: Letter.GAMMA },
          { position: GridPosition.BETA5, letter: Letter.BETA },
        ]
      : [
          { position: GridPosition.ALPHA2, letter: Letter.ALPHA },
          { position: GridPosition.GAMMA12, letter: Letter.GAMMA },
          { position: GridPosition.BETA6, letter: Letter.BETA },
        ];

    return this.createPictographsFromPositions(startPositionKeys);
  }

  async getAllStartPositionVariations(gridMode: GridMode): Promise<PictographData[]> {
    // Get all 16 start position variations for the specified grid mode
    // Based on legacy advanced start position picker
    const allVariations = gridMode === 'diamond'
      ? [
          // Diamond mode: 16 positions (alpha1/3/5/7, beta1/3/5/7, gamma1/3/5/7/9/11/13/15)
          { position: GridPosition.ALPHA1, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA3, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA5, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA7, letter: Letter.ALPHA },
          { position: GridPosition.BETA1, letter: Letter.BETA },
          { position: GridPosition.BETA3, letter: Letter.BETA },
          { position: GridPosition.BETA5, letter: Letter.BETA },
          { position: GridPosition.BETA7, letter: Letter.BETA },
          { position: GridPosition.GAMMA1, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA3, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA5, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA7, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA9, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA11, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA13, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA15, letter: Letter.GAMMA },
        ]
      : [
          // Box mode: 16 positions (alpha2/4/6/8, beta2/4/6/8, gamma2/4/6/8/10/12/14/16)
          { position: GridPosition.ALPHA2, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA4, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA6, letter: Letter.ALPHA },
          { position: GridPosition.ALPHA8, letter: Letter.ALPHA },
          { position: GridPosition.BETA2, letter: Letter.BETA },
          { position: GridPosition.BETA4, letter: Letter.BETA },
          { position: GridPosition.BETA6, letter: Letter.BETA },
          { position: GridPosition.BETA8, letter: Letter.BETA },
          { position: GridPosition.GAMMA2, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA4, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA6, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA8, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA10, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA12, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA14, letter: Letter.GAMMA },
          { position: GridPosition.GAMMA16, letter: Letter.GAMMA },
        ];

    return this.createPictographsFromPositions(allVariations);
  }

  private createPictographsFromPositions(
    positions: Array<{ position: GridPosition; letter: Letter }>
  ): PictographData[] {
    return positions.map((pos) => {
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
  }

  private getHandLocationsForPosition(position: GridPosition): [GridLocation, GridLocation] {
    // Use the GridPositionDeriver service to get hand locations for any position
    return this.gridPositionDeriver.getGridLocationsFromPosition(position);
  }

  async selectStartPosition(position: PictographData): Promise<void> {
    try {
      const startPosCopy = { ...position, isStartPosition: true };
      localStorage.setItem("startPosition", JSON.stringify(startPosCopy));
    } catch (error) {
      console.warn("StartPositionService: unable to persist start position selection", error);
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

