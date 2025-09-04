/**
 * Browse State Models
 *
 * Domain models for browse functionality state management.
 * Ported from desktop app's browse models.
 */

import type { GalleryFilterValue } from "../../domain/types";
import {
  GallerySortMethod,
  type FilterType,
} from "../../gallery/domain/enums/gallery-enums";

export interface BrowseState {
  filterType: FilterType | null;
  filterValues: GalleryFilterValue;
  selectedSequence: string | null;
  selectedVariation: number | null;
  sortMethod: GallerySortMethod;
}

// SequenceData eliminated - using SequenceData directly
// This eliminates 95% duplication and clarifies starting position types
