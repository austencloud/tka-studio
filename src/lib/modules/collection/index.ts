/**
 * Collection Module - Legacy Export
 *
 * This module has been renamed to "collect" to follow the verb naming pattern.
 * This file exists for backwards compatibility during migration.
 *
 * @deprecated Use "collect" module instead
 */

// Re-export everything from the new collect module
export * from "../collect";

// Legacy named exports
export { CollectTab as CollectionTab } from "../collect";
