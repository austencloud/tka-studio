import { GallerySortMethod } from "../enums";
import type { SortConfig } from "../models/sort-models";

// Predefined sort configurations
export const SORT_CONFIGS: Record<GallerySortMethod, SortConfig> = {
  [GallerySortMethod.ALPHABETICAL]: {
    method: GallerySortMethod.ALPHABETICAL,
    direction: "asc",
    displayName: "Name A-Z",
  },
  [GallerySortMethod.dateAdded]: {
    method: GallerySortMethod.dateAdded,
    direction: "desc",
    displayName: "Recently Added",
  },
  [GallerySortMethod.difficultyLevel]: {
    method: GallerySortMethod.difficultyLevel,
    direction: "asc",
    displayName: "Difficulty",
  },
  [GallerySortMethod.sequenceLength]: {
    method: GallerySortMethod.sequenceLength,
    direction: "asc",
    displayName: "Length",
  },
  [GallerySortMethod.AUTHOR]: {
    method: GallerySortMethod.AUTHOR,
    direction: "asc",
    displayName: "Author",
  },
  [GallerySortMethod.POPULARITY]: {
    method: GallerySortMethod.POPULARITY,
    direction: "desc",
    displayName: "Popularity",
  },
};
