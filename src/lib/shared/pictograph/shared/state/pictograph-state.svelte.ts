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
  PictographData,
  PropType,
} from "$shared";
import { resolve } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { getSettings } from "../../../application/state/app-state.svelte";
import type { ArrowAssets } from "../../arrow/orchestration/domain/arrow-models";
import type { PropAssets, PropPosition } from "../../prop/domain/models";

export interface PictographState {
  // Data state
  readonly effectivePictographData: PictographData | null;
  readonly hasValidData: boolean;
  readonly displayLetter: string | null;
  readonly motionsToRender: Array<{
    color: MotionColor;
    motionData: MotionData;
  }>;
  readonly requiredComponents: string[];

  // Arrow positioning state
  readonly arrowPositions: Record<
    string,
    { x: number; y: number; rotation: number }
  >;
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
  // Services will be resolved asynchronously to avoid container initialization errors
  let dataTransformationService: IDataTransformationService | null = null;
  let componentManagementService: IComponentManagementService | null = null;
  let arrowLifecycleManager:
    | import("../../arrow/orchestration/services/contracts/IArrowLifecycleManager").IArrowLifecycleManager
    | null = null;
  let propSvgLoader:
    | import("../../prop/services/contracts/IPropSvgLoader").IPropSvgLoader
    | null = null;
  let propPlacementService:
    | import("../../prop/services/contracts/IPropPlacementService").IPropPlacementService
    | null = null;
  let servicesInitialized = $state(false);

  // Initialize services asynchronously
  async function initializeServices() {
    try {
      dataTransformationService = await resolve<IDataTransformationService>(
        TYPES.IDataTransformationService
      );
      componentManagementService = await resolve<IComponentManagementService>(
        TYPES.IComponentManagementService
      );
      arrowLifecycleManager = await resolve<
        import("../../arrow/orchestration/services/contracts/IArrowLifecycleManager").IArrowLifecycleManager
      >(TYPES.IArrowLifecycleManager);
      propSvgLoader = await resolve<
        import("../../prop/services/contracts/IPropSvgLoader").IPropSvgLoader
      >(TYPES.IPropSvgLoader);
      propPlacementService = await resolve<
        import("../../prop/services/contracts/IPropPlacementService").IPropPlacementService
      >(TYPES.IPropPlacementService);
      servicesInitialized = true;
    } catch (error) {
      console.error("Failed to initialize pictograph services:", error);
      errorMessage = `Service initialization failed: ${error}`;
    }
  }

  // Initialize services immediately
  initializeServices();

  // Input data state
  let pictographData = $state<PictographData | null>(initialPictographData);

  // Component loading state
  let errorMessage = $state<string | null>(null);
  let loadedComponents = $state(new Set<string>());

  // Arrow positioning state
  let arrowPositions = $state<
    Record<string, { x: number; y: number; rotation: number }>
  >({});
  let arrowMirroring = $state<Record<string, boolean>>({});
  let arrowAssets = $state<Record<string, ArrowAssets>>({});
  let showArrows = $state(false);

  // Prop positioning state
  let propPositions = $state<Record<string, PropPosition>>({});
  let propAssets = $state<Record<string, PropAssets>>({});
  let showProps = $state(false);

  // Global prop type from settings - reactive to settings changes
  let currentPropType = $state<string | undefined>(undefined);

  // Watch for prop type changes in settings and trigger re-render
  $effect(() => {
    const settings = getSettings();
    const newPropType = settings.propType;

    // Only trigger recalculation if prop type actually changed and we have valid data
    if (newPropType !== currentPropType && dataState.hasValidData) {
      currentPropType = newPropType;
      calculatePropPositions();
    } else if (currentPropType === undefined) {
      // Initialize on first run
      currentPropType = newPropType;
    }
  });

  // Derived data transformation state - only when services are ready
  const dataState = $derived.by(() => {
    if (!servicesInitialized || !dataTransformationService) {
      return {
        hasValidData: false,
        effectivePictographData: null,
        transformedData: null,
      };
    }
    return dataTransformationService.transformPictographData(pictographData);
  });

  // Derived component requirements - only when services are ready
  const requiredComponents = $derived.by(() => {
    if (!servicesInitialized || !componentManagementService) {
      return [];
    }
    return componentManagementService.getRequiredComponents(pictographData);
  });

  // Derived loading states
  const allComponentsLoaded = $derived.by(() => {
    return requiredComponents.every((component: string) =>
      loadedComponents.has(component)
    );
  });

  const isLoading = $derived.by(() => {
    return dataState.hasValidData && !allComponentsLoaded;
  });

  const isLoaded = $derived.by(() => {
    return dataState.hasValidData && allComponentsLoaded;
  });

  // Effect to recalculate positions when data changes
  $effect(() => {
    const currentData = dataState.effectivePictographData;
    if (currentData) {
      errorMessage = null;

      // Explicitly track motion data properties that affect positioning
      // This ensures recalculation when turns/orientations change (e.g., via edit panel)
      const redMotion = currentData.motions?.red;
      const blueMotion = currentData.motions?.blue;

      // Track key properties that affect beta offset calculations:
      // - endOrientation (radial vs non-radial determines if offset is applied)
      // - endLocation (both props must end at same location for beta offset)
      // - turns (changes orientation, which affects offset logic)
      if (redMotion) {
        void redMotion.endOrientation;
        void redMotion.endLocation;
        void redMotion.turns;
      }
      if (blueMotion) {
        void blueMotion.endOrientation;
        void blueMotion.endLocation;
        void blueMotion.turns;
      }

      // Don't clear loadedComponents - keep elements visible during transitions
      // Recalculate arrow and prop positions when data changes
      calculateArrowPositions();
      calculatePropPositions();
    }
  });

  // Actions
  async function calculateArrowPositions(): Promise<void> {
    const currentData = dataState.effectivePictographData;

    if (
      !currentData?.motions ||
      !servicesInitialized ||
      !arrowLifecycleManager
    ) {
      // Only clear if we don't have valid data - don't clear during transitions
      arrowPositions = {};
      arrowMirroring = {};
      arrowAssets = {};
      showArrows = true;
      return;
    }

    try {
      // Use the arrow lifecycle manager to coordinate complete arrow loading
      const arrowLifecycleResult =
        await arrowLifecycleManager.coordinateArrowLifecycle(currentData);

      // Only update state after async loading completes - keeps old data visible during transitions
      arrowPositions = arrowLifecycleResult.positions;
      arrowMirroring = arrowLifecycleResult.mirroring;
      arrowAssets = arrowLifecycleResult.assets;
      showArrows =
        arrowLifecycleResult.allReady &&
        Object.keys(arrowLifecycleResult.positions).length > 0;

      // Log any errors
      if (Object.keys(arrowLifecycleResult.errors).length > 0) {
        console.warn(
          "⚠️ Arrow lifecycle had errors:",
          arrowLifecycleResult.errors
        );
      }
    } catch (error) {
      console.error("❌ Arrow lifecycle coordination failed:", error);
      // Only clear on error - keeps old data visible if loading fails
      arrowPositions = {};
      arrowMirroring = {};
      arrowAssets = {};
      showArrows = false;
    }
  }

  async function calculatePropPositions(): Promise<void> {
    const currentData = dataState.effectivePictographData;

    if (
      !currentData?.motions ||
      !servicesInitialized ||
      !propSvgLoader ||
      !propPlacementService
    ) {
      // Only clear if we don't have valid data - don't clear during transitions
      propPositions = {};
      propAssets = {};
      showProps = true;
      return;
    }

    try {
      const positions: Record<string, PropPosition> = {};
      const assets: Record<string, PropAssets> = {};
      const errors: Record<string, string> = {};

      // Get the user's selected prop type from settings
      const settings = getSettings();
      const selectedPropType = settings.propType || "Staff";

      // Map PropTypeTab IDs to actual filenames
      // PropTypeTab uses capitalized IDs, but filenames have specific formats
      const propTypeMapping: Record<string, string> = {
        Staff: "staff",
        Simplestaff: "simple_staff",
        Club: "club",
        Fan: "fan",
        Triad: "triad",
        Minihoop: "minihoop",
        Buugeng: "buugeng",
        Triquetra: "triquetra",
        Sword: "sword",
        Chicken: "chicken",
        Hand: "hand",
        Guitar: "guitar",
        Ukulele: "ukulele",
      };

      const userPropType =
        propTypeMapping[selectedPropType] || selectedPropType.toLowerCase();

      // Create an updated pictographData with all props set to user's selected type
      // This ensures beta offset logic sees the correct prop types
      const updatedPictographData = {
        ...currentData,
        motions: {
          red: currentData.motions.red
            ? {
                ...currentData.motions.red,
                propType: userPropType as PropType,
              }
            : currentData.motions.red,
          blue: currentData.motions.blue
            ? {
                ...currentData.motions.blue,
                propType: userPropType as PropType,
              }
            : currentData.motions.blue,
        },
      };

      // Process all motions in parallel for better performance
      const motionPromises = Object.entries(currentData.motions).map(
        async ([color, motionData]) => {
          try {
            if (!motionData || !motionData.propPlacementData) {
              throw new Error("No prop placement data available");
            }

            // Override the prop type with the user's selected type from settings
            // This ensures all props render as the user's chosen type
            // Cast to PropType - PropSvgLoader uses it as a string for the path anyway
            const motionDataWithUserProp: MotionData = {
              ...motionData,
              propType: userPropType as PropType,
              motionType: motionData.motionType!,
            };

            // Load assets and calculate position in parallel
            // IMPORTANT: Pass updatedPictographData so beta offset logic sees all props with user's type
            const [renderData, placementData] = await Promise.all([
              propSvgLoader!.loadPropSvg(
                motionData.propPlacementData,
                motionDataWithUserProp
              ),
              propPlacementService!.calculatePlacement(
                updatedPictographData,
                motionDataWithUserProp
              ),
            ]);

            if (!renderData.svgData) {
              throw new Error("Failed to load prop SVG data");
            }

            // Transform to expected format
            const propAssets = {
              imageSrc: renderData.svgData.svgContent,
              viewBox: `${renderData.svgData.viewBox.width} ${renderData.svgData.viewBox.height}`,
              center: renderData.svgData.center,
            };

            const position = {
              x: placementData.positionX,
              y: placementData.positionY,
              rotation: placementData.rotationAngle,
            };

            positions[color] = position;
            assets[color] = propAssets;
          } catch (error) {
            const errorMessage =
              error instanceof Error ? error.message : "Unknown error";
            errors[color] = errorMessage;
          }
        }
      );

      await Promise.all(motionPromises);

      // Only update state after async loading completes - keeps old data visible during transitions
      propPositions = positions;
      propAssets = assets;
      showProps =
        Object.keys(errors).length === 0 && Object.keys(positions).length > 0;

      // Log any errors
      if (Object.keys(errors).length > 0) {
        console.warn("⚠️ Prop lifecycle had errors:", errors);
      }
    } catch (error) {
      console.error("❌ Prop lifecycle coordination failed:", error);
      // Only clear on error - keeps old data visible if loading fails
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
    get effectivePictographData() {
      return dataState.effectivePictographData;
    },
    get hasValidData() {
      return dataState.hasValidData;
    },
    get displayLetter() {
      const data = dataState;
      return "displayLetter" in data ? data.displayLetter : null;
    },
    get motionsToRender() {
      const data = dataState;
      return "motionsToRender" in data ? data.motionsToRender : [];
    },
    get requiredComponents() {
      return requiredComponents;
    },

    // Arrow positioning state
    get arrowPositions() {
      return arrowPositions;
    },
    get arrowMirroring() {
      return arrowMirroring;
    },
    get arrowAssets() {
      return arrowAssets;
    },
    get showArrows() {
      return showArrows;
    },

    // Prop positioning state
    get propPositions() {
      return propPositions;
    },
    get propAssets() {
      return propAssets;
    },
    get showProps() {
      return showProps;
    },

    // Loading state
    get isLoading() {
      return isLoading;
    },
    get isLoaded() {
      return isLoaded;
    },
    get errorMessage() {
      return errorMessage;
    },
    get loadedComponents() {
      return loadedComponents;
    },
    get allComponentsLoaded() {
      return allComponentsLoaded;
    },

    // Actions
    calculateArrowPositions,
    calculatePropPositions,
    handleComponentLoaded,
    handleComponentError,
    clearLoadingState,
    updatePictographData,
  };
}
