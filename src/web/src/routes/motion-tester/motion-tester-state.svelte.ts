/**
 * Motion Tester State - Enhanced Dual Prop Version
 *
 * Manages reactive state for testing individual or combined motions.
 * Supports independent control and visibility of blue and red props.
 */

import {
  calculateStepEndpoints,
  lerpAngle,
  normalizeAnglePositive,
  normalizeAngleSigned,
  mapPositionToAngle,
  mapOrientationToAngle,
  type StepEndpoints,
  type PropAttributes,
} from "$lib/animator/utils/standalone-math.js";

import { StandalonePortedEngine, type PropState } from "$lib/animator";
import { OrientationCalculationService } from "$lib/services/implementations/OrientationCalculationService";
import {
  MotionType,
  Orientation,
  RotationDirection,
  Location,
} from "$lib/domain/enums";

export interface MotionTestParams {
  startLoc: string;
  endLoc: string;
  motionType: string;
  turns: number;
  propRotDir: string;
  startOri: string;
  endOri: string;
}

export interface PropVisibility {
  blue: boolean;
  red: boolean;
}

export interface AnimationTestState {
  progress: number;
  isPlaying: boolean;
  speed: number;
}

// Create a test sequence with separate blue and red parameters
function createDualPropTestSequence(
  blueParams: MotionTestParams,
  redParams: MotionTestParams
) {
  // Create a simple 2-beat sequence for testing
  const testSequence = [
    // Metadata (index 0)
    {
      word: "DUAL_TEST",
      author: "Motion Tester",
      totalBeats: 1,
    },
    // Start position (index 1)
    {
      beat: 0,
      letter: "START",
      letter_type: "start",
      blue_attributes: {
        start_loc: blueParams.startLoc,
        end_loc: blueParams.startLoc,
        start_ori: blueParams.startOri,
        end_ori: blueParams.startOri,
        motion_type: "static",
        prop_rot_dir: "cw",
        turns: 0,
      },
      red_attributes: {
        start_loc: redParams.startLoc,
        end_loc: redParams.startLoc,
        start_ori: redParams.startOri,
        end_ori: redParams.startOri,
        motion_type: "static",
        prop_rot_dir: "cw",
        turns: 0,
      },
    },
    // Target motion (index 2)
    {
      beat: 1,
      letter: "TEST",
      letter_type: "motion",
      blue_attributes: convertMotionTestParamsToPropAttributes(blueParams),
      red_attributes: convertMotionTestParamsToPropAttributes(redParams),
    },
  ];

  return testSequence;
}

// Helper function to calculate rotation direction based on motion type and locations
function calculateRotationDirection(
  motionType: string,
  startLoc: string,
  endLoc: string
): string {
  // Location order for clockwise movement: n -> e -> s -> w -> n
  const locationOrder = ["n", "e", "s", "w"];
  const startIndex = locationOrder.indexOf(startLoc);
  const endIndex = locationOrder.indexOf(endLoc);

  if (startIndex === -1 || endIndex === -1) {
    return "cw"; // Default to clockwise for unknown locations
  }

  // Calculate the direction of movement
  let clockwiseDistance = (endIndex - startIndex + 4) % 4;
  let counterClockwiseDistance = (startIndex - endIndex + 4) % 4;

  // For static motions, no rotation
  if (motionType === "static") {
    return "no_rot";
  }

  // For dash motions, typically no rotation unless specified
  if (motionType === "dash") {
    return "no_rot";
  }

  // For pro motions: follow natural circular progression
  // For anti motions: go opposite to natural progression
  if (clockwiseDistance <= counterClockwiseDistance) {
    return motionType === "pro" ? "cw" : "ccw";
  } else {
    return motionType === "pro" ? "ccw" : "cw";
  }
}

// Helper function to map string values to enum values
function mapMotionTypeToEnum(motionType: string): MotionType {
  switch (motionType.toLowerCase()) {
    case "pro":
      return MotionType.PRO;
    case "anti":
      return MotionType.ANTI;
    case "static":
      return MotionType.STATIC;
    case "dash":
      return MotionType.DASH;
    case "fl":
    case "float":
      return MotionType.FLOAT;
    default:
      return MotionType.PRO;
  }
}

function mapOrientationToEnum(orientation: string): Orientation {
  switch (orientation.toLowerCase()) {
    case "in":
      return Orientation.IN;
    case "out":
      return Orientation.OUT;
    case "clock":
      return Orientation.CLOCK;
    case "counter":
      return Orientation.COUNTER;
    case "n":
      return Orientation.IN; // Map cardinal directions to in/out for now
    case "e":
      return Orientation.IN;
    case "s":
      return Orientation.IN;
    case "w":
      return Orientation.IN;
    default:
      return Orientation.IN;
  }
}

function mapRotationDirectionToEnum(rotDir: string): RotationDirection {
  switch (rotDir.toLowerCase()) {
    case "cw":
    case "clockwise":
      return RotationDirection.CLOCKWISE;
    case "ccw":
    case "counter_clockwise":
    case "counterclockwise":
      return RotationDirection.COUNTER_CLOCKWISE;
    default:
      return RotationDirection.CLOCKWISE;
  }
}

function mapLocationToEnum(location: string): Location {
  switch (location.toLowerCase()) {
    case "n":
      return Location.NORTH;
    case "e":
      return Location.EAST;
    case "s":
      return Location.SOUTH;
    case "w":
      return Location.WEST;
    case "ne":
      return Location.NORTHEAST;
    case "se":
      return Location.SOUTHEAST;
    case "sw":
      return Location.SOUTHWEST;
    case "nw":
      return Location.NORTHWEST;
    default:
      return Location.NORTH;
  }
}

// Helper function to convert MotionTestParams to PropAttributes
function convertMotionTestParamsToPropAttributes(
  params: MotionTestParams
): PropAttributes {
  return {
    start_loc: params.startLoc,
    end_loc: params.endLoc,
    motion_type: params.motionType as any,
    turns: params.turns,
    prop_rot_dir: params.propRotDir as any,
    start_ori: params.startOri as any,
    end_ori: params.endOri as any,
  };
}

export function createMotionTesterState() {
  // Create orientation calculation service
  const orientationService = new OrientationCalculationService();

  // Separate motion parameters for blue and red props
  let blueMotionParams = $state<MotionTestParams>({
    startLoc: "n",
    endLoc: "e",
    motionType: "pro",
    turns: 0,
    propRotDir: "cw",
    startOri: "in",
    endOri: "in",
  });

  let redMotionParams = $state<MotionTestParams>({
    startLoc: "s",
    endLoc: "w",
    motionType: "pro",
    turns: 0,
    propRotDir: "cw",
    startOri: "in",
    endOri: "in",
  });

  // Prop visibility controls
  let propVisibility = $state<PropVisibility>({
    blue: true,
    red: false, // Start with just blue visible for single prop testing
  });

  // Animation state
  let animationState = $state<AnimationTestState>({
    progress: 0,
    isPlaying: false,
    speed: 0.01,
  });

  // Grid type state
  let gridType = $state<"diamond" | "box">("diamond");

  // Animation engine instance
  let animationEngine = new StandalonePortedEngine();
  let totalBeats = $state(1);
  let isEngineInitialized = $state(false);

  // Auto-calculate rotation direction when motion parameters change
  $effect(() => {
    const newRotDir = calculateRotationDirection(
      blueMotionParams.motionType,
      blueMotionParams.startLoc,
      blueMotionParams.endLoc
    );
    if (newRotDir !== blueMotionParams.propRotDir) {
      blueMotionParams.propRotDir = newRotDir;
    }
  });

  // Auto-calculate end orientation when motion parameters change
  $effect(() => {
    try {
      const motionData = {
        motion_type: mapMotionTypeToEnum(blueMotionParams.motionType),
        prop_rot_dir: mapRotationDirectionToEnum(blueMotionParams.propRotDir),
        start_loc: mapLocationToEnum(blueMotionParams.startLoc),
        end_loc: mapLocationToEnum(blueMotionParams.endLoc),
        turns: blueMotionParams.turns,
        start_ori: mapOrientationToEnum(blueMotionParams.startOri),
        end_ori: mapOrientationToEnum(blueMotionParams.endOri), // Will be overwritten
        is_visible: true,
        prefloat_motion_type: null,
        prefloat_prop_rot_dir: null,
      };

      const calculatedEndOri =
        orientationService.calculateEndOrientation(motionData);

      // Map back to string
      let endOriString = "in";
      switch (calculatedEndOri) {
        case Orientation.IN:
          endOriString = "in";
          break;
        case Orientation.OUT:
          endOriString = "out";
          break;
        case Orientation.CLOCK:
          endOriString = "clock";
          break;
        case Orientation.COUNTER:
          endOriString = "counter";
          break;
      }

      if (endOriString !== blueMotionParams.endOri) {
        blueMotionParams.endOri = endOriString;
      }
    } catch (error) {
      console.warn("Failed to calculate end orientation:", error);
    }
  });

  // Auto-calculate rotation direction for red prop
  $effect(() => {
    const newRotDir = calculateRotationDirection(
      redMotionParams.motionType,
      redMotionParams.startLoc,
      redMotionParams.endLoc
    );
    if (newRotDir !== redMotionParams.propRotDir) {
      redMotionParams.propRotDir = newRotDir;
    }
  });

  // Auto-calculate end orientation for red prop
  $effect(() => {
    try {
      const motionData = {
        motion_type: mapMotionTypeToEnum(redMotionParams.motionType),
        prop_rot_dir: mapRotationDirectionToEnum(redMotionParams.propRotDir),
        start_loc: mapLocationToEnum(redMotionParams.startLoc),
        end_loc: mapLocationToEnum(redMotionParams.endLoc),
        turns: redMotionParams.turns,
        start_ori: mapOrientationToEnum(redMotionParams.startOri),
        end_ori: mapOrientationToEnum(redMotionParams.endOri), // Will be overwritten
        is_visible: true,
        prefloat_motion_type: null,
        prefloat_prop_rot_dir: null,
      };

      const calculatedEndOri =
        orientationService.calculateEndOrientation(motionData);

      // Map back to string
      let endOriString = "in";
      switch (calculatedEndOri) {
        case Orientation.IN:
          endOriString = "in";
          break;
        case Orientation.OUT:
          endOriString = "out";
          break;
        case Orientation.CLOCK:
          endOriString = "clock";
          break;
        case Orientation.COUNTER:
          endOriString = "counter";
          break;
      }

      if (endOriString !== redMotionParams.endOri) {
        redMotionParams.endOri = endOriString;
      }
    } catch (error) {
      console.warn("Failed to calculate red end orientation:", error);
    }
  });

  // Initialize engine when motion parameters change
  $effect(() => {
    const testSequence = createDualPropTestSequence(
      blueMotionParams,
      redMotionParams
    );
    if (animationEngine.initialize(testSequence)) {
      const metadata = animationEngine.getMetadata();
      totalBeats = metadata.totalBeats;
      isEngineInitialized = true;

      // Reset animation progress
      animationState.progress = 0;

      console.log("🎯 Dual prop motion tester engine initialized:", {
        blueMotion: blueMotionParams,
        redMotion: redMotionParams,
        visibility: propVisibility,
        totalBeats,
        metadata,
      });
    } else {
      isEngineInitialized = false;
      console.error("❌ Failed to initialize dual prop motion tester engine");
    }
  });

  // Calculate current prop states from engine
  let currentPropStates = $derived(() => {
    if (!isEngineInitialized) {
      return {
        blue: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 },
        red: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 },
      };
    }

    // Calculate state for current progress
    const currentBeat = animationState.progress * totalBeats;
    animationEngine.calculateState(currentBeat);

    return {
      blue: animationEngine.getBluePropState(),
      red: animationEngine.getRedPropState(),
    };
  });

  // Motion descriptions (derived)
  let blueMotionDescription = $derived(() => {
    return `Blue: ${blueMotionParams.startLoc.toUpperCase()} → ${blueMotionParams.endLoc.toUpperCase()} (${blueMotionParams.motionType}, ${blueMotionParams.turns} turns, ${blueMotionParams.propRotDir.toUpperCase()})`;
  });

  let redMotionDescription = $derived(() => {
    return `Red: ${redMotionParams.startLoc.toUpperCase()} → ${redMotionParams.endLoc.toUpperCase()} (${redMotionParams.motionType}, ${redMotionParams.turns} turns, ${redMotionParams.propRotDir.toUpperCase()})`;
  });

  // Animation frame management
  let animationFrameId: number | null = null;

  // Animation control functions
  function startAnimation() {
    animationState.isPlaying = true;
    animate();
  }

  function pauseAnimation() {
    animationState.isPlaying = false;
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
  }

  function resetAnimation() {
    pauseAnimation();
    animationState.progress = 0;
  }

  function stepAnimation() {
    animationState.progress = Math.min(1, animationState.progress + 0.1);
  }

  function animate() {
    if (!animationState.isPlaying) return;

    animationState.progress += animationState.speed;
    if (animationState.progress > 1) {
      animationState.progress = 0;
    }

    animationFrameId = requestAnimationFrame(animate);
  }

  // Parameter update functions
  function updateBlueMotionParam<K extends keyof MotionTestParams>(
    key: K,
    value: MotionTestParams[K]
  ) {
    blueMotionParams[key] = value;
  }

  function updateRedMotionParam<K extends keyof MotionTestParams>(
    key: K,
    value: MotionTestParams[K]
  ) {
    redMotionParams[key] = value;
  }

  function setProgress(progress: number) {
    animationState.progress = Math.max(0, Math.min(1, progress));
  }

  function setSpeed(speed: number) {
    animationState.speed = Math.max(0.001, Math.min(0.1, speed));
  }

  // Visibility control functions
  function toggleBlueProp() {
    propVisibility.blue = !propVisibility.blue;
  }

  function toggleRedProp() {
    propVisibility.red = !propVisibility.red;
  }

  function setBluePropVisible(visible: boolean) {
    propVisibility.blue = visible;
  }

  function setRedPropVisible(visible: boolean) {
    propVisibility.red = visible;
  }

  function showBothProps() {
    propVisibility.blue = true;
    propVisibility.red = true;
  }

  function showOnlyBlue() {
    propVisibility.blue = true;
    propVisibility.red = false;
  }

  function showOnlyRed() {
    propVisibility.blue = false;
    propVisibility.red = true;
  }

  // Location update convenience functions
  function setBlueStartLocation(location: string) {
    updateBlueMotionParam("startLoc", location);
  }

  function setBlueEndLocation(location: string) {
    updateBlueMotionParam("endLoc", location);
  }

  function setRedStartLocation(location: string) {
    updateRedMotionParam("startLoc", location);
  }

  function setRedEndLocation(location: string) {
    updateRedMotionParam("endLoc", location);
  }

  // Debug calculations (derived) - Updated for dual prop approach
  let debugInfo = $derived(() => {
    if (!isEngineInitialized) return null;

    // Calculate endpoints for both props
    const blueStepDef = {
      blue_attributes:
        convertMotionTestParamsToPropAttributes(blueMotionParams),
    };
    const redStepDef = {
      red_attributes: convertMotionTestParamsToPropAttributes(redMotionParams),
    };

    const blueEndpoints = calculateStepEndpoints(blueStepDef, "blue");
    const redEndpoints = calculateStepEndpoints(redStepDef, "red");

    if (!blueEndpoints || !redEndpoints) return null;

    const blueDeltaAngle = normalizeAngleSigned(
      blueEndpoints.targetCenterAngle - blueEndpoints.startCenterAngle
    );
    const redDeltaAngle = normalizeAngleSigned(
      redEndpoints.targetCenterAngle - redEndpoints.startCenterAngle
    );

    const blueTurnAngle = Math.PI * blueMotionParams.turns;
    const redTurnAngle = Math.PI * redMotionParams.turns;

    const blueDistance = (Math.abs(blueDeltaAngle) * 180) / Math.PI;
    const redDistance = (Math.abs(redDeltaAngle) * 180) / Math.PI;

    return {
      blue: {
        startCenterAngle: blueEndpoints.startCenterAngle,
        startStaffAngle: blueEndpoints.startStaffAngle,
        targetCenterAngle: blueEndpoints.targetCenterAngle,
        targetStaffAngle: blueEndpoints.targetStaffAngle,
        deltaAngle: blueDeltaAngle,
        turnAngle: blueTurnAngle,
        distance: blueDistance,
      },
      red: {
        startCenterAngle: redEndpoints.startCenterAngle,
        startStaffAngle: redEndpoints.startStaffAngle,
        targetCenterAngle: redEndpoints.targetCenterAngle,
        targetStaffAngle: redEndpoints.targetStaffAngle,
        deltaAngle: redDeltaAngle,
        turnAngle: redTurnAngle,
        distance: redDistance,
      },
      interpolationT: animationState.progress,
      currentBeat: animationState.progress * totalBeats,
    };
  });

  // Orientation arrows for display
  function getOrientationArrow(orientation: string): string {
    const arrows: Record<string, string> = {
      in: "→",
      out: "←",
      n: "↑",
      e: "→",
      s: "↓",
      w: "←",
      clock: "↻",
      counter: "↺",
    };
    return arrows[orientation] || "→";
  }

  // Grid type actions
  function setGridType(type: "diamond" | "box") {
    gridType = type;
  }

  // Cleanup on destroy
  function destroy() {
    pauseAnimation();
  }

  // Return the reactive state and methods
  return {
    // Reactive state (getters for proper reactivity)
    get blueMotionParams() {
      return blueMotionParams;
    },
    get redMotionParams() {
      return redMotionParams;
    },
    get propVisibility() {
      return propVisibility;
    },
    get animationState() {
      return animationState;
    },
    get gridType() {
      return gridType;
    },
    get currentPropStates() {
      return currentPropStates();
    },
    get blueMotionDescription() {
      return blueMotionDescription();
    },
    get redMotionDescription() {
      return redMotionDescription();
    },
    get debugInfo() {
      return debugInfo();
    },
    get isEngineInitialized() {
      return isEngineInitialized;
    },
    get totalBeats() {
      return totalBeats;
    },

    // Motion parameter actions
    updateBlueMotionParam,
    updateRedMotionParam,
    setBlueStartLocation,
    setBlueEndLocation,
    setRedStartLocation,
    setRedEndLocation,

    // Animation actions
    setProgress,
    setSpeed,
    startAnimation,
    pauseAnimation,
    resetAnimation,
    stepAnimation,

    // Visibility actions
    toggleBlueProp,
    toggleRedProp,
    setBluePropVisible,
    setRedPropVisible,
    showBothProps,
    showOnlyBlue,
    showOnlyRed,

    // Grid actions
    setGridType,

    // Utility actions
    getOrientationArrow,
    destroy,
  };
}

export type MotionTesterState = ReturnType<typeof createMotionTesterState>;
