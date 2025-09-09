/**
 * Arrow Positioning Service Contracts
 */

export * from './IArrowLocationService';
export * from './IArrowPlacementKeyService';
export * from './IArrowPositioningOrchestrator';
export * from './IArrowPositioningService';
export * from './IDirectionalTupleService';

// Consolidated contract files
export type {
    IArrowPathResolutionService, IArrowPointCalculator, IDashLocationCalculator,
    IQuadrantIndexCalculator
} from "./arrow-calculation-contracts";

export type {
    IAttributeKeyGenerator, IPlacementKeyGenerator, ISpecialPlacementOriKeyGenerator,
    ITurnsTupleKeyGenerator
} from "./arrow-key-generation-contracts";

export type {
    IArrowAdjustmentLookup, IDefaultPlacementService, ISpecialPlacementService
} from "./arrow-placement-contracts";

// Export placement data types from placement contracts
export type {
    AllPlacementData, GridPlacementData, IArrowPlacementService, JsonPlacementData
} from "../../placement/services/contracts/IArrowPlacementService";

