/**
 * Explore Module Integration Helper
 *
 * Helper functions to integrate gamification into the Explore module.
 */

import { trackXP } from "../init/gamification-initializer";

/**
 * Track sequence exploration
 * Call this when user views a sequence in the gallery
 *
 * Note: To prevent spam, consider throttling this (e.g., only track once per sequence per session)
 */
let exploredSequences = new Set<string>();

export async function trackSequenceExplored(
  sequenceId: string,
  shouldThrottle: boolean = true
): Promise<void> {
  // Throttle: only track once per sequence per session
  if (shouldThrottle && exploredSequences.has(sequenceId)) {
    return;
  }

  await trackXP("sequence_explored", {
    sequenceId,
    timestamp: Date.now(),
  });

  exploredSequences.add(sequenceId);

  console.log(`🔍 Tracked sequence exploration: ${sequenceId}`);
}

/**
 * Reset explored sequences (e.g., when user navigates away)
 */
export function resetExploredSequences(): void {
  exploredSequences.clear();
}

/**
 * Example: How to integrate into Explore/Browse
 *
 * In your SequenceCard.svelte or ExploreGrid.svelte:
 *
 * ```typescript
 * import { trackSequenceExplored } from "$shared/gamification/helpers/explore-module-integration";
 *
 * async function handleSequenceClick(sequence: SequenceData) {
 *   // Your existing logic (open spotlight, etc.)
 *   ...
 *
 *   // Track XP (throttled - only once per sequence)
 *   trackSequenceExplored(sequence.id);
 * }
 * ```
 */

/**
 * Alternative: Track on Spotlight Open
 *
 * In your SpotlightViewer.svelte:
 *
 * ```typescript
 * import { trackSequenceExplored } from "$shared/gamification/helpers/explore-module-integration";
 *
 * $effect(() => {
 *   if (spotlightSequence) {
 *     trackSequenceExplored(spotlightSequence.id);
 *   }
 * });
 * ```
 */
