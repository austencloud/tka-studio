/**
 * Consolidated effect coordination for BuildTab
 * All reactive effects in one manageable place
 */

import type { PictographData } from "$shared";
import { navigationState } from "$shared";
import type { LayoutConfiguration } from "../orchestration/types";

export interface EffectConfig {
  buildTabState: any;
  constructTabState: any;
  layoutService: any;
  onTabAccessibilityChange?: (canAccess: boolean) => void;
}

export function createBuildTabEffects(config: EffectConfig) {
  const { buildTabState, constructTabState, layoutService, onTabAccessibilityChange } = config;

  let layoutConfig = $state<LayoutConfiguration | null>(null);

  // Effect 1: Tab accessibility notification
  $effect(() => {
    if (!buildTabState) return;

    const canAccess = buildTabState.canAccessEditTab;
    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Effect 2: Navigation → BuildTab sync
  $effect(() => {
    if (!buildTabState) return;

    const currentMode = navigationState.currentSubMode;
    const buildTabCurrentMode = buildTabState.activeSubTab;

    if (
      currentMode !== buildTabCurrentMode &&
      buildTabState.isPersistenceInitialized &&
      !buildTabState.isNavigatingBack
    ) {
      // Guard: Prevent navigation to tabs without a valid sequence
      if (
        (currentMode === "edit" ||
          currentMode === "animate" ||
          currentMode === "share" ||
          currentMode === "record") &&
        !buildTabState.canAccessEditTab
      ) {
        console.warn(`Cannot access ${currentMode} tab without sequence`);
        navigationState.setCurrentSubMode("construct");
        return;
      }

      buildTabState.setactiveToolPanel(currentMode as any);
    }
  });

  // Effect 3: BuildTab → Navigation sync
  $effect(() => {
    if (!buildTabState) return;

    const buildTabCurrentMode = buildTabState.activeSubTab;
    const navCurrentMode = navigationState.currentSubMode;

    if (buildTabCurrentMode && buildTabCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSubMode(buildTabCurrentMode);
    }
  });

  // Effect 4: Layout tracking
  $effect(() => {
    if (!layoutService) return;

    layoutConfig = layoutService.calculateLayout();

    const unsubscribe = layoutService.onLayoutChange((config: LayoutConfiguration) => {
      layoutConfig = config;
    });

    return unsubscribe;
  });

  // Effect 5: Start position event handling
  $effect(() => {
    if (!constructTabState || typeof window === "undefined") return;

    const handleStartPositionSelected: EventListener = (event) => {
      const customEvent = event as CustomEvent<{ startPosition?: PictographData }>;
      const pictographData = customEvent.detail?.startPosition;

      if (pictographData) {
        constructTabState.handleStartPositionSelected(pictographData);
      }
    };

    window.addEventListener("start-position-selected", handleStartPositionSelected);

    return () => {
      window.removeEventListener("start-position-selected", handleStartPositionSelected);
    };
  });

  return {
    get layoutConfig() {
      return layoutConfig;
    },
  };
}
