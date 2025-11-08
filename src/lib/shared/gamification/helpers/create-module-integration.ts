/**
 * Create Module Integration Helper
 *
 * Helper functions to integrate gamification into the Create module.
 * Import and use these in your Create Module Components.
 */

import { trackXP } from "../init/gamification-initializer";
import type { SequenceData } from "../../foundation/domain/models/SequenceData";

/**
 * Track sequence creation
 * Call this after a sequence is successfully created
 */
export async function trackSequenceCreated(
  sequence: SequenceData
): Promise<void> {
  const letters = sequence.word.split("");
  const beatCount = sequence.beats.length;

  await trackXP("sequence_created", {
    beatCount,
    letters,
    word: sequence.word,
    sequenceId: sequence.id,
  });

  console.log(
    `📝 Tracked sequence creation: ${sequence.word} (${beatCount} beats)`
  );
}

/**
 * Track sequence generation
 * Call this when user uses the Generate tab
 */
export async function trackSequenceGenerated(
  sequence: SequenceData
): Promise<void> {
  await trackXP("sequence_generated", {
    word: sequence.word,
    beatCount: sequence.beats.length,
  });

  console.log(`🎲 Tracked sequence generation: ${sequence.word}`);
}

/**
 * Example: How to integrate into ConstructTab
 *
 * In your ConstructTab.svelte or wherever sequences are created:
 *
 * ```typescript
 * import { trackSequenceCreated } from "$shared/gamification/helpers/create-module-integration";
 *
 * async function handleSequenceComplete(sequence: SequenceData) {
 *   // Your existing logic to save/display the sequence
 *   ...
 *
 *   // Track XP (won't block UI)
 *   trackSequenceCreated(sequence);
 * }
 * ```
 */

/**
 * Example: How to integrate into GenerateTab
 *
 * In your GenerateTab.svelte:
 *
 * ```typescript
 * import { trackSequenceGenerated } from "$shared/gamification/helpers/create-module-integration";
 *
 * async function handleGenerate() {
 *   const sequence = await generationService.generate(...);
 *
 *   // Your existing logic
 *   ...
 *
 *   // Track XP
 *   trackSequenceGenerated(sequence);
 * }
 * ```
 */
