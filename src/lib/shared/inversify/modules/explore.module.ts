import { ContainerModule, type ContainerModuleLoadOptions } from "inversify";
import {
  ExploreCacheService,
  ExploreDeleteService,
  ExploreFilterService,
  ExploreLoader,
  ExploreMetadataExtractor,
  ExploreSectionService,
  ExploreSortService,
  ExploreThumbnailService,
  FavoritesService,
  NavigationService,
} from "../../../modules";
import { OptimizedExploreService } from "../../../modules/explore/shared/services/implementations/OptimizedExploreService";
import { FilterPersistenceService } from "../../persistence/services/implementations/FilterPersistenceService";
import { UserExploreService } from "../../../modules/explore/users/services/implementations/UserExploreService";
import { TYPES } from "../types";

export const exploreModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === EXPLORE SERVICES ===

    // Specialized explore/Explore services (use directly, no orchestration layer needed!)
    options.bind(TYPES.IExploreMetadataExtractor).to(ExploreMetadataExtractor);
    options.bind(TYPES.IExploreCacheService).to(ExploreCacheService);
    options.bind(TYPES.IExploreFilterService).to(ExploreFilterService);
    options.bind(TYPES.IExploreSortService).to(ExploreSortService);
    options.bind(TYPES.IExploreLoader).to(ExploreLoader);

    // Other explore/Explore services
    options.bind(TYPES.IFavoritesService).to(FavoritesService);
    options.bind(TYPES.IFilterPersistenceService).to(FilterPersistenceService);

    // Note: IPersistenceService is now bound in data.module.ts to DexiePersistenceService
    // options.bind(TYPES.IPersistenceService).to(ExplorePersistenceService); // REMOVED - conflicts with DexiePersistenceService
    options.bind(TYPES.ISectionService).to(ExploreSectionService);
    options.bind(TYPES.IExploreThumbnailService).to(ExploreThumbnailService);
    options.bind(TYPES.IOptimizedExploreService).to(OptimizedExploreService);
    options.bind(TYPES.INavigationService).to(NavigationService);
    options.bind(TYPES.IDeleteService).to(ExploreDeleteService);

    // User Explore Service
    options.bind(TYPES.IUserExploreService).to(UserExploreService);
  }
);
