/**
 * Service Contracts Index
 *
 * Central export for all service behavioral contracts.
 * These define what operations and behaviors are available.
 */

// ENTERPRISE PATTERN: One-to-one interface-to-implementation mapping
// Organized by domain structure that mirrors implementations

// Animation Domain
export * from "./animation/IAnimationControlService";
export * from "./animation/IAnimationStateService";
export * from "./animation/IBeatCalculationService";
export * from "./animation/IPropInterpolationService";
export * from "./animation/ISequenceAnimationOrchestrator";

// Application Domain
export * from "./application/IApplicationInitializer";
export * from "./application/ICodexService";
export * from "./application/IConstructTabCoordinator";
export * from "./application/ICSVLoader";
export * from "./application/ICSVParser";
export * from "./application/IDeviceDetector";
export * from "./application/IEnumMapper";
export * from "./application/IOptionDataService";
export * from "./application/ISettingsService";
export * from "./application/IStartPositionService";

// Background Domain
export * from "./background/IBackgroundFactory";
export * from "./background/IBackgroundService";
export * from "./background/IBackgroundSystem";
// Browse Domain - TODO: Move to individual interface files
// TEMPORARILY REMOVED: export * from "./browse-interfaces"; (conflicts with DeleteConfirmationData, DeleteResult, IDeleteService)

// Build Domain - TODO: Move to individual interface files
export * from "./build-interfaces";

// Generation Domain - TODO: Move to individual interface files
// TEMPORARILY REMOVED: export * from "./generation-interfaces"; (conflicts with IOptionDataService)

// TODO: Replace these consolidated interface files with individual domain-organized interfaces
// Following the one-to-one interface-to-implementation pattern

// Sequence Domain - Individual interface (correct pattern)
export * from "./sequence/ISequenceStateService";

// Temporary exports until migration to individual interfaces is complete
// TEMPORARILY REMOVED: export * from "./motion-tester-interfaces"; (conflicts with IAnimationControlService)
export * from "./option-picker-interfaces";
export * from "./panel-interfaces";
// TEMPORARILY REMOVED: export * from "./pictograph-interfaces"; (conflicts with IArrowPathResolutionService, IArrowPositioningService)
// TEMPORARILY REMOVED: export * from "./positioning-interfaces"; (conflicts with pictograph services)
export * from "./responsive-layout-interfaces";
export * from "./sequence-interfaces";
// TEMPORARILY REMOVED: export * from "./sequence-state-interfaces"; (conflicts with ISequenceStateService)
export * from "./svg-conversion-interfaces";
export * from "./text-rendering-interfaces";
export * from "./workbench-interfaces";
