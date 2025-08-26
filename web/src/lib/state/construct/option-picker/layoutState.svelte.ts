/**
 * Layout State - Pure Svelte 5 Runes
 *
 * Handles responsive layout configuration and calculations
 */

import type { ResponsiveLayoutConfig } from "./config";
import { getResponsiveLayout } from "./utils/layoutUtils";
import type { ContainerState } from "./containerState.svelte";
import type { DeviceState } from "./deviceState.svelte";

export interface LayoutState {
  layoutConfig: ResponsiveLayoutConfig;
}

export function createLayoutState(
  deviceState: DeviceState,
  containerState: ContainerState,
  optionsCount: number = 0
) {
  // Derived layout configuration using runes
  const layoutConfig = $derived(() => {
    return getResponsiveLayout(
      deviceState.deviceType,
      containerState.containerWidth,
      containerState.containerHeight
    );
  });

  return {
    // State accessors
    get layoutConfig() {
      return layoutConfig();
    },

    // Derived state object
    get state(): LayoutState {
      return {
        layoutConfig: layoutConfig(),
      };
    },
  };
}
