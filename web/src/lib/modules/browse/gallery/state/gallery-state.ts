import type { SequenceData } from "../../../../shared/domain";

export interface GalleryLoadingState {
  isLoading: boolean;
  loadedCount: number;
  totalCount: number;
  currentOperation: string;
  error: string | null;
}

export interface GalleryDisplayState {
  sequences: SequenceData[];
  sortedSections: Record<string, SequenceData[]>;
  currentSection: string | null;
  thumbnailWidth: number;
  gridColumns: number;
}
