import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  ApplicationInitializer,
  ComponentManagementService,
  DataTransformationService,
  ErrorHandlingService,
  ResourceTracker
} from "../../application/services/implementations";
import { DeviceDetector } from "../../device/services/implementations/DeviceDetector";
import {
  FileDownloadService,
  SeoService,
  StorageService,
  SvgImageService
} from "../../foundation";
import { SettingsService } from "../../settings/services/implementations/SettingsService";
import { TYPES } from "../types";

export const coreModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === APPLICATION SERVICES ===
    options.bind(TYPES.IApplicationInitializer).to(ApplicationInitializer);
    options.bind(TYPES.IResourceTracker).to(ResourceTracker);
    options.bind(TYPES.IComponentManagementService).to(ComponentManagementService);
    options.bind(TYPES.IDataTransformationService).to(DataTransformationService);
    options.bind(TYPES.IErrorHandlingService).to(ErrorHandlingService);

    // === DEVICE SERVICES ===
    options.bind(TYPES.IDeviceDetector).to(DeviceDetector);

    // === FOUNDATION SERVICES ===
    options.bind(TYPES.IFileDownloadService).to(FileDownloadService);
    options.bind(TYPES.IStorageService).to(StorageService);
    options.bind(TYPES.ISeoService).to(SeoService);
    options.bind(TYPES.ISvgImageService).to(SvgImageService);

    // === SETTINGS SERVICES ===
    options.bind(TYPES.ISettingsService).to(SettingsService);
  }
);
