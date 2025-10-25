/**
 * Mock Persistence Service for Testing
 *
 * In-memory implementation of IPersistenceService for testing
 * without actual IndexedDB dependencies.
 */

import type {
    AppSettings,
    CompleteGalleryState,
    IPersistenceService,
    PictographData,
    SequenceData,
    TabId,
    UserProject,
} from "$shared";
import { injectable } from "inversify";

@injectable()
export class MockPersistenceService implements IPersistenceService {
  // In-memory stores
  private sequences = new Map<string, SequenceData>();
  private pictographs = new Map<string, PictographData>();
  private projects = new Map<number, UserProject>();
  private settings: AppSettings | null = null;
  private userWork = new Map<string, unknown>();
  private activeTab: TabId | null = null;
  private tabStates = new Map<TabId, unknown>();
  private galleryState: CompleteGalleryState | null = null;
  private currentSequenceState: unknown | null = null;

  private _isInitialized = false;
  private _isAvailable = true;

  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  async initialize(): Promise<void> {
    this._isInitialized = true;
  }

  isAvailable(): boolean {
    return this._isAvailable;
  }

  // ============================================================================
  // SEQUENCE OPERATIONS
  // ============================================================================

  async saveSequence(sequence: SequenceData): Promise<void> {
    this.sequences.set(sequence.id, sequence);
  }

  async loadSequence(id: string): Promise<SequenceData | null> {
    return this.sequences.get(id) || null;
  }

  async getAllSequences(filter?: {
    author?: string;
    level?: number;
    isFavorite?: boolean;
    tags?: string[];
  }): Promise<SequenceData[]> {
    let results = Array.from(this.sequences.values());

    if (filter) {
      if (filter.author) {
        results = results.filter((seq) => seq.author === filter.author);
      }
      if (filter.level !== undefined) {
        results = results.filter((seq) => seq.level === filter.level);
      }
      if (filter.isFavorite !== undefined) {
        results = results.filter((seq) => seq.isFavorite === filter.isFavorite);
      }
      if (filter.tags && filter.tags.length > 0) {
        results = results.filter((seq) =>
          filter.tags!.some((tag) => seq.tags.includes(tag))
        );
      }
    }

    return results;
  }

  async deleteSequence(id: string): Promise<void> {
    this.sequences.delete(id);
  }

  async searchSequences(query: string): Promise<SequenceData[]> {
    const searchTerm = query.toLowerCase();
    return Array.from(this.sequences.values()).filter(
      (seq) =>
        seq.name.toLowerCase().includes(searchTerm) ||
        seq.word.toLowerCase().includes(searchTerm) ||
        (seq.author?.toLowerCase().includes(searchTerm) ?? false)
    );
  }

  // ============================================================================
  // PICTOGRAPH OPERATIONS
  // ============================================================================

  async savePictograph(pictograph: PictographData): Promise<void> {
    this.pictographs.set(pictograph.id, pictograph);
  }

  async loadPictograph(id: string): Promise<PictographData | null> {
    return this.pictographs.get(id) || null;
  }

  async getPictographsByLetter(letter: string): Promise<PictographData[]> {
    return Array.from(this.pictographs.values()).filter(
      (p) => p.letter === letter
    );
  }

  async getAllPictographs(): Promise<PictographData[]> {
    return Array.from(this.pictographs.values());
  }

  // ============================================================================
  // TAB STATE PERSISTENCE
  // ============================================================================

  async saveActiveTab(tabId: TabId): Promise<void> {
    this.activeTab = tabId;
  }

  async getActiveTab(): Promise<TabId | null> {
    return this.activeTab;
  }

  async saveTabState(tabId: TabId, state: unknown): Promise<void> {
    this.tabStates.set(tabId, state);
  }

  async loadTabState<T = unknown>(tabId: TabId): Promise<T | null> {
    return (this.tabStates.get(tabId) as T) || null;
  }

  // ============================================================================
  // GALLERY STATE PERSISTENCE
  // ============================================================================

  async saveGalleryState(state: CompleteGalleryState): Promise<void> {
    this.galleryState = state;
  }

  async loadGalleryState(): Promise<CompleteGalleryState | null> {
    return this.galleryState;
  }

  // ============================================================================
  // SETTINGS PERSISTENCE
  // ============================================================================

  async saveSettings(settings: AppSettings): Promise<void> {
    this.settings = settings;
  }

  async loadSettings(): Promise<AppSettings | null> {
    return this.settings;
  }

  // ============================================================================
  // USER PROJECTS
  // ============================================================================

  async saveProject(project: UserProject): Promise<void> {
    const id = project.id ?? this.getNextProjectId();
    this.projects.set(id, { ...project, id });
  }

  async loadProjects(): Promise<UserProject[]> {
    return Array.from(this.projects.values()).sort(
      (a, b) => b.lastModified.getTime() - a.lastModified.getTime()
    );
  }

  async deleteProject(id: number): Promise<void> {
    this.projects.delete(id);
  }

  private getNextProjectId(): number {
    const ids = Array.from(this.projects.keys());
    return ids.length > 0 ? Math.max(...ids) + 1 : 1;
  }

  // ============================================================================
  // UTILITY OPERATIONS
  // ============================================================================

  async exportAllData(): Promise<unknown> {
    return {
      sequences: Array.from(this.sequences.values()),
      pictographs: Array.from(this.pictographs.values()),
      userWork: Array.from(this.userWork.entries()),
      userProjects: Array.from(this.projects.values()),
      settings: this.settings,
      exportedAt: new Date().toISOString(),
      version: 1,
    };
  }

  async importData(data: unknown): Promise<void> {
    // Mock implementation - would need proper validation
    console.log("Mock import:", data);
  }

  async clearAllData(): Promise<void> {
    this.sequences.clear();
    this.pictographs.clear();
    this.projects.clear();
    this.settings = null;
    this.userWork.clear();
    this.activeTab = null;
    this.tabStates.clear();
    this.galleryState = null;
    this.currentSequenceState = null;
  }

  async getStorageInfo() {
    return {
      sequences: this.sequences.size,
      pictographs: this.pictographs.size,
      userWork: this.userWork.size,
      projects: this.projects.size,
    };
  }

  // ============================================================================
  // SEQUENCE STATE PERSISTENCE
  // ============================================================================

  async saveCurrentSequenceState(state: {
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSubTab?: string;
  }): Promise<void> {
    this.currentSequenceState = state;
  }

  async loadCurrentSequenceState(): Promise<{
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSubTab?: string;
  } | null> {
    return this.currentSequenceState as {
      currentSequence: SequenceData | null;
      selectedStartPosition: PictographData | null;
      hasStartPosition: boolean;
      activeBuildSubTab?: string;
    } | null;
  }

  async clearCurrentSequenceState(): Promise<void> {
    this.currentSequenceState = null;
  }
}
