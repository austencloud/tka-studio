/**
 * Unified Type 1 Pictograph Generator
 *
 * Handles ALL Type 1 letters (A-V) across all position systems.
 * Generates pictograph data for Type 1 letters using logical rules.
 */

import { Direction, Letter, PositionSystem, Timing } from "$domain";
import { BaseType1Generator } from "./BaseType1Generator";
import {
  TYPE1_ALPHA_TO_ALPHA_LETTERS,
  TYPE1_ALPHA_TO_BETA_LETTERS,
  TYPE1_BETA_TO_ALPHA_LETTERS,
  TYPE1_BETA_TO_BETA_LETTERS,
  TYPE1_GAMMA_TO_GAMMA_LETTERS,
  type Type1LetterConfig,
  getType1LetterConfig,
} from "./Type1Configurations";

/**
 * Position system configuration for Type 1 letters
 */
interface PositionSystemConfig {
  letters: Record<string, Type1LetterConfig>;
  positionSystem: PositionSystem;
  timing: Timing;
  direction: Direction;
}

export class Type1Generator extends BaseType1Generator {
  private readonly positionSystemConfig: PositionSystemConfig;

  // All Type 1 position system configurations
  private static readonly POSITION_SYSTEM_CONFIGS: Record<
    string,
    PositionSystemConfig
  > = {
    alpha_to_alpha: {
      letters: TYPE1_ALPHA_TO_ALPHA_LETTERS,
      positionSystem: PositionSystem.ALPHA_TO_ALPHA,
      timing: Timing.SPLIT,
      direction: Direction.SAME,
    },
    beta_to_alpha: {
      letters: TYPE1_BETA_TO_ALPHA_LETTERS,
      positionSystem: PositionSystem.BETA_TO_ALPHA,
      timing: Timing.SPLIT,
      direction: Direction.OPP,
    },
    beta_to_beta: {
      letters: TYPE1_BETA_TO_BETA_LETTERS,
      positionSystem: PositionSystem.BETA_TO_BETA,
      timing: Timing.SPLIT,
      direction: Direction.SAME,
    },
    alpha_to_beta: {
      letters: TYPE1_ALPHA_TO_BETA_LETTERS,
      positionSystem: PositionSystem.ALPHA_TO_BETA,
      timing: Timing.SPLIT,
      direction: Direction.OPP,
    },
    gamma_to_gamma: {
      letters: TYPE1_GAMMA_TO_GAMMA_LETTERS,
      positionSystem: PositionSystem.GAMMA_TO_GAMMA,
      timing: Timing.SPLIT,
      direction: Direction.SAME,
    },
  };

  constructor(
    letter: string,
    patternService: import("../../../../../contracts/generation-interfaces").IPositionPatternService,
    positionCalculator: import("../../../../../contracts/generation-interfaces").IDirectionCalculator,
    validator: import("../../../../../contracts/generation-interfaces").IPictographValidatorService
  ) {
    // Convert string to Letter enum for internal use
    const letterEnum = letter as Letter;
    super(letterEnum, patternService, positionCalculator, validator);

    // Find which position system this letter belongs to
    const config = getType1LetterConfig(letter);
    if (!config) {
      throw new Error(`Letter ${letter} is not a Type 1 letter`);
    }

    // Find the position system configuration
    let foundConfig: PositionSystemConfig | null = null;
    for (const [, posConfig] of Object.entries(
      Type1Generator.POSITION_SYSTEM_CONFIGS
    )) {
      if (letterEnum in posConfig.letters) {
        foundConfig = posConfig;
        break;
      }
    }

    if (!foundConfig) {
      throw new Error(
        `No position system configuration found for letter ${letter}`
      );
    }

    this.positionSystemConfig = foundConfig;
  }

  /**
   * Get the letter configuration for this letter's position system
   */
  protected getLetterConfiguration(): Record<string, Type1LetterConfig> {
    return this.positionSystemConfig.letters;
  }

  /**
   * Get the position system for this letter
   */
  protected getPositionSystem(): PositionSystem {
    return this.positionSystemConfig.positionSystem;
  }

  /**
   * Get the position system name as a string for calculations
   */
  protected getPositionSystemName(): string {
    // Find the position system name by looking up the config
    for (const [posSystemName, config] of Object.entries(
      Type1Generator.POSITION_SYSTEM_CONFIGS
    )) {
      if (config === this.positionSystemConfig) {
        return posSystemName;
      }
    }
    throw new Error(`Position system name not found for letter ${this.letter}`);
  }

  /**
   * Get the timing for this letter's position system
   */
  protected getTiming(): Timing {
    return this.positionSystemConfig.timing;
  }

  /**
   * Get the direction for this letter's position system
   */
  protected getDirection(): Direction {
    return this.positionSystemConfig.direction;
  }

  /**
   * Get all supported Type 1 letters
   */
  static getSupportedLetters(): string[] {
    const allLetters: string[] = [];
    for (const config of Object.values(
      Type1Generator.POSITION_SYSTEM_CONFIGS
    )) {
      allLetters.push(...Object.keys(config.letters));
    }
    return allLetters;
  }

  /**
   * Check if a letter is a Type 1 letter
   */
  static supportsLetter(letter: string): boolean {
    return getType1LetterConfig(letter) !== null;
  }

  /**
   * Get letters for a specific position system
   */
  static getLettersForPositionSystem(positionSystem: string): string[] {
    const config = Type1Generator.POSITION_SYSTEM_CONFIGS[positionSystem];
    return config ? Object.keys(config.letters) : [];
  }

  /**
   * Get all position systems supported by Type 1
   */
  static getSupportedPositionSystems(): string[] {
    return Object.keys(Type1Generator.POSITION_SYSTEM_CONFIGS);
  }
}
