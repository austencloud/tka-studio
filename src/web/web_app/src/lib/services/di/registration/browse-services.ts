/**
 * Browse Services Registration
 * Handles registration of browsing, thumbnail, and navigation services
 */

import type { ServiceContainer } from '../ServiceContainer';
import {
	IBrowseServiceInterface,
	IDeleteServiceInterface,
	IFavoritesServiceInterface,
	IFilterPersistenceServiceInterface,
	INavigationServiceInterface,
	ISectionServiceInterface,
	ISequenceIndexServiceInterface,
	IThumbnailServiceInterface,
} from '../interfaces/browse-interfaces';

/**
 * Register all browse services
 */
export async function registerBrowseServices(container: ServiceContainer): Promise<void> {
	// Register browse services
	container.registerSingletonClass(IBrowseServiceInterface);
	container.registerSingletonClass(IThumbnailServiceInterface);
	container.registerSingletonClass(ISequenceIndexServiceInterface);

	// Register advanced browse services
	container.registerSingletonClass(IFavoritesServiceInterface);
	container.registerSingletonClass(INavigationServiceInterface);
	container.registerSingletonClass(ISectionServiceInterface);
	container.registerSingletonClass(IFilterPersistenceServiceInterface);
	container.registerSingletonClass(IDeleteServiceInterface);
}
