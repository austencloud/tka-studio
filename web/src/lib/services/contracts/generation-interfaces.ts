/**
 * Generation Service Interfaces - Complete interface definitions
 *
 * Complete interfaces for motion generation, sequence generation, and related algorithms.
 * Updated to match exact legacy generation parameters and options.
 */
// ============================================================================
// GENERATION OPTIONS
// ============================================================================
import type {
  BeatData,
  GenerationOptions,
  GridMode,
  Letter,
  LetterDerivationResult,
  MotionData,
  PictographData,
  SequenceData,
} from "$domain";
import { GenerationMode, GridPosition, MotionColor } from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISequenceGenerationService {
  generateSequence(options: GenerationOptions): Promise<SequenceData>;
  generatePatternSequence(
    pattern: GenerationMode,
    options: GenerationOptions
  ): Promise<SequenceData>;

  getGenerationStats(): {
    totalGenerated: number;
    averageGenerationTime: number;
    lastGenerated: string | null;
  };
}

export interface IMotionGenerationService {
  generateMotion(
    color: MotionColor,
    options: GenerationOptions,
    previousBeats: BeatData[]
  ): Promise<MotionData>;
  generateConstrainedMotion(
    color: MotionColor,
    options: GenerationOptions,
    previousBeats: BeatData[],
    constraints: {
      allowedMotionTypes?: string[];
      allowedStartLocations?: string[];
      allowedEndLocations?: string[];
    }
  ): Promise<MotionData>;
  validateMotion(
    motion: MotionData,
    color: MotionColor,
    previousBeats: BeatData[]
  ): { isValid: boolean; reasons: string[] };
}

export interface ITurnIntensityManagerService {
  allocateTurnsForBlueAndRed(): {
    blue: (number | "fl")[];
    red: (number | "fl")[];
  };
}

export interface IOptionDataService {
  initialize(): Promise<void>;
  getNextOptions(sequence: BeatData[]): Promise<PictographData[]>;
  getNextOptionsFromEndPosition(
    endPosition: string,
    gridMode: GridMode,
    options: Record<string, unknown>
  ): Promise<PictographData[]>;
  filterOptionsByLetterTypes(
    options: PictographData[],
    letterTypes: string[]
  ): PictographData[];
  filterOptionsByRotation(
    options: PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): PictographData[];
}

export interface IOrientationCalculationService {
  calculateEndOrientation(motion: MotionData, color: MotionColor): string;
  updateStartOrientations(nextBeat: BeatData, lastBeat: BeatData): BeatData;
  updateEndOrientations(beat: BeatData): BeatData;
}

export interface IPictographGenerator {
  // Standard letter generators
  generateA(): PictographData[];
  generateB(): PictographData[];
  generateC(): PictographData[];
  generateD(): PictographData[];
  generateE(): PictographData[];
  generateF(): PictographData[];
  generateG(): PictographData[];
  generateH(): PictographData[];
  generateI(): PictographData[];
  generateJ(): PictographData[];
  generateK(): PictographData[];
  generateL(): PictographData[];
  generateM(): PictographData[];
  generateN(): PictographData[];
  generateO(): PictographData[];
  generateP(): PictographData[];
  generateQ(): PictographData[];
  generateR(): PictographData[];
  generateS(): PictographData[];
  generateT(): PictographData[];
  generateU(): PictographData[];
  generateV(): PictographData[];
  generateW(): PictographData[];
  generateX(): PictographData[];
  generateY(): PictographData[];
  generateZ(): PictographData[];

  // Greek letter generators
  generateSigma(): PictographData[];
  generateDelta(): PictographData[];
  generateTheta(): PictographData[];
  generateOmega(): PictographData[];
  generatePhi(): PictographData[];
  generatePsi(): PictographData[];
  generateLambda(): PictographData[];
  generateAlpha(): PictographData[];
  generateBeta(): PictographData[];
  generateGamma(): PictographData[];

  // Dash variant generators
  generateWDash(): PictographData[];
  generateXDash(): PictographData[];
  generateYDash(): PictographData[];
  generateZDash(): PictographData[];
  generateSigmaDash(): PictographData[];
  generateDeltaDash(): PictographData[];
  generateThetaDash(): PictographData[];
  generateOmegaDash(): PictographData[];
  generatePhiDash(): PictographData[];
  generatePsiDash(): PictographData[];
  generateLambdaDash(): PictographData[];

  // Utility methods
  getAllPictographs(): PictographData[];
  getPictographsByLetter(letter: string): PictographData[] | undefined;
}

export interface IPositionPatternService {
  getAlphaSequence(): GridPosition[];
  getBetaSequence(): GridPosition[];
  getGammaSequence(): GridPosition[];
  getCustomSequence(positions: GridPosition[]): GridPosition[];

  generatePositionSequence(
    positionSystem: string,
    length?: number
  ): GridPosition[];
}

export interface IPositionSequenceService {
  getPositionSequence(
    system: "alpha" | "beta" | "gamma",
    count: number
  ): GridPosition[];
  getNextPosition(current: GridPosition, forward: boolean): GridPosition;
  calculatePositionPairs(
    sequence: GridPosition[]
  ): Array<[GridPosition, GridPosition]>;
}

export interface IDirectionCalculator {
  getCardinalDirections(
    startPosition: GridPosition,
    endPosition: GridPosition,
    motionType: string
  ): [import("$domain").Location, import("$domain").Location];
}

export interface IPictographValidatorService {
  validatePictograph(pictograph: PictographData): boolean;
  validatePictographs(pictographs: PictographData[]): boolean;
  getValidationErrors(pictograph: PictographData): string[];
  validatePositionSequence(positions: GridPosition[]): boolean;
}

export interface ILetterGenerator {
  /**
   * The letter this generator handles
   */
  readonly letter: string;

  /**
   * Generate movement set for this letter
   */
  generate(): PictographData;
}

export interface ILetterGeneratorFactory {
  /**
   * Create generator for the specified letter
   */
  createGenerator(letter: string): ILetterGenerator | null;

  /**
   * Get all supported letters
   */
  getSupportedLetters(): string[];
}

export interface ILetterDeriver {
  deriveLetterFromMotions(
    blueMotion: MotionData,
    redMotion: MotionData
  ): LetterDerivationResult;
  deriveLetterFromPictograph(
    pictograph: PictographData
  ): LetterDerivationResult;
  validateLetterMatch(
    letter: Letter,
    blueMotion: MotionData,
    redMotion: MotionData
  ): boolean;
}

// ============================================================================
// RE-EXPORT TYPES FOR EXTERNAL USE
// ============================================================================

// REMOVED: Domain model re-exports. Import directly from $domain instead.
// Contracts should only contain service interface definitions.
