import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  AnimationControlService,
  AnimationStateService,
  BeatCalculationService,
  MotionLetterIdentificationService,
  MotionParameterService,
  OverlayRenderer,
  PropInterpolationService,
  SequenceAnimationEngine,
  SequenceAnimationOrchestrator,
  SvgConfig,
  SvgUtilityService,
} from "../../../modules/animator/services";
import { AnimationService } from "../../application/services/implementations";
import { TYPES } from "../types";

export const animatorModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === ANIMATION SERVICES ===
    options.bind(TYPES.IAnimationService).to(AnimationService);
    options.bind(TYPES.IAnimationControlService).to(AnimationControlService);
    options.bind(TYPES.IMotionParameterService).to(MotionParameterService);
    options.bind(TYPES.ISequenceAnimationEngine).to(SequenceAnimationEngine);
    options.bind(TYPES.ISequenceAnimationOrchestrator).to(SequenceAnimationOrchestrator);
    options.bind(TYPES.IAnimationStateService).to(AnimationStateService);
    options.bind(TYPES.IBeatCalculationService).to(BeatCalculationService);
    options.bind(TYPES.IPropInterpolationService).to(PropInterpolationService);
    options.bind(TYPES.IMotionLetterIdentificationService).to(MotionLetterIdentificationService);

    // === RENDERING SERVICES ===
    options.bind(TYPES.IOverlayRenderer).to(OverlayRenderer);
    options.bind(TYPES.ISvgConfig).to(SvgConfig);
    options.bind(TYPES.ISvgUtilityService).to(SvgUtilityService);
  }
);
