/**
 * Browse State Models
 *
 * Domain models for browse functionality state management.
 * Ported from desktop app's browse models.
 */

import {
  GallerySortMethod,
  type GalleryFilterType,
} from "../../gallery/domain/enums/gallery-enums";
import type { GalleryFilterValue } from "../../gallery/domain/types/gallery-types";

export interface BrowseState {
  filterType: GalleryFilterType | null;
  filterValues: GalleryFilterValue;
  selectedSequence: string | null;
  selectedVariation: number | null;
  sortMethod: GallerySortMethod;
}

// SequenceData eliminated - using SequenceData directly
// This eliminates 95% duplication and clarifies starting position types
