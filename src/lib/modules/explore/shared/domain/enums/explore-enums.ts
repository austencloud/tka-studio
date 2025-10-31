// ============================================================================
// BROWSE ENUMS
// ============================================================================

// Note: ExploreFilterType has been moved to filtering/domain/filtering-enums.ts
// and is re-exported from this module's index.ts for compatibility

export enum ExploreSortMethod {
  ALPHABETICAL = "alphabetical",
  DATE_ADDED = "date",
  DIFFICULTY_LEVEL = "level",
  SEQUENCE_LENGTH = "length",
  AUTHOR = "author",
  POPULARITY = "popularity",
}

export enum ExploreNavigationMode {
  FILTER_SELECTION = "filter_selection",
  SEQUENCE_BROWSER = "sequence_browser",
}
