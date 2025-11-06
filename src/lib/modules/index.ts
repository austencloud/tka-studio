/**
 * TKA Modules - Module-First Architecture
 *
 * Main export point for all TKA modules organized by business features.
 * Each module contains its own components, domain, services, and state.
 *
 * WARNING: Some type names (e.g., GridLayout) exist in multiple modules.
 * When using types from this barrel export, TypeScript may report ambiguity errors.
 * Solution: Import directly from the specific module you need:
 *   - import { GridLayout } from "$create/workspace-panel/sequence-display/domain"
 *   - import { GridLayout } from "$wordcard/domain/models/PageLayout"
 */

export * from "./about";
export * from "./animate";
export * from "./create";
export * from "./explore";
export * from "./learn";
export * from "./collect";
export * from "./collection"; // Legacy - kept for backwards compatibility
export * from "./library"; // Legacy - kept for backwards compatibility
export * from "./word-card";
export * from "./write";
