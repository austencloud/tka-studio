/**
 * CreateModuleEffectCoordinator.ts
 *
 * Service implementation for coordinating all reactive effects in CreateModule.
 * Centralizes effect setup to reduce complexity in the component.
 *
 * Domain: Create module - Effect Orchestration
 */

import { injectable } from "inversify";
import type {
  ICreateModuleEffectCoordinator,
  CreateModuleEffectConfig,
} from "../contracts/ICreateModuleEffectCoordinator";
import {
  createAutoEditPanelEffect,
  createCurrentWordDisplayEffect,
  createLayoutEffects,
  createNavigationSyncEffects,
  createPanelHeightTracker,
  createPWAEngagementEffect,
  createSingleBeatEditEffect,
} from "../../state/managers";

@injectable()
export class CreateModuleEffectCoordinator
  implements ICreateModuleEffectCoordinator
{
  /**
   * Set up all reactive effects for CreateModule
   * Coordinates:
   * - Navigation synchronization
   * - Responsive layout management
   * - Auto edit panel behavior
   * - Single beat edit mode
   * - PWA engagement tracking
   * - Current word display updates
   * - Panel height tracking
   */
  setupEffects(config: CreateModuleEffectConfig): () => void {
    const {
      CreateModuleState,
      constructTabState,
      panelState,
      navigationState,
      layoutService,
      navigationSyncService,
      hasSelectedCreationMethod,
      onLayoutChange,
      onCurrentWordChange,
      toolPanelElement,
      buttonPanelElement,
    } = config;

    const cleanups: (() => void)[] = [];

    // Navigation sync effects
    const navigationCleanup = createNavigationSyncEffects({
      CreateModuleState,
      navigationState,
      navigationSyncService,
    });
    cleanups.push(navigationCleanup);

    // Layout effects
    const layoutCleanup = createLayoutEffects({
      layoutService,
      onLayoutChange,
    });
    cleanups.push(layoutCleanup);

    // Auto edit panel effects
    const autoEditCleanup = createAutoEditPanelEffect({
      CreateModuleState,
      panelState,
    });
    cleanups.push(autoEditCleanup);

    // Single beat edit effects
    const singleBeatCleanup = createSingleBeatEditEffect({
      CreateModuleState,
      panelState,
    });
    cleanups.push(singleBeatCleanup);

    // PWA engagement tracking
    const pwaCleanup = createPWAEngagementEffect({ CreateModuleState });
    cleanups.push(pwaCleanup);

    // Current word display effects (if callback provided)
    if (onCurrentWordChange) {
      const currentWordCleanup = createCurrentWordDisplayEffect({
        CreateModuleState,
        constructTabState,
        hasSelectedCreationMethod,
        onCurrentWordChange,
      });
      cleanups.push(currentWordCleanup);
    }

    // Panel height tracking (if elements are available)
    if (toolPanelElement || buttonPanelElement) {
      const panelHeightCleanup = createPanelHeightTracker({
        toolPanelElement,
        buttonPanelElement,
        panelState,
      });
      cleanups.push(panelHeightCleanup);
    }

    // Return combined cleanup function
    return () => {
      cleanups.forEach((cleanup) => cleanup());
    };
  }
}
