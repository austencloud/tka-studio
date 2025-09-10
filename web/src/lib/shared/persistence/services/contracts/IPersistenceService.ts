/**
 * Persistence Service Interface
 * 
 * This defines the contract for all persistence operations in your app.
 * Think of this as your "database API" - it abstracts away the complexity
 * of Dexie and provides simple methods for your components to use.
 */

import type {
  AppSettings,
  CompleteGalleryState,
  PictographData,
  SequenceData,
  TabId
} from '$shared';
import type { UserProject, UserWorkData } from '../../domain/models';

// ============================================================================
// MAIN PERSISTENCE SERVICE
// ============================================================================

export interface IPersistenceService {
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  /**
   * Initialize the persistence layer
   */
  initialize(): Promise<void>;

  /**
   * Check if persistence is available
   */
  isAvailable(): boolean;

  // ============================================================================
  // SEQUENCE OPERATIONS
  // ============================================================================
  
  /**
   * Save a sequence to the database
   */
  saveSequence(sequence: SequenceData): Promise<void>;

  /**
   * Load a sequence by ID
   */
  loadSequence(id: string): Promise<SequenceData | null>;

  /**
   * Get all sequences (with optional filtering)
   */
  getAllSequences(filter?: {
    author?: string;
    level?: number;
    isFavorite?: boolean;
    tags?: string[];
  }): Promise<SequenceData[]>;

  /**
   * Delete a sequence
   */
  deleteSequence(id: string): Promise<void>;

  /**
   * Search sequences by name or word
   */
  searchSequences(query: string): Promise<SequenceData[]>;

  // ============================================================================
  // PICTOGRAPH OPERATIONS
  // ============================================================================
  
  /**
   * Save a pictograph
   */
  savePictograph(pictograph: PictographData): Promise<void>;

  /**
   * Load a pictograph by ID
   */
  loadPictograph(id: string): Promise<PictographData | null>;

  /**
   * Get pictographs by letter
   */
  getPictographsByLetter(letter: string): Promise<PictographData[]>;

  /**
   * Get all pictographs
   */
  getAllPictographs(): Promise<PictographData[]>;

  // ============================================================================
  // TAB STATE PERSISTENCE
  // ============================================================================
  
  /**
   * Save the current active tab
   */
  saveActiveTab(tabId: TabId): Promise<void>;

  /**
   * Get the last active tab
   */
  getActiveTab(): Promise<TabId | null>;

  /**
   * Save state for a specific tab
   */
  saveTabState(tabId: TabId, state: unknown): Promise<void>;

  /**
   * Load state for a specific tab
   */
  loadTabState<T = unknown>(tabId: TabId): Promise<T | null>;

  // ============================================================================
  // GALLERY STATE PERSISTENCE
  // ============================================================================
  
  /**
   * Save complete gallery state (filters, sorts, scroll position, etc.)
   */
  saveGalleryState(state: CompleteGalleryState): Promise<void>;

  /**
   * Load gallery state
   */
  loadGalleryState(): Promise<CompleteGalleryState | null>;

  // ============================================================================
  // SETTINGS PERSISTENCE
  // ============================================================================
  
  /**
   * Save app settings
   */
  saveSettings(settings: AppSettings): Promise<void>;

  /**
   * Load app settings
   */
  loadSettings(): Promise<AppSettings | null>;

  // ============================================================================
  // USER PROJECTS
  // ============================================================================
  
  /**
   * Save a user project
   */
  saveProject(project: UserProject): Promise<void>;

  /**
   * Load all user projects
   */
  loadProjects(): Promise<UserProject[]>;

  /**
   * Delete a project
   */
  deleteProject(id: number): Promise<void>;

  // ============================================================================
  // UTILITY OPERATIONS
  // ============================================================================
  
  /**
   * Export all data for backup
   */
  exportAllData(): Promise<unknown>;

  /**
   * Import data from backup
   */
  importData(data: unknown): Promise<void>;

  /**
   * Clear all data (for development/reset)
   */
  clearAllData(): Promise<void>;

  /**
   * Get storage statistics
   */
  getStorageInfo(): Promise<{
    sequences: number;
    pictographs: number;
    userWork: number;
    projects: number;
    totalSize?: number;
  }>;
}
