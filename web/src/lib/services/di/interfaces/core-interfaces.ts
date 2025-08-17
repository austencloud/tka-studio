/**
 * Core Service Interface Definitions
 * These are the main business logic and infrastructure services
 */

import type {
  IApplicationInitializationService,
  IConstructTabCoordinationService,
  IOptionDataService,
  ISettingsService,
  IStartPositionService,
} from "../../interfaces/application-interfaces";
import type {
  ISequenceDomainService,
  ISequenceService,
  IPersistenceService,
} from "../../interfaces/sequence-interfaces";
import type {
  IArrowRenderingService,
  IDataTransformationService,
  IGridRenderingService,
  IOverlayRenderingService,
  IPictographRenderingService,
  IPictographService,
  ISvgConfiguration,
  ISvgUtilityService,
} from "../../interfaces/pictograph-interfaces";
import type {
  IArrowPositioningService,
  IPropRenderingService,
} from "../../interfaces/positioning-interfaces";
import type {
  IMotionGenerationService,
  ISequenceGenerationService,
} from "../../interfaces/generation-interfaces";
import type { IDeviceDetectionService } from "../../interfaces/device-interfaces";
import type { IExportService } from "../../interfaces/export-interfaces";
import type { IPanelManagementService } from "../../interfaces/panel-interfaces";
import { createServiceInterface } from "../types";

// Import service implementations
import { ApplicationInitializationService } from "../../implementations/ApplicationInitializationService";
import { ArrowRenderingService } from "../../implementations/ArrowRenderingService";
import { ConstructTabCoordinationService } from "../../implementations/ConstructTabCoordinationService";
import { DataTransformationService } from "../../implementations/DataTransformationService";
import { DeviceDetectionService } from "../../implementations/DeviceDetectionService";
import { ExportService } from "../../implementations/ExportService";
import { GridRenderingService } from "../../implementations/GridRenderingService";
import { LocalStoragePersistenceService } from "../../implementations/LocalStoragePersistenceService";
import { MotionGenerationService } from "../../implementations/MotionGenerationService";
import { OptionDataService } from "../../implementations/OptionDataService";
import { OverlayRenderingService } from "../../implementations/OverlayRenderingService";
import { PanelManagementService } from "../../implementations/PanelManagementService";
import { PictographRenderingService } from "../../implementations/PictographRenderingService";
import { PictographService } from "../../implementations/PictographService";
import { PropRenderingService } from "../../implementations/PropRenderingService";
import { SequenceDomainService } from "../../implementations/SequenceDomainService";
import { SequenceGenerationService } from "../../implementations/SequenceGenerationService";
import { SequenceService } from "../../implementations/SequenceService";
import { SettingsService } from "../../implementations/SettingsService";
import { StartPositionService } from "../../implementations/StartPositionService";
import { SvgConfiguration } from "../../implementations/SvgConfiguration";
import { SvgUtilityService } from "../../implementations/SvgUtilityService";

// Core domain services
export const ISequenceServiceInterface =
  createServiceInterface<ISequenceService>(
    "ISequenceService",
    class extends SequenceService {
      constructor(...args: unknown[]) {
        super(
          args[0] as ISequenceDomainService,
          args[1] as IPersistenceService
        );
      }
    }
  );

export const ISequenceDomainServiceInterface =
  createServiceInterface<ISequenceDomainService>(
    "ISequenceDomainService",
    SequenceDomainService
  );

export const IPictographServiceInterface =
  createServiceInterface<IPictographService>(
    "IPictographService",
    class extends PictographService {
      constructor(...args: unknown[]) {
        super(args[0] as IPictographRenderingService);
      }
    }
  );

export const IPictographRenderingServiceInterface =
  createServiceInterface<IPictographRenderingService>(
    "IPictographRenderingService",
    class extends PictographRenderingService {
      constructor(...args: unknown[]) {
        super(
          args[0] as IArrowPositioningService,
          args[1] as IPropRenderingService,
          args[2] as ISvgUtilityService,
          args[3] as IGridRenderingService,
          args[4] as IArrowRenderingService,
          args[5] as IOverlayRenderingService,
          args[6] as IDataTransformationService
        );
      }
    }
  );

export const IPropRenderingServiceInterface =
  createServiceInterface<IPropRenderingService>(
    "IPropRenderingService",
    PropRenderingService
  );

// Rendering microservices
export const ISvgConfigurationInterface =
  createServiceInterface<ISvgConfiguration>(
    "ISvgConfiguration",
    SvgConfiguration
  );

export const ISvgUtilityServiceInterface =
  createServiceInterface<ISvgUtilityService>(
    "ISvgUtilityService",
    class extends SvgUtilityService {
      constructor(...args: unknown[]) {
        super(args[0] as ISvgConfiguration);
      }
    }
  );

export const IDataTransformationServiceInterface =
  createServiceInterface<IDataTransformationService>(
    "IDataTransformationService",
    DataTransformationService
  );

export const IGridRenderingServiceInterface =
  createServiceInterface<IGridRenderingService>(
    "IGridRenderingService",
    class extends GridRenderingService {
      constructor(...args: unknown[]) {
        super(args[0] as ISvgConfiguration);
      }
    }
  );

export const IArrowRenderingServiceInterface =
  createServiceInterface<IArrowRenderingService>(
    "IArrowRenderingService",
    class extends ArrowRenderingService {
      constructor(...args: unknown[]) {
        super(args[0] as ISvgConfiguration);
      }
    }
  );

export const IOverlayRenderingServiceInterface =
  createServiceInterface<IOverlayRenderingService>(
    "IOverlayRenderingService",
    class extends OverlayRenderingService {
      constructor(...args: unknown[]) {
        super(args[0] as ISvgConfiguration);
      }
    }
  );

// Infrastructure services
export const IPersistenceServiceInterface =
  createServiceInterface<IPersistenceService>(
    "IPersistenceService",
    LocalStoragePersistenceService
  );

export const ISettingsServiceInterface =
  createServiceInterface<ISettingsService>("ISettingsService", SettingsService);

export const IDeviceDetectionServiceInterface =
  createServiceInterface<IDeviceDetectionService>(
    "IDeviceDetectionService",
    DeviceDetectionService
  );

export const IPanelManagementServiceInterface =
  createServiceInterface<IPanelManagementService>(
    "IPanelManagementService",
    PanelManagementService
  );

// Application services
export const IApplicationInitializationServiceInterface =
  createServiceInterface<IApplicationInitializationService>(
    "IApplicationInitializationService",
    class extends ApplicationInitializationService {
      constructor(...args: unknown[]) {
        super(args[0] as ISettingsService, args[1] as IPersistenceService);
      }
    }
  );

export const IExportServiceInterface = createServiceInterface<IExportService>(
  "IExportService",
  class extends ExportService {
    constructor(...args: unknown[]) {
      super(args[0] as IPictographService);
    }
  }
);

// Generation services
export const IMotionGenerationServiceInterface =
  createServiceInterface<IMotionGenerationService>(
    "IMotionGenerationService",
    MotionGenerationService
  );

export const ISequenceGenerationServiceInterface =
  createServiceInterface<ISequenceGenerationService>(
    "ISequenceGenerationService",
    class extends SequenceGenerationService {
      constructor(...args: unknown[]) {
        super(args[0] as IMotionGenerationService);
      }
    }
  );

// Construct tab services
export const IConstructTabCoordinationServiceInterface =
  createServiceInterface<IConstructTabCoordinationService>(
    "IConstructTabCoordinationService",
    class extends ConstructTabCoordinationService {
      constructor(...args: unknown[]) {
        super(args[0] as ISequenceService, args[1] as IStartPositionService);
      }
    }
  );

export const IOptionDataServiceInterface =
  createServiceInterface<IOptionDataService>(
    "IOptionDataService",
    OptionDataService
  );

export const IStartPositionServiceInterface =
  createServiceInterface<IStartPositionService>(
    "IStartPositionService",
    StartPositionService
  );
