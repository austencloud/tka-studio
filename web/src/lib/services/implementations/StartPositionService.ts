/**
 * StartPositionService.ts - Complete start position service implementation
 */
import type { IGridPositionDeriver, IStartPositionService } from "$contracts";
import type { BeatData, PictographData } from "$domain";
import {
  type ValidationError,
  type ValidationResult,
  GridMode,
  Letter,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  createMotionData,
  createPictographData,
} from "$domain";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class StartPositionService implements IStartPositionService {
  constructor(
    @inject(TYPES.IPositionMapper)
    private positionMapper: IGridPositionDeriver
  ) {}

  async getAvailableStartPositions(
    propType: string,
    gridMode: GridMode
  ): Promise<BeatData[]> {
    console.log(
      `📍 Getting available start positions for ${propType} in ${gridMode} mode`
    );

    try {
      // For SKEWED mode, default to diamond positions
      const actualGridMode =
        gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
      const startPositionKeys = this.DEFAULT_START_POSITIONS[actualGridMode];

      if (!startPositionKeys) {
        console.error(
          `❌ Unsupported grid mode: ${gridMode}. Supported modes: ${Object.keys(this.DEFAULT_START_POSITIONS).join(", ")}`
        );
        // Fallback to diamond mode
        const fallbackKeys = this.DEFAULT_START_POSITIONS[GridMode.DIAMOND];
        console.log(`🔄 Falling back to diamond mode`);

        const beatData: BeatData[] = fallbackKeys.map((key, index) => {
          return {
            beatNumber: 0,
            isBlank: false,
            pictographData: this.createStartPositionPictograph(key, index),
          } as BeatData;
        });

        console.log(
          `✅ Generated ${beatData.length} available start positions (fallback)`
        );
        return beatData;
      }

      const beatData: BeatData[] = startPositionKeys.map((key, index) => {
        return {
          beatNumber: 0,
          isBlank: false,
          pictographData: this.createStartPositionPictograph(key, index),
        } as BeatData;
      });

      console.log(`✅ Generated ${beatData.length} available start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting available start positions:", error);
      throw new Error(
        `Failed to get available start positions: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  async setStartPosition(startPosition: BeatData): Promise<void> {
    console.log("🎯 Setting start position:", startPosition);

    try {
      if (!startPosition.pictographData) {
        throw new Error("Start position must have pictograph data");
      }

      // Update selected position
      this._selectedPosition = startPosition.pictographData;

      // Create data in the format option picker expects
      const { pictographData, ...beatWithoutPictographData } = startPosition;

      // Compute endPosition from motion data
      const endPosition =
        pictographData.motions?.blue && pictographData.motions?.red
          ? this.positionMapper.getPositionFromLocations(
              pictographData.motions.blue.endLocation,
              pictographData.motions.red.endLocation
            )
          : null;

      const optionPickerFormat = {
        endPosition,
        pictographData,
        letter: pictographData.letter,
        gridMode: GridMode.DIAMOND, // Default
        isStartPosition: true,
        ...beatWithoutPictographData,
      };

      localStorage.setItem("startPosition", JSON.stringify(optionPickerFormat));
    } catch (error) {
      console.error("Error setting start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  // Clean constructor - no debug logging needed
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

  // Internal state
  private _startPositions: PictographData[] = [];
  private _selectedPosition: PictographData | null = null;
  private _isLoading: boolean = false;
  private _error: string | null = null;

  // Readonly getters
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
    this.notifyStateChange();
  }

  setError(error: string | null): void {
    console.log(`🔧 StartPositionService: setError(${error})`);
    this._error = error;
    this.notifyStateChange();
  }

  clearSelection(): void {
    console.log(`🔧 StartPositionService: clearSelection()`);
    this._selectedPosition = null;
    this.notifyStateChange();
  }

  // Simple state change notification
  private notifyStateChange(): void {
    if (typeof window !== "undefined") {
      window.dispatchEvent(new CustomEvent("startPositionServiceStateChange"));
    }
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

      // Update state - positions first, then loading state
      this._startPositions = pictographs;
      this.setLoading(false);

      console.log(
        `✅ StartPositionService: Loaded ${pictographs.length} start positions`
      );

      // Explicitly notify that positions were loaded
      this.notifyStateChange();
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
   * Select a start position and handle all coordination
   */
  async selectStartPosition(position: PictographData): Promise<void> {
    console.log(`🎯 StartPositionService: Selecting start position`, position);

    try {
      // Update selected position
      this._selectedPosition = position;
      this.notifyStateChange();

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
    // Map position keys to actual Location enum values (matching domain service)
    const positionMappings: Record<string, { blue: Location; red: Location }> =
      {
        alpha1_alpha1: { blue: Location.SOUTH, red: Location.NORTH },
        beta5_beta5: { blue: Location.SOUTH, red: Location.SOUTH },
        gamma11_gamma11: { blue: Location.SOUTH, red: Location.EAST },
        // Box mode positions
        alpha2_alpha2: { blue: Location.SOUTHWEST, red: Location.NORTHEAST },
        beta4_beta4: { blue: Location.SOUTHEAST, red: Location.SOUTHEAST },
        gamma12_gamma12: { blue: Location.SOUTHWEST, red: Location.SOUTHEAST },
      };

    const mapping = positionMappings[key];
    if (!mapping) {
      console.warn(`No position mapping found for ${key}, using fallback`);
    }

    const blueLocation = mapping?.blue || Location.SOUTH;
    const redLocation = mapping?.red || Location.NORTH;

    // Map position to letter
    const letterMap: Record<string, Letter> = {
      alpha1_alpha1: Letter.ALPHA,
      beta5_beta5: Letter.BETA,
      gamma11_gamma11: Letter.GAMMA,
      alpha2_alpha2: Letter.ALPHA,
      beta4_beta4: Letter.BETA,
      gamma12_gamma12: Letter.GAMMA,
    };
    const letter = letterMap[key] || Letter.ALPHA;

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
