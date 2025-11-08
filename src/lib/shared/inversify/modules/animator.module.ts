import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  AngleCalculator,
  AnimationLoopService,
  AnimationPlaybackController,
  AnimationStateService,
  AnimatedImageTranscoder,
  BeatCalculationService,
  CanvasRenderer,
  CoordinateUpdater,
  EndpointCalculator,
  GifExportService,
  GifExportOrchestrator,
  MotionCalculator,
  PropInterpolationService,
  SequenceAnimationOrchestrator,
  SequenceLoopabilityChecker,
  SVGGenerator,
} from "../../../modules/create/animate/services";
import { AnimationService } from "../../application/services/implementations";
import { TYPES } from "../types";

export const animatorModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === CORE ANIMATION SERVICES ===
    options.bind(TYPES.IAnimationService).to(AnimationService);
    options.bind(TYPES.IAnimationLoopService).to(AnimationLoopService);
    options
      .bind(TYPES.IAnimationPlaybackController)
      .to(AnimationPlaybackController);
    options
      .bind(TYPES.ISequenceAnimationOrchestrator)
      .to(SequenceAnimationOrchestrator);
    options.bind(TYPES.IAnimationStateService).to(AnimationStateService);
    options.bind(TYPES.IBeatCalculationService).to(BeatCalculationService);
    options.bind(TYPES.IPropInterpolationService).to(PropInterpolationService);
    options
      .bind(TYPES.ISequenceLoopabilityChecker)
      .to(SequenceLoopabilityChecker);

    // === CALCULATION SERVICES ===
    options.bind(TYPES.IAngleCalculator).to(AngleCalculator);
    options.bind(TYPES.ICoordinateUpdater).to(CoordinateUpdater);
    options.bind(TYPES.IMotionCalculator).to(MotionCalculator);
    options.bind(TYPES.IEndpointCalculator).to(EndpointCalculator);

    // === RENDERING SERVICES ===
    options.bind(TYPES.ICanvasRenderer).to(CanvasRenderer);
    options.bind(TYPES.ISVGGenerator).to(SVGGenerator);
    options.bind(TYPES.IGifExportService).to(GifExportService);
    options.bind(TYPES.IAnimatedImageTranscoder).to(AnimatedImageTranscoder);
    options.bind(TYPES.IGifExportOrchestrator).to(GifExportOrchestrator);

    // ============================================================================
    // ARCHIVED BINDINGS (services moved to archive/animator-unused-services/)
    // ============================================================================
    // options.bind(TYPES.IAnimationControlService).to(AnimationControlService);
    // options.bind(TYPES.IMotionParameterService).to(MotionParameterService);
    // options.bind(TYPES.IMotionLetterIdentificationService).to(MotionLetterIdentificationService);
    // options.bind(TYPES.IOverlayRenderer).to(OverlayRenderer);
    // options.bind(TYPES.ISvgConfig).to(SvgConfig);
    // options.bind(TYPES.ISvgUtilityService).to(SvgUtilityService);
  }
);
