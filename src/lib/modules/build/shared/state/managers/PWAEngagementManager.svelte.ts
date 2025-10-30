/**
 * PWA Engagement Manager
 *
 * Tracks PWA engagement when user creates a sequence.
 * Consolidates PWA tracking logic from BuildTab.svelte.
 *
 * Domain: Build Module - PWA Engagement Tracking
 */

import { createComponentLogger, resolve, TYPES } from "$shared";
import type { createBuildTabState as BuildTabStateType } from "../build-tab-state.svelte";

type BuildTabState = ReturnType<typeof BuildTabStateType>;

const logger = createComponentLogger('PWAEngagementManager');

export interface PWAEngagementConfig {
  buildTabState: BuildTabState;
}

/**
 * Creates PWA engagement tracking effect
 * @returns Cleanup function
 */
export function createPWAEngagementEffect(config: PWAEngagementConfig): () => void {
  const { buildTabState } = config;
  let hasTrackedSequenceCreation = false;

  return $effect.root(() => {
    $effect(() => {
      if (hasTrackedSequenceCreation) return;
      if (!buildTabState.hasSequence) return;

      try {
        const engagementService = resolve(TYPES.IPWAEngagementService) as any;
        engagementService?.recordSequenceCreated?.();
        engagementService?.recordInteraction?.(); // Also count as interaction
        hasTrackedSequenceCreation = true;
        logger.log("PWA engagement: sequence created");
      } catch (error) {
        // Service may not be available, that's ok
      }
    });
  });
}
