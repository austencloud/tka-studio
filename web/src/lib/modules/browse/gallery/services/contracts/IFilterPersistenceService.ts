import type { BrowseState } from "../../../shared/state/browse-state-models";
import type { FilterHistoryEntry } from "../implementations/BrowseStatePersister";

/**
 * Service for persisting filter and browse state
 */
export interface IFilterPersistenceService {
  saveFilterState(state: FilterHistoryEntry): Promise<void>;
  loadFilterState(): Promise<FilterHistoryEntry>;
  saveBrowseState(state: BrowseState): Promise<void>;
  loadBrowseState(): Promise<BrowseState | null>;
}
