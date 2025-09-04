/**
 * Favorites Models
 *
 * Interface definitions for managing user favorites and collections.
 */

export interface FavoriteItem {
  sequenceId: string;
  addedDate: Date;
  tags: string[];
  notes?: string;
}

export interface FavoritesCollection {
  items: FavoriteItem[];
  totalCount: number;
  lastUpdated: Date;
}
