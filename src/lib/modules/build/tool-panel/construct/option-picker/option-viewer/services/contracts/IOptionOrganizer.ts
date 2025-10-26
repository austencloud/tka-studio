/**
 * Option Organizer Service Contract
 *
 * Handles organization of pictograph options into sections and groups.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData } from "$shared";
import type { OrganizedSection, SortMethod } from "../../domain";



export interface IOptionOrganizer {
  /**
   * Organize pictographs by sort method into sections
   */
  organizePictographs(
    pictographs: PictographData[],
    sortMethod: SortMethod
  ): OrganizedSection[];
}
