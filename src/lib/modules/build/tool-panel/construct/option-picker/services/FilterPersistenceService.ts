import { injectable } from 'inversify';
import type { SortMethod, TypeFilter } from '../option-viewer';

export interface IFilterPersistenceService {
  saveFilters(sortMethod: SortMethod, typeFilter: TypeFilter, endPositionFilter: Record<string, boolean>, reversalFilter: Record<string, boolean>): void;
  loadFilters(): {
    sortMethod: SortMethod;
    typeFilter: TypeFilter;
    endPositionFilter: Record<string, boolean>;
    reversalFilter: Record<string, boolean>;
  } | null;
  clearFilters(): void;
}

@injectable()
export class FilterPersistenceService implements IFilterPersistenceService {
  private readonly STORAGE_KEY = 'tka-option-picker-filters';

  saveFilters(
    sortMethod: SortMethod,
    typeFilter: TypeFilter,
    endPositionFilter: Record<string, boolean>,
    reversalFilter: Record<string, boolean>
  ): void {
    try {
      const filterData = {
        sortMethod,
        typeFilter,
        endPositionFilter,
        reversalFilter,
        timestamp: Date.now()
      };

      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(filterData));

    } catch (error) {
      console.warn('⚠️ FilterPersistenceService: Failed to save filters:', error);
    }
  }

  loadFilters(): {
    sortMethod: SortMethod;
    typeFilter: TypeFilter;
    endPositionFilter: Record<string, boolean>;
    reversalFilter: Record<string, boolean>;
  } | null {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (!stored) {

        return null;
      }

      const filterData = JSON.parse(stored);

      // Validate the data structure
      if (!filterData.sortMethod || !filterData.typeFilter) {
        console.warn('⚠️ FilterPersistenceService: Invalid filter data structure');
        return null;
      }


      return {
        sortMethod: filterData.sortMethod,
        typeFilter: filterData.typeFilter,
        endPositionFilter: filterData.endPositionFilter || {},
        reversalFilter: filterData.reversalFilter || {}
      };
    } catch (error) {
      console.warn('⚠️ FilterPersistenceService: Failed to load filters:', error);
      return null;
    }
  }

  clearFilters(): void {
    try {
      localStorage.removeItem(this.STORAGE_KEY);

    } catch (error) {
      console.warn('⚠️ FilterPersistenceService: Failed to clear filters:', error);
    }
  }
}
