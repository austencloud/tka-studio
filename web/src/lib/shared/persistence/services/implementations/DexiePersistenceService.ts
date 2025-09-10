/**
 * Dexie Persistence Service Implementation
 * 
 * This is where the magic happens! This service implements all the database
 * operations using Dexie. Your components will call these methods, and this
 * service handles all the IndexedDB complexity behind the scenes.
 */

import type {
  AppSettings,
  CompleteGalleryState,
  PictographData,
  SequenceData,
  TabId
} from '$shared';
import { injectable } from 'inversify';
import { db } from '../../database/TKADatabase';
import type { UserProject, UserWorkData } from '../../domain/models';
import type { IPersistenceService } from '../contracts/IPersistenceService';

@injectable()
export class DexiePersistenceService implements IPersistenceService {
  
  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  
  async initialize(): Promise<void> {
    try {
      await db.open();
      console.log('✅ DexiePersistenceService: Database initialized');
    } catch (error) {
      console.error('❌ DexiePersistenceService: Failed to initialize:', error);
      throw error;
    }
  }

  isAvailable(): boolean {
    return typeof window !== 'undefined' && 'indexedDB' in window;
  }

  // ============================================================================
  // SEQUENCE OPERATIONS
  // ============================================================================
  
  async saveSequence(sequence: SequenceData): Promise<void> {
    try {
      await db.sequences.put(sequence);
      console.log(`✅ Saved sequence: ${sequence.name} (${sequence.id})`);
    } catch (error) {
      console.error('❌ Failed to save sequence:', error);
      throw error;
    }
  }

  async loadSequence(id: string): Promise<SequenceData | null> {
    try {
      const sequence = await db.sequences.get(id);
      return sequence || null;
    } catch (error) {
      console.error('❌ Failed to load sequence:', error);
      return null;
    }
  }

  async getAllSequences(filter?: {
    author?: string;
    level?: number;
    isFavorite?: boolean;
    tags?: string[];
  }): Promise<SequenceData[]> {
    try {
      let query = db.sequences.toCollection();

      // Apply filters if provided
      if (filter) {
        if (filter.author) {
          query = query.filter(seq => seq.author === filter.author);
        }
        if (filter.level !== undefined) {
          query = query.filter(seq => seq.level === filter.level);
        }
        if (filter.isFavorite !== undefined) {
          query = query.filter(seq => seq.isFavorite === filter.isFavorite);
        }
        if (filter.tags && filter.tags.length > 0) {
          query = query.filter(seq => 
            filter.tags!.some(tag => seq.tags.includes(tag))
          );
        }
      }

      return await query.toArray();
    } catch (error) {
      console.error('❌ Failed to get sequences:', error);
      return [];
    }
  }

  async deleteSequence(id: string): Promise<void> {
    try {
      await db.sequences.delete(id);
      console.log(`🗑️ Deleted sequence: ${id}`);
    } catch (error) {
      console.error('❌ Failed to delete sequence:', error);
      throw error;
    }
  }

  async searchSequences(query: string): Promise<SequenceData[]> {
    try {
      const searchTerm = query.toLowerCase();
      return await db.sequences
        .filter(seq =>
          seq.name.toLowerCase().includes(searchTerm) ||
          seq.word.toLowerCase().includes(searchTerm) ||
          (seq.author?.toLowerCase().includes(searchTerm) ?? false)
        )
        .toArray();
    } catch (error) {
      console.error('❌ Failed to search sequences:', error);
      return [];
    }
  }

  // ============================================================================
  // PICTOGRAPH OPERATIONS
  // ============================================================================
  
  async savePictograph(pictograph: PictographData): Promise<void> {
    try {
      await db.pictographs.put(pictograph);
      console.log(`✅ Saved pictograph: ${pictograph.id}`);
    } catch (error) {
      console.error('❌ Failed to save pictograph:', error);
      throw error;
    }
  }

  async loadPictograph(id: string): Promise<PictographData | null> {
    try {
      const pictograph = await db.pictographs.get(id);
      return pictograph || null;
    } catch (error) {
      console.error('❌ Failed to load pictograph:', error);
      return null;
    }
  }

  async getPictographsByLetter(letter: string): Promise<PictographData[]> {
    try {
      return await db.pictographs
        .where('letter')
        .equals(letter)
        .toArray();
    } catch (error) {
      console.error('❌ Failed to get pictographs by letter:', error);
      return [];
    }
  }

  async getAllPictographs(): Promise<PictographData[]> {
    try {
      return await db.pictographs.toArray();
    } catch (error) {
      console.error('❌ Failed to get all pictographs:', error);
      return [];
    }
  }

  // ============================================================================
  // TAB STATE PERSISTENCE
  // ============================================================================
  
  async saveActiveTab(tabId: TabId): Promise<void> {
    try {
      await this.saveUserWork('active-tab', 'app', { activeTab: tabId });
      console.log(`✅ Saved active tab: ${tabId}`);
    } catch (error) {
      console.error('❌ Failed to save active tab:', error);
      throw error;
    }
  }

  async getActiveTab(): Promise<TabId | null> {
    try {
      const data = await this.loadUserWork('active-tab', 'app') as { activeTab?: TabId } | null;
      return data?.activeTab || null;
    } catch (error) {
      console.error('❌ Failed to get active tab:', error);
      return null;
    }
  }

  async saveTabState(tabId: TabId, state: unknown): Promise<void> {
    try {
      await this.saveUserWork('tab-state', tabId, state);
      console.log(`✅ Saved state for tab: ${tabId}`);
    } catch (error) {
      console.error('❌ Failed to save tab state:', error);
      throw error;
    }
  }

  async loadTabState<T = unknown>(tabId: TabId): Promise<T | null> {
    try {
      return await this.loadUserWork('tab-state', tabId) as T | null;
    } catch (error) {
      console.error('❌ Failed to load tab state:', error);
      return null;
    }
  }

  // ============================================================================
  // GALLERY STATE PERSISTENCE
  // ============================================================================
  
  async saveGalleryState(state: CompleteGalleryState): Promise<void> {
    try {
      await this.saveUserWork('gallery-state', 'browse', state);
      console.log('✅ Saved gallery state');
    } catch (error) {
      console.error('❌ Failed to save gallery state:', error);
      throw error;
    }
  }

  async loadGalleryState(): Promise<CompleteGalleryState | null> {
    try {
      return await this.loadUserWork('gallery-state', 'browse') as CompleteGalleryState | null;
    } catch (error) {
      console.error('❌ Failed to load gallery state:', error);
      return null;
    }
  }

  // ============================================================================
  // SETTINGS PERSISTENCE
  // ============================================================================
  
  async saveSettings(settings: AppSettings): Promise<void> {
    try {
      await db.settings.put({ ...settings, id: 'default' } as AppSettings & { id: string });
      console.log('✅ Saved app settings');
    } catch (error) {
      console.error('❌ Failed to save settings:', error);
      throw error;
    }
  }

  async loadSettings(): Promise<AppSettings | null> {
    try {
      const settings = await db.settings.where('id').equals('default').first();
      return settings || null;
    } catch (error) {
      console.error('❌ Failed to load settings:', error);
      return null;
    }
  }

  // ============================================================================
  // USER PROJECTS
  // ============================================================================
  
  async saveProject(project: UserProject): Promise<void> {
    try {
      await db.userProjects.put(project);
      console.log(`✅ Saved project: ${project.name}`);
    } catch (error) {
      console.error('❌ Failed to save project:', error);
      throw error;
    }
  }

  async loadProjects(): Promise<UserProject[]> {
    try {
      return await db.userProjects.orderBy('lastModified').reverse().toArray();
    } catch (error) {
      console.error('❌ Failed to load projects:', error);
      return [];
    }
  }

  async deleteProject(id: number): Promise<void> {
    try {
      await db.userProjects.delete(id);
      console.log(`🗑️ Deleted project: ${id}`);
    } catch (error) {
      console.error('❌ Failed to delete project:', error);
      throw error;
    }
  }

  // ============================================================================
  // UTILITY OPERATIONS
  // ============================================================================
  
  async exportAllData(): Promise<unknown> {
    try {
      const data = {
        sequences: await db.sequences.toArray(),
        pictographs: await db.pictographs.toArray(),
        userWork: await db.userWork.toArray(),
        userProjects: await db.userProjects.toArray(),
        settings: await db.settings.toArray(),
        exportedAt: new Date().toISOString(),
        version: 1
      };
      console.log('✅ Exported all data');
      return data;
    } catch (error) {
      console.error('❌ Failed to export data:', error);
      throw error;
    }
  }

  async importData(data: unknown): Promise<void> {
    // Implementation would go here - complex operation
    console.log('📥 Import data not yet implemented');
    throw new Error('Import not yet implemented');
  }

  async clearAllData(): Promise<void> {
    try {
      await db.transaction('rw', [db.sequences, db.pictographs, db.userWork, db.userProjects, db.settings], async () => {
        await db.sequences.clear();
        await db.pictographs.clear();
        await db.userWork.clear();
        await db.userProjects.clear();
        await db.settings.clear();
      });
      console.log('🗑️ Cleared all data');
    } catch (error) {
      console.error('❌ Failed to clear data:', error);
      throw error;
    }
  }

  async getStorageInfo() {
    try {
      return {
        sequences: await db.sequences.count(),
        pictographs: await db.pictographs.count(),
        userWork: await db.userWork.count(),
        projects: await db.userProjects.count(),
      };
    } catch (error) {
      console.error('❌ Failed to get storage info:', error);
      return { sequences: 0, pictographs: 0, userWork: 0, projects: 0 };
    }
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================
  
  /**
   * Generic method to save user work data
   */
  private async saveUserWork(type: string, tabId: string, data: unknown): Promise<void> {
    const workData: UserWorkData = {
      type: type as any,
      tabId,
      data,
      lastModified: new Date(),
      version: 1
    };

    // Update existing record or create new one
    const existing = await db.userWork
      .where({ type, tabId })
      .first();

    if (existing) {
      await db.userWork.update(existing.id!, { data, lastModified: new Date() });
    } else {
      await db.userWork.add(workData);
    }
  }

  /**
   * Generic method to load user work data
   */
  private async loadUserWork(type: string, tabId: string): Promise<unknown | null> {
    const workData = await db.userWork
      .where({ type, tabId })
      .first();

    return workData?.data || null;
  }
}
