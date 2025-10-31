import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";

// PERFORMANCE FIX: Import services directly to avoid circular dependencies
// Arrow services
import { ArrowAdjustmentProcessor } from "../../pictograph/arrow/orchestration/services/implementations/ArrowAdjustmentProcessor";
import { ArrowCoordinateTransformer } from "../../pictograph/arrow/orchestration/services/implementations/ArrowCoordinateTransformer";
import { ArrowDataProcessor } from "../../pictograph/arrow/orchestration/services/implementations/ArrowDataProcessor";
import { ArrowGridCoordinateService } from "../../pictograph/arrow/orchestration/services/implementations/ArrowGridCoordinateService";
import { ArrowLifecycleManager } from "../../pictograph/arrow/orchestration/services/implementations/ArrowLifecycleManager";
import { ArrowPositioningOrchestrator } from "../../pictograph/arrow/orchestration/services/implementations/ArrowPositioningOrchestrator";
import { ArrowQuadrantCalculator } from "../../pictograph/arrow/orchestration/services/implementations/ArrowQuadrantCalculator";
import { ArrowAdjustmentCalculator } from "../../pictograph/arrow/positioning/calculation/services/implementations/ArrowAdjustmentCalculator";
import { ArrowLocationCalculator } from "../../pictograph/arrow/positioning/calculation/services/implementations/ArrowLocationCalculator";
import { ArrowLocationService } from "../../pictograph/arrow/positioning/calculation/services/implementations/ArrowLocationService";
import { ArrowRotationCalculator } from "../../pictograph/arrow/positioning/calculation/services/implementations/ArrowRotationCalculator";
import { DashLocationCalculator } from "../../pictograph/arrow/positioning/calculation/services/implementations/DashLocationCalculator";
import {
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  QuadrantIndexCalculator,
} from "../../pictograph/arrow/positioning/calculation/services/implementations/DirectionalTupleProcessor";
import { ArrowPlacementKeyService } from "../../pictograph/arrow/positioning/key-generation/services/implementations/ArrowPlacementKeyService";
import { AttributeKeyGenerator } from "../../pictograph/arrow/positioning/key-generation/services/implementations/AttributeKeyGenerator";
import { SpecialPlacementOriKeyGenerator } from "../../pictograph/arrow/positioning/key-generation/services/implementations/SpecialPlacementOriKeyGenerator";
import { RotationAngleOverrideKeyGenerator } from "../../pictograph/arrow/positioning/key-generation/services/implementations/RotationAngleOverrideKeyGenerator";
import { TurnsTupleKeyGenerator } from "../../pictograph/arrow/positioning/key-generation/services/implementations/TurnsTupleKeyGenerator";
import { ArrowPlacementService } from "../../pictograph/arrow/positioning/placement/services/implementations/ArrowPlacementService";
import { DefaultPlacementService } from "../../pictograph/arrow/positioning/placement/services/implementations/DefaultPlacementService";
import { SpecialPlacementService } from "../../pictograph/arrow/positioning/placement/services/implementations/SpecialPlacementService";
import { ArrowPathResolver } from "../../pictograph/arrow/rendering/services/implementations/ArrowPathResolver";
import { ArrowRenderer } from "../../pictograph/arrow/rendering/services/implementations/ArrowRenderer";
import { ArrowSvgColorTransformer } from "../../pictograph/arrow/rendering/services/implementations/ArrowSvgColorTransformer";
import { ArrowSvgLoader } from "../../pictograph/arrow/rendering/services/implementations/ArrowSvgLoader";
import { ArrowSvgParser } from "../../pictograph/arrow/rendering/services/implementations/ArrowSvgParser";

// Grid services
import { GridModeDeriver } from "../../pictograph/grid/services/implementations/GridModeDeriver";
import { GridPositionDeriver } from "../../pictograph/grid/services/implementations/GridPositionDeriver";
import { GridRenderingService } from "../../pictograph/grid/services/implementations/GridRenderingService";

// Prop services
import { BetaDetectionService } from "../../pictograph/prop/services/implementations/BetaDetectionService";
import { OrientationCalculator } from "../../pictograph/prop/services/implementations/OrientationCalculator";
import { PropPlacementService } from "../../pictograph/prop/services/implementations/PropPlacementService";
import { PropSvgLoader } from "../../pictograph/prop/services/implementations/PropSvgLoader";

// Shared services
import { CSVPictographParser } from "../../pictograph/shared/services/implementations/CSVPictographParser";
import { MotionQueryHandler } from "../../pictograph/shared/services/implementations/MotionQueryHandler";
import { PictographCoordinator } from "../../pictograph/shared/services/implementations/PictographCoordinator";
import { SvgPreloadService } from "../../pictograph/shared/services/implementations/SvgPreloadService";
import { LetterQueryHandler } from "../../pictograph/tka-glyph/services/implementations/LetterQueryHandler";
import { TYPES } from "../types";

export const pictographModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === ARROW SERVICES ===
    options.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService);
    options.bind(TYPES.IArrowLocationService).to(ArrowLocationService);
    options.bind(TYPES.IArrowPlacementKeyService).to(ArrowPlacementKeyService);
    options.bind(TYPES.IArrowRenderer).to(ArrowRenderer);
    options.bind(TYPES.IArrowLifecycleManager).to(ArrowLifecycleManager);
    options.bind(TYPES.IArrowPathResolutionService).to(ArrowPathResolver);
    options
      .bind(TYPES.IArrowGridCoordinateService)
      .to(ArrowGridCoordinateService);

    // === ARROW RENDERING SERVICES ===
    options.bind(TYPES.IArrowPathResolver).to(ArrowPathResolver);
    options.bind(TYPES.IArrowSvgLoader).to(ArrowSvgLoader);
    options.bind(TYPES.IArrowSvgParser).to(ArrowSvgParser);
    options.bind(TYPES.IArrowSvgColorTransformer).to(ArrowSvgColorTransformer);

    // === ARROW ORCHESTRATION SERVICES ===
    options.bind(TYPES.IArrowAdjustmentProcessor).to(ArrowAdjustmentProcessor);
    options
      .bind(TYPES.IArrowCoordinateTransformer)
      .to(ArrowCoordinateTransformer);
    options.bind(TYPES.IArrowDataProcessor).to(ArrowDataProcessor);
    options.bind(TYPES.IArrowQuadrantCalculator).to(ArrowQuadrantCalculator);

    // === ARROW POSITIONING SERVICES ===
    options
      .bind(TYPES.IArrowPositioningOrchestrator)
      .to(ArrowPositioningOrchestrator);
    options
      .bind(TYPES.IArrowAdjustmentCalculator)
      .to(ArrowAdjustmentCalculator);
    options.bind(TYPES.IArrowLocationCalculator).to(ArrowLocationCalculator);
    options.bind(TYPES.IArrowRotationCalculator).to(ArrowRotationCalculator);
    options.bind(TYPES.IDashLocationCalculator).to(DashLocationCalculator);
    options.bind(TYPES.ISpecialPlacementService).to(SpecialPlacementService);
    options.bind(TYPES.IDefaultPlacementService).to(DefaultPlacementService);

    // === KEY GENERATORS AND PROCESSORS ===
    options
      .bind(TYPES.ISpecialPlacementOriKeyGenerator)
      .to(SpecialPlacementOriKeyGenerator);
    options.bind(TYPES.ITurnsTupleKeyGenerator).to(TurnsTupleKeyGenerator);
    options.bind(TYPES.IAttributeKeyGenerator).to(AttributeKeyGenerator);
    options
      .bind(TYPES.IRotationAngleOverrideKeyGenerator)
      .to(RotationAngleOverrideKeyGenerator);
    options
      .bind(TYPES.IDirectionalTupleProcessor)
      .to(DirectionalTupleProcessor);
    options
      .bind(TYPES.IDirectionalTupleCalculator)
      .to(DirectionalTupleCalculator);
    options.bind(TYPES.IQuadrantIndexCalculator).to(QuadrantIndexCalculator);

    // === GRID SERVICES ===
    options.bind(TYPES.IGridModeDeriver).to(GridModeDeriver);
    options.bind(TYPES.IGridPositionDeriver).to(GridPositionDeriver);
    options.bind(TYPES.IGridRenderingService).to(GridRenderingService);

    // === PROP SERVICES ===
    options.bind(TYPES.IBetaDetectionService).to(BetaDetectionService);
    options.bind(TYPES.IPropPlacementService).to(PropPlacementService);
    options.bind(TYPES.IPropSvgLoader).to(PropSvgLoader);
    options
      .bind(TYPES.IOrientationCalculationService)
      .to(OrientationCalculator);

    // === COORDINATION SERVICES ===
    options.bind(TYPES.IPictographCoordinator).to(PictographCoordinator);

    // === SVG SERVICES ===
    options
      .bind(TYPES.ISvgPreloadService)
      .to(SvgPreloadService)
      .inSingletonScope();

    // === QUERY HANDLERS ===
    options.bind(TYPES.IMotionQueryHandler).to(MotionQueryHandler);
    options.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);

    // === DATA PARSERS ===
    options.bind(TYPES.ICSVPictographParserService).to(CSVPictographParser);
  }
);
