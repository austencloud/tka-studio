/**
 * CAP Component definitions and metadata
 * Re-exports from domain layer for UI convenience
 */

// Re-export domain models and constants
export type { CAPComponentInfo } from "../../shared/domain";
export { CAP_COMPONENTS } from "../../shared/domain";

// Re-export service functionality
import { CAPExplanationTextGenerator } from "../../shared/services/implementations";
import type { CAPComponent } from "$shared";

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
