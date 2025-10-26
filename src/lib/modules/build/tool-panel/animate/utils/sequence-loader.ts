/**
 * Sequence Loading Utility
 *
 * Handles loading and preparing sequence data for animation.
 * Works with both pre-loaded sequences (from Build tab) and sequences
 * that need to be loaded from the service.
 */

import type { ISequenceService } from "$build/shared";
import type { SequenceData } from "$shared";

export interface SequenceLoadResult {
  success: boolean;
  sequence: SequenceData | null;
  error: string | null;
}

/**
 * Load sequence data, handling both working sequences and database sequences
 * @param sequence The sequence to load (may be partial or complete)
 * @param sequenceService Service to load full sequence data if needed
 * @returns Load result with sequence data or error
 */
export async function loadSequenceForAnimation(
  sequence: SequenceData | null,
  sequenceService: ISequenceService
): Promise<SequenceLoadResult> {
  if (!sequence) {
    return {
      success: false,
      sequence: null,
      error: "No sequence provided",
    };
  }

  try {
    let fullSequence = sequence;

    // Check if sequence needs to be loaded from database
    const needsLoading =
      sequence.id && (!sequence.beats || sequence.beats.length === 0);

    if (needsLoading) {
      // Load from service using word or id
      const sequenceIdentifier = sequence.word || sequence.id.toUpperCase();
      console.log("🎬 Loading sequence from service:", sequenceIdentifier);

      const loadedSequence =
        await sequenceService.getSequence(sequenceIdentifier);

      if (!loadedSequence) {
        return {
          success: false,
          sequence: null,
          error: `Sequence not found: ${sequenceIdentifier}`,
        };
      }

      fullSequence = loadedSequence;
    } else {
      // Working sequence from Build tab - use directly
      console.log(
        "🎬 Using working sequence directly:",
        sequence.beats?.length || 0,
        "beats"
      );
    }

    // Log sequence data for debugging
    console.log("✅ Sequence loaded for animation:", {
      id: fullSequence.id,
      name: fullSequence.name,
      beatCount: fullSequence.beats?.length || 0,
    });

    // Debug logging for critical motion types
    if (fullSequence.beats) {
      fullSequence.beats.forEach((beat, index) => {
        const letter = beat?.letter;
        if (letter === "L" || letter === "F") {
          console.log(`🔍 Beat ${index + 1} (${letter}):`, {
            blue_motion: beat?.motions?.blue?.motionType,
            red_motion: beat?.motions?.red?.motionType,
          });
        }
      });
    }

    return {
      success: true,
      sequence: fullSequence,
      error: null,
    };
  } catch (err) {
    console.error("❌ Failed to load sequence:", err);
    return {
      success: false,
      sequence: null,
      error: err instanceof Error ? err.message : "Failed to load sequence",
    };
  }
}
