/**
 * Pictograph State Management - Svelte 5 runes
 *
 * Reactive state management for pictograph rendering and arrow positioning.
 * Wraps pictograph services with runes for UI reactivity.
 * Follows TKA architecture: services handle business logic, runes handle reactivity.
 */

import type {
  IArrowPositioningOrchestrator,
  IComponentManagementService,
  IDataTransformationService,
  MotionColor,
  MotionData,
  PictographData,
} from "$shared";
import { resolve, TYPES } from "$shared";

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
  readonly showArrows: boolean;

  // Loading state
  readonly isLoading: boolean;
  readonly isLoaded: boolean;
  readonly errorMessage: string | null;
  readonly loadedComponents: Set<string>;
  readonly allComponentsLoaded: boolean;

  // Actions
  calculateArrowPositions(): Promise<void>;
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
  const arrowOrchestrator = resolve(TYPES.IArrowPositioningOrchestrator) as IArrowPositioningOrchestrator;

  // Input data state
  let pictographData = $state<PictographData | null>(initialPictographData);

  // Component loading state
  let errorMessage = $state<string | null>(null);
  let loadedComponents = $state(new Set<string>());

  // Arrow positioning state
  let arrowPositions = $state<Record<string, { x: number; y: number; rotation: number }>>({});
  let arrowMirroring = $state<Record<string, boolean>>({});
  let showArrows = $state(false);

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
      // Recalculate arrow positions when data changes
      calculateArrowPositions();
    }
  });

  // Actions
  async function calculateArrowPositions(): Promise<void> {
    const currentData = dataState().effectivePictographData;
    
    if (!currentData?.motions) {
      arrowPositions = {};
      arrowMirroring = {};
      showArrows = true;
      return;
    }

    try {
      // Use the arrow orchestrator to calculate positions
      const updatedPictographData = await arrowOrchestrator.calculateAllArrowPoints(currentData);
      
      const newPositions: Record<string, { x: number; y: number; rotation: number }> = {};
      const newMirroring: Record<string, boolean> = {};

      // Extract positions and mirroring from the updated data
      for (const [color, motionData] of Object.entries(updatedPictographData.motions || {})) {
        const typedMotionData = motionData as MotionData;
        if (typedMotionData?.isVisible && typedMotionData.arrowPlacementData) {
          try {
            const arrowPlacement = typedMotionData.arrowPlacementData;

            newPositions[color] = {
              x: arrowPlacement.positionX,
              y: arrowPlacement.positionY,
              rotation: arrowPlacement.rotationAngle || 0,
            };

            newMirroring[color] = arrowPlacement.svgMirrored || false;
          } catch (error) {
            console.error(`❌ Failed to extract position for ${color} arrow:`, error);
          }
        }
      }

      arrowPositions = newPositions;
      arrowMirroring = newMirroring;
      showArrows = Object.keys(newPositions).length > 0;
    } catch (error) {
      console.error("❌ Arrow positioning calculation failed:", error);
      arrowPositions = {};
      arrowMirroring = {};
      showArrows = false;
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
    get showArrows() { return showArrows; },

    // Loading state
    get isLoading() { return isLoading(); },
    get isLoaded() { return isLoaded(); },
    get errorMessage() { return errorMessage; },
    get loadedComponents() { return loadedComponents; },
    get allComponentsLoaded() { return allComponentsLoaded(); },

    // Actions
    calculateArrowPositions,
    handleComponentLoaded,
    handleComponentError,
    clearLoadingState,
    updatePictographData,
  };
}
