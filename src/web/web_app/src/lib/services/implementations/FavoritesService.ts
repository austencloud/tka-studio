/**
 * Favorites Service - Manages sequence favorites
 * 
 * Handles favoriting/unfavoriting sequences with persistence
 * following the microservices architecture pattern.
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

export class FavoritesService implements IFavoritesService {
	private readonly STORAGE_KEY = 'tka-favorites';
	private favoritesCache: Set<string> | null = null;

	constructor() {
		// Initialize cache
		this.loadFavoritesFromStorage();
	}

	async toggleFavorite(sequenceId: string): Promise<void> {
		await this.ensureCacheLoaded();
		
		if (this.favoritesCache!.has(sequenceId)) {
			this.favoritesCache!.delete(sequenceId);
		} else {
			this.favoritesCache!.add(sequenceId);
		}
		
		await this.saveFavoritesToStorage();
	}

	async isFavorite(sequenceId: string): Promise<boolean> {
		await this.ensureCacheLoaded();
		return this.favoritesCache!.has(sequenceId);
	}

	async getFavorites(): Promise<string[]> {
		await this.ensureCacheLoaded();
		return Array.from(this.favoritesCache!);
	}

	async setFavorite(sequenceId: string, isFavorite: boolean): Promise<void> {
		await this.ensureCacheLoaded();
		
		if (isFavorite) {
			this.favoritesCache!.add(sequenceId);
		} else {
			this.favoritesCache!.delete(sequenceId);
		}
		
		await this.saveFavoritesToStorage();
	}

	async clearFavorites(): Promise<void> {
		this.favoritesCache = new Set();
		await this.saveFavoritesToStorage();
	}

	async getFavoritesCount(): Promise<number> {
		await this.ensureCacheLoaded();
		return this.favoritesCache!.size;
	}

	// Private methods
	private async ensureCacheLoaded(): Promise<void> {
		if (this.favoritesCache === null) {
			await this.loadFavoritesFromStorage();
		}
	}

	private async loadFavoritesFromStorage(): Promise<void> {
		try {
			// Note: Using sessionStorage instead of localStorage as localStorage is not supported in artifacts
			const stored = sessionStorage.getItem(this.STORAGE_KEY);
			const favorites = stored ? JSON.parse(stored) : [];
			this.favoritesCache = new Set(favorites);
		} catch (error) {
			console.warn('Failed to load favorites from storage:', error);
			this.favoritesCache = new Set();
		}
	}

	private async saveFavoritesToStorage(): Promise<void> {
		try {
			const favorites = Array.from(this.favoritesCache!);
			sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
		} catch (error) {
			console.error('Failed to save favorites to storage:', error);
		}
	}
}
