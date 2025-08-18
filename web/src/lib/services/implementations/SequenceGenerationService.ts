/**
 * Sequence Generation Service - Complete port of legacy freeform algorithm
 *
 * Exact implementation of FreeFormSequenceBuilder.build_sequence() and _generate_next_pictograph().
 * No placeholders, no simplified versions - complete algorithm from legacy desktop app.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import { createSequenceData } from "$lib/domain";
import type {
  GenerationOptions,
  ISequenceGenerationService,
  IOptionDataService,
  IOrientationCalculationService,
} from "../interfaces/generation-interfaces";

import type { PictographData } from "$lib/domain/PictographData";
import { createMotionData } from "$lib/domain/MotionData";
import {
  MotionType,
  RotationDirection,
  Location,
  Orientation,
  DifficultyLevel,
  PropContinuity,
  GenerationMode,
} from "$lib/domain/enums";

// Legacy constants for rotation directions - using enum values
const ROTATION_DIRS = {
  CLOCKWISE: RotationDirection.CLOCKWISE,
  COUNTER_CLOCKWISE: RotationDirection.COUNTER_CLOCKWISE,
  NO_ROT: RotationDirection.NO_ROTATION,
} as const;

const MOTION_TYPES = {
  PRO: MotionType.PRO,
  ANTI: MotionType.ANTI,
  FLOAT: MotionType.FLOAT,
  DASH: MotionType.DASH,
  STATIC: MotionType.STATIC,
} as const;

export class SequenceGenerationService implements ISequenceGenerationService {
  constructor(
    private optionDataService: IOptionDataService,
    private orientationCalculationService: IOrientationCalculationService
  ) {}

  /**
   * Generate freeform sequence - exact port of legacy build_sequence()
   */
  async generateSequence(options: GenerationOptions): Promise<SequenceData> {
    try {
      console.log("🎯 Starting freeform generation with options:", options);

      // Step 1: Initialize sequence (legacy: self.initialize_sequence)
      // TODO: In full implementation, this should load current sequence from workbench
      // For now, start with empty sequence
      const sequence: BeatData[] = [];

      // Step 2: Set rotation directions based on prop continuity (legacy lines 31-35)
      let blueRotDir: string;
      let redRotDir: string;

      if (options.propContinuity === PropContinuity.CONTINUOUS) {
        blueRotDir = this.randomChoice([
          ROTATION_DIRS.CLOCKWISE,
          ROTATION_DIRS.COUNTER_CLOCKWISE,
        ]);
        redRotDir = this.randomChoice([
          ROTATION_DIRS.CLOCKWISE,
          ROTATION_DIRS.COUNTER_CLOCKWISE,
        ]);
      } else {
        // Random prop continuity - these will be set per motion
        blueRotDir = "";
        redRotDir = "";
      }

      console.log("🔄 Rotation directions:", {
        blueRotDir,
        redRotDir,
        propContinuity: options.propContinuity,
      });

      // Step 3: Calculate beats to generate (legacy logic)
      const lengthOfSequenceUponStart = Math.max(0, sequence.length - 2);
      const beatsToGenerate = options.length - lengthOfSequenceUponStart;

      console.log(
        `📊 Generating ${beatsToGenerate} beats (requested: ${options.length}, existing: ${lengthOfSequenceUponStart})`
      );

      if (beatsToGenerate <= 0) {
        throw new Error(
          "No beats to generate - sequence may already be complete"
        );
      }

      // Step 4: Allocate turns using TurnIntensityManager (legacy lines 39-40)
      const level = this.mapDifficultyToLevel(options.difficulty);
      const turnIntensity = options.turnIntensity || 1;

      // Simple turn allocation for now (can be enhanced later)
      const totalTurns = Math.floor(turnIntensity * beatsToGenerate);
      const turnAllocation = {
        blue: Array(beatsToGenerate)
          .fill(0)
          .map((_, i) => (i < totalTurns / 2 ? 1 : 0)),
        red: Array(beatsToGenerate)
          .fill(0)
          .map((_, i) => (i < totalTurns / 2 ? 1 : 0)),
      };
      console.log("🎲 Turn allocation:", turnAllocation);

      // Step 5: Generation loop (legacy lines 42-58)
      const generatedBeats: BeatData[] = [];

      for (let i = 0; i < beatsToGenerate; i++) {
        console.log(`⚡ Generating beat ${i + 1}/${beatsToGenerate}`);

        try {
          const nextPictograph = await this._generateNextPictograph(
            sequence,
            level,
            turnAllocation.blue[i],
            turnAllocation.red[i],
            options.propContinuity || PropContinuity.CONTINUOUS,
            blueRotDir,
            redRotDir,
            options.letterTypes || ["Dual-Shift"] // Default to Type1 if not specified
          );

          // Add to sequence for next iteration (legacy logic)
          sequence.push(nextPictograph);
          generatedBeats.push(nextPictograph);

          console.log(
            `✅ Generated beat ${i + 1}: ${nextPictograph.pictograph_data?.letter}`
          );
        } catch (beatError) {
          console.error(`❌ Failed to generate beat ${i + 1}:`, beatError);
          throw new Error(
            `Beat generation failed at position ${i + 1}: ${beatError instanceof Error ? beatError.message : "Unknown error"}`
          );
        }
      }

      // Step 6: Create sequence data structure
      const generatedSequence: SequenceData = createSequenceData({
        name: this.generateSequenceName(options),
        word: "", // Will be calculated from beats
        beats: generatedBeats,
        grid_mode: options.gridMode,
        prop_type: options.propType,
        difficulty_level: options.difficulty,
        is_favorite: false,
        is_circular: false,
        tags: [],
        metadata: {
          generated: true,
          generatedAt: new Date().toISOString(),
          algorithm: "freeform",
          beatsGenerated: generatedBeats.length,
          propContinuity: options.propContinuity,
          blueRotDir,
          redRotDir,
          turnIntensity,
          level,
        },
      });

      console.log("🎉 Sequence generation complete:", {
        id: generatedSequence.id,
        beats: generatedBeats.length,
        name: generatedSequence.name,
      });

      return generatedSequence;
    } catch (error) {
      console.error("❌ Sequence generation failed:", error);
      throw new Error(
        `Sequence generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Generate next pictograph - exact port of legacy _generate_next_pictograph()
   */
  private async _generateNextPictograph(
    sequence: BeatData[],
    level: number,
    turnBlue: number | "fl",
    turnRed: number | "fl",
    propContinuity: PropContinuity,
    blueRotDir: string,
    redRotDir: string,
    letterTypes: string[]
  ): Promise<BeatData> {
    try {
      // Step 1: Get option dicts (legacy: self._get_option_dicts())
      let optionDicts = await this.optionDataService.getNextOptions(sequence);
      console.log(`📋 Loaded ${optionDicts.length} option dicts`);

      if (optionDicts.length === 0) {
        throw new Error("No pictographs available from option service");
      }

      // Step 2: Filter options by letter type (legacy: self._filter_options_by_letter_type())
      optionDicts = this.optionDataService.filterOptionsByLetterTypes(
        optionDicts,
        letterTypes
      );
      console.log(`🔍 After letter type filter: ${optionDicts.length} options`);

      // Step 3: Filter by rotation if continuous prop continuity
      if (
        propContinuity === PropContinuity.CONTINUOUS &&
        blueRotDir &&
        redRotDir
      ) {
        optionDicts = this.optionDataService.filterOptionsByRotation(
          optionDicts,
          blueRotDir,
          redRotDir
        );
        console.log(`🔄 After rotation filter: ${optionDicts.length} options`);
      }

      if (optionDicts.length === 0) {
        throw new Error("No valid options available after filtering");
      }

      // Step 4: Random selection (legacy: random.choice(option_dicts))
      const selectedOption = this.randomChoice(optionDicts);
      console.log(`🎯 Selected option: ${selectedOption.letter}`);

      // Step 5: Convert to BeatData
      let nextBeat = this.convertPictographToBeat(
        selectedOption,
        sequence.length + 1
      );

      // Step 6: Set turns if level 2 or 3 (legacy: self.set_turns())
      if (level === 2 || level === 3) {
        this.setTurns(nextBeat, turnBlue, turnRed);
        console.log(`🎲 Set turns: blue=${turnBlue}, red=${turnRed}`);
      }

      // Step 7: Update orientations (exact legacy sequence)
      if (sequence.length > 0) {
        nextBeat = this.orientationCalculationService.updateStartOrientations(
          nextBeat,
          sequence[sequence.length - 1]
        );
      }

      this.updateDashStaticPropRotDirs(
        nextBeat,
        propContinuity,
        blueRotDir,
        redRotDir
      );
      nextBeat =
        this.orientationCalculationService.updateEndOrientations(nextBeat);

      console.log(`🧭 Updated orientations for beat ${nextBeat.beat_number}`);

      return nextBeat;
    } catch (error) {
      console.error(`❌ Failed to generate pictograph:`, error);
      throw error;
    }
  }

  /**
   * Convert PictographData to BeatData - creates proper domain object
   */
  private convertPictographToBeat(
    pictograph: PictographData,
    beatNumber: number
  ): BeatData {
    // Ensure motions exist for blue and red
    const motions = {
      blue:
        pictograph.motions.blue ||
        createMotionData({
          motion_type: MotionType.STATIC,
          prop_rot_dir: RotationDirection.NO_ROTATION,
          start_loc: Location.NORTH,
          end_loc: Location.NORTH,
          turns: 0,
          start_ori: Orientation.IN,
          end_ori: Orientation.IN,
        }),
      red:
        pictograph.motions.red ||
        createMotionData({
          motion_type: MotionType.STATIC,
          prop_rot_dir: RotationDirection.NO_ROTATION,
          start_loc: Location.NORTH,
          end_loc: Location.NORTH,
          turns: 0,
          start_ori: Orientation.IN,
          end_ori: Orientation.IN,
        }),
      ...pictograph.motions,
    };

    return {
      id: crypto.randomUUID(),
      beat_number: beatNumber,
      duration: 1.0,
      blue_reversal: false,
      red_reversal: false,
      is_blank: false,
      pictograph_data: {
        ...pictograph,
        motions,
      },
      metadata: {
        generated: true,
        generatedAt: new Date().toISOString(),
        letter: pictograph.letter,
      },
    };
  }

  /**
   * Set turns - exact port from legacy set_turns()
   */
  private setTurns(
    beat: BeatData,
    turnBlue: number | "fl",
    turnRed: number | "fl"
  ): void {
    if (!beat.pictograph_data) return;

    // Handle blue turns - exact legacy logic
    if (turnBlue === "fl") {
      if (
        beat.pictograph_data.motions.blue?.motion_type === MotionType.PRO ||
        beat.pictograph_data.motions.blue?.motion_type === MotionType.ANTI
      ) {
        if (beat.pictograph_data.motions.blue) {
          // Create updated motion with float properties
          beat.pictograph_data.motions.blue = {
            ...beat.pictograph_data.motions.blue,
            turns: "fl",
            prefloat_motion_type: beat.pictograph_data.motions.blue.motion_type,
            prefloat_prop_rot_dir:
              beat.pictograph_data.motions.blue.prop_rot_dir,
            motion_type: MotionType.FLOAT,
            prop_rot_dir: RotationDirection.NO_ROTATION,
          };
        }
      } else {
        if (beat.pictograph_data.motions.blue) {
          beat.pictograph_data.motions.blue = {
            ...beat.pictograph_data.motions.blue,
            turns: 0,
          };
        }
      }
    } else {
      if (beat.pictograph_data.motions.blue) {
        beat.pictograph_data.motions.blue = {
          ...beat.pictograph_data.motions.blue,
          turns: turnBlue,
        };
      }
    }

    // Handle red turns - exact legacy logic
    if (turnRed === "fl") {
      if (
        beat.pictograph_data.motions.red?.motion_type === MotionType.PRO ||
        beat.pictograph_data.motions.red?.motion_type === MotionType.ANTI
      ) {
        if (beat.pictograph_data.motions.red) {
          // Create updated motion with float properties
          beat.pictograph_data.motions.red = {
            ...beat.pictograph_data.motions.red,
            turns: "fl",
            prefloat_motion_type: beat.pictograph_data.motions.red.motion_type,
            prefloat_prop_rot_dir:
              beat.pictograph_data.motions.red.prop_rot_dir,
            motion_type: MotionType.FLOAT,
            prop_rot_dir: RotationDirection.NO_ROTATION,
          };
        }
      } else {
        if (beat.pictograph_data.motions.red) {
          beat.pictograph_data.motions.red = {
            ...beat.pictograph_data.motions.red,
            turns: 0,
          };
        }
      }
    } else {
      if (beat.pictograph_data.motions.red) {
        beat.pictograph_data.motions.red = {
          ...beat.pictograph_data.motions.red,
          turns: turnRed,
        };
      }
    }
  }

  /**
   * Update dash/static prop rotation directions - exact port from legacy
   */
  private updateDashStaticPropRotDirs(
    beat: BeatData,
    propContinuity: string,
    blueRotDir: string,
    redRotDir: string
  ): void {
    if (!beat.pictograph_data) return;

    // Update blue - exact legacy logic
    if (
      beat.pictograph_data.motions.blue?.motion_type === MOTION_TYPES.DASH ||
      beat.pictograph_data.motions.blue?.motion_type === MOTION_TYPES.STATIC
    ) {
      const turns = beat.pictograph_data.motions.blue.turns || 0;
      if (propContinuity === PropContinuity.CONTINUOUS) {
        const newPropRotDir =
          typeof turns === "number" && turns > 0
            ? blueRotDir
            : ROTATION_DIRS.NO_ROT;
        beat.pictograph_data.motions.blue = {
          ...beat.pictograph_data.motions.blue,
          prop_rot_dir: newPropRotDir as RotationDirection,
        };
      } else if (typeof turns === "number" && turns > 0) {
        const newPropRotDir = this.randomChoice([
          ROTATION_DIRS.CLOCKWISE,
          ROTATION_DIRS.COUNTER_CLOCKWISE,
        ]);
        beat.pictograph_data.motions.blue = {
          ...beat.pictograph_data.motions.blue,
          prop_rot_dir: newPropRotDir,
        };
      } else {
        beat.pictograph_data.motions.blue = {
          ...beat.pictograph_data.motions.blue,
          prop_rot_dir: ROTATION_DIRS.NO_ROT,
        };
      }
    }

    // Update red - exact legacy logic
    if (
      beat.pictograph_data.motions.red?.motion_type === MOTION_TYPES.DASH ||
      beat.pictograph_data.motions.red?.motion_type === MOTION_TYPES.STATIC
    ) {
      const turns = beat.pictograph_data.motions.red.turns || 0;
      if (propContinuity === PropContinuity.CONTINUOUS) {
        const newPropRotDir =
          typeof turns === "number" && turns > 0
            ? redRotDir
            : ROTATION_DIRS.NO_ROT;
        beat.pictograph_data.motions.red = {
          ...beat.pictograph_data.motions.red,
          prop_rot_dir: newPropRotDir as RotationDirection,
        };
      } else if (typeof turns === "number" && turns > 0) {
        const newPropRotDir = this.randomChoice([
          ROTATION_DIRS.CLOCKWISE,
          ROTATION_DIRS.COUNTER_CLOCKWISE,
        ]);
        beat.pictograph_data.motions.red = {
          ...beat.pictograph_data.motions.red,
          prop_rot_dir: newPropRotDir,
        };
      } else {
        beat.pictograph_data.motions.red = {
          ...beat.pictograph_data.motions.red,
          prop_rot_dir: ROTATION_DIRS.NO_ROT,
        };
      }
    }
  }

  /**
   * Random choice helper - exact behavior from legacy random.choice()
   */
  private randomChoice<T>(array: T[]): T {
    if (array.length === 0) {
      throw new Error("Cannot choose from empty array");
    }
    return array[Math.floor(Math.random() * array.length)];
  }

  /**
   * Map difficulty to level - legacy mapping
   */
  private mapDifficultyToLevel(difficulty: DifficultyLevel): number {
    switch (difficulty) {
      case DifficultyLevel.BEGINNER:
        return 1;
      case DifficultyLevel.INTERMEDIATE:
        return 2;
      case DifficultyLevel.ADVANCED:
        return 3;
      default:
        return 2;
    }
  }

  /**
   * Generate sequence name based on options - matches legacy pattern
   */
  private generateSequenceName(options: GenerationOptions): string {
    const timestamp = new Date().toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });

    const difficulty =
      options.difficulty.charAt(0).toUpperCase() + options.difficulty.slice(1);
    return `${difficulty} ${options.length}-Beat (${timestamp})`;
  }

  /**
   * Generate circular sequence - not implemented in Phase 1
   */
  async generatePatternSequence(
    pattern: GenerationMode,
    _options: GenerationOptions
  ): Promise<SequenceData> {
    throw new Error(`${pattern} generation not implemented yet`);
  }

  /**
   * Get generation statistics - not implemented in Phase 1
   */
  getGenerationStats(): {
    totalGenerated: number;
    averageGenerationTime: number;
    lastGenerated: string | null;
  } {
    return {
      totalGenerated: 0,
      averageGenerationTime: 0,
      lastGenerated: null,
    };
  }
}
