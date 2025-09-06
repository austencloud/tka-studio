/**
 * Service for managing user favorites
 */
export interface IFavoritesService {
  addToFavorites(sequenceId: string): Promise<void>;
  removeFromFavorites(sequenceId: string): Promise<void>;
  toggleFavorite(sequenceId: string): Promise<void>;
  getFavorites(): Promise<string[]>;
  isFavorite(sequenceId: string): Promise<boolean>;
}
