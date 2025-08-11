/**
 * Browse Service Interface Definitions
 * These handle browsing, thumbnails, favorites, and navigation
 */

import type {
	IBrowseService,
	IDeleteService,
	IFavoritesService,
	IFilterPersistenceService,
	INavigationService,
	ISectionService,
	ISequenceIndexService,
	IThumbnailService,
} from '../../interfaces';
import { createServiceInterface } from '../types';

// Import service implementations
import { BrowseService } from '../../implementations/BrowseService';
import { DeleteService } from '../../implementations/DeleteService';
import { FavoritesService } from '../../implementations/FavoritesService';
import { FilterPersistenceService } from '../../implementations/FilterPersistenceService';
import { NavigationService } from '../../implementations/NavigationService';
import { SectionService } from '../../implementations/SectionService';
import { SequenceIndexService } from '../../implementations/SequenceIndexService';
import { ThumbnailService } from '../../implementations/ThumbnailService';

// Core browse services
export const IBrowseServiceInterface = createServiceInterface<IBrowseService>(
	'IBrowseService',
	BrowseService
);

export const IThumbnailServiceInterface = createServiceInterface<IThumbnailService>(
	'IThumbnailService',
	ThumbnailService
);

export const ISequenceIndexServiceInterface = createServiceInterface<ISequenceIndexService>(
	'ISequenceIndexService',
	SequenceIndexService
);

// Advanced browse services
export const IFavoritesServiceInterface = createServiceInterface<IFavoritesService>(
	'IFavoritesService',
	FavoritesService
);

export const INavigationServiceInterface = createServiceInterface<INavigationService>(
	'INavigationService',
	NavigationService
);

export const ISectionServiceInterface = createServiceInterface<ISectionService>(
	'ISectionService',
	SectionService
);

export const IFilterPersistenceServiceInterface = createServiceInterface<IFilterPersistenceService>(
	'IFilterPersistenceService',
	FilterPersistenceService
);

export const IDeleteServiceInterface = createServiceInterface<IDeleteService>(
	'IDeleteService',
	DeleteService
);
