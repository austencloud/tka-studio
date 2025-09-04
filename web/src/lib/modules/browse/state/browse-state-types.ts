/**
 * Browse State Type Definitions
 */

export interface BrowseScrollState {
  scrollTop: number;
  scrollLeft: number;
  containerHeight: number;
  containerWidth: number;
}

export interface BrowseSortState {
  sortMethod: string;
  sortDirection: "asc" | "desc";
}

export interface BrowseViewState {
  viewMode: "grid" | "list";
  showPreview: boolean;
  itemsPerPage: number;
}

export interface CompleteBrowseState {
  scroll: BrowseScrollState;
  sort: BrowseSortState;
  view: BrowseViewState;
  searchQuery?: string;
  selectedItems?: string[];
}
