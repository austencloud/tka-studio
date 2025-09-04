/**
 * Shared Services - Main Export Point
 *
 * Central barrel export for ONLY truly shared/core services.
 * Module-specific services should be imported directly from their modules:
 * - Browse: import from "$browse/services"
 * - Build: import from "$build/services"
 * - Learn: import from "$learn/services"
 * etc.
 */

// ============================================================================
// CORE SERVICES (Truly shared across modules)
// ============================================================================
export * from "./core";
