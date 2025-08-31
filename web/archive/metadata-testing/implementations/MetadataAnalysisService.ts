// @ts-nocheck
/**
 * Metadata Analysis Service
 *
 * Analyzes extracted metadata for validation issues, inconsistencies,
 * and data integrity problems. Calculates health scores and statistics.
 */

import type {
  MetadataStats,
  InvalidMotionType,
  MetadataValidationIssue,
  MetadataTestingConfig,
  MetadataAnalysisResult,
} from "$lib/domain/metadata-testing/types";

export interface IMetadataAnalysisService {
  analyzeMetadata(
    metadata: Record<string, unknown>[],
    sequenceName?: string
  ): MetadataAnalysisResult;
  validateMotionTypes(metadata: Record<string, unknown>[]): InvalidMotionType[];
  calculateHealthScore(stats: MetadataStats): number;
}

export class MetadataAnalysisService implements IMetadataAnalysisService {
  private readonly config: MetadataTestingConfig = {
    validMotionTypes: ["pro", "anti", "static", "float", "dash"],
    requiredFields: ["letter"],
    healthScoreWeights: {
      authorWeight: 0.15,
      levelWeight: 0.15,
      startPositionWeight: 0.2,
      beatIntegrityWeight: 0.3,
      motionDataWeight: 0.2,
    },
  };

  analyzeMetadata(
    metadata: Record<string, unknown>[],
    sequenceName = ""
  ): MetadataAnalysisResult {
    console.log("🔍 Starting comprehensive metadata analysis...");

    if (!metadata || !Array.isArray(metadata)) {
      const emptyStats = this.createEmptyStats();
      return {
        sequenceName,
        stats: emptyStats,
        issues: { errors: {}, warnings: {} },
      };
    }

    // Separate start positions from real beats
    const startPositionEntries = metadata.filter(
      (step: Record<string, unknown>) => step.sequence_start_position
    );
    const realBeats = metadata.filter(
      (step: Record<string, unknown>) =>
        step.letter && !step.sequence_start_position
    );

    // Basic counts
    const basicStats = this.calculateBasicStats(
      metadata,
      realBeats,
      startPositionEntries
    );

    // Author analysis
    const authorStats = this.analyzeAuthor(metadata);

    // Level analysis
    const levelStats = this.analyzeLevel(metadata);

    // Start position analysis
    const startPositionStats = this.analyzeStartPosition(startPositionEntries);

    // Beat validation
    const beatValidation = this.validateBeats(realBeats);

    // Combine all stats
    const stats: MetadataStats = {
      ...basicStats,
      ...authorStats,
      ...levelStats,
      ...startPositionStats,
      ...beatValidation,
      healthScore: 0, // Will be calculated
      hasErrors: false, // Will be set below
      hasWarnings: false, // Will be set below
    };

    // Calculate health score
    stats.healthScore = this.calculateHealthScore(stats);

    // Set overall flags
    stats.hasErrors = stats.errorCount > 0;
    stats.hasWarnings = stats.warningCount > 0;

    console.log(`✅ Analysis complete. Health score: ${stats.healthScore}/100`);

    // Create issues structure for better reporting
    const issues = {
      errors: {
        motion: stats.invalidMotionTypes.map(
          (item) =>
            `Beat ${item.beat}: Invalid ${item.prop} motion type "${item.type}"`
        ),
        beats: stats.missingBeatNumbers.map(
          (beat) => `Missing beat number: ${beat}`
        ),
        structure: stats.invalidBeatStructure.map(
          (beat) => `Invalid structure at beat: ${beat}`
        ),
        duplicates: stats.duplicateBeats.map(
          (beat) => `Duplicate beat: ${beat}`
        ),
      },
      warnings: {
        metadata: [
          ...(stats.authorMissing ? ["Missing author information"] : []),
          ...(stats.levelMissing ? ["Missing level information"] : []),
          ...(stats.startPositionMissing ? ["Missing start position"] : []),
        ],
        data: stats.missingMotionData.map(
          (beat) => `Missing motion data at beat: ${beat}`
        ),
      },
    };

    return {
      sequenceName,
      stats,
      issues,
    };
  }

  validateMotionTypes(
    metadata: Record<string, unknown>[]
  ): InvalidMotionType[] {
    const invalidTypes: InvalidMotionType[] = [];

    metadata.forEach((beat: Record<string, unknown>, index: number) => {
      const beatNumber = index + 1;

      // Check blue motion
      if (beat.blueAttributes) {
        const blueMotion = (beat.blueAttributes as { motionType?: string })
          ?.motionType;
        if (blueMotion && !this.config.validMotionTypes.includes(blueMotion)) {
          invalidTypes.push({
            beat: beatNumber,
            prop: "blue",
            type: blueMotion,
          });
        }
      }

      // Check red motion
      if (beat.redAttributes) {
        const redMotion = (beat.redAttributes as { motionType?: string })
          ?.motionType;
        if (redMotion && !this.config.validMotionTypes.includes(redMotion)) {
          invalidTypes.push({
            beat: beatNumber,
            prop: "red",
            type: redMotion,
          });
        }
      }
    });

    return invalidTypes;
  }

  calculateHealthScore(stats: MetadataStats): number {
    const weights = this.config.healthScoreWeights;
    let totalScore = 0;

    // Author score (0-100)
    const authorScore = stats.hasAuthor && !stats.authorInconsistent ? 100 : 0;
    totalScore += authorScore * weights.authorWeight;

    // Level score (0-100)
    const levelScore =
      stats.hasLevel && !stats.levelInconsistent && !stats.levelZero ? 100 : 0;
    totalScore += levelScore * weights.levelWeight;

    // Start position score (0-100)
    const startPositionScore =
      stats.hasStartPosition && !stats.startPositionInconsistent ? 100 : 0;
    totalScore += startPositionScore * weights.startPositionWeight;

    // Beat integrity score (0-100)
    const beatIssues =
      stats.missingLetters.length +
      stats.duplicateBeats.length +
      stats.invalidBeatStructure.length;
    const beatIntegrityScore =
      stats.realBeatsCount > 0
        ? Math.max(0, 100 - (beatIssues / stats.realBeatsCount) * 100)
        : 0;
    totalScore += beatIntegrityScore * weights.beatIntegrityWeight;

    // Motion data score (0-100)
    const motionIssues =
      stats.missingMotionData.length + stats.invalidMotionTypes.length;
    const motionDataScore =
      stats.realBeatsCount > 0
        ? Math.max(0, 100 - (motionIssues / stats.realBeatsCount) * 100)
        : 0;
    totalScore += motionDataScore * weights.motionDataWeight;

    return Math.round(totalScore);
  }

  private createEmptyStats(): MetadataStats {
    return {
      totalBeats: 0,
      sequenceLength: 0,
      realBeatsCount: 0,
      startPositionCount: 0,
      hasAuthor: false,
      authorName: null,
      authorMissing: true,
      authorInconsistent: false,
      hasLevel: false,
      level: null,
      levelMissing: true,
      levelInconsistent: false,
      levelZero: false,
      hasStartPosition: false,
      startPositionMissing: true,
      startPositionInconsistent: false,
      startPositionValue: null,
      missingBeatNumbers: [],
      missingLetters: [],
      missingMotionData: [],
      invalidMotionTypes: [],
      duplicateBeats: [],
      invalidBeatStructure: [],
      missingRequiredFields: [],
      hasErrors: false,
      hasWarnings: false,
      errorCount: 0,
      warningCount: 0,
      healthScore: 0,
    };
  }

  private calculateBasicStats(
    metadata: Record<string, unknown>[],
    realBeats: Record<string, unknown>[],
    startPositionEntries: Record<string, unknown>[]
  ) {
    return {
      totalBeats: realBeats.length,
      sequenceLength: metadata.length,
      realBeatsCount: realBeats.length,
      startPositionCount: startPositionEntries.length,
    };
  }

  private analyzeAuthor(metadata: Record<string, unknown>[]) {
    const firstStep = metadata[0] || {};
    const hasAuthor = !!firstStep.author;
    const authorName = (firstStep.author as string) || null;

    // Check for author inconsistency
    const authorsFound = new Set(
      metadata
        .map((step: Record<string, unknown>) => step.author)
        .filter(Boolean)
    );

    return {
      hasAuthor,
      authorName,
      authorMissing: !hasAuthor,
      authorInconsistent: authorsFound.size > 1,
    };
  }

  private analyzeLevel(metadata: Record<string, unknown>[]) {
    const firstStep = metadata[0] || {};
    const hasLevel = firstStep.level !== undefined && firstStep.level !== null;
    const level = (firstStep.level as number) || null;

    // Check for level inconsistency
    const levelsFound = new Set(
      metadata
        .map((step: Record<string, unknown>) => step.level)
        .filter((l) => l !== undefined && l !== null)
    );

    return {
      hasLevel,
      level,
      levelMissing: !hasLevel,
      levelInconsistent: levelsFound.size > 1,
      levelZero: level === 0,
    };
  }

  private analyzeStartPosition(
    startPositionEntries: Record<string, unknown>[]
  ) {
    const hasStartPosition = startPositionEntries.length > 0;
    const startPositionValue =
      (startPositionEntries[0]?.sequence_start_position as string) || null;

    // Check for inconsistency
    const startPositionsFound = new Set(
      startPositionEntries.map(
        (step: Record<string, unknown>) => step.sequence_start_position
      )
    );

    return {
      hasStartPosition,
      startPositionMissing: !hasStartPosition,
      startPositionInconsistent: startPositionsFound.size > 1,
      startPositionValue,
    };
  }

  private validateBeats(realBeats: Record<string, unknown>[]) {
    const missingLetters: number[] = [];
    const missingMotionData: number[] = [];
    const duplicateBeats: number[] = [];
    const invalidBeatStructure: number[] = [];
    const missingRequiredFields: MetadataValidationIssue[] = [];

    const seenBeatNumbers = new Set<number>();

    realBeats.forEach((beat: Record<string, unknown>, index: number) => {
      const beatNumber = index + 1;

      // Check for missing letter
      if (!beat.letter) {
        missingLetters.push(beatNumber);
        missingRequiredFields.push({
          beat: beatNumber,
          field: "letter",
          type: "error",
          message: "Missing required letter field",
        });
      }

      // Check for duplicate beat numbers
      if (beat.beatNumber !== undefined) {
        const beatNum = beat.beatNumber as number;
        if (seenBeatNumbers.has(beatNum)) {
          duplicateBeats.push(beatNumber);
        }
        seenBeatNumbers.add(beatNum);
      }

      // Check motion data
      if (!beat.blueAttributes && !beat.redAttributes) {
        missingMotionData.push(beatNumber);
      }
    });

    // Validate motion types
    const invalidMotionTypes = this.validateMotionTypes(realBeats);

    // Calculate error/warning counts
    const errorCount =
      missingLetters.length +
      duplicateBeats.length +
      invalidBeatStructure.length;
    const warningCount = missingMotionData.length + invalidMotionTypes.length;

    return {
      missingBeatNumbers: [], // Not implemented in current logic
      missingLetters,
      missingMotionData,
      invalidMotionTypes,
      duplicateBeats,
      invalidBeatStructure,
      missingRequiredFields,
      errorCount,
      warningCount,
    };
  }
}

