/**
 * Arrow Debug State Integration
 * Provides a simpler interface to the existing arrow debug state
 */

import type { PictographData, MotionData, ArrowData } from "$lib/domain";
import { createPictographData } from "$lib/domain/PictographData";
import { createGridData } from "$lib/domain/GridData";
import { GridMode } from "$lib/domain/enums";
import type { DebugStepData } from "./types";

// Import real data services
import { CodexService } from "$lib/services/codex/CodexService";

// Import real arrow positioning services
import { ArrowPositioningOrchestrator } from "$lib/services/positioning/arrows/orchestration/ArrowPositioningOrchestrator";
import { ArrowLocationCalculator } from "$lib/services/positioning/arrows/calculation/ArrowLocationCalculator";
import { ArrowCoordinateSystemService } from "$lib/services/positioning/arrows/coordinate_system/ArrowCoordinateSystemService";
import { ArrowRotationCalculator } from "$lib/services/positioning/arrows/calculation/ArrowRotationCalculator";
import { ArrowAdjustmentCalculator } from "$lib/services/positioning/arrows/calculation/ArrowAdjustmentCalculator";

// Simple reactive state for the debug components
export function createDebugState() {
  let selectedPictograph = $state<PictographData | null>(null);
  let selectedArrowColor = $state<"red" | "blue">("blue");
  let availablePictographs = $state<PictographData[]>([]);

  let stepByStepMode = $state(true);
  let currentStep = $state(0);
  const maxSteps = $state(4); // 0: Input, 1: Location, 2: Coordinate System, 3: Rotation, 4: Adjustments

  let showCoordinateGrid = $state(true);
  let showHandPoints = $state(true);
  let showLayer2Points = $state(true);
  let showAdjustmentVectors = $state(true);

  let isCalculating = $state(false);
  let autoUpdate = $state(true);

  // Grid mode state (diamond/box toggle)
  let gridMode = $state<"diamond" | "box">("diamond");

  let expandedSections = $state(
    new Set(["input_data", "location_calculation"])
  );

  // Initialize real data services
  const codexService = new CodexService();

  // Initialize real arrow positioning services
  const locationCalculator = new ArrowLocationCalculator();
  const rotationCalculator = new ArrowRotationCalculator();
  const adjustmentCalculator = new ArrowAdjustmentCalculator();
  const coordinateSystemService = new ArrowCoordinateSystemService();

  // Create the orchestrator with real services
  const arrowPositioningOrchestrator = new ArrowPositioningOrchestrator(
    locationCalculator,
    rotationCalculator,
    adjustmentCalculator,
    coordinateSystemService
  );

  // Create debug data with proper structure
  const currentDebugData = $state<DebugStepData>({
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
  });

  // Computed values
  const currentMotionData = $derived.by(() => {
    if (!selectedPictograph?.motions) return null;
    return selectedPictograph.motions[selectedArrowColor] || null;
  });

  const currentArrowData = $derived.by(() => {
    if (!selectedPictograph?.arrows) return null;
    return selectedPictograph.arrows[selectedArrowColor] || null;
  });

  // Load real pictographs from codex service
  async function loadRealPictographs(): Promise<PictographData[]> {
    try {
      console.log("🔧 Loading real pictographs from CodexService...");

      // Load all pictographs from the codex service
      const allPictographs = await codexService.loadAllPictographs();

      console.log(
        `✅ Loaded ${allPictographs.length} real pictographs from CSV data`
      );
      return allPictographs;
    } catch (error) {
      console.error("❌ Failed to load real pictographs:", error);
      return [];
    }
  }

  // Initialize with real data
  async function initializeRealData() {
    try {
      console.log("🚀 Initializing Arrow Debug with real pictograph data...");

      // Load real pictographs from CSV data
      const realPictographs = await loadRealPictographs();
      availablePictographs = realPictographs;

      if (realPictographs.length > 0) {
        selectedPictograph = realPictographs[0];
        console.log(
          `✅ Selected first pictograph: ${selectedPictograph.letter || selectedPictograph.id}`
        );
      }
    } catch (error) {
      console.error("❌ Failed to initialize real data:", error);
    }
  }

  // Toggle section expansion
  function toggleSection(section: string) {
    if (expandedSections.has(section)) {
      expandedSections.delete(section);
    } else {
      expandedSections.add(section);
    }
    // Trigger reactivity
    expandedSections = new Set(expandedSections);
  }

  // Set grid mode and update pictograph data
  function setGridMode(mode: "diamond" | "box") {
    gridMode = mode;

    // Update the selected pictograph's grid data if it exists
    if (selectedPictograph) {
      const newGridMode = mode === "diamond" ? GridMode.DIAMOND : GridMode.BOX;
      selectedPictograph = createPictographData({
        ...selectedPictograph,
        grid_data: createGridData({ grid_mode: newGridMode }),
      });

      // Trigger recalculation if auto-update is enabled
      if (autoUpdate) {
        calculatePositioning();
      }
    }
  }

  // Get step-by-step data for current step
  function getCurrentStepData() {
    if (!stepByStepMode) {
      return currentDebugData;
    }

    // Create a copy of debug data showing only up to current step
    const stepData = {
      ...currentDebugData,
      // Reset future steps based on current step
      calculatedLocation:
        currentStep >= 1 ? currentDebugData.calculatedLocation : null,
      locationDebugInfo:
        currentStep >= 1 ? currentDebugData.locationDebugInfo : null,
      initialPosition:
        currentStep >= 2 ? currentDebugData.initialPosition : null,
      coordinateSystemDebugInfo:
        currentStep >= 2 ? currentDebugData.coordinateSystemDebugInfo : null,
      finalRotation: currentStep >= 3 ? currentDebugData.finalRotation : 0,
      defaultAdjustment:
        currentStep >= 4 ? currentDebugData.defaultAdjustment : null,
      finalPosition: currentStep >= 4 ? currentDebugData.finalPosition : null,
    };

    return stepData;
  }

  // Get step name for current step
  function getCurrentStepName(): string {
    const stepNames = [
      "Input Data",
      "Location Calculation",
      "Coordinate System",
      "Rotation Calculation",
      "Adjustment Calculation",
    ];
    return stepNames[currentStep] || "Unknown Step";
  }

  // Real positioning calculation using arrow positioning services
  async function calculatePositioning() {
    if (!selectedPictograph || !currentMotionData || !currentArrowData) {
      return;
    }

    isCalculating = true;
    const startTime = performance.now();
    const stepTimes: Record<string, number> = {};

    try {
      // Clear previous errors
      currentDebugData.errors = [];

      // Update debug data with current inputs
      currentDebugData.pictographData = selectedPictograph;
      currentDebugData.motionData = currentMotionData;
      currentDebugData.arrowData = currentArrowData;

      // STEP 1: Calculate arrow location
      const locationStart = performance.now();
      try {
        const calculatedLocation = locationCalculator.calculateLocation(
          currentMotionData,
          selectedPictograph
        );
        currentDebugData.calculatedLocation = calculatedLocation;
        currentDebugData.locationDebugInfo = {
          motionType: currentMotionData.motion_type || "",
          startOri: currentMotionData.start_ori || "",
          endOri: currentMotionData.end_ori || "",
          calculationMethod: "ArrowLocationCalculator",
        };
        stepTimes.location_calculation = performance.now() - locationStart;
      } catch (error) {
        currentDebugData.errors.push({
          step: "location_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }

      // STEP 2: Get initial position from coordinate system
      const coordinateStart = performance.now();
      try {
        if (currentDebugData.calculatedLocation) {
          const initialPosition = coordinateSystemService.getInitialPosition(
            currentMotionData,
            currentDebugData.calculatedLocation as any
          );
          currentDebugData.initialPosition = initialPosition;

          const sceneCenter = coordinateSystemService.getSceneCenter();
          const sceneDimensions = coordinateSystemService.getSceneDimensions();
          const handPoints = coordinateSystemService.getAllHandPoints();
          const layer2Points = coordinateSystemService.getAllLayer2Points();

          currentDebugData.coordinateSystemDebugInfo = {
            sceneCenter,
            sceneDimensions,
            handPoints,
            layer2Points,
            usedCoordinateSet:
              currentMotionData.motion_type === "static" ||
              currentMotionData.motion_type === "dash"
                ? "hand_points"
                : "layer2_points",
            coordinateSystemType: "TKA_950x950",
          };
        }
        stepTimes.coordinate_system = performance.now() - coordinateStart;
      } catch (error) {
        currentDebugData.errors.push({
          step: "coordinate_system",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }

      // STEP 3: Calculate rotation
      const rotationStart = performance.now();
      try {
        if (currentDebugData.calculatedLocation) {
          const rotation = rotationCalculator.calculateRotation(
            currentMotionData,
            currentDebugData.calculatedLocation as any
          );
          currentDebugData.finalRotation = rotation;
        }
        stepTimes.rotation_calculation = performance.now() - rotationStart;
      } catch (error) {
        currentDebugData.errors.push({
          step: "rotation_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }

      // STEP 4: Calculate adjustments
      const adjustmentStart = performance.now();
      try {
        if (currentDebugData.calculatedLocation) {
          const adjustment = await adjustmentCalculator.calculateAdjustment(
            selectedPictograph,
            currentMotionData,
            selectedPictograph.letter || "A",
            currentDebugData.calculatedLocation as any
          );
          currentDebugData.defaultAdjustment = adjustment;

          // For now, use the adjustment as final position
          // In a more sophisticated implementation, we'd apply it to the initial position
          if (currentDebugData.initialPosition && adjustment) {
            currentDebugData.finalPosition = {
              x: currentDebugData.initialPosition.x + adjustment.x,
              y: currentDebugData.initialPosition.y + adjustment.y,
            };
          } else {
            currentDebugData.finalPosition = currentDebugData.initialPosition;
          }
        }
        stepTimes.adjustment_calculation = performance.now() - adjustmentStart;
      } catch (error) {
        currentDebugData.errors.push({
          step: "adjustment_calculation",
          error: error instanceof Error ? error.message : String(error),
          timestamp: Date.now(),
        });
      }

      // Calculate total timing
      const endTime = performance.now();
      currentDebugData.timing = {
        totalDuration: endTime - startTime,
        stepDurations: stepTimes,
      };

      console.log("🎯 Arrow positioning calculation completed:", {
        location: currentDebugData.calculatedLocation,
        initialPosition: currentDebugData.initialPosition,
        finalPosition: currentDebugData.finalPosition,
        rotation: currentDebugData.finalRotation,
        errors: currentDebugData.errors,
        timing: currentDebugData.timing,
      });
    } catch (error) {
      currentDebugData.errors.push({
        step: "overall_calculation",
        error: error instanceof Error ? error.message : String(error),
        timestamp: Date.now(),
      });
    } finally {
      isCalculating = false;
    }
  }

  // Auto-update effect
  $effect(() => {
    if (
      autoUpdate &&
      selectedPictograph &&
      currentMotionData &&
      currentArrowData
    ) {
      calculatePositioning();
    }
  });

  return {
    // State
    get selectedPictograph() {
      return selectedPictograph;
    },
    set selectedPictograph(value: PictographData | null) {
      selectedPictograph = value;
    },

    get selectedArrowColor() {
      return selectedArrowColor;
    },
    set selectedArrowColor(value: "red" | "blue") {
      selectedArrowColor = value;
    },

    get availablePictographs() {
      return availablePictographs;
    },
    set availablePictographs(value: PictographData[]) {
      availablePictographs = value;
    },

    get stepByStepMode() {
      return stepByStepMode;
    },
    set stepByStepMode(value: boolean) {
      stepByStepMode = value;
    },

    get currentStep() {
      return currentStep;
    },
    set currentStep(value: number) {
      currentStep = value;
    },

    get maxSteps() {
      return maxSteps;
    },

    get showCoordinateGrid() {
      return showCoordinateGrid;
    },
    set showCoordinateGrid(value: boolean) {
      showCoordinateGrid = value;
    },

    get showHandPoints() {
      return showHandPoints;
    },
    set showHandPoints(value: boolean) {
      showHandPoints = value;
    },

    get showLayer2Points() {
      return showLayer2Points;
    },
    set showLayer2Points(value: boolean) {
      showLayer2Points = value;
    },

    get showAdjustmentVectors() {
      return showAdjustmentVectors;
    },
    set showAdjustmentVectors(value: boolean) {
      showAdjustmentVectors = value;
    },

    get isCalculating() {
      return isCalculating;
    },
    get autoUpdate() {
      return autoUpdate;
    },
    set autoUpdate(value: boolean) {
      autoUpdate = value;
    },

    get expandedSections() {
      return expandedSections;
    },
    get currentDebugData() {
      return currentDebugData;
    },

    // Grid mode properties
    get gridMode() {
      return gridMode;
    },
    set gridMode(value: "diamond" | "box") {
      setGridMode(value);
    },

    // Computed
    get currentMotionData() {
      return currentMotionData;
    },
    get currentArrowData() {
      return currentArrowData;
    },
    get currentStepData() {
      return getCurrentStepData();
    },
    get currentStepName() {
      return getCurrentStepName();
    },

    // Actions
    toggleSection,
    setGridMode,
    calculatePositioning,
    initializeRealData,
    getCurrentStepData,
    getCurrentStepName,
  };
}
