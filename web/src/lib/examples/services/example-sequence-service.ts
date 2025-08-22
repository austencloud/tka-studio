/**
 * EXAMPLE: Pure Business Service (Clean Architecture)
 *
 * This demonstrates the CORRECT way to implement business services:
 *
 * ✅ Pure TypeScript (no Svelte dependencies)
 * ✅ Registered in DI container
 * ✅ Testable without UI framework
 * ✅ Single responsibility
 * ✅ Clear interfaces
 *
 * REPLACE PATTERN: Services with runes or Svelte dependencies
 * MIGRATION TARGET: Any service in src/lib/services/ with .svelte.ts extension
 */

import type { BeatData, SequenceData } from "$lib/domain";
import { GridMode, PropType } from "$lib/domain/enums";

// ============================================================================
// INTERFACES (Define contracts)
// ============================================================================

export interface IExampleSequenceService {
  createSequence(name: string, length: number): Promise<SequenceData>;
  validateSequence(sequence: SequenceData): Promise<ValidationResult>;
  calculateSequenceMetrics(sequence: SequenceData): SequenceMetrics;
}

export interface IValidationService {
  validateBeat(beat: BeatData): ValidationResult;
  validateSequenceLength(beats: BeatData[]): ValidationResult;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export interface SequenceMetrics {
  totalBeats: number;
  complexity: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  estimatedDuration: number;
}

// ============================================================================
// PURE BUSINESS SERVICE IMPLEMENTATION
// ============================================================================

export class ExampleSequenceService implements IExampleSequenceService {
  constructor(
    private validationService: IValidationService,
    private persistenceService: IPersistenceService
  ) {
    // Dependencies injected via DI container
    // NO runes, NO reactive state, NO Svelte imports
  }

  /**
   * Create a new sequence with validation
   */
  async createSequence(name: string, length: number): Promise<SequenceData> {
    // Input validation
    if (!name.trim()) {
      throw new Error("Sequence name is required");
    }

    if (length < 1 || length > 64) {
      throw new Error("Sequence length must be between 1 and 64 beats");
    }

    // Business logic - create beats
    const beats: BeatData[] = Array.from({ length }, (_, i) => ({
      id: crypto.randomUUID(),
      beatNumber: i + 1,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: true,
      metadata: {},
    }));

    // Create sequence domain object
    const sequence: SequenceData = {
      id: crypto.randomUUID(),
      name: name.trim(),
      word: name.trim().toUpperCase(),
      beats,
      thumbnails: [],
      sequenceLength: length,
      author: "Unknown",
      level: 1,
      dateAdded: new Date(),
      gridMode: GridMode.DIAMOND,
      propType: PropType.POI,
      isFavorite: false,
      isCircular: false,
      // startingPosition: TODO - needs to be BeatData, not string
      difficultyLevel: "beginner",
      tags: ["flow", "practice"],
      metadata: {
        created_by: "sequence_service",
        created_at: new Date().toISOString(),
      },
    };

    // Validate the created sequence
    const validation = await this.validateSequence(sequence);
    if (!validation.isValid) {
      throw new Error(`Invalid sequence: ${validation.errors.join(", ")}`);
    }

    // Persist using injected service
    await this.persistenceService.saveSequence(sequence);

    return sequence;
  }

  /**
   * Validate a complete sequence
   */
  async validateSequence(sequence: SequenceData): Promise<ValidationResult> {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Basic validation
    if (!sequence.name?.trim()) {
      errors.push("Sequence name is required");
    }

    if (sequence.beats.length === 0) {
      errors.push("Sequence must have at least one beat");
    }

    // Validate each beat using injected validation service
    for (const beat of sequence.beats) {
      const beatValidation = this.validationService.validateBeat(beat);
      errors.push(...beatValidation.errors);
      warnings.push(...beatValidation.warnings);
    }

    // Validate sequence structure
    const lengthValidation = this.validationService.validateSequenceLength([
      ...sequence.beats,
    ]);
    errors.push(...lengthValidation.errors);
    warnings.push(...lengthValidation.warnings);

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Calculate sequence complexity metrics
   */
  calculateSequenceMetrics(sequence: SequenceData): SequenceMetrics {
    const totalBeats = sequence.beats.length;

    // Calculate complexity based on non-blank beats and motion types
    let complexity = 0;
    for (const beat of sequence.beats) {
      if (!beat.isBlank) {
        complexity += 1;

        // Add complexity for motion types
        if (beat.pictographData?.motions) {
          const motions = Object.values(beat.pictographData.motions);
          complexity +=
            motions.filter(
              (motion) =>
                typeof motion === "object" && motion?.motionType !== "static"
            ).length * 0.5;
        }
      }
    }

    // Determine difficulty
    let difficulty: "beginner" | "intermediate" | "advanced" = "beginner";
    if (complexity > totalBeats * 0.7) {
      difficulty = "advanced";
    } else if (complexity > totalBeats * 0.3) {
      difficulty = "intermediate";
    }

    // Estimate duration (assuming 120 BPM)
    const estimatedDuration = (totalBeats * 60) / 120; // seconds

    return {
      totalBeats,
      complexity: Math.round(complexity * 10) / 10,
      difficulty,
      estimatedDuration,
    };
  }
}

// ============================================================================
// DI REGISTRATION EXAMPLE
// ============================================================================

/**
 * How to register this service in the DI container:
 *
 * ```typescript
 * // In src/lib/services/di/registration/example-services.ts
 * import { ExampleSequenceService } from '$lib/examples/services/example-sequence-service';
 *
 * export async function registerExampleServices(container: ServiceContainer) {
 *   container.register('IExampleSequenceService', (c) =>
 *     new ExampleSequenceService(
 *       c.resolve('IValidationService'),
 *       c.resolve('IPersistenceService')
 *     )
 *   );
 * }
 * ```
 *
 * How to use in components:
 *
 * ```svelte
 * <script lang="ts">
 *   import { resolve } from '$services/bootstrap';
 *
 *   const sequenceService = resolve('IExampleSequenceService');
 *
 *   async function createNewSequence() {
 *     const sequence = await sequenceService.createSequence('My Sequence', 16);
 *     console.log('Created:', sequence);
 *   }
 * </script>
 * ```
 */

// Type for DI container resolution
export type ExampleSequenceServiceType = ExampleSequenceService;

// Import for persistence service (would be defined elsewhere)
interface IPersistenceService {
  saveSequence(sequence: SequenceData): Promise<void>;
  loadSequence(id: string): Promise<SequenceData | null>;
}
