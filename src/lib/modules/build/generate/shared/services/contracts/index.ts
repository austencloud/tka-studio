/**
 * Service Contracts - ACTIVE CONTRACTS ONLY
 * Deprecated contracts moved to _deprecated/ folder (2025-10-25)
 */

// Core Generation Service Contracts
export * from "./IBeatConverterService";
export * from "./IBeatGenerationOrchestrator";
export * from "./IComplementaryLetterService";
export * from "./IPictographFilterService";
export * from "./IPictographGenerator";
export * from "./ISequenceMetadataService";
export * from "./IStartPositionSelector";
export * from "./ITurnAllocator";
export * from "./ITurnIntensityManagerService";
export * from "./ITurnManagementService";

// Re-export IOrientationCalculationService from shared pictograph services
export type { IOrientationCalculationService } from "$shared/pictograph/prop/services/contracts";

// UI Service Contracts (SRP Refactoring - Dec 2024)
export * from "./ICAPExplanationTextGenerator";
export * from "./ICAPTypeService";
export * from "./ICardConfigurationService";
export * from "./ILevelConversionService";
export * from "./IResponsiveTypographyService";

// Orchestration Service Contracts (SRP Refactoring - Dec 2024)
export * from "./IGenerationOrchestrationService";
