import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  ArrowAdjustmentCalculator,
  ArrowAdjustmentProcessor,
  ArrowCoordinateTransformer,
  ArrowDataProcessor,
  ArrowGridCoordinateService,
  ArrowLifecycleManager,
  ArrowLocationCalculator,
  ArrowLocationService,
  ArrowPathResolutionService,
  ArrowPlacementKeyService,
  ArrowPlacementService,
  ArrowPositioningOrchestrator,
  ArrowQuadrantCalculator,
  ArrowRenderer,
  ArrowRotationCalculator,
  AttributeKeyGenerator,
  BetaDetectionService, BetaOffsetCalculator,
  DashLocationCalculator,
  DefaultPlacementService,
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  GridModeDeriver, GridPositionDeriver, GridRenderingService,
  GridService,
  LetterQueryHandler,
  MotionQueryHandler,
  OrientationCalculationService,
  PictographCoordinator,
  PropCoordinator, PropLifecycleManager,
  PropPlacementService, PropSvgLoader,
  QuadrantIndexCalculator,
  SpecialPlacementOriKeyGenerator,
  SpecialPlacementService,
  SvgPreloadService,
  TurnsTupleKeyGenerator
} from "../../pictograph";
import { TYPES } from "../types";

export const pictographModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === ARROW SERVICES ===
    options.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService);
    options.bind(TYPES.IArrowLocationService).to(ArrowLocationService);
    options.bind(TYPES.IArrowPlacementKeyService).to(ArrowPlacementKeyService);
    options.bind(TYPES.IArrowRenderer).to(ArrowRenderer);
    options.bind(TYPES.IArrowLifecycleManager).to(ArrowLifecycleManager);
    options.bind(TYPES.IArrowPathResolutionService).to(ArrowPathResolutionService);
    options.bind(TYPES.IArrowGridCoordinateService).to(ArrowGridCoordinateService);

    // === ARROW ORCHESTRATION SERVICES ===
    options.bind(TYPES.IArrowAdjustmentProcessor).to(ArrowAdjustmentProcessor);
    options.bind(TYPES.IArrowCoordinateTransformer).to(ArrowCoordinateTransformer);
    options.bind(TYPES.IArrowDataProcessor).to(ArrowDataProcessor);
    options.bind(TYPES.IArrowQuadrantCalculator).to(ArrowQuadrantCalculator);

    // === ARROW POSITIONING SERVICES ===
    options.bind(TYPES.IArrowPositioningOrchestrator).to(ArrowPositioningOrchestrator);
    options.bind(TYPES.IArrowAdjustmentCalculator).to(ArrowAdjustmentCalculator);
    options.bind(TYPES.IArrowLocationCalculator).to(ArrowLocationCalculator);
    options.bind(TYPES.IArrowRotationCalculator).to(ArrowRotationCalculator);
    options.bind(TYPES.IDashLocationCalculator).to(DashLocationCalculator);
    options.bind(TYPES.ISpecialPlacementService).to(SpecialPlacementService);
    options.bind(TYPES.IDefaultPlacementService).to(DefaultPlacementService);

    // === KEY GENERATORS AND PROCESSORS ===
    options.bind(TYPES.ISpecialPlacementOriKeyGenerator).to(SpecialPlacementOriKeyGenerator);
    options.bind(TYPES.ITurnsTupleKeyGenerator).to(TurnsTupleKeyGenerator);
    options.bind(TYPES.IAttributeKeyGenerator).to(AttributeKeyGenerator);
    options.bind(TYPES.IDirectionalTupleProcessor).to(DirectionalTupleProcessor);
    options.bind(TYPES.IDirectionalTupleCalculator).to(DirectionalTupleCalculator);
    options.bind(TYPES.IQuadrantIndexCalculator).to(QuadrantIndexCalculator);

    // === GRID SERVICES ===
    options.bind(TYPES.IGridModeDeriver).to(GridModeDeriver);
    options.bind(TYPES.IGridPositionDeriver).to(GridPositionDeriver);
    options.bind(TYPES.IGridRenderingService).to(GridRenderingService);
    options.bind(TYPES.IGridService).to(GridService);

    // === PROP SERVICES ===
    options.bind(TYPES.IBetaDetectionService).to(BetaDetectionService);
    options.bind(TYPES.IBetaOffsetCalculator).to(BetaOffsetCalculator);
    options.bind(TYPES.IPropCoordinator).to(PropCoordinator);
    options.bind(TYPES.IPropLifecycleManager).to(PropLifecycleManager);
    options.bind(TYPES.IPropPlacementService).to(PropPlacementService);
    options.bind(TYPES.IPropSvgLoader).to(PropSvgLoader);
    options.bind(TYPES.IOrientationCalculationService).to(OrientationCalculationService);

    // === COORDINATION SERVICES ===
    options.bind(TYPES.IPictographCoordinator).to(PictographCoordinator);

    // === SVG SERVICES ===
    options.bind(TYPES.ISvgPreloadService).to(SvgPreloadService).inSingletonScope();

    // === QUERY HANDLERS ===
    options.bind(TYPES.IMotionQueryHandler).to(MotionQueryHandler);
    options.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);
  }
);
