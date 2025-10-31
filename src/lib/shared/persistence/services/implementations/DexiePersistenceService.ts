/**
 * Dexie Persistence Service Implementation
 *
 * This is where the magic happens! This service implements all the database
 * operations using Dexie. Your components will call these methods, and this
 * service handles all the IndexedDB complexity behind the scenes.
 */

import type {
    AppSettings,
    CompleteExploreState,
    PictographData,
    SequenceData,
    TabId,
} from "$shared";
import { injectable } from "inversify";
import { db } from "../../database/TKADatabase";
import { UserWorkType } from "../../domain/enums";
import type { UserProject, UserWorkData } from "../../domain/models";
import type { IPersistenceService } from "../contracts/IPersistenceService";

@injectable()
export class DexiePersistenceService implements IPersistenceService {
  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  async initialize(): Promise<void> {
    try {
      await db.open();
    } catch (error) {
      console.error("❌ DexiePersistenceService: Failed to initialize:", error);
      throw error;
    }
  }

  isAvailable(): boolean {
    return typeof window !== "undefined" && "indexedDB" in window;
  }

  // ============================================================================
  // SEQUENCE OPERATIONS
  // ============================================================================

  async saveSequence(sequence: SequenceData): Promise<void> {
    try {
      await db.sequences.put(sequence);
    } catch (error) {
      console.error("❌ Failed to save sequence:", error);
      throw error;
    }
  }

  async loadSequence(id: string): Promise<SequenceData | null> {
    try {
      const sequence = await db.sequences.get(id);
      return sequence || null;
    } catch (error) {
      console.error("❌ Failed to load sequence:", error);
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
          query = query.filter((seq) => seq.author === filter.author);
        }
        if (filter.level !== undefined) {
          query = query.filter((seq) => seq.level === filter.level);
        }
        if (filter.isFavorite !== undefined) {
          query = query.filter((seq) => seq.isFavorite === filter.isFavorite);
        }
        if (filter.tags && filter.tags.length > 0) {
          query = query.filter((seq) =>
            filter.tags!.some((tag) => seq.tags.includes(tag))
          );
        }
      }

      return await query.toArray();
    } catch (error) {
      console.error("❌ Failed to get sequences:", error);
      return [];
    }
  }

  async deleteSequence(id: string): Promise<void> {
    try {
      await db.sequences.delete(id);
    } catch (error) {
      console.error("❌ Failed to delete sequence:", error);
      throw error;
    }
  }

  async searchSequences(query: string): Promise<SequenceData[]> {
    try {
      const searchTerm = query.toLowerCase();
      return await db.sequences
        .filter(
          (seq) =>
            seq.name.toLowerCase().includes(searchTerm) ||
            seq.word.toLowerCase().includes(searchTerm) ||
            (seq.author?.toLowerCase().includes(searchTerm) ?? false)
        )
        .toArray();
    } catch (error) {
      console.error("❌ Failed to search sequences:", error);
      return [];
    }
  }

  // ============================================================================
  // PICTOGRAPH OPERATIONS
  // ============================================================================

  async savePictograph(pictograph: PictographData): Promise<void> {
    try {
      await db.pictographs.put(pictograph);
    } catch (error) {
      console.error("❌ Failed to save pictograph:", error);
      throw error;
    }
  }

  async loadPictograph(id: string): Promise<PictographData | null> {
    try {
      const pictograph = await db.pictographs.get(id);
      return pictograph || null;
    } catch (error) {
      console.error("❌ Failed to load pictograph:", error);
      return null;
    }
  }

  async getPictographsByLetter(letter: string): Promise<PictographData[]> {
    try {
      return await db.pictographs.where("letter").equals(letter).toArray();
    } catch (error) {
      console.error("❌ Failed to get pictographs by letter:", error);
      return [];
    }
  }

  async getAllPictographs(): Promise<PictographData[]> {
    try {
      return await db.pictographs.toArray();
    } catch (error) {
      console.error("❌ Failed to get all pictographs:", error);
      return [];
    }
  }

  // ============================================================================
  // TAB STATE PERSISTENCE
  // ============================================================================

  async saveActiveTab(tabId: TabId): Promise<void> {
    try {
      await this.saveUserWork(UserWorkType.TAB_STATE, "app", {
        activeTab: tabId,
      });
    } catch (error) {
      console.error("❌ Failed to save active tab:", error);
      throw error;
    }
  }

  async getActiveTab(): Promise<TabId | null> {
    try {
      const data = (await this.loadUserWork(UserWorkType.TAB_STATE, "app")) as {
        activeTab?: TabId;
      } | null;
      return data?.activeTab || null;
    } catch (error) {
      console.error("❌ Failed to get active tab:", error);
      return null;
    }
  }

  async saveTabState(tabId: TabId, state: unknown): Promise<void> {
    try {
      await this.saveUserWork(UserWorkType.TAB_STATE, tabId, state);
    } catch (error) {
      console.error("❌ Failed to save tab state:", error);
      throw error;
    }
  }

  async loadTabState<T = unknown>(tabId: TabId): Promise<T | null> {
    try {
      return (await this.loadUserWork(
        UserWorkType.TAB_STATE,
        tabId
      )) as T | null;
    } catch (error) {
      console.error("❌ Failed to load tab state:", error);
      return null;
    }
  }

  // ============================================================================
  // Explore STATE PERSISTENCE
  // ============================================================================

  async saveExploreState(state: CompleteExploreState): Promise<void> {
    try {
      await this.saveUserWork(UserWorkType.Explore_STATE, "browse", state);
    } catch (error) {
      console.error("❌ Failed to save Explore state:", error);
      throw error;
    }
  }

  async loadExploreState(): Promise<CompleteExploreState | null> {
    try {
      return (await this.loadUserWork(
        UserWorkType.Explore_STATE,
        "browse"
      )) as CompleteExploreState | null;
    } catch (error) {
      console.error("❌ Failed to load Explore state:", error);
      return null;
    }
  }

  // ============================================================================
  // SETTINGS PERSISTENCE
  // ============================================================================

  async saveSettings(settings: AppSettings): Promise<void> {
    try {
      await db.settings.put({ ...settings, id: "default" } as AppSettings & {
        id: string;
      });
    } catch (error) {
      console.error("❌ Failed to save settings:", error);
      throw error;
    }
  }

  async loadSettings(): Promise<AppSettings | null> {
    try {
      const settings = await db.settings.where("id").equals("default").first();
      return settings || null;
    } catch (error) {
      console.error("❌ Failed to load settings:", error);
      return null;
    }
  }

  // ============================================================================
  // USER PROJECTS
  // ============================================================================

  async saveProject(project: UserProject): Promise<void> {
    try {
      await db.userProjects.put(project);
    } catch (error) {
      console.error("❌ Failed to save project:", error);
      throw error;
    }
  }

  async loadProjects(): Promise<UserProject[]> {
    try {
      return await db.userProjects.orderBy("lastModified").reverse().toArray();
    } catch (error) {
      console.error("❌ Failed to load projects:", error);
      return [];
    }
  }

  async deleteProject(id: number): Promise<void> {
    try {
      await db.userProjects.delete(id);
    } catch (error) {
      console.error("❌ Failed to delete project:", error);
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
        version: 1,
      };
      return data;
    } catch (error) {
      console.error("❌ Failed to export data:", error);
      throw error;
    }
  }

  async importData(data: unknown): Promise<void> {
    // Implementation would go here - complex operation
    console.log("📥 Import data not yet implemented");
    throw new Error("Import not yet implemented");
  }

  async clearAllData(): Promise<void> {
    try {
      await db.transaction(
        "rw",
        [
          db.sequences,
          db.pictographs,
          db.userWork,
          db.userProjects,
          db.settings,
        ],
        async () => {
          await db.sequences.clear();
          await db.pictographs.clear();
          await db.userWork.clear();
          await db.userProjects.clear();
          await db.settings.clear();
        }
      );
    } catch (error) {
      console.error("❌ Failed to clear data:", error);
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
      console.error("❌ Failed to get storage info:", error);
      return { sequences: 0, pictographs: 0, userWork: 0, projects: 0 };
    }
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Generic method to save user work data
   */
  private async saveUserWork(
    type: UserWorkType,
    tabId: string,
    data: unknown
  ): Promise<void> {
    const workData: UserWorkData = {
      type,
      tabId,
      data,
      lastModified: new Date(),
      version: 1,
    };

    // Update existing record or create new one
    const existing = await db.userWork.where({ type, tabId }).first();

    if (existing) {
      await db.userWork.update(existing.id!, {
        data,
        lastModified: new Date(),
      });
    } else {
      await db.userWork.add(workData);
    }
  }

  /**
   * Generic method to load user work data
   */
  private async loadUserWork(
    type: UserWorkType,
    tabId: string
  ): Promise<unknown | null> {
    const workData = await db.userWork.where({ type, tabId }).first();

    return workData?.data || null;
  }

  // ============================================================================
  // SEQUENCE STATE PERSISTENCE (for hot module replacement survival)
  // ============================================================================

  private readonly CURRENT_SEQUENCE_STATE_KEY = "tka-current-sequence-state-v1";

  async saveCurrentSequenceState(state: {
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSubTab?: string;
  }): Promise<void> {
    try {
      // Use localStorage for immediate persistence that survives hot module replacement
      const stateData = {
        currentSequence: state.currentSequence,
        selectedStartPosition: state.selectedStartPosition,
        hasStartPosition: state.hasStartPosition,
        activeBuildSubTab: state.activeBuildSubTab || "construct",
        timestamp: Date.now(),
      };

      localStorage.setItem(
        this.CURRENT_SEQUENCE_STATE_KEY,
        JSON.stringify(stateData)
      );
    } catch (error) {
      console.error("❌ Failed to save current sequence state:", error);
      throw error;
    }
  }

  async loadCurrentSequenceState(): Promise<{
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSubTab?: string;
  } | null> {
    try {
      const stateJson = localStorage.getItem(this.CURRENT_SEQUENCE_STATE_KEY);
      if (!stateJson) {
        return null;
      }

      const stateData = JSON.parse(stateJson);

      // Check if the state is not too old (24 hours max)
      const maxAge = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
      if (stateData.timestamp && Date.now() - stateData.timestamp > maxAge) {
        await this.clearCurrentSequenceState();
        return null;
      }

      return {
        currentSequence: stateData.currentSequence || null,
        selectedStartPosition: stateData.selectedStartPosition || null,
        hasStartPosition: stateData.hasStartPosition || false,
        activeBuildSubTab: stateData.activeBuildSubTab || "construct",
      };
    } catch (error) {
      console.error("❌ Failed to load current sequence state:", error);
      return null;
    }
  }

  async clearCurrentSequenceState(): Promise<void> {
    try {
      localStorage.removeItem(this.CURRENT_SEQUENCE_STATE_KEY);
    } catch (error) {
      console.error("❌ Failed to clear current sequence state:", error);
      throw error;
    }
  }
}
