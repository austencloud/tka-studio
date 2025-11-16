/**
 * Optimized Explore Service Implementation
 *
 * Mobile-first gallery loading with:
 * - Progressive pagination (20 items per page on mobile)
 * - WebP image optimization with PNG fallback
 * - Intelligent preloading
 * - Virtual scrolling support
 */

import { inject, injectable } from "inversify";
import { TYPES } from "$shared";
import type { IDeviceDetector } from "$shared/device/services/contracts/IDeviceDetector";
import type {
  IOptimizedExploreService,
  PaginatedSequences,
  SequenceMetadata,
} from "../contracts/IOptimizedExploreService";

@injectable()
export class OptimizedExploreService implements IOptimizedExploreService {
  private cache = new Map<number, SequenceMetadata[]>();
  private totalCount: number = 0;
  private readonly MOBILE_PAGE_SIZE = 20;
  private readonly DESKTOP_PAGE_SIZE = 40;

  constructor(
    @inject(TYPES.IDeviceDetector) private deviceDetector: IDeviceDetector
  ) {}

  private get pageSize(): number {
    // Use DeviceDetector for consistent device detection
    return this.deviceDetector.isMobile()
      ? this.MOBILE_PAGE_SIZE
      : this.DESKTOP_PAGE_SIZE;
  }

  async loadInitialSequences(): Promise<PaginatedSequences> {
    console.log("🚀 OptimizedGallery: Loading initial sequences...");

    try {
      // Load first page with priority images
      const response = await fetch(
        `/api/sequences/paginated?page=1&limit=${this.pageSize}&priority=true`
      );

      if (!response.ok) {
        throw new Error(`Failed to load sequences: ${response.status}`);
      }

      const data = await response.json();

      // Cache the results
      this.cache.set(1, data.sequences);
      this.totalCount = data.totalCount;

      console.log(
        `✅ OptimizedGallery: Loaded ${data.sequences.length} initial sequences`
      );

      return {
        sequences: data.sequences,
        totalCount: data.totalCount,
        hasMore: data.hasMore,
        nextPage: 2,
      };
    } catch (error) {
      console.error(
        "❌ OptimizedGallery: Failed to load initial sequences:",
        error
      );
      throw error;
    }
  }

  async loadMoreSequences(page: number): Promise<PaginatedSequences> {
    console.log(`🔄 OptimizedGallery: Loading page ${page}...`);

    // Check cache first
    if (this.cache.has(page)) {
      const sequences = this.cache.get(page)!;
      return {
        sequences,
        totalCount: this.totalCount || 0,
        hasMore: page * this.pageSize < (this.totalCount || 0),
        nextPage: page + 1,
      };
    }

    try {
      const response = await fetch(
        `/api/sequences/paginated?page=${page}&limit=${this.pageSize}`
      );

      if (!response.ok) {
        throw new Error(`Failed to load page ${page}: ${response.status}`);
      }

      const data = await response.json();

      // Cache the results
      this.cache.set(page, data.sequences);

      console.log(
        `✅ OptimizedGallery: Loaded page ${page} with ${data.sequences.length} sequences`
      );

      return {
        sequences: data.sequences,
        totalCount: data.totalCount,
        hasMore: data.hasMore,
        nextPage: page + 1,
      };
    } catch (error) {
      console.error(`❌ OptimizedGallery: Failed to load page ${page}:`, error);
      throw error;
    }
  }

  getOptimizedThumbnailUrl(
    sequenceId: string,
    preferWebP: boolean = true
  ): string {
    // Try WebP first for modern browsers, fallback to PNG
    if (preferWebP && this.supportsWebP()) {
      return `/gallery/${sequenceId}/thumbnail.webp`;
    }
    return `/gallery/${sequenceId}/thumbnail.png`;
  }

  async preloadNextBatch(sequences: SequenceMetadata[]): Promise<void> {
    // Preload next 5-10 images for smooth scrolling
    const preloadCount = Math.min(sequences.length, 10);
    const preloadPromises: Promise<void>[] = [];

    for (let i = 0; i < preloadCount; i++) {
      const sequence = sequences[i];
      if (sequence) {
        preloadPromises.push(this.preloadImage(sequence.thumbnailUrl));
      }
    }

    try {
      await Promise.allSettled(preloadPromises);
      console.log(`✅ OptimizedGallery: Preloaded ${preloadCount} images`);
    } catch (error) {
      console.warn(
        "⚠️ OptimizedGallery: Some images failed to preload:",
        error
      );
    }
  }

  async getTotalSequenceCount(): Promise<number> {
    if (this.totalCount > 0) {
      return this.totalCount;
    }

    try {
      const response = await fetch("/api/sequences/count");
      const data = await response.json();
      this.totalCount = data.count ?? 0;
      return this.totalCount;
    } catch (error) {
      console.error("❌ OptimizedGallery: Failed to get total count:", error);
      return 0;
    }
  }

  async searchSequences(
    query: string,
    page: number = 1
  ): Promise<PaginatedSequences> {
    try {
      const response = await fetch(
        `/api/sequences/search?q=${encodeURIComponent(query)}&page=${page}&limit=${this.pageSize}`
      );

      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }

      const data = await response.json();

      return {
        sequences: data.sequences,
        totalCount: data.totalCount,
        hasMore: data.hasMore,
        nextPage: page + 1,
      };
    } catch (error) {
      console.error("❌ OptimizedGallery: Search failed:", error);
      throw error;
    }
  }

  clearCache(): void {
    this.cache.clear();
    this.totalCount = 0;
    console.log("🧹 OptimizedGallery: Cache cleared");
  }

  private supportsWebP(): boolean {
    // Check if browser supports WebP
    const canvas = document.createElement("canvas");
    canvas.width = 1;
    canvas.height = 1;
    return canvas.toDataURL("image/webp").indexOf("data:image/webp") === 0;
  }

  private async preloadImage(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve();
      img.onerror = () => reject(new Error(`Failed to preload ${url}`));
      img.src = url;
    });
  }
}
