/**
 * Explore Tab Types
 * Type definitions for the explore module tab navigation
 */

export type ExploreTabType = "sequences" | "users" | "collections" | "search";

export interface ExploreTab {
  id: ExploreTabType;
  label: string;
  icon: string;
  disabled?: boolean;
}
