import type { SequenceData } from "$shared/domain";
import type { NavigationItem, NavigationSectionConfig } from "../../domain/models/gallery-models";

export interface INavigationService {
  buildNavigationStructure(
    sequences: SequenceData[]
  ): Promise<NavigationSectionConfig[]>;
  getNavigationItem(
    sectionId: string,
    itemId: string
  ): Promise<NavigationItem | null>;
  generateNavigationSections(
    sequences: SequenceData[],
    favorites: string[]
  ): Promise<NavigationSectionConfig[]>;
  getSequencesForNavigationItem(
    item: NavigationItem,
    sectionType:
      | "letter"
      | "author"
      | "level"
      | "length"
      | "favorites"
      | "date",
    allSequences: SequenceData[]
  ): SequenceData[];
  toggleSectionExpansion(
    sectionId: string,
    sections: NavigationSectionConfig[]
  ): NavigationSectionConfig[];
  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: NavigationSectionConfig[]
  ): NavigationSectionConfig[];
}
