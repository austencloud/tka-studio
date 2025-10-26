/**
 * Service contract for generating CAP transformation explanation text
 */

import type { CAPComponent } from "../../domain";

/**
 * Generates user-friendly explanation text for CAP transformations
 */
export interface ICAPExplanationTextGenerator {
  /**
   * Generate explanation text based on selected CAP components
   * @param selectedComponents Set of selected CAP components
   * @returns Human-readable explanation text
   */
  generateExplanationText(selectedComponents: Set<CAPComponent>): string;
}
