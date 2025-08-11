/**
 * Thumbnail Service Implementation
 *
 * Handles loading and serving thumbnail images for sequence browsing.
 * Manages caching and provides URLs for thumbnail access.
 */

import type { IThumbnailService } from '$lib/services/interfaces';

export class ThumbnailService implements IThumbnailService {
	private thumbnailCache = new Map<string, Promise<void>>();
	private metadataCache = new Map<string, { width: number; height: number }>();
	private baseUrl = '/dictionary';

	getThumbnailUrl(_sequenceId: string, thumbnailPath: string): string {
		// Handle different thumbnail path formats

		// If path starts with /dictionary/, it's already a complete path - return as-is
		if (thumbnailPath.startsWith('/dictionary/')) {
			return thumbnailPath;
		}

		// If path starts with /, it's already absolute - return as-is
		if (thumbnailPath.startsWith('/')) {
			return thumbnailPath;
		}

		// If thumbnailPath is just a filename, construct the full URL using legacy browse_thumbnails
		if (!thumbnailPath.includes('/')) {
			return `${this.baseUrl}/${thumbnailPath}`;
		}

		// If thumbnailPath is relative, prepend base URL (legacy support)
		return `${this.baseUrl}/${thumbnailPath}`;
	}

	async preloadThumbnail(sequenceId: string, thumbnailPath: string): Promise<void> {
		const cacheKey = `${sequenceId}-${thumbnailPath}`;

		// Return existing promise if already loading
		if (this.thumbnailCache.has(cacheKey)) {
			return this.thumbnailCache.get(cacheKey);
		}

		// Create new preload promise
		const preloadPromise = this.loadThumbnailImage(sequenceId, thumbnailPath);
		this.thumbnailCache.set(cacheKey, preloadPromise);

		try {
			await preloadPromise;
		} catch (error) {
			// Remove failed attempts from cache
			this.thumbnailCache.delete(cacheKey);
			throw error;
		}
	}

	async getThumbnailMetadata(
		sequenceId: string
	): Promise<{ width: number; height: number } | null> {
		const cacheKey = sequenceId;

		if (this.metadataCache.has(cacheKey)) {
			return this.metadataCache.get(cacheKey) || null;
		}

		try {
			// Try to get thumbnail path for this sequence
			const thumbnailPath = await this.getThumbnailPathForSequence(sequenceId);
			if (!thumbnailPath) {
				return null;
			}

			const metadata = await this.loadImageMetadata(thumbnailPath);
			this.metadataCache.set(cacheKey, metadata);
			return metadata;
		} catch (error) {
			console.warn(`Failed to get thumbnail metadata for ${sequenceId}:`, error);
			return null;
		}
	}

	clearThumbnailCache(): void {
		this.thumbnailCache.clear();
		this.metadataCache.clear();
	}

	// Additional helper methods for thumbnail management
	async validateThumbnailExists(sequenceId: string, thumbnailPath: string): Promise<boolean> {
		try {
			const url = this.getThumbnailUrl(sequenceId, thumbnailPath);
			const response = await fetch(url, { method: 'HEAD' });
			return response.ok;
		} catch {
			return false;
		}
	}

	async getThumbnailsForSequence(sequenceId: string): Promise<string[]> {
		// This would ideally scan the thumbnail directory for files matching the sequence
		// For now, return common thumbnail patterns
		const commonPatterns = [
			`${sequenceId}_ver1.png`,
			`${sequenceId.toUpperCase()}_ver1.png`,
			`${sequenceId.toLowerCase()}_ver1.png`,
		];

		const validThumbnails: string[] = [];

		for (const pattern of commonPatterns) {
			if (await this.validateThumbnailExists(sequenceId, pattern)) {
				validThumbnails.push(pattern);
			}
		}

		return validThumbnails;
	}

	getOptimizedThumbnailUrl(
		sequenceId: string,
		thumbnailPath: string,
		targetWidth?: number
	): string {
		// For now, return the original URL
		// In the future, could implement server-side resizing or WebP conversion
		const baseUrl = this.getThumbnailUrl(sequenceId, thumbnailPath);

		if (targetWidth) {
			// Could append query parameters for resizing if server supports it
			// return `${baseUrl}?w=${targetWidth}`;
		}

		return baseUrl;
	}

	// Private helper methods
	private async loadThumbnailImage(sequenceId: string, thumbnailPath: string): Promise<void> {
		return new Promise((resolve, reject) => {
			const img = new Image();
			const url = this.getThumbnailUrl(sequenceId, thumbnailPath);

			img.onload = () => {
				// Store metadata if successful
				this.metadataCache.set(sequenceId, {
					width: img.naturalWidth,
					height: img.naturalHeight,
				});
				resolve();
			};

			img.onerror = () => {
				reject(new Error(`Failed to load thumbnail: ${url}`));
			};

			img.src = url;
		});
	}

	private async loadImageMetadata(
		thumbnailPath: string
	): Promise<{ width: number; height: number }> {
		return new Promise((resolve, reject) => {
			const img = new Image();

			img.onload = () => {
				resolve({
					width: img.naturalWidth,
					height: img.naturalHeight,
				});
			};

			img.onerror = () => {
				reject(new Error(`Failed to load image metadata: ${thumbnailPath}`));
			};

			img.src = thumbnailPath;
		});
	}

	private async getThumbnailPathForSequence(sequenceId: string): Promise<string | null> {
		// Try common thumbnail naming patterns
		const patterns = [
			`${sequenceId}_ver1.png`,
			`${sequenceId.toUpperCase()}_ver1.png`,
			`${sequenceId.toLowerCase()}_ver1.png`,
		];

		for (const pattern of patterns) {
			if (await this.validateThumbnailExists(sequenceId, pattern)) {
				return pattern;
			}
		}

		return null;
	}

	// Batch operations for performance
	async preloadThumbnails(
		thumbnails: Array<{ sequenceId: string; thumbnailPath: string }>
	): Promise<void> {
		const preloadPromises = thumbnails.map((thumb) =>
			this.preloadThumbnail(thumb.sequenceId, thumb.thumbnailPath).catch((error) => {
				console.warn(
					`Failed to preload thumbnail ${thumb.sequenceId}/${thumb.thumbnailPath}:`,
					error
				);
			})
		);

		await Promise.all(preloadPromises);
	}

	getThumbnailCacheStats(): {
		cached: number;
		metadataCached: number;
	} {
		return {
			cached: this.thumbnailCache.size,
			metadataCached: this.metadataCache.size,
		};
	}
}
