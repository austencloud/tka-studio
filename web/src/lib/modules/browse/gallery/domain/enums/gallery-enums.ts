// ============================================================================
// BROWSE ENUMS
// ============================================================================

export enum GalleryFilterType {
  STARTING_LETTER = "starting_letter",
  CONTAINS_LETTERS = "contains_letters",
  LENGTH = "length",
  DIFFICULTY = "difficulty",
  START_POSITION = "startPosition",
  AUTHOR = "author",
  GRID_MODE = "gridMode",
  ALL_SEQUENCES = "all_sequences",
  FAVORITES = "favorites",
  RECENT = "recent",
}

export enum GallerySortMethod {
  ALPHABETICAL = "alphabetical",
  dateAdded = "dateAdded",
  difficultyLevel = "difficultyLevel",
  sequenceLength = "sequenceLength",
  AUTHOR = "author",
  POPULARITY = "popularity",
}

export enum GalleryNavigationMode {
  FILTER_SELECTION = "filter_selection",
  SEQUENCE_BROWSER = "sequence_browser",
}
