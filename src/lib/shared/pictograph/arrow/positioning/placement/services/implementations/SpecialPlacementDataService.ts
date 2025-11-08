/**
 * Special Placement Data Service
 *
 * Handles loading and caching of special placement JSON data.
 * Uses Promise-based caching to prevent race conditions during concurrent loads.
 */

import { injectable } from "inversify";
import { jsonCache } from "$shared";
import type { ISpecialPlacementDataService } from "../contracts/ISpecialPlacementDataService";

@injectable()
export class SpecialPlacementDataService
  implements ISpecialPlacementDataService
{
  // Structure: [gridMode][oriKey][letter] -> Record<string, unknown>
  private cache: Record<
    string,
    Record<string, Record<string, Record<string, unknown>>>
  > = {
    diamond: {},
    box: {},
  };

  // Track in-flight loading operations to prevent race conditions
  private loadingPromises = new Map<string, Promise<void>>();

  // Manifest of which files actually exist (loaded lazily)
  private manifest: Record<string, string[]> | null = null;
  private manifestLoadPromise: Promise<void> | null = null;

  /**
   * Load the manifest file that tells us which placement files exist
   */
  private async loadManifest(gridMode: string): Promise<void> {
    if (this.manifest !== null) return;

    if (this.manifestLoadPromise) {
      await this.manifestLoadPromise;
      return;
    }

    this.manifestLoadPromise = (async () => {
      try {
        const manifestPath = `/data/arrow_placement/${gridMode}/special/placement_manifest.json`;
        this.manifest = (await jsonCache.get(manifestPath)) as Record<
          string,
          string[]
        >;
      } catch (error) {
        // If manifest doesn't exist, assume empty (no special placements)
        this.manifest = {};
      }
    })();

    await this.manifestLoadPromise;
  }

  /**
   * Check if a placement file exists for the given letter
   */
  private async hasPlacementFile(
    gridMode: string,
    oriKey: string,
    letter: string
  ): Promise<boolean> {
    await this.loadManifest(gridMode);
    return this.manifest?.[oriKey]?.includes(letter) ?? false;
  }

  /**
   * Get special placement data for a specific letter.
   * Returns cached data if available, otherwise loads from JSON.
   */
  async getLetterData(
    gridMode: string,
    oriKey: string,
    letter: string
  ): Promise<Record<string, unknown>> {
    try {
      // Ensure cache structure exists
      this.ensureCacheStructure(gridMode, oriKey);

      // Return cached data if available
      if (this.cache[gridMode]![oriKey]![letter]) {
        return this.cache[gridMode]![oriKey]![letter]!;
      }

      // Check manifest to see if file exists before attempting to fetch
      const fileExists = await this.hasPlacementFile(gridMode, oriKey, letter);
      if (!fileExists) {
        // No placement file exists - cache and return empty object immediately
        this.cache[gridMode]![oriKey]![letter] = {};
        return {};
      }

      const cacheKey = `${gridMode}:${oriKey}:${letter}`;

      // Check if loading is already in progress
      if (this.loadingPromises.has(cacheKey)) {
        await this.loadingPromises.get(cacheKey);
        return this.cache[gridMode]![oriKey]![letter] || {};
      }

      // Start new loading operation
      const loadingPromise = this.loadData(gridMode, oriKey, letter);
      this.loadingPromises.set(cacheKey, loadingPromise);

      try {
        await loadingPromise;
        return this.cache[gridMode]![oriKey]![letter] || {};
      } finally {
        // Clean up the promise from cache when done
        this.loadingPromises.delete(cacheKey);
      }
    } catch (error) {
      // Missing special placement files are expected - return empty object (interpreted as zero adjustment)
      return {};
    }
  }

  /**
   * Ensure cache structure exists for gridMode and oriKey
   */
  private ensureCacheStructure(gridMode: string, oriKey: string): void {
    if (!this.cache[gridMode]) {
      this.cache[gridMode] = {} as Record<
        string,
        Record<string, Record<string, unknown>>
      >;
    }
    if (!this.cache[gridMode]![oriKey]) {
      this.cache[gridMode]![oriKey] = {} as Record<
        string,
        Record<string, unknown>
      >;
    }
  }

  /**
   * Load data from JSON file and store in cache
   */
  private async loadData(
    gridMode: string,
    oriKey: string,
    letter: string
  ): Promise<void> {
    // Files are served under /data/... in the web app
    // Example path: /data/arrow_placement/diamond/special/from_layer1/A_placements.json
    const encodedLetter = encodeURIComponent(letter);
    const basePath = `/data/arrow_placement/${gridMode}/special/${oriKey}/${encodedLetter}_placements.json`;

    try {
      const data = (await jsonCache.get(basePath)) as Record<string, unknown>;
      this.cache[gridMode]![oriKey]![letter] = data;
    } catch (error) {
      // If file doesn't exist, store empty object
      this.cache[gridMode]![oriKey]![letter] = {};
    }
  }
}
