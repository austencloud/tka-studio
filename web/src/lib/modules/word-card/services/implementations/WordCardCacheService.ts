/**
 * Word Card Cache Service
 *
 * Handles caching of word card images and data.
 * Single responsibility: Cache storage and retrieval.
 */

import type { SequenceData, WordCardExportOptions } from "$shared";
import { injectable } from "inversify";
import type { IWordCardCacheService } from "../contracts";

interface CacheEntry {
  data: Blob | SequenceData;
  timestamp: Date;
  size: number;
  accessCount: number;
  lastAccessed: Date;
  options?: WordCardExportOptions;
}

interface CacheStats {
  entryCount: number;
  totalSize: number;
  hitRate: number;
  lastCleanup: Date;
}

@injectable()
export class WordCardCacheService implements IWordCardCacheService {
  private imageCache = new Map<string, CacheEntry>();
  private dataCache = new Map<string, CacheEntry>();
  private hitCount = 0;
  private missCount = 0;
  private lastCleanup = new Date();

  // Cache configuration
  private readonly maxCacheSize = 100 * 1024 * 1024; // 100MB
  private readonly maxEntries = 1000;
  private readonly maxAge = 24 * 60 * 60 * 1000; // 24 hours

  /**
   * Store image in cache
   */
  async storeImage(
    sequenceId: string,
    imageBlob: Blob,
    options?: WordCardExportOptions
  ): Promise<void> {
    try {
      const cacheKey = this.generateImageCacheKey(sequenceId, options);
      const entry: CacheEntry = {
        data: imageBlob,
        timestamp: new Date(),
        size: imageBlob.size,
        accessCount: 0,
        lastAccessed: new Date(),
        options,
      };

      // Check if we need to cleanup before adding
      await this.ensureCacheSpace(entry.size);

      this.imageCache.set(cacheKey, entry);
      console.log(
        `📦 Cached image for sequence ${sequenceId} (${imageBlob.size} bytes)`
      );
    } catch (error) {
      console.error("Failed to store image in cache:", error);
      // Don't throw - caching failures should not break the main flow
    }
  }

  /**
   * Retrieve image from cache
   */
  async retrieveImage(
    sequenceId: string,
    options?: WordCardExportOptions
  ): Promise<Blob | null> {
    try {
      const cacheKey = this.generateImageCacheKey(sequenceId, options);
      const entry = this.imageCache.get(cacheKey);

      if (!entry) {
        this.missCount++;
        return null;
      }

      // Check if entry is expired
      if (this.isExpired(entry)) {
        this.imageCache.delete(cacheKey);
        this.missCount++;
        return null;
      }

      // Update access stats
      entry.accessCount++;
      entry.lastAccessed = new Date();
      this.hitCount++;

      console.log(`🎯 Cache hit for sequence ${sequenceId}`);
      return entry.data as Blob;
    } catch (error) {
      console.error("Failed to retrieve image from cache:", error);
      this.missCount++;
      return null;
    }
  }

  /**
   * Store sequence data in cache
   */
  async storeSequenceData(
    sequenceId: string,
    data: SequenceData
  ): Promise<void> {
    try {
      const dataSize = this.estimateSequenceDataSize(data);
      const entry: CacheEntry = {
        data,
        timestamp: new Date(),
        size: dataSize,
        accessCount: 0,
        lastAccessed: new Date(),
      };

      // Check if we need to cleanup before adding
      await this.ensureCacheSpace(entry.size);

      this.dataCache.set(sequenceId, entry);
      console.log(
        `📦 Cached sequence data for ${sequenceId} (${dataSize} bytes)`
      );
    } catch (error) {
      console.error("Failed to store sequence data in cache:", error);
    }
  }

  /**
   * Retrieve sequence data from cache
   */
  async retrieveSequenceData(sequenceId: string): Promise<SequenceData | null> {
    try {
      const entry = this.dataCache.get(sequenceId);

      if (!entry) {
        this.missCount++;
        return null;
      }

      // Check if entry is expired
      if (this.isExpired(entry)) {
        this.dataCache.delete(sequenceId);
        this.missCount++;
        return null;
      }

      // Update access stats
      entry.accessCount++;
      entry.lastAccessed = new Date();
      this.hitCount++;

      return entry.data as SequenceData;
    } catch (error) {
      console.error("Failed to retrieve sequence data from cache:", error);
      this.missCount++;
      return null;
    }
  }

  /**
   * Clear all cached data
   */
  async clearCache(): Promise<void> {
    try {
      this.imageCache.clear();
      this.dataCache.clear();
      this.hitCount = 0;
      this.missCount = 0;
      this.lastCleanup = new Date();
      console.log("🧹 Cache cleared");
    } catch (error) {
      console.error("Failed to clear cache:", error);
    }
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): CacheStats {
    const totalRequests = this.hitCount + this.missCount;
    const hitRate = totalRequests > 0 ? this.hitCount / totalRequests : 0;

    const totalSize = this.calculateTotalCacheSize();
    const entryCount = this.imageCache.size + this.dataCache.size;

    return {
      entryCount,
      totalSize,
      hitRate,
      lastCleanup: this.lastCleanup,
    };
  }

  /**
   * Cleanup expired cache entries
   */
  async cleanup(): Promise<void> {
    try {
      const now = new Date();
      let removedCount = 0;
      let freedSpace = 0;

      // Clean up image cache
      for (const [key, entry] of this.imageCache.entries()) {
        if (this.isExpired(entry)) {
          freedSpace += entry.size;
          this.imageCache.delete(key);
          removedCount++;
        }
      }

      // Clean up data cache
      for (const [key, entry] of this.dataCache.entries()) {
        if (this.isExpired(entry)) {
          freedSpace += entry.size;
          this.dataCache.delete(key);
          removedCount++;
        }
      }

      this.lastCleanup = now;
      console.log(
        `🧹 Cache cleanup: removed ${removedCount} entries, freed ${this.formatBytes(freedSpace)}`
      );
    } catch (error) {
      console.error("Cache cleanup failed:", error);
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private generateImageCacheKey(
    sequenceId: string,
    options?: WordCardExportOptions
  ): string {
    if (!options) {
      return sequenceId;
    }

    // Create a consistent cache key based on sequence ID and export options
    const optionsParts = [
      options.quality || "default",
      options.format || "PNG",
      options.scale || "1.0",
    ];

    return `${sequenceId}_${optionsParts.join("_")}`;
  }

  private isExpired(entry: CacheEntry): boolean {
    const age = Date.now() - entry.timestamp.getTime();
    return age > this.maxAge;
  }

  private estimateSequenceDataSize(data: SequenceData): number {
    // Rough estimation of sequence data size in bytes
    const jsonString = JSON.stringify(data);
    return new Blob([jsonString]).size;
  }

  private calculateTotalCacheSize(): number {
    let totalSize = 0;

    for (const entry of this.imageCache.values()) {
      totalSize += entry.size;
    }

    for (const entry of this.dataCache.values()) {
      totalSize += entry.size;
    }

    return totalSize;
  }

  private async ensureCacheSpace(requiredSpace: number): Promise<void> {
    const currentSize = this.calculateTotalCacheSize();
    const totalEntries = this.imageCache.size + this.dataCache.size;

    // Check if we need to free space
    if (
      currentSize + requiredSpace > this.maxCacheSize ||
      totalEntries >= this.maxEntries
    ) {
      await this.freeUpSpace(requiredSpace);
    }
  }

  private async freeUpSpace(requiredSpace: number): Promise<void> {
    // First, try cleaning up expired entries
    await this.cleanup();

    const currentSize = this.calculateTotalCacheSize();

    // If still need space, remove least recently used entries
    if (currentSize + requiredSpace > this.maxCacheSize) {
      await this.evictLeastRecentlyUsed(requiredSpace);
    }
  }

  private async evictLeastRecentlyUsed(requiredSpace: number): Promise<void> {
    const allEntries: Array<{
      key: string;
      entry: CacheEntry;
      type: "image" | "data";
    }> = [];

    // Collect all entries with their keys and types
    for (const [key, entry] of this.imageCache.entries()) {
      allEntries.push({ key, entry, type: "image" });
    }
    for (const [key, entry] of this.dataCache.entries()) {
      allEntries.push({ key, entry, type: "data" });
    }

    // Sort by last accessed time (oldest first)
    allEntries.sort(
      (a, b) => a.entry.lastAccessed.getTime() - b.entry.lastAccessed.getTime()
    );

    let freedSpace = 0;
    let removedCount = 0;

    for (const { key, entry, type } of allEntries) {
      if (freedSpace >= requiredSpace) {
        break;
      }

      if (type === "image") {
        this.imageCache.delete(key);
      } else {
        this.dataCache.delete(key);
      }

      freedSpace += entry.size;
      removedCount++;
    }

    console.log(
      `🗑️ Evicted ${removedCount} cache entries, freed ${this.formatBytes(freedSpace)}`
    );
  }

  /**
   * Cache word card data
   */
  async cacheWordCard(sequenceId: string, data: SequenceData): Promise<void> {
    try {
      const cacheKey = `data_${sequenceId}`;
      const serializedData = JSON.stringify(data);
      const size = new Blob([serializedData]).size;

      const entry: CacheEntry = {
        data,
        timestamp: new Date(),
        size,
        accessCount: 0,
        lastAccessed: new Date(),
      };

      this.dataCache.set(cacheKey, entry);
      console.log(`💾 Cached word card data for sequence: ${sequenceId}`);

      // Cleanup if needed
      await this.cleanup();
    } catch (error) {
      console.error(
        `❌ Failed to cache word card data for ${sequenceId}:`,
        error
      );
    }
  }

  /**
   * Get cached word card data
   */
  async getCachedWordCard(sequenceId: string): Promise<SequenceData | null> {
    try {
      const cacheKey = `data_${sequenceId}`;
      const entry = this.dataCache.get(cacheKey);

      if (!entry) {
        this.missCount++;
        return null;
      }

      // Check if entry is expired
      const age = Date.now() - entry.timestamp.getTime();
      if (age > this.maxAge) {
        this.dataCache.delete(cacheKey);
        this.missCount++;
        return null;
      }

      // Update access statistics
      entry.accessCount++;
      entry.lastAccessed = new Date();
      this.hitCount++;

      console.log(`🎯 Cache hit for word card data: ${sequenceId}`);
      return entry.data as SequenceData;
    } catch (error) {
      console.error(
        `❌ Failed to retrieve cached word card data for ${sequenceId}:`,
        error
      );
      this.missCount++;
      return null;
    }
  }

  private formatBytes(bytes: number): string {
    const sizes = ["Bytes", "KB", "MB", "GB"];
    if (bytes === 0) return "0 Bytes";
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + " " + sizes[i];
  }
}
