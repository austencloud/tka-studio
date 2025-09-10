import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { BrowseStatePersister } from "../../../modules/browse/gallery/services/implementations/BrowseStatePersister";
import { FavoritesService } from "../../../modules/browse/gallery/services/implementations/FavoritesService";
import { FilterPersistenceService } from "../../../modules/browse/gallery/services/implementations/FilterPersistenceService";
import { GalleryPanelManager } from "../../../modules/browse/gallery/services/implementations/GalleryPanelManager";
import { BrowseSectionService } from "../../../modules/browse/gallery/services/implementations/GallerySectionService";
import { GalleryService } from "../../../modules/browse/gallery/services/implementations/GalleryService";
import { GalleryThumbnailService } from "../../../modules/browse/gallery/services/implementations/GalleryThumbnailService";
import { NavigationService } from "../../../modules/browse/gallery/services/implementations/NavigationService";
import { SequenceDeleteService } from "../../../modules/browse/gallery/services/implementations/SequenceDeleteService";
import { TYPES } from "../types";

export const browseModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === BROWSE GALLERY SERVICES ===
    options.bind(TYPES.IBrowseStatePersister).to(BrowseStatePersister);
    options.bind(TYPES.IFavoritesService).to(FavoritesService);
    options.bind(TYPES.IFilterPersistenceService).to(FilterPersistenceService);
    options.bind(TYPES.IGalleryPanelManager).to(GalleryPanelManager);
    // Note: IPersistenceService is now bound in data.module.ts to DexiePersistenceService
    // options.bind(TYPES.IPersistenceService).to(GalleryPersistenceService); // REMOVED - conflicts with DexiePersistenceService
    options.bind(TYPES.ISectionService).to(BrowseSectionService);
    options.bind(TYPES.IGalleryService).to(GalleryService);
    options.bind(TYPES.IGalleryThumbnailService).to(GalleryThumbnailService);
    options.bind(TYPES.INavigationService).to(NavigationService);
    options.bind(TYPES.IDeleteService).to(SequenceDeleteService);
  }
);
