/**
 * Learn Module Integration Helper
 *
 * Helper functions to integrate gamification into the Learn module.
 */

import { trackXP } from "../init/gamification-initializer";

/**
 * Track concept completion
 * Call this when user completes a concept
 */
export async function trackConceptLearned(conceptId: string): Promise<void> {
  await trackXP("concept_learned", {
    conceptId,
    timestamp: Date.now(),
  });

  console.log(`📚 Tracked concept completion: ${conceptId}`);
}

/**
 * Track drill completion
 * Call this when user completes a drill/quiz
 */
export async function trackDrillCompleted(
  drillId: string,
  score?: number
): Promise<void> {
  await trackXP("drill_completed", {
    drillId,
    score,
    timestamp: Date.now(),
  });

  console.log(`🎯 Tracked drill completion: ${drillId} (score: ${score || "N/A"})`);
}

/**
 * Example: How to integrate into Learn/Concepts
 *
 * In your ConceptCard.svelte or similar:
 *
 * ```typescript
 * import { trackConceptLearned } from "$shared/gamification/helpers/learn-module-integration";
 *
 * async function handleConceptComplete(conceptId: string) {
 *   // Your existing logic (mark as complete, save progress, etc.)
 *   ...
 *
 *   // Track XP
 *   trackConceptLearned(conceptId);
 * }
 * ```
 */

/**
 * Example: How to integrate into Drills
 *
 * In your DrillSession.svelte:
 *
 * ```typescript
 * import { trackDrillCompleted } from "$shared/gamification/helpers/learn-module-integration";
 *
 * async function handleDrillComplete(score: number) {
 *   // Your existing logic
 *   ...
 *
 *   // Track XP
 *   trackDrillCompleted(currentDrillId, score);
 * }
 * ```
 */
