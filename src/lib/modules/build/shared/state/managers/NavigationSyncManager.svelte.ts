/**
 * Navigation Sync Manager
 *
 * Consolidates navigation synchronization effects into a single manager.
 * Handles bidirectional sync between navigation state and build tab state.
 *
 * Domain: Build Module - Navigation State Management
 */

import type { INavigationSyncService } from "../../services/contracts";
import type { createBuildTabState as BuildTabStateType } from "../build-tab-state.svelte";
import { navigationState } from "$shared";

type BuildTabState = ReturnType<typeof BuildTabStateType>;
type NavigationState = typeof navigationState;

export interface NavigationSyncManagerConfig {
  buildTabState: BuildTabState;
  navigationState: NavigationState;
  navigationSyncService: INavigationSyncService;
}

/**
 * Creates navigation sync effects
 * @returns Cleanup function
 */
export function createNavigationSyncEffects(config: NavigationSyncManagerConfig): () => void {
  const { buildTabState, navigationState, navigationSyncService } = config;

  // Effect: Sync navigation state TO build tab state
  const cleanup1 = $effect.root(() => {
    $effect(() => {
      navigationSyncService.syncNavigationToBuildTab(
        buildTabState,
        navigationState
      );
    });
  });

  // Effect: Sync build tab state BACK to navigation state
  const cleanup2 = $effect.root(() => {
    $effect(() => {
      if (buildTabState.isUpdatingFromToggle) return;

      navigationSyncService.syncBuildTabToNavigation(
        buildTabState,
        navigationState
      );
    });
  });

  return () => {
    cleanup1();
    cleanup2();
  };
}
