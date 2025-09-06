/**
 * Browse State Type Definitions
 */

import type { SequenceData } from "../../../../shared/domain";

export interface GalleryScrollState {
  scrollTop: number;
  scrollLeft: number;
  containerHeight: number;
  containerWidth: number;
}

export interface GallerySortState {
  sortMethod: string;
  sortDirection: "asc" | "desc";
}

export interface GalleryViewState {
  viewMode: "grid" | "list";
  showPreview: boolean;
  itemsPerPage: number;
}

export interface CompleteGalleryState {
  scroll: GalleryScrollState;
  sort: GallerySortState;
  view: GalleryViewState;
  searchQuery?: string;
  selectedItems?: string[];
}
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
