/**
 * Browse Sort Models
 *
 * Interface definitions for browse sorting functionality.
 */
import type { SortMethod, SortDirection } from "$domain";

export interface SortConfig {
  method: SortMethod;
  direction: SortDirection;
  displayName: string;
}
