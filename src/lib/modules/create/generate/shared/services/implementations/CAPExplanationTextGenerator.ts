/**
 * CAPExplanationTextGenerator - Generates explanation text for CAP transformations
 */

import { injectable } from "inversify";
import { CAPComponent, CAP_COMPONENTS } from "../../domain";
import type { ICAPExplanationTextGenerator } from "../contracts/ICAPExplanationTextGenerator";

/**
 * Service for generating user-friendly explanation text for CAP transformations
 */
@injectable()
export class CAPExplanationTextGenerator
  implements ICAPExplanationTextGenerator
{
  /**
   * Descriptions for each CAP transformation type
   * Kept in the service layer as they're only used for explanation generation
   */
  private readonly descriptions: Record<CAPComponent, string> = {
    [CAPComponent.ROTATED]:
      "Rotates the sequence 180 degrees, flipping all movements to their opposite positions.",
    [CAPComponent.MIRRORED]:
      "Mirrors the sequence horizontally, creating a reflection of all movements.",
    [CAPComponent.SWAPPED]:
      "Swaps the left and right hand movements throughout the sequence.",
    [CAPComponent.COMPLEMENTARY]:
      "Applies complementary transformations to create variations of the base sequence.",
  };

  /**
   * Generate explanation text based on selected components
   */
  public generateExplanationText(
    selectedComponents: Set<CAPComponent>
  ): string {
    const selected = Array.from(selectedComponents);

    if (selected.length === 0) {
      return "Select one or more CAP types to transform your sequence. You can combine multiple transformations for complex variations.";
    }

    if (selected.length === 1) {
      const component = selected[0]!;
      const componentInfo = CAP_COMPONENTS.find(
        (c) => c.component === component
      );
      const description = this.descriptions[component];
      return `Your sequence will be ${componentInfo?.label.toLowerCase()}: ${description}`;
    }

    const labels = selected
      .map((c) => CAP_COMPONENTS.find((comp) => comp.component === c)?.label)
      .join(" + ");
    return `Your sequence will combine ${labels}: This creates a complex transformation by applying all selected operations in sequence.`;
  }
}
