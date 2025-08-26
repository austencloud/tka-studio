import {
  MotionParameterService,
  type MotionTestParams,
} from "$lib/services/implementations/motion-tester/MotionParameterService";
import {
  AnimationControlService,
  type AnimationState,
  type PropVisibility,
  type PropStates,
} from "$lib/services/implementations/motion-tester/AnimationControlService";
import { resolve } from "$lib/services/bootstrap";
import type { ISequenceAnimationEngine } from "$lib/services/di/interfaces/animator-interfaces";
import { OrientationCalculationService } from "$lib/services/implementations/positioning/OrientationCalculationService";
import {
  MotionLetterIdentificationService,
  type LetterIdentificationResult,
} from "$lib/services/implementations/motion-tester/MotionLetterIdentificationService";

import { MotionType, MotionColor, GridMode, Location } from "$lib/domain/enums";

export interface MotionTesterState {
  // Reactive state getters
  get blueMotionParams(): MotionTestParams;
  get redMotionParams(): MotionTestParams;
  get animationState(): AnimationState;
  get propVisibility(): PropVisibility;
  get currentPropStates(): PropStates;
  get isEngineInitialized(): boolean;
  get gridMode(): GridMode;
  get identifiedLetter(): LetterIdentificationResult;

  // Blue prop methods
  setBlueStartLocation: (location: Location) => void;
  setBlueEndLocation: (location: Location) => void;
  updateBlueMotionParam: <K extends keyof MotionTestParams>(
    param: K,
    value: MotionTestParams[K]
  ) => void;

  // Red prop methods
  setRedStartLocation: (location: Location) => void;
  setRedEndLocation: (location: Location) => void;
  updateRedMotionParam: <K extends keyof MotionTestParams>(
    param: K,
    value: MotionTestParams[K]
  ) => void;

  // Animation control methods
  setProgress: (progress: number) => void;
  startAnimation: () => void;
  stopAnimation: () => void;
  resetAnimation: () => void;

  // Grid control methods
  setGridType: (gridMode: GridMode) => void;
}

export function createMotionTesterState(): MotionTesterState {
  // Services
  const motionService = new MotionParameterService();
  const animationEngine = resolve(
    "ISequenceAnimationEngine"
  ) as ISequenceAnimationEngine;
  const animationService = new AnimationControlService(animationEngine);
  const orientationService = new OrientationCalculationService();
  const letterIdentificationService = new MotionLetterIdentificationService();

  // Reactive state
  let blueMotionParams = $state<MotionTestParams>(
    motionService.createDefaultParams()
  );
  let redMotionParams = $state<MotionTestParams>({
    ...motionService.createDefaultParams(),
    startLocation: Location.EAST,
    endLocation: Location.WEST,
    motionType: MotionType.DASH,
  });

  // Props are always visible - no user controls needed
  const propVisibility = $state<PropVisibility>({
    blue: true,
    red: true,
  });

  const animationState = $state<AnimationState>({
    isPlaying: false,
    progress: 0,
    currentBeat: 0,
  });

  let isEngineInitialized = $state(false);
  let gridMode = $state<GridMode>(GridMode.DIAMOND);

  // Letter identification - reactive to motion parameter changes
  const identifiedLetter = $derived(() => {
    return letterIdentificationService.identifyLetter(
      blueMotionParams,
      redMotionParams,
      gridMode
    );
  });

  // Auto-calculate rotation direction for blue prop
  $effect(() => {
    // Properly access reactive state
    const { motionType, startLocation, endLocation, rotationDirection } =
      blueMotionParams;
    const newRotDir = motionService.calculateRotationDirection(
      motionType,
      startLocation,
      endLocation
    );
    if (newRotDir !== rotationDirection) {
      blueMotionParams.rotationDirection = newRotDir;
    }
  });

  // Auto-calculate end orientation for blue prop
  $effect(() => {
    const motionData = motionService.convertToMotionData(
      blueMotionParams,
      MotionColor.BLUE
    );
    const newEndOri = orientationService.calculateEndOrientation(
      motionData,
      MotionColor.BLUE
    );
    if (newEndOri !== blueMotionParams.endOrientation) {
      blueMotionParams.endOrientation = newEndOri;
    }
  });

  // Auto-calculate rotation direction for red prop
  $effect(() => {
    // Properly access reactive state
    const { motionType, startLocation, endLocation, rotationDirection } =
      redMotionParams;
    console.log(
      `🔴 Red rotation effect triggered: ${startLocation}→${endLocation} (${motionType})`
    );
    const newRotDir = motionService.calculateRotationDirection(
      motionType,
      startLocation,
      endLocation
    );
    console.log(
      `🔴 Red rotation calculated: ${newRotDir}, current: ${rotationDirection}`
    );
    if (newRotDir !== rotationDirection) {
      console.log(
        `🔴 Red rotation updating from ${rotationDirection} to ${newRotDir}`
      );
      redMotionParams.rotationDirection = newRotDir;
    }
  });

  // Auto-calculate end orientation for red prop
  $effect(() => {
    const motionData = motionService.convertToMotionData(
      redMotionParams,
      MotionColor.RED
    );
    const newEndOri = orientationService.calculateEndOrientation(
      motionData,
      MotionColor.RED
    );
    if (newEndOri !== redMotionParams.endOrientation) {
      redMotionParams.endOrientation = newEndOri;
    }
  });

  // Initialize engine when motion parameters change
  $effect(() => {
    const initEngine = async () => {
      // Create copies to properly capture reactive state
      const blueParams = { ...blueMotionParams };
      const redParams = { ...redMotionParams };
      const success = await animationService.initializeEngine(
        blueParams,
        redParams
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
    get gridMode() {
      return gridMode;
    },
    get identifiedLetter() {
      return identifiedLetter();
    },

    // Blue prop methods
    setBlueStartLocation: (location: Location) => {
      blueMotionParams.startLocation = location;
      const updatedParams =
        motionService.updateMotionTypeForLocations(blueMotionParams);
      blueMotionParams = updatedParams;
    },

    setBlueEndLocation: (location: Location) => {
      console.log(
        `🔵 Blue end location changing from ${blueMotionParams.endLocation} to ${location}`
      );
      blueMotionParams.endLocation = location;
      const updatedParams =
        motionService.updateMotionTypeForLocations(blueMotionParams);
      blueMotionParams = updatedParams;
      console.log(`🔵 Blue motion params updated:`, blueMotionParams);
    },

    updateBlueMotionParam: <K extends keyof MotionTestParams>(
      param: K,
      value: MotionTestParams[K]
    ) => {
      blueMotionParams[param] = value;
    },

    // Red prop methods
    setRedStartLocation: (location: Location) => {
      redMotionParams.startLocation = location;
      const updatedParams =
        motionService.updateMotionTypeForLocations(redMotionParams);
      redMotionParams = updatedParams;
    },

    setRedEndLocation: (location: Location) => {
      console.log(
        `🔴 Red end location changing from ${redMotionParams.endLocation} to ${location}`
      );
      redMotionParams.endLocation = location;
      const updatedParams =
        motionService.updateMotionTypeForLocations(redMotionParams);
      redMotionParams = updatedParams;
      console.log(`🔴 Red motion params updated:`, redMotionParams);
    },

    updateRedMotionParam: <K extends keyof MotionTestParams>(
      param: K,
      value: MotionTestParams[K]
    ) => {
      redMotionParams[param] = value;
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
    setGridType: (newGridType: GridMode) => {
      gridMode = newGridType;
    },
  };
}
