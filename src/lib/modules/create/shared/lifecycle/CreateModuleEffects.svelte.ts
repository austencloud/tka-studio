/**
 * Consolidated effect coordination for CreateModule
 * All reactive effects in one manageable place
 */

import { navigationState } from "$shared";
import type { LayoutConfiguration } from "../orchestration/types";

export interface EffectConfig {
  CreateModuleState: any;
  constructTabState?: any;
  layoutService: any;
  onTabAccessibilityChange?: (canAccess: boolean) => void;
}

export function createCreateModuleEffects(config: EffectConfig) {
  const { CreateModuleState, layoutService, onTabAccessibilityChange } = config;

  let layoutConfig = $state<LayoutConfiguration | null>(null);

  // Effect 1: Tab accessibility notification
  $effect(() => {
    if (!CreateModuleState) return;

    const canAccess = CreateModuleState.canAccessEditTab;
    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Effect 2: Navigation → CreateModule sync
  $effect(() => {
    if (!CreateModuleState) return;

    const currentMode = navigationState.currentSection;
    const CreateModuleCurrentMode = CreateModuleState.activeSection;

    if (
      currentMode !== CreateModuleCurrentMode &&
      CreateModuleState.isPersistenceInitialized &&
      !CreateModuleState.isNavigatingBack
    ) {
      // Note: No need to guard navigation anymore - only construct and generate exist
      // and both are always accessible. Animate and share are separate panels now.

      CreateModuleState.setactiveToolPanel(currentMode as any);
    }
  });

  // Effect 3: CreateModule → Navigation sync
  $effect(() => {
    if (!CreateModuleState) return;

    const CreateModuleCurrentMode = CreateModuleState.activeSection;
    const navCurrentMode = navigationState.currentSection;

    if (CreateModuleCurrentMode && CreateModuleCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSection(CreateModuleCurrentMode);
    }
  });

  // Effect 4: Layout tracking
  $effect(() => {
    if (!layoutService) return;

    layoutConfig = layoutService.calculateLayout();

    const unsubscribe = layoutService.onLayoutChange(
      (config: LayoutConfiguration) => {
        layoutConfig = config;
      }
    );

    return unsubscribe;
  });

  return {
    get layoutConfig() {
      return layoutConfig;
    },
  };
}
