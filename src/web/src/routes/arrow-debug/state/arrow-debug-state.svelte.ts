/**
 * Arrow Debug State Management
 *
 * Comprehensive state for debugging arrow positioning issues.
 * Tracks each step of the 3-phase positioning process.
 */

import type { ArrowData, MotionData, PictographData } from "$lib/domain";
import { Location } from "$lib/domain";
import { resolve, createWebApplication } from "$lib/services/bootstrap";
import type {
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowRotationCalculator,
  IArrowAdjustmentCalculator,
} from "$lib/services/interfaces";
import type { Point } from "$lib/services/positioning/types";

export interface ArrowPositioningDebugData {
  // Input data
  pictographData: PictographData | null;
  motionData: MotionData | null;
  arrowData: ArrowData | null;

  // Step 1: Location calculation
  calculatedLocation: Location | null;
  locationDebugInfo: {
    motionType: string;
    startOri: string;
    endOri: string;
    calculationMethod: string;
  } | null;

  // Step 2: Initial position from coordinate system
  initialPosition: Point | null;
  coordinateSystemDebugInfo: {
    sceneCenter: Point;
    sceneDimensions: [number, number];
    handPoints: Record<Location, Point>;
    layer2Points: Record<Location, Point>;
    usedCoordinateSet: "hand_points" | "layer2_points" | "center";
    coordinateSystemType: string;
  } | null;

  // Step 3: Default adjustment calculation
  defaultAdjustment: Point | null;
  defaultAdjustmentDebugInfo: {
    placementKey: string;
    turns: number | string;
    motionType: string;
    gridMode: string;
    adjustmentSource: "default_placement" | "calculated" | "fallback";
    rawPlacementData: any;
  } | null;

  // Step 4: Special adjustment calculation
  specialAdjustment: Point | null;
  specialAdjustmentDebugInfo: {
    letter: string;
    oriKey: string;
    turnsTuple: string;
    arrowColor: string;
    specialPlacementFound: boolean;
    specialPlacementData: any;
    adjustmentSource: "special_placement" | "none";
  } | null;

  // Step 5: Directional tuple processing
  tupleProcessedAdjustment: Point | null;
  tupleProcessingDebugInfo: {
    baseAdjustment: Point;
    quadrantIndex: number;
    directionalTuples: Array<[number, number]>;
    selectedTuple: [number, number];
    transformationMethod: string;
  } | null;

  // Final result
  finalPosition: Point | null;
  finalRotation: number;

  // Error tracking
  errors: Array<{
    step: string;
    error: string;
    timestamp: number;
  }>;

  // Performance tracking
  timing: {
    totalDuration: number;
    stepDurations: Record<string, number>;
  } | null;
}

export interface ArrowDebugState {
  // Current pictograph and arrow selection
  selectedPictograph: PictographData | null;
  selectedArrowColor: "red" | "blue";
  availablePictographs: PictographData[];

  // Debug modes
  stepByStepMode: boolean;
  currentStep: number;
  maxSteps: number;

  // Coordinate system visualization
  showCoordinateGrid: boolean;
  showHandPoints: boolean;
  showLayer2Points: boolean;
  showAdjustmentVectors: boolean;

  // Current positioning data for selected arrow
  currentDebugData: ArrowPositioningDebugData;

  // Services (injected)
  coordinateSystemService: IArrowCoordinateSystemService;
  locationCalculator: IArrowLocationCalculator;
  rotationCalculator: IArrowRotationCalculator;
  adjustmentCalculator: IArrowAdjustmentCalculator;

  // UI state
  isCalculating: boolean;
  autoUpdate: boolean;

  // Debug panel expansion
  expandedSections: Set<string>;

  // Computed values
  currentMotionData: MotionData | null;
  currentArrowData: ArrowData | null;

  // Methods
  calculateFullPositioning: () => Promise<void>;
  loadSamplePictographs: () => Promise<void>;
  toggleSection: (section: string) => void;
}

export function createArrowDebugState(): ArrowDebugState {
  // Initialize services (ensure DI container is ready)
  let coordinateSystemService: IArrowCoordinateSystemService;
  let locationCalculator: IArrowLocationCalculator;
  let rotationCalculator: IArrowRotationCalculator;
  let adjustmentCalculator: IArrowAdjustmentCalculator;

  try {
    // Get services from DI container
    coordinateSystemService = resolve("IArrowCoordinateSystemService");
    locationCalculator = resolve("IArrowLocationCalculator");
    rotationCalculator = resolve("IArrowRotationCalculator");
    adjustmentCalculator = resolve("IArrowAdjustmentCalculator");
  } catch (error) {
    console.warn("Services not yet available, will retry when needed:", error);
    // Create placeholder services - these will be replaced when container is ready
    coordinateSystemService = null as any;
    locationCalculator = null as any;
    rotationCalculator = null as any;
    adjustmentCalculator = null as any;
  }

  // Initialize reactive state
  let selectedPictograph = $state<PictographData | null>(null);
  let selectedArrowColor = $state<"red" | "blue">("blue");
  let availablePictographs = $state<PictographData[]>([]);

  let stepByStepMode = $state(true);
  let currentStep = $state(0);
  let maxSteps = $state(5);

  let showCoordinateGrid = $state(true);
  let showHandPoints = $state(true);
  let showLayer2Points = $state(true);
  let showAdjustmentVectors = $state(true);

  let currentDebugData = $state<ArrowPositioningDebugData>(
    createEmptyDebugData()
  );

  let isCalculating = $state(false);
  let autoUpdate = $state(true);

  let expandedSections = $state(
    new Set(["coordinate_system", "positioning_steps"])
  );

  // Computed values
  let currentMotionData = $derived(() => {
    if (!selectedPictograph?.motions) return null;
    return selectedPictograph.motions[selectedArrowColor];
  });

  let currentArrowData = $derived(() => {
    if (!selectedPictograph?.arrows) return null;
    return selectedPictograph.arrows[selectedArrowColor];
  });

  // Function to ensure services are initialized
  function ensureServicesInitialized(): boolean {
    if (
      !coordinateSystemService ||
      !locationCalculator ||
      !rotationCalculator ||
      !adjustmentCalculator
    ) {
      try {
        coordinateSystemService = resolve("IArrowCoordinateSystemService");
        locationCalculator = resolve("IArrowLocationCalculator");
        rotationCalculator = resolve("IArrowRotationCalculator");
        adjustmentCalculator = resolve("IArrowAdjustmentCalculator");
        return true;
      } catch (error) {
        console.error("Services still not available:", error);
        return false;
      }
    }
    return true;
  }

  // Auto-update positioning when inputs change
  $effect(() => {
    if (
      autoUpdate &&
      selectedPictograph &&
      currentMotionData &&
      currentArrowData
    ) {
      if (ensureServicesInitialized()) {
        calculateFullPositioning();
      }
    }
  });

  async function calculateFullPositioning(): Promise<void> {
    if (!selectedPictograph || !currentMotionData || !currentArrowData) {
      return;
    }

    if (!ensureServicesInitialized()) {
      console.error("Cannot calculate positioning: services not available");
      return;
    }

    isCalculating = true;
    const startTime = performance.now();

    try {
      const debugData = createEmptyDebugData();
      debugData.pictographData = selectedPictograph;
      debugData.motionData = currentMotionData;
      debugData.arrowData = currentArrowData;

      // Step 1: Calculate location
      const locationStart = performance.now();
      try {
        debugData.calculatedLocation = locationCalculator.calculateLocation(
          currentMotionData,
          selectedPictograph
        );
        debugData.locationDebugInfo = {
          motionType: currentMotionData.motion_type || "",
          startOri: currentMotionData.start_ori || "",
          endOri: currentMotionData.end_ori || "",
          calculationMethod: getLocationCalculationMethod(currentMotionData),
        };
      } catch (error) {
        debugData.errors.push({
          step: "location_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }
      debugData.timing = {
        totalDuration: 0,
        stepDurations: { location: performance.now() - locationStart },
      };

      // Step 2: Get initial position
      const positionStart = performance.now();
      try {
        if (debugData.calculatedLocation) {
          debugData.initialPosition =
            coordinateSystemService.getInitialPosition(
              currentMotionData,
              debugData.calculatedLocation
            );

          debugData.coordinateSystemDebugInfo = {
            sceneCenter: coordinateSystemService.getSceneCenter(),
            sceneDimensions: coordinateSystemService.getSceneDimensions(),
            handPoints: coordinateSystemService.getAllHandPoints(),
            layer2Points: coordinateSystemService.getAllLayer2Points(),
            usedCoordinateSet: getUsedCoordinateSet(currentMotionData),
            coordinateSystemType: getCoordinateSystemType(currentMotionData),
          };
        }
      } catch (error) {
        debugData.errors.push({
          step: "initial_position",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }
      debugData.timing.stepDurations.initial_position =
        performance.now() - positionStart;

      // Step 3: Calculate rotation
      const rotationStart = performance.now();
      try {
        if (debugData.calculatedLocation) {
          debugData.finalRotation = rotationCalculator.calculateRotation(
            currentMotionData,
            debugData.calculatedLocation
          );
        }
      } catch (error) {
        debugData.errors.push({
          step: "rotation_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }
      debugData.timing.stepDurations.rotation =
        performance.now() - rotationStart;

      // Step 4: Calculate adjustment (this is where the 3-step process should happen)
      const adjustmentStart = performance.now();
      try {
        if (debugData.calculatedLocation) {
          const fullAdjustment = await adjustmentCalculator.calculateAdjustment(
            selectedPictograph,
            currentMotionData,
            selectedPictograph.letter || "",
            debugData.calculatedLocation,
            selectedArrowColor
          );

          // Also try to get individual components for debugging
          await calculateIndividualAdjustments(
            debugData,
            selectedPictograph,
            currentMotionData
          );

          debugData.tupleProcessedAdjustment = fullAdjustment;
        }
      } catch (error) {
        debugData.errors.push({
          step: "adjustment_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }
      debugData.timing.stepDurations.adjustment =
        performance.now() - adjustmentStart;

      // Step 5: Calculate final position
      if (debugData.initialPosition && debugData.tupleProcessedAdjustment) {
        debugData.finalPosition = {
          x: debugData.initialPosition.x + debugData.tupleProcessedAdjustment.x,
          y: debugData.initialPosition.y + debugData.tupleProcessedAdjustment.y,
        };
      }

      debugData.timing.totalDuration = performance.now() - startTime;
      currentDebugData = debugData;
    } catch (error) {
      currentDebugData.errors.push({
        step: "full_calculation",
        error: error instanceof Error ? error.message : String(error),
        timestamp: Date.now(),
      });
    } finally {
      isCalculating = false;
    }
  }

  async function calculateIndividualAdjustments(
    debugData: ArrowPositioningDebugData,
    pictograph: PictographData,
    motion: MotionData
  ): Promise<void> {
    // This would require access to the internal services of the adjustment calculator
    // For now, we'll provide placeholder debug info
    // In a full implementation, you'd need to expose more granular methods

    debugData.defaultAdjustmentDebugInfo = {
      placementKey: "placeholder",
      turns: motion.turns || 0,
      motionType: motion.motion_type || "",
      gridMode: pictograph.grid_mode || "diamond",
      adjustmentSource: "default_placement",
      rawPlacementData: null,
    };

    debugData.specialAdjustmentDebugInfo = {
      letter: pictograph.letter || "",
      oriKey: "placeholder",
      turnsTuple: "placeholder",
      arrowColor: selectedArrowColor,
      specialPlacementFound: false,
      specialPlacementData: null,
      adjustmentSource: "none",
    };
  }

  function getLocationCalculationMethod(motion: MotionData): string {
    const motionType = motion.motion_type?.toLowerCase();
    if (["static", "dash"].includes(motionType || "")) {
      return "static_calculator";
    } else if (["pro", "anti", "float"].includes(motionType || "")) {
      return "shift_calculator";
    }
    return "unknown";
  }

  function getUsedCoordinateSet(
    motion: MotionData
  ): "hand_points" | "layer2_points" | "center" {
    const motionType = motion.motion_type?.toLowerCase();
    if (["pro", "anti", "float"].includes(motionType || "")) {
      return "layer2_points";
    } else if (["static", "dash"].includes(motionType || "")) {
      return "hand_points";
    }
    return "center";
  }

  function getCoordinateSystemType(motion: MotionData): string {
    const motionType = motion.motion_type?.toLowerCase();
    if (["pro", "anti", "float"].includes(motionType || "")) {
      return "shift_arrow_layer2";
    } else if (["static", "dash"].includes(motionType || "")) {
      return "static_arrow_hand";
    }
    return "unknown";
  }

  function createEmptyDebugData(): ArrowPositioningDebugData {
    return {
      pictographData: null,
      motionData: null,
      arrowData: null,
      calculatedLocation: null,
      locationDebugInfo: null,
      initialPosition: null,
      coordinateSystemDebugInfo: null,
      defaultAdjustment: null,
      defaultAdjustmentDebugInfo: null,
      specialAdjustment: null,
      specialAdjustmentDebugInfo: null,
      tupleProcessedAdjustment: null,
      tupleProcessingDebugInfo: null,
      finalPosition: null,
      finalRotation: 0,
      errors: [],
      timing: null,
    };
  }

  // Load sample pictographs for testing
  async function loadSamplePictographs(): Promise<void> {
    try {
      // Load some sample pictographs for testing
      // You can replace this with actual data loading logic
      const samplePictographs: PictographData[] = [
        {
          letter: "A",
          grid_mode: "diamond",
          motions: {
            blue: {
              motion_type: "pro",
              start_ori: "in",
              end_ori: "out",
              prop_rot_dir: "cw",
              turns: 1,
            },
            red: {
              motion_type: "anti",
              start_ori: "out",
              end_ori: "in",
              prop_rot_dir: "ccw",
              turns: 1,
            },
          },
          arrows: {
            blue: {
              id: "blue_arrow",
              color: "blue",
              arrow_type: "BLUE",
              is_visible: true,
              is_selected: false,
              position_x: 0,
              position_y: 0,
              rotation_angle: 0,
              is_mirrored: false,
              motion_type: "pro",
              location: "center",
              start_orientation: "in",
              end_orientation: "out",
              rotation_direction: "cw",
              turns: 1,
            },
            red: {
              id: "red_arrow",
              color: "red",
              arrow_type: "RED",
              is_visible: true,
              is_selected: false,
              position_x: 0,
              position_y: 0,
              rotation_angle: 0,
              is_mirrored: false,
              motion_type: "anti",
              location: "center",
              start_orientation: "out",
              end_orientation: "in",
              rotation_direction: "ccw",
              turns: 1,
            },
          },
        } as PictographData,
      ];

      availablePictographs = samplePictographs;
      if (samplePictographs.length > 0) {
        selectedPictograph = samplePictographs[0];
      }
    } catch (error) {
      console.error("Failed to load sample pictographs:", error);
    }
  }

  // Initialize with sample data
  loadSamplePictographs();

  return {
    // Reactive state
    get selectedPictograph() {
      return selectedPictograph;
    },
    set selectedPictograph(value) {
      selectedPictograph = value;
    },

    get selectedArrowColor() {
      return selectedArrowColor;
    },
    set selectedArrowColor(value) {
      selectedArrowColor = value;
    },

    get availablePictographs() {
      return availablePictographs;
    },

    get stepByStepMode() {
      return stepByStepMode;
    },
    set stepByStepMode(value) {
      stepByStepMode = value;
    },

    get currentStep() {
      return currentStep;
    },
    set currentStep(value) {
      currentStep = value;
    },

    get maxSteps() {
      return maxSteps;
    },

    get showCoordinateGrid() {
      return showCoordinateGrid;
    },
    set showCoordinateGrid(value) {
      showCoordinateGrid = value;
    },

    get showHandPoints() {
      return showHandPoints;
    },
    set showHandPoints(value) {
      showHandPoints = value;
    },

    get showLayer2Points() {
      return showLayer2Points;
    },
    set showLayer2Points(value) {
      showLayer2Points = value;
    },

    get showAdjustmentVectors() {
      return showAdjustmentVectors;
    },
    set showAdjustmentVectors(value) {
      showAdjustmentVectors = value;
    },

    get currentDebugData() {
      return currentDebugData;
    },

    get isCalculating() {
      return isCalculating;
    },

    get autoUpdate() {
      return autoUpdate;
    },
    set autoUpdate(value) {
      autoUpdate = value;
    },

    get expandedSections() {
      return expandedSections;
    },

    // Computed values
    get currentMotionData() {
      return currentMotionData;
    },
    get currentArrowData() {
      return currentArrowData;
    },

    // Services
    coordinateSystemService,
    locationCalculator,
    rotationCalculator,
    adjustmentCalculator,

    // Methods
    calculateFullPositioning,
    loadSamplePictographs,

    toggleSection(section: string) {
      if (expandedSections.has(section)) {
        expandedSections.delete(section);
      } else {
        expandedSections.add(section);
      }
      // Trigger reactivity
      expandedSections = new Set(expandedSections);
    },
  };
}
