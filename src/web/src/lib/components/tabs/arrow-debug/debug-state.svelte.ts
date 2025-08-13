/**
 * Arrow Debug State Integration
 * Provides a simpler interface to the existing arrow debug state
 */

import type { PictographData, MotionData, ArrowData } from "$lib/domain";
import { createPictographData } from "$lib/domain/PictographData";
import { createArrowData } from "$lib/domain/ArrowData";
import { createMotionData } from "$lib/domain/MotionData";
import { createGridData } from "$lib/domain/GridData";
import {
  GridMode,
  ArrowType,
  MotionType,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import type { DebugStepData } from "./types";

// Simple reactive state for the debug components
export function createDebugState() {
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

  let isCalculating = $state(false);
  let autoUpdate = $state(true);

  let expandedSections = $state(
    new Set(["input_data", "location_calculation"]),
  );

  // Create debug data with proper structure
  let currentDebugData = $state<DebugStepData>({
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
  let currentMotionData = $derived.by(() => {
    if (!selectedPictograph?.motions) return null;
    return selectedPictograph.motions[selectedArrowColor] || null;
  });

  let currentArrowData = $derived.by(() => {
    if (!selectedPictograph?.arrows) return null;
    return selectedPictograph.arrows[selectedArrowColor] || null;
  });

  // Create sample pictographs for testing
  function createSamplePictographs(): PictographData[] {
    try {
      const blueMotion = createMotionData({
        motion_type: MotionType.PRO,
        start_ori: Orientation.IN,
        end_ori: Orientation.OUT,
        prop_rot_dir: RotationDirection.CLOCKWISE,
        turns: 1,
      });

      const redMotion = createMotionData({
        motion_type: MotionType.ANTI,
        start_ori: Orientation.OUT,
        end_ori: Orientation.IN,
        prop_rot_dir: RotationDirection.COUNTER_CLOCKWISE,
        turns: 1,
      });

      const blueArrow = createArrowData({
        id: "blue_arrow",
        color: "blue",
        arrow_type: ArrowType.BLUE,
      });

      const redArrow = createArrowData({
        id: "red_arrow",
        color: "red",
        arrow_type: ArrowType.RED,
      });

      const sampleData = createPictographData({
        letter: "A",
        grid_data: createGridData({ grid_mode: GridMode.DIAMOND }),
        motions: {
          blue: blueMotion,
          red: redMotion,
        },
        arrows: {
          blue: blueArrow,
          red: redArrow,
        },
      });

      return [sampleData];
    } catch (error) {
      console.error("Failed to create sample pictographs:", error);
      return [];
    }
  }

  // Initialize with sample data
  function initializeSampleData() {
    try {
      const samples = createSamplePictographs();
      availablePictographs = samples;
      if (samples.length > 0) {
        selectedPictograph = samples[0];
      }
    } catch (error) {
      console.error("Failed to initialize sample data:", error);
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

  // Placeholder for positioning calculation
  async function calculatePositioning() {
    if (!selectedPictograph || !currentMotionData || !currentArrowData) {
      return;
    }

    isCalculating = true;
    const startTime = performance.now();

    try {
      // Update debug data with current inputs
      currentDebugData.pictographData = selectedPictograph;
      currentDebugData.motionData = currentMotionData;
      currentDebugData.arrowData = currentArrowData;

      // For now, create mock debug data
      // This will be replaced with actual service calls once DI is fixed
      currentDebugData.calculatedLocation = "center";
      currentDebugData.locationDebugInfo = {
        motionType: currentMotionData.motion_type || "",
        startOri: currentMotionData.start_ori || "",
        endOri: currentMotionData.end_ori || "",
        calculationMethod: "mock_calculator",
      };

      currentDebugData.initialPosition = { x: 0, y: 0 };
      currentDebugData.finalPosition = { x: 10, y: -5 };
      currentDebugData.finalRotation = 45;

      const endTime = performance.now();
      currentDebugData.timing = {
        totalDuration: endTime - startTime,
        stepDurations: { mock: endTime - startTime },
      };
    } catch (error) {
      currentDebugData.errors.push({
        step: "mock_calculation",
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

    // Computed
    get currentMotionData() {
      return currentMotionData;
    },
    get currentArrowData() {
      return currentArrowData;
    },

    // Actions
    toggleSection,
    calculatePositioning,
    initializeSampleData,
  };
}
