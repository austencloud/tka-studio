/**
 * Animator Service Implementations
 *
 * ONLY implementation classes - NO interfaces re-exported here.
 * Interfaces are exported from contracts/index.ts
 */

// Core animation services
export { AnimationLoopService } from "./AnimationLoopService";
export { AnimationPlaybackController } from "./AnimationPlaybackController";
export { AnimationStateManager as AnimationStateService } from "./AnimationStateManager";
export { BeatCalculator as BeatCalculationService } from "./BeatCalculator";
export { PropInterpolator as PropInterpolationService } from "./PropInterpolator";
export { SequenceAnimationOrchestrator } from "./SequenceAnimationOrchestrator";

// Calculation services
export { AngleCalculator } from "./AngleCalculator";
export { CoordinateUpdater } from "./CoordinateUpdater";
export { EndpointCalculator } from "./EndpointCalculator";
export { MotionCalculator } from "./MotionCalculator";

// Rendering services
export { CanvasRenderer } from "./CanvasRenderer";
export { SVGGenerator } from "./SVGGenerator";
export { GifExportService } from "./GifExportService";
export { GifExportOrchestrator } from "./GifExportOrchestrator";

