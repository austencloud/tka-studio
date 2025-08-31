/**
 * Other Types
 *
 * Domain models extracted from service implementations.
 */

// Add missing type definitions at the top
export type QualityLevel = "low" | "medium" | "high" | "ultra";

// Import required types

export interface CometConfig {
  size: number;
  speed: number;
  color: string;
  tailLength: number;
  interval: number;
  enabledOnQuality: QualityLevel[];
}
