/**
 * Explore Type Aliases
 *
 * Type aliases and utility types for gallery functionality.
 * Separated from interfaces and enums for clean architecture.
 */

// Re-export filtering types for compatibility
export type { ExploreFilterValue } from "$shared/persistence/domain";

// Explore-specific type aliases
export type SortDirection = "asc" | "desc";
