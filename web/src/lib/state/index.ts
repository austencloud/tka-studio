/**
 * State Management Barrel Exports
 *
 * Central export point for all state management modules.
 * Use `$state` imports to access any state functionality.
 *
 * Note: Domain types should be imported from $domain, not from here.
 */

// ============================================================================
// CORE APPLICATION STATE
// ============================================================================
export * from "./app-mode-state.svelte";
export * from "./app-state.svelte";

// ============================================================================
// BACKGROUND STATE
// ============================================================================
export * from "./background-state.svelte";

// ============================================================================
// TAB STATES
// ============================================================================
export * from "./build-tab-state.svelte";
export * from "./construct-tab-state.svelte";

// ============================================================================
// BROWSE STATE
// ============================================================================
export * from "./browse-state-factory.svelte";
export * from "./browse-tab-state-manager.svelte";

// ============================================================================
// SEQUENCE CARD STATE
// ============================================================================
export * from "./sequence-card/display-state.svelte";
export * from "./sequence-card/sequence-card-state-factory.svelte";

// ============================================================================
// WORKBENCH & BUILD STATES
// ============================================================================
export * from "./beat-frame/beat-frame-state.svelte";
export * from "./sequence/sequence-state.svelte";
export * from "./workbench/workbench-state.svelte";

// ============================================================================
// COMPONENT STATES
// ============================================================================
export * from "./codex-state.svelte";
export * from "./modal-state.svelte";
export * from "./option-picker-state.svelte";
export * from "./page-layout-state.svelte";
export * from "./panel-state.svelte";
export * from "./start-position-state.svelte";

// ============================================================================
// GENERATION STATES
// ============================================================================
export * from "./generate/generate-actions.svelte";
export { createGenerationConfigState } from "./generate/generate-config.svelte";
export * from "./generate/generate-device.svelte";

// ============================================================================
// EXPORT STATES
// ============================================================================
export * from "./image-export-state.svelte";

// ============================================================================
// MOTION TESTER STATE
// ============================================================================
export * from "./motion-tester/motion-tester-state.svelte";

// ============================================================================
// PICTOGRAPH GENERATION STATE
// ============================================================================
export * from "./pictograph-generation.svelte";

// ============================================================================
// STATE SERVICES
// ============================================================================
export * from "./services/ApplicationStateService.svelte";
export * from "./services/InitializationService.svelte";
export * from "./services/PerformanceMetricsService.svelte";
export * from "./services/SettingsService.svelte";
export * from "./services/TabStateService.svelte";

// Browse state services
export * from "./services/BrowseDisplayStateService.svelte";
export * from "./services/BrowseFilterStateService.svelte";
export * from "./services/BrowseNavigationStateService.svelte";
export * from "./services/BrowseSearchStateService.svelte";
export * from "./services/BrowseSelectionStateService.svelte";
export * from "./services/BrowseStateCoordinator.svelte";

// Service interfaces and implementations
export * from "./services/implementations/ApplicationStateService";
export * from "./services/state-service-interfaces";

// ============================================================================
// UTILITIES
// ============================================================================
export * from "./utils/auto-sync-state.svelte";
