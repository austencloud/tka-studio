/**
 * Navigation Sync Manager
 *
 * Consolidates navigation synchronization effects into a single manager.
 * Handles bidirectional sync between navigation state and Create Module State.
 *
 * Domain: Create module - Navigation State Management
 */

import type { INavigationSyncService } from "../../services/contracts";
import type { createCreateModuleState as CreateModuleStateType } from "../create-module-state.svelte";
import { navigationState } from "$shared";

type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
type NavigationState = typeof navigationState;

export interface NavigationSyncManagerConfig {
  CreateModuleState: CreateModuleState;
  navigationState: NavigationState;
  navigationSyncService: INavigationSyncService;
}

/**
 * Creates navigation sync effects
 * @returns Cleanup function
 */
export function createNavigationSyncEffects(
  config: NavigationSyncManagerConfig
): () => void {
  const { CreateModuleState, navigationState, navigationSyncService } = config;

  // Effect: Sync navigation state TO Create Module State
  const cleanup1 = $effect.root(() => {
    $effect(() => {
      navigationSyncService.syncNavigationToCreateModule(
        CreateModuleState,
        navigationState
      );
    });
  });

  // Effect: Sync Create Module State BACK to navigation state
  const cleanup2 = $effect.root(() => {
    $effect(() => {
      if (CreateModuleState.isUpdatingFromToggle) return;

      navigationSyncService.syncCreateModuleToNavigation(
        CreateModuleState,
        navigationState
      );
    });
  });

  return () => {
    cleanup1();
    cleanup2();
  };
}
