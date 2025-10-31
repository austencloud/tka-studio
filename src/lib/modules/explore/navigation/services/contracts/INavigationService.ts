import type { SequenceData } from "../../../../../shared";
import type {
  ExploreNavigationConfig,
  ExploreNavigationItem,
} from "../../domain";

export interface INavigationService {
  buildNavigationStructure(
    sequences: SequenceData[]
  ): Promise<ExploreNavigationConfig[]>;
  getNavigationItem(
    sectionId: string,
    itemId: string
  ): Promise<ExploreNavigationItem | null>;
  generateNavigationSections(
    sequences: SequenceData[],
    favorites: string[]
  ): Promise<ExploreNavigationConfig[]>;
  getSequencesForNavigationItem(
    item: ExploreNavigationItem,
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
    sections: ExploreNavigationConfig[]
  ): ExploreNavigationConfig[];
  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: ExploreNavigationConfig[]
  ): ExploreNavigationConfig[];
  filterSequencesByNavigation(
    sequences: SequenceData[],
    item: unknown,
    sectionType: string
  ): Promise<SequenceData[]>;
}
