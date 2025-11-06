/**
 * ICreateModuleEffectCoordinator.ts
 *
 * Service interface for coordinating all reactive effects in CreateModule.
 * Centralizes effect setup to reduce complexity in the component.
 *
 * Domain: Create module - Effect Orchestration
 */

import type { NavigationState } from "$shared/navigation/state/navigation-state.svelte";
import type { CreateModuleState } from "../../state/create-module-state.svelte";
import type { ConstructTabState } from "../../state/construct-tab-state.svelte";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type { IResponsiveLayoutService } from "./IResponsiveLayoutService";
import type { INavigationSyncService } from "./INavigationSyncService";

/**
 * Configuration for CreateModule effects
 */
export interface CreateModuleEffectConfig {
  CreateModuleState: CreateModuleState;
  constructTabState: ConstructTabState;
  panelState: PanelCoordinationState;
  navigationState: NavigationState;
  layoutService: IResponsiveLayoutService;
  navigationSyncService: INavigationSyncService;
  hasSelectedCreationMethod: () => boolean;
  onLayoutChange: (shouldUseSideBySideLayout: boolean) => void;
  onCurrentWordChange?: (word: string) => void;
  toolPanelElement: HTMLElement | null;
  buttonPanelElement: HTMLElement | null;
}

/**
 * Service for coordinating all reactive effects in CreateModule
 */
export interface ICreateModuleEffectCoordinator {
  /**
   * Set up all reactive effects for CreateModule
   * @param config Configuration object containing all dependencies
   * @returns Cleanup function to dispose all effects
   */
  setupEffects(config: CreateModuleEffectConfig): () => void;
}
