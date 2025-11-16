/**
 * Gallery Cache Clear Utility
 *
 * Clears all gallery caching layers to force fresh metadata extraction
 * with the new difficulty calculator.
 *
 * USE THIS to fix cached difficulty levels after implementing the calculator!
 */

import { resolve } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { IExploreCacheService } from "../../modules/explore/display/services/contracts/IExploreCacheService";
import type { IOptimizedExploreService } from "../../modules/explore/shared/services/contracts/IOptimizedExploreService";

export async function clearAllGalleryCaches(): Promise<void> {
  console.log("🧹 Clearing ALL gallery caches...");

  try {
    // 1. Clear ExploreCacheService
    const exploreCacheService = resolve<IExploreCacheService>(
      TYPES.IExploreCacheService
    );
    exploreCacheService.clearCache();
    console.log("✅ Cleared ExploreCacheService");

    // 2. Clear OptimizedExploreService
    const optimizedService = resolve<IOptimizedExploreService>(
      TYPES.IOptimizedExploreService
    );
    optimizedService.clearCache();
    console.log("✅ Cleared OptimizedExploreService");

    // 3. Clear IndexedDB/Dexie cache if it exists
    if ("indexedDB" in window) {
      try {
        const dbName = "tka-persistence";
        await new Promise<void>((resolve, reject) => {
          const request = indexedDB.deleteDatabase(dbName);
          request.onsuccess = () => {
            console.log("✅ Cleared IndexedDB");
            resolve();
          };
          request.onerror = () => reject(request.error);
        });
      } catch (err) {
        console.log("⚠️ No IndexedDB to clear");
      }
    }

    // 4. Clear localStorage gallery data
    const galleryKeys = Object.keys(localStorage).filter(
      (key) =>
        key.includes("gallery") ||
        key.includes("explore") ||
        key.includes("sequence")
    );
    galleryKeys.forEach((key) => localStorage.removeItem(key));
    if (galleryKeys.length > 0) {
      console.log(`✅ Cleared ${galleryKeys.length} localStorage entries`);
    }

    console.log(
      "🎉 All gallery caches cleared! Refresh the page to load fresh data."
    );

    // Return success message
    return Promise.resolve();
  } catch (error) {
    console.error("❌ Error clearing caches:", error);
    throw error;
  }
}

/**
 * Call this from browser console to clear caches:
 *
 * ```javascript
 * import { clearAllGalleryCaches } from './src/lib/shared/utils/clear-gallery-cache';
 * await clearAllGalleryCaches();
 * location.reload();
 * ```
 */

// Make it available globally for easy console access
if (typeof window !== "undefined") {
  (window as any).__clearGalleryCache = clearAllGalleryCaches;
}
