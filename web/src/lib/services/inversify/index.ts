/**
 * Barrel export for InversifyJS dependency injection system.
 * 
 * This provides a clean, centralized way to import all DI-related
 * functionality using the $inversify alias.
 */

// Export the configured container and resolve function
export { container, resolve } from "./container";

// Export all type symbols
export { TYPES } from "./types";

// Export bootstrap function
export { bootstrap } from "./bootstrap";

// Re-export commonly used inversify decorators and types
export { injectable, inject, Container } from "inversify";
export type { interfaces } from "inversify";
