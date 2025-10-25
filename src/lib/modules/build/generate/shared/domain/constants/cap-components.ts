/**
 * CAP Component definitions and metadata
 * Unified export point for all CAP component-related data
 */

// Re-export domain models
export { CAPComponent, type CAPComponentInfo } from "../models";

// Re-export constants
export { CAP_COMPONENTS } from "./cap-constants";

// Re-export service functionality
import { CAPExplanationTextGenerator } from "../../services";
import type { CAPComponent } from "../models";

// Create a singleton instance for convenience
const explanationGenerator = new CAPExplanationTextGenerator();

/**
 * Generate explanation text based on selected components
 * @deprecated Use CAPExplanationTextGenerator service instead
 */
export function generateExplanationText(
  selectedComponents: Set<CAPComponent>
): string {
  return explanationGenerator.generateExplanationText(selectedComponents);
}
