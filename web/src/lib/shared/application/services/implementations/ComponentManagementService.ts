/**
 * Component Management Service Implementation
 * 
 * Handles loading state tracking and coordination for all sub-components
 * within complex UI components like Pictograph.
 */

import { injectable } from "inversify";
import type { PictographData, MotionColor } from "$shared";
import { MotionColor as MotionColorEnum } from "$shared";
import type { 
  IComponentManagementService, 
  ComponentLoadingState 
} from "../contracts/IComponentManagementService";

@injectable()
export class ComponentManagementService implements IComponentManagementService {
  /**
   * Calculate required components based on pictograph data
   */
  getRequiredComponents(data: PictographData | null): string[] {
    const components = ["grid"];

    if (!data) return components;

    // Check motion data for visible components
    if (data.motions?.[MotionColorEnum.BLUE]?.isVisible) {
      components.push("blue-arrow", "blue-prop");
    }
    if (data.motions?.[MotionColorEnum.RED]?.isVisible) {
      components.push("red-arrow", "red-prop");
    }

    return components;
  }

  /**
   * Create initial loading state for a set of components
   */
  createLoadingState(components: string[]): ComponentLoadingState {
    const loadingStates: Record<string, boolean> = {};
    components.forEach(component => {
      loadingStates[component] = true; // Start as loading
    });

    return {
      loadingStates,
      isLoading: components.length > 0,
      loadingComponents: [...components],
      loadedComponents: [],
    };
  }

  /**
   * Update loading state for a specific component
   */
  updateComponentLoadingState(
    state: ComponentLoadingState,
    componentName: string,
    isLoading: boolean
  ): ComponentLoadingState {
    const newLoadingStates = { ...state.loadingStates };
    newLoadingStates[componentName] = isLoading;

    const loadingComponents = Object.entries(newLoadingStates)
      .filter(([_, loading]) => loading)
      .map(([name]) => name);

    const loadedComponents = Object.entries(newLoadingStates)
      .filter(([_, loading]) => !loading)
      .map(([name]) => name);

    return {
      loadingStates: newLoadingStates,
      isLoading: loadingComponents.length > 0,
      loadingComponents,
      loadedComponents,
    };
  }

  /**
   * Check if all components have finished loading
   */
  areAllComponentsLoaded(state: ComponentLoadingState): boolean {
    return !state.isLoading;
  }

  /**
   * Get the overall loading progress as a percentage
   */
  getLoadingProgress(state: ComponentLoadingState): number {
    const totalComponents = Object.keys(state.loadingStates).length;
    if (totalComponents === 0) return 100;

    const loadedCount = state.loadedComponents.length;
    return Math.round((loadedCount / totalComponents) * 100);
  }

  /**
   * Clear all loading states
   */
  clearLoadingState(state: ComponentLoadingState): ComponentLoadingState {
    const clearedStates: Record<string, boolean> = {};
    Object.keys(state.loadingStates).forEach(component => {
      clearedStates[component] = false;
    });

    return {
      loadingStates: clearedStates,
      isLoading: false,
      loadingComponents: [],
      loadedComponents: Object.keys(clearedStates),
    };
  }
}
