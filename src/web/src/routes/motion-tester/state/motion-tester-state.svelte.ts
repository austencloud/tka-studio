import {
  MotionParameterService,
  type MotionTestParams,
} from "../services/MotionParameterService";
import {
  AnimationControlService,
  type AnimationState,
  type PropVisibility,
  type PropStates,
} from "../services/AnimationControlService";
import { OrientationAutoCalculationService } from "../services/OrientationAutoCalculationService";

export interface MotionTesterState {
  // Reactive state getters
  get blueMotionParams(): MotionTestParams;
  get redMotionParams(): MotionTestParams;
  get animationState(): AnimationState;
  get propVisibility(): PropVisibility;
  get currentPropStates(): PropStates;
  get isEngineInitialized(): boolean;
  get gridType(): "diamond" | "box";

  // Blue prop methods
  setBlueStartLocation: (location: string) => void;
  setBlueEndLocation: (location: string) => void;
  updateBlueMotionParam: (param: keyof MotionTestParams, value: any) => void;

  // Red prop methods
  setRedStartLocation: (location: string) => void;
  setRedEndLocation: (location: string) => void;
  updateRedMotionParam: (param: keyof MotionTestParams, value: any) => void;

  // Animation control methods
  setProgress: (progress: number) => void;
  startAnimation: () => void;
  stopAnimation: () => void;
  resetAnimation: () => void;

  // Grid control methods
  setGridType: (gridType: "diamond" | "box") => void;
}

export function createMotionTesterState(): MotionTesterState {
  // Services
  const motionService = new MotionParameterService();
  const animationService = new AnimationControlService();
  const orientationService = new OrientationAutoCalculationService();

  // Reactive state
  let blueMotionParams = $state<MotionTestParams>(
    motionService.createDefaultParams(),
  );
  let redMotionParams = $state<MotionTestParams>({
    ...motionService.createDefaultParams(),
    startLoc: "e",
    endLoc: "w",
    motionType: "dash",
  });

  // Props are always visible - no user controls needed
  let propVisibility = $state<PropVisibility>({
    blue: true,
    red: true,
  });

  let animationState = $state<AnimationState>({
    isPlaying: false,
    progress: 0,
    currentBeat: 0,
  });

  let isEngineInitialized = $state(false);
  let gridType = $state<"diamond" | "box">("diamond");

  // Auto-calculate rotation direction for blue prop
  $effect(() => {
    const newRotDir = motionService.calculateRotationDirection(
      blueMotionParams.motionType,
      blueMotionParams.startLoc,
      blueMotionParams.endLoc,
    );
    if (newRotDir !== blueMotionParams.propRotDir) {
      blueMotionParams.propRotDir = newRotDir;
    }
  });

  // Auto-calculate end orientation for blue prop
  $effect(() => {
    const newEndOri =
      orientationService.calculateEndOrientation(blueMotionParams);
    if (newEndOri !== blueMotionParams.endOri) {
      blueMotionParams.endOri = newEndOri;
    }
  });

  // Auto-calculate rotation direction for red prop
  $effect(() => {
    const newRotDir = motionService.calculateRotationDirection(
      redMotionParams.motionType,
      redMotionParams.startLoc,
      redMotionParams.endLoc,
    );
    if (newRotDir !== redMotionParams.propRotDir) {
      redMotionParams.propRotDir = newRotDir;
    }
  });

  // Auto-calculate end orientation for red prop
  $effect(() => {
    const newEndOri =
      orientationService.calculateEndOrientation(redMotionParams);
    if (newEndOri !== redMotionParams.endOri) {
      redMotionParams.endOri = newEndOri;
    }
  });

  // Initialize engine when motion parameters change
  $effect(() => {
    const initEngine = async () => {
      const success = await animationService.initializeEngine(
        blueMotionParams,
        redMotionParams,
      );
      isEngineInitialized = success;
    };
    initEngine();
  });

  // Update animation state
  $effect(() => {
    animationState.progress = animationService.getProgress();
    animationState.currentBeat = animationService.getCurrentBeat();
    animationState.isPlaying = animationService.isPlaying();
  });

  return {
    // Reactive state getters
    get blueMotionParams() {
      return blueMotionParams;
    },
    get redMotionParams() {
      return redMotionParams;
    },
    get animationState() {
      return animationState;
    },
    get propVisibility() {
      return propVisibility;
    },
    get currentPropStates() {
      return animationService.getCurrentPropStates();
    },
    get isEngineInitialized() {
      return isEngineInitialized;
    },
    get gridType() {
      return gridType;
    },

    // Blue prop methods
    setBlueStartLocation: (location: string) => {
      blueMotionParams.startLoc = location;
      blueMotionParams =
        motionService.updateMotionTypeForLocations(blueMotionParams);
    },

    setBlueEndLocation: (location: string) => {
      blueMotionParams.endLoc = location;
      blueMotionParams =
        motionService.updateMotionTypeForLocations(blueMotionParams);
    },

    updateBlueMotionParam: (param: keyof MotionTestParams, value: any) => {
      (blueMotionParams as any)[param] = value;
    },

    // Red prop methods
    setRedStartLocation: (location: string) => {
      redMotionParams.startLoc = location;
      redMotionParams =
        motionService.updateMotionTypeForLocations(redMotionParams);
    },

    setRedEndLocation: (location: string) => {
      redMotionParams.endLoc = location;
      redMotionParams =
        motionService.updateMotionTypeForLocations(redMotionParams);
    },

    updateRedMotionParam: (param: keyof MotionTestParams, value: any) => {
      (redMotionParams as any)[param] = value;
    },

    // Animation control methods
    setProgress: (progress: number) => {
      animationService.setProgress(progress);
    },

    startAnimation: () => {
      animationService.startAnimation();
    },

    stopAnimation: () => {
      animationService.stopAnimation();
    },

    resetAnimation: () => {
      animationService.resetAnimation();
    },

    // Grid control methods
    setGridType: (newGridType: "diamond" | "box") => {
      gridType = newGridType;
    },
  };
}
