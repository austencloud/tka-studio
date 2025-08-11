/**
 * Browse Domain Models - Main Export
 *
 * Central export for all browse-related domain models and types.
 */

// Filter Types
export {
	FilterType,
	createFilterConfig,
	formatFilterDisplayName,
	isMultiValueFilter,
	isRangeFilter,
} from './FilterType';
export type { FilterConfig, FilterValue } from './FilterType';

// Sort Methods
export {
	SORT_CONFIGS,
	SortMethod,
	createCustomSortConfig,
	getAvailableSortConfigs,
	getAvailableSortMethods,
	getSortConfig,
	getSortDisplayName,
} from './SortMethod';
export type { SortConfig } from './SortMethod';

// Browse State
export {
	NavigationMode,
	createBrowseSequenceMetadata,
	createDefaultBrowseState,
	createDefaultDisplayState,
	createDefaultLoadingState,
	updateBrowseState,
} from './BrowseState';
export type {
	BrowseDisplayState,
	BrowseLoadingState,
	BrowseSequenceMetadata,
	BrowseState,
	SequenceFilterResult,
} from './BrowseState';

// Re-export GridMode from main enums to maintain compatibility
export { GridMode } from '../enums';

// Re-export common domain types for convenience
export type { SequenceData } from '../SequenceData';
