import { inject, injectable } from "inversify";
import { TYPES } from "$shared/inversify/types";
import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import type { BeatData } from "../../domain/models/BeatData";
import type { SequenceData } from "$shared/foundation/domain/models/SequenceData";
import type { IBetaDetectionService } from "$shared/pictograph/prop/services/contracts/IBetaDetectionService";
import type {
  ISequenceAnalysisService,
  CircularityAnalysis,
  CircularType,
  StrictCapType,
} from "../contracts/ISequenceAnalysisService";
import {
  QUARTERED_CAPS,
  HALVED_CAPS,
} from "$create/generate/circular/domain/constants/circular-position-maps";
import {
  VERTICAL_MIRROR_POSITION_MAP,
  SWAPPED_POSITION_MAP,
  COMPLEMENTARY_CAP_VALIDATION_SET,
} from "$create/generate/circular/domain/constants/strict-cap-position-maps";

/**
 * Sequence Analysis Service Implementation
 *
 * Analyzes sequences to detect circular patterns and CAP (Continuous Assembly Pattern) potential.
 *
 * Key Concepts:
 * - Circular sequences can be "autocompleted" by applying CAP transformations
 * - The start→end position relationship determines which CAP types are possible
 * - Uses predefined position maps (quartered, halved, mirrored, swapped, complementary)
 * - Intermediate pictographs are irrelevant - only start/end positions matter
 */
@injectable()
export class SequenceAnalysisService implements ISequenceAnalysisService {
  constructor(
    @inject(TYPES.IBetaDetectionService)
    private readonly betaDetectionService: IBetaDetectionService
  ) {}

  /**
   * Analyze a sequence for circular properties
   */
  analyzeCircularity(sequence: SequenceData): CircularityAnalysis {
    // Get start and end beats
    const startBeat = this.getStartBeat(sequence);
    const endBeat = this.getEndBeat(sequence);

    // Default non-circular result
    const defaultResult: CircularityAnalysis = {
      isCircular: false,
      circularType: null,
      startPosition: null,
      endPosition: null,
      startIsBeta: false,
      endIsBeta: false,
      possibleCapTypes: [],
      description: "Not circular",
    };

    // Check if we have valid start and end beats
    if (!startBeat || !endBeat) {
      return defaultResult;
    }

    // Get start and end positions
    const startPosition = startBeat.startPosition;
    const endPosition = endBeat.endPosition;

    if (!startPosition || !endPosition) {
      return defaultResult;
    }

    // Check if both positions are in the same position group
    const sameGroup = this.areSamePositionGroup(startPosition, endPosition);
    const startIsBeta = this.isBetaPosition(startPosition);
    const endIsBeta = this.isBetaPosition(endPosition);

    if (!sameGroup) {
      return {
        ...defaultResult,
        startPosition,
        endPosition,
        startIsBeta,
        endIsBeta,
        description: "Positions are not in the same position group",
      };
    }

    // Determine circular type
    const circularType = this.getCircularType(startPosition, endPosition);

    if (!circularType) {
      return {
        ...defaultResult,
        startPosition,
        endPosition,
        startIsBeta,
        endIsBeta,
        description: "Invalid circular relationship",
      };
    }

    // Get possible CAP types based on circular type
    const possibleCapTypes =
      this.getPossibleCapTypesForCircularType(circularType);

    return {
      isCircular: true,
      circularType,
      startPosition,
      endPosition,
      startIsBeta,
      endIsBeta,
      possibleCapTypes,
      description: this.buildCircularDescription(
        startPosition,
        endPosition,
        circularType
      ),
    };
  }

  /**
   * Check if a sequence is circular-capable (simple boolean check)
   */
  isCircularCapable(sequence: SequenceData): boolean {
    const analysis = this.analyzeCircularity(sequence);
    return analysis.isCircular;
  }

  /**
   * Get possible CAP types for a circular sequence
   */
  getPossibleCapTypes(sequence: SequenceData): readonly StrictCapType[] {
    const analysis = this.analyzeCircularity(sequence);
    return analysis.possibleCapTypes;
  }

  /**
   * Determine the circular relationship between two positions
   *
   * Uses the predefined transformation maps to check if the start→end pair
   * exists in any of the CAP validation sets:
   * - Same position → 'same' (complementary, mirrored, swapped)
   * - Quartered map → 'quartered' (90° rotation)
   * - Halved map → 'halved' (180° rotation)
   */
  getCircularType(
    startPosition: GridPosition,
    endPosition: GridPosition
  ): CircularType | null {
    const positionKey = `${startPosition},${endPosition}`;

    // Check if same position (complementary CAP)
    if (startPosition === endPosition) {
      return "same";
    }

    // Check quartered CAPs (90° rotation)
    if (QUARTERED_CAPS.has(positionKey)) {
      return "quartered";
    }

    // Check halved CAPs (180° rotation)
    if (HALVED_CAPS.has(positionKey)) {
      return "halved";
    }

    // Check mirrored positions (also 'same' type)
    if (VERTICAL_MIRROR_POSITION_MAP[startPosition] === endPosition) {
      return "same";
    }

    // Check swapped positions (also 'halved' type since alpha1→alpha5 is both)
    if (SWAPPED_POSITION_MAP[startPosition] === endPosition) {
      return "halved";
    }

    return null;
  }

  /**
   * Check if a position is a beta position
   */
  isBetaPosition(position: GridPosition): boolean {
    return this.betaDetectionService.isBetaPosition(position);
  }

  /**
   * Check if both positions are in the same position group
   */
  private areSamePositionGroup(
    pos1: GridPosition,
    pos2: GridPosition
  ): boolean {
    const info1 = this.extractPositionInfo(pos1);
    const info2 = this.extractPositionInfo(pos2);

    if (!info1 || !info2) return false;

    return info1.group === info2.group;
  }

  /**
   * Get the first beat with valid pictograph data (start beat)
   */
  getStartBeat(sequence: SequenceData): BeatData | null {
    if (!sequence.beats || sequence.beats.length === 0) {
      return null;
    }

    // Find first beat with a start position
    for (const beat of sequence.beats) {
      if (beat.startPosition && !beat.isBlank) {
        return beat;
      }
    }

    return null;
  }

  /**
   * Get the last beat with valid pictograph data (end beat)
   */
  getEndBeat(sequence: SequenceData): BeatData | null {
    if (!sequence.beats || sequence.beats.length === 0) {
      return null;
    }

    // Find last beat with an end position (iterate backwards)
    for (let i = sequence.beats.length - 1; i >= 0; i--) {
      const beat = sequence.beats[i]!;
      if (beat.endPosition && !beat.isBlank) {
        return beat ?? null;
      }
    }

    return null;
  }

  /**
   * Get a human-readable description of the circular relationship
   */
  getCircularDescription(analysis: CircularityAnalysis): string {
    return analysis.description;
  }

  /**
   * Detect the actual CAP type of a COMPLETED sequence
   *
   * Analyzes ALL consecutive beat transformations to determine what type
   * of completed CAP pattern the sequence represents.
   */
  detectCompletedCapTypes(sequence: SequenceData): readonly StrictCapType[] {
    if (!sequence.beats || sequence.beats.length === 0) {
      return [];
    }

    // Filter out blank beats
    const validBeats = sequence.beats.filter(
      (beat) => !beat.isBlank && beat.endPosition
    );

    if (validBeats.length === 0) {
      return [];
    }

    // Check 1: Static CAP - all beats at the same position
    const allSamePosition = validBeats.every(
      (beat) =>
        beat.startPosition === validBeats[0]!.startPosition &&
        beat.endPosition === validBeats[0]!.endPosition
    );

    if (allSamePosition) {
      return ["static"] as const;
    }

    // Build consecutive pairs: each beat's end → next beat's start
    const consecutivePairs: Array<{ from: GridPosition; to: GridPosition }> =
      [];

    for (let i = 0; i < validBeats.length; i++) {
      const currentBeat = validBeats[i]!;
      const nextBeat = validBeats[(i + 1) % validBeats.length]!; // Wrap around to first beat

      if (
        currentBeat &&
        nextBeat &&
        currentBeat.endPosition &&
        nextBeat.startPosition
      ) {
        consecutivePairs.push({
          from: currentBeat.endPosition,
          to: nextBeat.startPosition,
        });
      }
    }

    if (consecutivePairs.length === 0) {
      return [];
    }

    // Check 2: Rotated CAP - all consecutive pairs show 90° rotation
    const allQuartered = consecutivePairs.every((pair) => {
      const key = `${pair.from},${pair.to}`;
      return QUARTERED_CAPS.has(key);
    });

    if (allQuartered) {
      return ["rotated"] as const;
    }

    // Check 3: Mirrored CAP - all consecutive pairs show mirroring
    const allMirrored = consecutivePairs.every((pair) => {
      const key = `${pair.from},${pair.to}`;

      // Check halved caps (180° mirroring)
      if (HALVED_CAPS.has(key)) {
        return true;
      }

      // Check vertical mirror map
      if (VERTICAL_MIRROR_POSITION_MAP[pair.from] === pair.to) {
        return true;
      }

      // Check swapped positions
      if (SWAPPED_POSITION_MAP[pair.from] === pair.to) {
        return true;
      }

      // Check if same position (like alpha1 → alpha1 with mirrored turns)
      if (pair.from === pair.to) {
        return true;
      }

      return false;
    });

    if (allMirrored) {
      return ["mirrored"] as const;
    }

    // If none of the patterns match, return empty
    return [];
  }

  /**
   * Get possible CAP types based on circular type
   *
   * Mapping:
   * - 'same' → ['static']
   * - 'halved' → ['mirrored']
   * - 'quartered' → ['rotated']
   */
  private getPossibleCapTypesForCircularType(
    circularType: CircularType
  ): readonly StrictCapType[] {
    switch (circularType) {
      case "same":
        return ["static"] as const;
      case "halved":
        return ["mirrored"] as const;
      case "quartered":
        return ["rotated"] as const;
    }
  }

  /**
   * Build a human-readable description
   */
  private buildCircularDescription(
    startPosition: GridPosition,
    endPosition: GridPosition,
    circularType: CircularType
  ): string {
    const typeDescriptions: Record<CircularType, string> = {
      same: "Same position",
      halved: "Opposite/halved position (180°)",
      quartered: "Adjacent/quartered position (90°)",
    };

    const typeDesc = typeDescriptions[circularType];
    return `${typeDesc}: ${startPosition} → ${endPosition}`;
  }

  /**
   * Extract position group and number from a GridPosition
   */
  private extractPositionInfo(
    position: GridPosition
  ): { group: string; number: number; groupSize: number } | null {
    const positionStr = position.toString().toLowerCase();
    const match = positionStr.match(/^(alpha|beta|gamma)(\d+)$/);
    if (!match) return null;

    const group = match[1]!;
    const num = parseInt(match[2]!, 10);

    let groupSize: number;
    let maxNum: number;

    if (group === "alpha" || group === "beta") {
      groupSize = 8;
      maxNum = 8;
    } else if (group === "gamma") {
      groupSize = 16;
      maxNum = 16;
    } else {
      return null;
    }

    if (num < 1 || num > maxNum) {
      return null;
    }

    return { group, number: num, groupSize };
  }
}
