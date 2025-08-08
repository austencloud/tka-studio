/**
 * Arrow Placement Data Service
 * 
 * Loads and manages arrow placement JSON data for positioning calculations.
 * Ports the exact functionality from desktop DefaultPlacementService.
 */

import type { MotionType, GridMode } from '../interfaces';

// Placement data structure from JSON files
export interface PlacementData {
  [placementKey: string]: {
    [turns: string]: [number, number]; // [x, y] adjustment
  };
}

// Complete placement data for all motion types
export interface GridPlacementData {
  [motionType: string]: PlacementData;
}

// All placement data for all grid modes
export interface AllPlacementData {
  [gridMode: string]: GridPlacementData;
}

export interface IArrowPlacementDataService {
  getDefaultAdjustment(
    motionType: MotionType,
    placementKey: string,
    turns: number | string,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;
  
  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;
  
  isLoaded(): boolean;
  loadPlacementData(): Promise<void>;
}

export class ArrowPlacementDataService implements IArrowPlacementDataService {
  private allPlacements: AllPlacementData = {
    diamond: {},
    box: {}
  };
  
  private isDataLoaded = false;
  
  // File mapping for placement data
  private readonly placementFiles = {
    diamond: {
      pro: '/data/arrow_placement/diamond/default/default_diamond_pro_placements.json',
      anti: '/data/arrow_placement/diamond/default/default_diamond_anti_placements.json',
      float: '/data/arrow_placement/diamond/default/default_diamond_float_placements.json',
      dash: '/data/arrow_placement/diamond/default/default_diamond_dash_placements.json',
      static: '/data/arrow_placement/diamond/default/default_diamond_static_placements.json'
    },
    box: {
      pro: '/data/arrow_placement/box/default/default_box_pro_placements.json',
      anti: '/data/arrow_placement/box/default/default_box_anti_placements.json',
      float: '/data/arrow_placement/box/default/default_box_float_placements.json',
      dash: '/data/arrow_placement/box/default/default_box_dash_placements.json',
      static: '/data/arrow_placement/box/default/default_box_static_placements.json'
    }
  };

  /**
   * Load all placement data from JSON files
   */
  async loadPlacementData(): Promise<void> {
    if (this.isDataLoaded) {
      return;
    }

    console.log('Loading arrow placement data...');
    
    try {
      // Load diamond placements
      await this.loadGridPlacements('diamond');
      
      // Load box placements (may not exist yet)
      await this.loadGridPlacements('box');
      
      this.isDataLoaded = true;
      console.log('✅ Arrow placement data loaded successfully');
      
    } catch (error) {
      console.error('❌ Failed to load arrow placement data:', error);
      throw new Error(`Placement data loading failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Load placements for a specific grid mode
   */
  private async loadGridPlacements(gridMode: 'diamond' | 'box'): Promise<void> {
    const files = this.placementFiles[gridMode];
    this.allPlacements[gridMode] = {};

    for (const [motionType, filePath] of Object.entries(files)) {
      try {
        const placementData = await this.loadJsonFile(filePath);
        this.allPlacements[gridMode][motionType] = placementData;
        console.log(`Loaded ${motionType} placements for ${gridMode} grid`);
      } catch (error) {
        console.warn(`Could not load ${motionType} placements for ${gridMode}: ${error}`);
        this.allPlacements[gridMode][motionType] = {};
      }
    }
  }

  /**
   * Load JSON file with error handling
   */
  private async loadJsonFile(path: string): Promise<PlacementData> {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.warn(`Failed to load placement data from ${path}:`, error);
      return {};
    }
  }

  /**
   * Get default adjustment using placement key and turns
   */
  async getDefaultAdjustment(
    motionType: MotionType,
    placementKey: string,
    turns: number | string,
    gridMode: GridMode = 'diamond'
  ): Promise<{ x: number; y: number }> {
    await this.ensureDataLoaded();

    const gridPlacements = this.allPlacements[gridMode];
    if (!gridPlacements) {
      console.warn(`No placement data for grid mode: ${gridMode}`);
      return { x: 0, y: 0 };
    }

    const motionPlacements = gridPlacements[motionType];
    if (!motionPlacements) {
      console.warn(`No placement data for motion type: ${motionType}`);
      return { x: 0, y: 0 };
    }

    const placementData = motionPlacements[placementKey];
    if (!placementData) {
      console.warn(`No placement data for key: ${placementKey}`);
      return { x: 0, y: 0 };
    }

    // Convert turns to string format used in JSON
    const turnsStr = this.formatTurnsForLookup(turns);
    const adjustment = placementData[turnsStr];
    
    if (!adjustment) {
      console.warn(`No adjustment for turns: ${turnsStr} in placement: ${placementKey}`);
      return { x: 0, y: 0 };
    }

    const [x, y] = adjustment;
    console.log(`Found adjustment for ${motionType} ${placementKey} ${turnsStr}: [${x}, ${y}]`);
    
    return { x, y };
  }

  /**
   * Get available placement keys for a motion type
   */
  async getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode = 'diamond'
  ): Promise<string[]> {
    await this.ensureDataLoaded();

    const motionPlacements = this.allPlacements[gridMode]?.[motionType];
    if (!motionPlacements) {
      return [];
    }

    return Object.keys(motionPlacements);
  }

  /**
   * Check if data is loaded
   */
  isLoaded(): boolean {
    return this.isDataLoaded;
  }

  /**
   * Ensure data is loaded before operations
   */
  private async ensureDataLoaded(): Promise<void> {
    if (!this.isDataLoaded) {
      await this.loadPlacementData();
    }
  }

  /**
   * Format turns value for JSON lookup
   * Converts: 1.0 → "1", 0.5 → "0.5", etc.
   */
  private formatTurnsForLookup(turns: number | string): string {
    if (typeof turns === 'string') {
      return turns; // Already formatted (e.g., "fl" for float)
    }
    
    // Convert numbers: remove .0 for whole numbers
    if (turns === Math.floor(turns)) {
      return Math.floor(turns).toString();
    }
    
    return turns.toString();
  }

  /**
   * Debug method to log available keys
   */
  async debugAvailableKeys(motionType: MotionType, gridMode: GridMode = 'diamond'): Promise<void> {
    const keys = await this.getAvailablePlacementKeys(motionType, gridMode);
    console.log(`Available placement keys for ${motionType} (${gridMode}):`, keys);
  }

  /**
   * Get raw placement data for debugging
   */
  async getPlacementData(
    motionType: MotionType,
    placementKey: string,
    gridMode: GridMode = 'diamond'
  ): Promise<{ [turns: string]: [number, number] }> {
    await this.ensureDataLoaded();
    
    const motionPlacements = this.allPlacements[gridMode]?.[motionType];
    return motionPlacements?.[placementKey] || {};
  }
}
