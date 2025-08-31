/**
 * StartPositionService.unified.ts - Single, unified start position service
 *
 * Consolidates all start position functionality into one clean service:
 * - Data loading and management
 * - Selection handling
 * - Reactive state management
 * - Storage operations
 *
 * NO MORE CONFUSION - ONE SERVICE TO RULE THEM ALL!
 */

import { GridMode, Orientation, PropType, RotationDirection } from "$domain";
import type { BeatData } from "$domain/build/workbench/BeatData";
import { Letter } from "$domain/core/Letter";
import { createMotionData } from "$domain/core/pictograph/MotionData";
import type { PictographData } from "$domain/core/pictograph/PictographData";
import { createPictographData } from "$domain/core/pictograph/PictographData";
import { Location, MotionColor, MotionType } from "$domain/enums";
import type {
  ValidationError,
  ValidationResult,
} from "$domain/sequence-card/SequenceCard";
import { injectable } from "inversify";

/**
 * SINGLE START POSITION SERVICE INTERFACE
 * Everything you need for start positions in one place
 */
export interface IStartPositionService {
  // Data operations
  getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;

  // Selection operations
  selectStartPosition(position: PictographData): Promise<void>;

  // Validation
  validateStartPosition(position: BeatData): ValidationResult;

  // State access (reactive)
  readonly startPositions: PictographData[];
  readonly selectedPosition: PictographData | null;
  readonly isLoading: boolean;
  readonly error: string | null;

  // State mutations
  setLoading(loading: boolean): void;
  setError(error: string | null): void;
  clearSelection(): void;
}

@injectable()
export class UnifiedStartPositionService implements IStartPositionService {
  // Default start positions for each grid mode
  private readonly DEFAULT_START_POSITIONS: Record<string, string[]> = {
    [GridMode.DIAMOND]: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    [GridMode.BOX]: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"],
  };

  // Default end positions for letters
  private readonly DEFAULT_END_POSITIONS: Record<string, string> = {
    α: "alpha1",
    β: "beta5",
    Γ: "gamma11",
  };

  // Reactive state
  private _startPositions: PictographData[] = $state([]);
  private _selectedPosition: PictographData | null = $state(null);
  private _isLoading: boolean = $state(false);
  private _error: string | null = $state(null);

  // Reactive getters
  get startPositions(): PictographData[] {
    return this._startPositions;
  }

  get selectedPosition(): PictographData | null {
    return this._selectedPosition;
  }

  get isLoading(): boolean {
    return this._isLoading;
  }

  get error(): string | null {
    return this._error;
  }

  // State mutations
  setLoading(loading: boolean): void {
    console.log(`🔧 StartPositionService: setLoading(${loading})`);
    this._isLoading = loading;
  }

  setError(error: string | null): void {
    console.log(`🔧 StartPositionService: setError(${error})`);
    this._error = error;
  }

  clearSelection(): void {
    console.log(`🔧 StartPositionService: clearSelection()`);
    this._selectedPosition = null;
  }

  /**
   * Load default start positions for a grid mode
   */
  async getDefaultStartPositions(
    gridMode: GridMode
  ): Promise<PictographData[]> {
    console.log(
      `🚀 StartPositionService: Loading start positions for ${gridMode}`
    );

    this.setLoading(true);
    this.setError(null);

    try {
      // Get position keys for the grid mode
      const actualGridMode =
        gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
      const startPositionKeys = this.DEFAULT_START_POSITIONS[actualGridMode];

      if (!startPositionKeys) {
        throw new Error(`Unsupported grid mode: ${gridMode}`);
      }

      // Create pictograph data for each position
      const pictographs = startPositionKeys.map((key, index) =>
        this.createStartPositionPictograph(key, index)
      );

      // Update state
      this._startPositions = pictographs;
      this.setLoading(false);

      console.log(
        `✅ StartPositionService: Loaded ${pictographs.length} start positions`
      );
      return pictographs;
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Failed to load start positions";
      console.error(`❌ StartPositionService: ${errorMessage}`, error);

      this.setError(errorMessage);
      this.setLoading(false);

      return [];
    }
  }

  /**
   * Select a start position and handle all the coordination
   */
  async selectStartPosition(position: PictographData): Promise<void> {
    console.log(`🎯 StartPositionService: Selecting start position`, position);

    try {
      // Update selected position
      this._selectedPosition = position;

      // Extract end position for option picker
      const endPosition = this.extractEndPosition(position);

      // Create data in the format option picker expects
      const startPositionData = {
        endPosition,
        pictographData: position,
        letter: position.letter,
        gridMode: GridMode.DIAMOND,
        isStartPosition: true,
      };

      // Store in localStorage for persistence
      if (typeof window !== "undefined") {
        localStorage.setItem(
          "startPosition",
          JSON.stringify(startPositionData)
        );
        console.log(`💾 StartPositionService: Saved to localStorage`);
      }

      // Dispatch event for other components
      if (typeof window !== "undefined") {
        window.dispatchEvent(
          new CustomEvent("startPositionSelected", {
            detail: { startPositionData, endPosition },
          })
        );
        console.log(
          `📡 StartPositionService: Dispatched startPositionSelected event`
        );
      }

      console.log(
        `✅ StartPositionService: Start position selected successfully`
      );
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Failed to select start position";
      console.error(`❌ StartPositionService: ${errorMessage}`, error);
      this.setError(errorMessage);
      throw error;
    }
  }

  /**
   * Validate a start position
   */
  validateStartPosition(position: BeatData): ValidationResult {
    const errors: ValidationError[] = [];

    if (!position.pictographData) {
      errors.push({
        code: "MISSING_PICTOGRAPH_DATA",
        message: "Start position must have pictograph data",
        severity: "error",
      });
    }

    if (
      !position.pictographData?.motions?.blue &&
      !position.pictographData?.motions?.red
    ) {
      errors.push({
        code: "MISSING_MOTIONS",
        message: "Start position must have at least one motion",
        severity: "error",
      });
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings: [],
    };
  }

  /**
   * Extract end position from pictograph data
   */
  private extractEndPosition(pictographData: PictographData): string {
    if (
      pictographData.letter &&
      this.DEFAULT_END_POSITIONS[pictographData.letter]
    ) {
      return this.DEFAULT_END_POSITIONS[pictographData.letter];
    }
    return "alpha1"; // Default fallback
  }

  /**
   * Create a start position pictograph from a position key
   */
  private createStartPositionPictograph(
    key: string,
    index: number
  ): PictographData {
    // Parse the key (e.g., "alpha1_alpha1" -> both hands at alpha1)
    const [blueLocationStr, redLocationStr] = key.split("_");

    // Map position strings to Location enum values
    const locationMap: Record<string, Location> = {
      alpha1: Location.SOUTH,
      beta5: Location.SOUTH,
      gamma11: Location.SOUTH,
    };
    const blueLocation = locationMap[blueLocationStr] || Location.SOUTH;
    const redLocation = locationMap[redLocationStr] || Location.NORTH;

    // Map position to letter
    const letterMap: Record<string, Letter> = {
      alpha1: Letter.ALPHA,
      beta5: Letter.BETA,
      gamma11: Letter.GAMMA,
    };
    const letter = letterMap[blueLocation] || Letter.ALPHA;

    return createPictographData({
      id: `start-pos-${key}-${index}`,
      letter,
      motions: {
        blue: createMotionData({
          motionType: MotionType.STATIC,
          rotationDirection: RotationDirection.NO_ROTATION,
          startLocation: blueLocation,
          endLocation: blueLocation,
          turns: 0,
          startOrientation: Orientation.IN,
          endOrientation: Orientation.IN,
          color: MotionColor.BLUE,
          isVisible: true,
          propType: PropType.STAFF,
          arrowLocation: blueLocation,
        }),
        red: createMotionData({
          motionType: MotionType.STATIC,
          rotationDirection: RotationDirection.NO_ROTATION,
          startLocation: redLocation,
          endLocation: redLocation,
          turns: 0,
          startOrientation: Orientation.IN,
          endOrientation: Orientation.IN,
          color: MotionColor.RED,
          isVisible: true,
          propType: PropType.STAFF,
          arrowLocation: redLocation,
        }),
      },
    });
  }
}
