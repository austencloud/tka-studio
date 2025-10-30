import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";

// PERFORMANCE FIX: Import services directly to avoid circular dependencies
import { ApplicationInitializer } from "../../application/services/implementations/ApplicationInitializer";
import { ComponentManagementService } from "../../application/services/implementations/ComponentManagementService";
import { DataTransformationService } from "../../application/services/implementations/DataTransformationService";
import { ErrorHandlingService } from "../../application/services/implementations/ErrorHandlingService";
import { HapticFeedbackService } from "../../application/services/implementations/HapticFeedbackService";
import { ResourceTracker } from "../../application/services/implementations/ResourceTracker";
import { RippleEffectService } from "../../application/services/implementations/RippleEffectService";
import { createAppState } from "../../application/state/app-state-factory.svelte";
import { createPerformanceMetricsState } from "../../application/state/PerformanceMetricsState.svelte";
import { DeviceDetector } from "../../device/services/implementations/DeviceDetector";
import { ViewportService } from "../../device/services/implementations/ViewportService.svelte";
import { createAppStateInitializer } from "../../foundation/services/implementations/data/app-state-initializer.svelte";
import { FileDownloadService } from "../../foundation/services/implementations/FileDownloadService";
import { SeoService } from "../../foundation/services/implementations/SeoService";
import { StorageService } from "../../foundation/services/implementations/StorageService";
import { SvgImageService } from "../../foundation/services/implementations/SvgImageService";
import { MobileFullscreenService } from "../../mobile/services/implementations/MobileFullscreenService";
import { PlatformDetectionService } from "../../mobile/services/implementations/PlatformDetectionService";
import { GestureService } from "../../mobile/services/implementations/GestureService";
import { PWAEngagementService } from "../../mobile/services/implementations/PWAEngagementService";
import { PWAInstallDismissalService } from "../../mobile/services/implementations/PWAInstallDismissalService";
import { SettingsState } from "../../settings/state/SettingsState.svelte.js";
import { TYPES } from "../types";

export const coreModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === APPLICATION SERVICES ===
    options.bind(TYPES.IApplicationInitializer).to(ApplicationInitializer);
    options.bind(TYPES.IResourceTracker).to(ResourceTracker);
    options
      .bind(TYPES.IComponentManagementService)
      .to(ComponentManagementService);
    options
      .bind(TYPES.IDataTransformationService)
      .to(DataTransformationService);
    options.bind(TYPES.IErrorHandlingService).to(ErrorHandlingService);
    options.bind(TYPES.IHapticFeedbackService).to(HapticFeedbackService);
    options.bind(TYPES.IRippleEffectService).to(RippleEffectService);

    // === MOBILE SERVICES ===
    options.bind(TYPES.IMobileFullscreenService).to(MobileFullscreenService);
    options.bind(TYPES.IPlatformDetectionService).to(PlatformDetectionService);
    options.bind(TYPES.IGestureService).to(GestureService);
    options.bind(TYPES.IPWAEngagementService).to(PWAEngagementService);
    options
      .bind(TYPES.IPWAInstallDismissalService)
      .to(PWAInstallDismissalService);

    // === DEVICE SERVICES ===
    options.bind(TYPES.IViewportService).to(ViewportService);
    options.bind(TYPES.IDeviceDetector).to(DeviceDetector);

    // === FOUNDATION SERVICES ===
    options.bind(TYPES.IFileDownloadService).to(FileDownloadService);
    options.bind(TYPES.IStorageService).to(StorageService);
    options.bind(TYPES.ISeoService).to(SeoService);
    options.bind(TYPES.ISvgImageService).to(SvgImageService);

    // === SETTINGS SERVICES ===
    options.bind(TYPES.ISettingsService).to(SettingsState);

    // === STATE SERVICES ===
    options.bind(TYPES.IAppState).toConstantValue(createAppState());
    options
      .bind(TYPES.IAppStateInitializer)
      .toConstantValue(createAppStateInitializer());
    options
      .bind(TYPES.IPerformanceMetricsState)
      .toConstantValue(createPerformanceMetricsState());
  }
);
