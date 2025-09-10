/**
 * Pictograph State Management - Svelte 5 runes
 *
 * Reactive state management for pictograph rendering and arrow positioning.
 * Wraps pictograph services with runes for UI reactivity.
 * Follows TKA architecture: services handle business logic, runes handle reactivity.
 */

import type {
  IComponentManagementService,
  IDataTransformationService,
  MotionColor,
  MotionData,
  PictographData
} from "$shared";
import { resolve, TYPES } from "$shared";
import type { ArrowAssets } from "../../arrow/orchestration/domain/arrow-models";
import type { PropAssets, PropPosition } from "../../prop/domain/models";

export interface PictographState {
  // Data state
  readonly effectivePictographData: PictographData | null;
  readonly hasValidData: boolean;
  readonly displayLetter: string | null;
  readonly motionsToRender: Array<{ color: MotionColor; motionData: MotionData }>;
  readonly requiredComponents: string[];

  // Arrow positioning state
  readonly arrowPositions: Record<string, { x: number; y: number; rotation: number }>;
  readonly arrowMirroring: Record<string, boolean>;
  readonly arrowAssets: Record<string, ArrowAssets>;
  readonly showArrows: boolean;

  // Prop positioning state
  readonly propPositions: Record<string, PropPosition>;
  readonly propAssets: Record<string, PropAssets>;
  readonly showProps: boolean;

  // Loading state
  readonly isLoading: boolean;
  readonly isLoaded: boolean;
  readonly errorMessage: string | null;
  readonly loadedComponents: Set<string>;
  readonly allComponentsLoaded: boolean;

  // Actions
  calculateArrowPositions(): Promise<void>;
  calculatePropPositions(): Promise<void>;
  handleComponentLoaded(componentName: string): void;
  handleComponentError(componentName: string, error: string): void;
  clearLoadingState(): void;
  updatePictographData(newData: PictographData | null): void;
}

/**
 * Creates reactive state for pictograph rendering and management
 */
export function createPictographState(
  initialPictographData: PictographData | null = null
): PictographState {
  // Get services from DI container
  const dataTransformationService = resolve(TYPES.IDataTransformationService) as IDataTransformationService;
  const componentManagementService = resolve(TYPES.IComponentManagementService) as IComponentManagementService;
  const arrowLifecycleManager = resolve(TYPES.IArrowLifecycleManager) as import("../../arrow/orchestration/services/contracts/IArrowLifecycleManager").IArrowLifecycleManager;
  const propLifecycleManager = resolve(TYPES.IPropLifecycleManager) as import("../../prop/services/contracts/IPropLifecycleManager").IPropLifecycleManager;

  // Input data state
  let pictographData = $state<PictographData | null>(initialPictographData);

  // Component loading state
  let errorMessage = $state<string | null>(null);
  let loadedComponents = $state(new Set<string>());

  // Arrow positioning state
  let arrowPositions = $state<Record<string, { x: number; y: number; rotation: number }>>({});
  let arrowMirroring = $state<Record<string, boolean>>({});
  let arrowAssets = $state<Record<string, ArrowAssets>>({});
  let showArrows = $state(false);

  // Prop positioning state
  let propPositions = $state<Record<string, PropPosition>>({});
  let propAssets = $state<Record<string, PropAssets>>({});
  let showProps = $state(false);

  // Derived data transformation state
  const dataState = $derived(() => dataTransformationService.transformPictographData(pictographData));

  // Derived component requirements
  const requiredComponents = $derived(() => componentManagementService.getRequiredComponents(pictographData));

  // Derived loading states
  const allComponentsLoaded = $derived(() => {
    return requiredComponents().every((component: string) =>
      loadedComponents.has(component)
    );
  });

  const isLoading = $derived(() => {
    return dataState().hasValidData && !allComponentsLoaded();
  });

  const isLoaded = $derived(() => {
    return dataState().hasValidData && allComponentsLoaded();
  });

  // Effect to clear loading state when data changes
  $effect(() => {
    if (dataState().effectivePictographData) {
      errorMessage = null;
      loadedComponents.clear();
      // Recalculate arrow and prop positions when data changes
      calculateArrowPositions();
      calculatePropPositions();
    }
  });

  // Actions
  async function calculateArrowPositions(): Promise<void> {
    const currentData = dataState().effectivePictographData;

    if (!currentData?.motions) {
      arrowPositions = {};
      arrowMirroring = {};
      arrowAssets = {};
      showArrows = true;
      return;
    }

    try {
      // Use the arrow lifecycle manager to coordinate complete arrow loading
      const arrowLifecycleResult = await arrowLifecycleManager.coordinateArrowLifecycle(currentData);

      // Extract positions, mirroring, and assets from the lifecycle result
      arrowPositions = arrowLifecycleResult.positions;
      arrowMirroring = arrowLifecycleResult.mirroring;
      arrowAssets = arrowLifecycleResult.assets;
      showArrows = arrowLifecycleResult.allReady && Object.keys(arrowLifecycleResult.positions).length > 0;

      // Log any errors
      if (Object.keys(arrowLifecycleResult.errors).length > 0) {
        console.warn("⚠️ Arrow lifecycle had errors:", arrowLifecycleResult.errors);
      }
    } catch (error) {
      console.error("❌ Arrow lifecycle coordination failed:", error);
      arrowPositions = {};
      arrowMirroring = {};
      arrowAssets = {};
      showArrows = false;
    }
  }

  async function calculatePropPositions(): Promise<void> {
    const currentData = dataState().effectivePictographData;

    if (!currentData?.motions) {
      propPositions = {};
      propAssets = {};
      showProps = true;
      return;
    }

    try {
      const positions: Record<string, PropPosition> = {};
      const assets: Record<string, PropAssets> = {};
      const errors: Record<string, string> = {};

      // Process all motions in parallel for better performance
      const motionPromises = Object.entries(currentData.motions).map(
        async ([color, motionData]) => {
          try {
            const propState = await propLifecycleManager.coordinatePropState(motionData, currentData);

            if (propState.error) {
              errors[color] = propState.error;
            } else if (propState.assets && propState.position) {
              positions[color] = propState.position;
              assets[color] = propState.assets;
            }
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            errors[color] = errorMessage;
          }
        }
      );

      await Promise.all(motionPromises);

      // Update state
      propPositions = positions;
      propAssets = assets;
      showProps = Object.keys(errors).length === 0 && Object.keys(positions).length > 0;

      // Log any errors
      if (Object.keys(errors).length > 0) {
        console.warn("⚠️ Prop lifecycle had errors:", errors);
      }
    } catch (error) {
      console.error("❌ Prop lifecycle coordination failed:", error);
      propPositions = {};
      propAssets = {};
      showProps = false;
    }
  }

  function handleComponentLoaded(componentName: string): void {
    loadedComponents.add(componentName);
    loadedComponents = new Set(loadedComponents); // Trigger reactivity
  }

  function handleComponentError(componentName: string, error: string): void {
    console.error(`❌ Component ${componentName} failed to load:`, error);
    errorMessage = `Failed to load ${componentName}: ${error}`;
  }

  function clearLoadingState(): void {
    errorMessage = null;
    loadedComponents.clear();
    loadedComponents = new Set(); // Trigger reactivity
  }

  // Update pictograph data (for external updates)
  function updatePictographData(newData: PictographData | null): void {
    pictographData = newData;
  }

  return {
    // Data state (derived)
    get effectivePictographData() { return dataState().effectivePictographData; },
    get hasValidData() { return dataState().hasValidData; },
    get displayLetter() { return dataState().displayLetter; },
    get motionsToRender() { return dataState().motionsToRender; },
    get requiredComponents() { return requiredComponents(); },

    // Arrow positioning state
    get arrowPositions() { return arrowPositions; },
    get arrowMirroring() { return arrowMirroring; },
    get arrowAssets() { return arrowAssets; },
    get showArrows() { return showArrows; },

    // Prop positioning state
    get propPositions() { return propPositions; },
    get propAssets() { return propAssets; },
    get showProps() { return showProps; },

    // Loading state
    get isLoading() { return isLoading(); },
    get isLoaded() { return isLoaded(); },
    get errorMessage() { return errorMessage; },
    get loadedComponents() { return loadedComponents; },
    get allComponentsLoaded() { return allComponentsLoaded(); },

    // Actions
    calculateArrowPositions,
    calculatePropPositions,
    handleComponentLoaded,
    handleComponentError,
    clearLoadingState,
    updatePictographData,
  };
}
