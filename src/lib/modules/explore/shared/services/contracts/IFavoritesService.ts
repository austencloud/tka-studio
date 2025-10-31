/**
 * Service for managing user favorites
 */
export interface IFavoritesService {
  /** Toggle favorite status for a sequence */
  toggleFavorite(sequenceId: string): Promise<void>;

  /** Check if sequence is favorited */
  isFavorite(sequenceId: string): Promise<boolean>;

  /** Get all favorited sequence IDs */
  getFavorites(): Promise<string[]>;

  /** Set favorite status for a sequence */
  setFavorite(sequenceId: string, isFavorite: boolean): Promise<void>;

  /** Remove all favorites */
  clearFavorites(): Promise<void>;

  /** Get favorites count */
  getFavoritesCount(): Promise<number>;
}
