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

// Re-export commonly used inversify decorators and types
export { Container, inject, injectable } from "inversify";
