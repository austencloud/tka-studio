import type { SequenceData } from "$shared/domain";
import type {
  GalleryFilterType,
  GalleryFilterValue,
  GallerySortMethod,
} from "../../domain";

export interface IGalleryService {
  loadSequenceMetadata(): Promise<SequenceData[]>;
  applyFilter(
    sequences: SequenceData[],
    filterType: GalleryFilterType,
    filterValue: GalleryFilterValue
  ): Promise<SequenceData[]>;
  sortSequences(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
  ): Promise<SequenceData[]>;
  groupSequencesIntoSections(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
  ): Promise<Record<string, SequenceData[]>>;
  getUniqueValues(field: keyof SequenceData): Promise<string[]>;
  getFilterOptions(filterType: GalleryFilterType): Promise<string[]>;
}
