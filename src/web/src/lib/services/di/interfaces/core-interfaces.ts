/**
 * Core Service Interface Definitions
 * These are the main business logic and infrastructure services
 */

import type {
  IApplicationInitializationService,
  IArrowPositioningService,
  IConstructTabCoordinationService,
  IDeviceDetectionService,
  IExportService,
  IMotionGenerationService,
  IOptionDataService,
  IPanelManagementService,
  IPersistenceService,
  IPictographRenderingService,
  IPictographService,
  IPropRenderingService,
  ISequenceDomainService,
  ISequenceGenerationService,
  ISequenceService,
  ISettingsService,
  IStartPositionService,
} from "../../interfaces";
import { createServiceInterface } from "../types";

// Import service implementations
import { ApplicationInitializationService } from "../../implementations/ApplicationInitializationService";
import { ConstructTabCoordinationService } from "../../implementations/ConstructTabCoordinationService";
import { DeviceDetectionService } from "../../implementations/DeviceDetectionService";
import { ExportService } from "../../implementations/ExportService";
import { LocalStoragePersistenceService } from "../../implementations/LocalStoragePersistenceService";
import { MotionGenerationService } from "../../implementations/MotionGenerationService";
import { OptionDataService } from "../../implementations/OptionDataService";
import { PanelManagementService } from "../../implementations/PanelManagementService";
import { PictographRenderingService } from "../../implementations/PictographRenderingService";
import { PictographService } from "../../implementations/PictographService";
import { PropRenderingService } from "../../implementations/PropRenderingService";
import { SequenceDomainService } from "../../implementations/SequenceDomainService";
import { SequenceGenerationService } from "../../implementations/SequenceGenerationService";
import { SequenceService } from "../../implementations/SequenceService";
import { SettingsService } from "../../implementations/SettingsService";
import { StartPositionService } from "../../implementations/StartPositionService";

// Core domain services
export const ISequenceServiceInterface =
  createServiceInterface<ISequenceService>(
    "ISequenceService",
    class extends SequenceService {
      constructor(...args: unknown[]) {
        super(
          args[0] as ISequenceDomainService,
          args[1] as IPersistenceService,
        );
      }
    },
  );

export const ISequenceDomainServiceInterface =
  createServiceInterface<ISequenceDomainService>(
    "ISequenceDomainService",
    SequenceDomainService,
  );

export const IPictographServiceInterface =
  createServiceInterface<IPictographService>(
    "IPictographService",
    class extends PictographService {
      constructor(...args: unknown[]) {
        super(args[0] as IPictographRenderingService);
      }
    },
  );

export const IPictographRenderingServiceInterface =
  createServiceInterface<IPictographRenderingService>(
    "IPictographRenderingService",
    class extends PictographRenderingService {
      constructor(...args: unknown[]) {
        super(
          args[0] as IArrowPositioningService,
          args[1] as IPropRenderingService,
        );
      }
    },
  );

export const IPropRenderingServiceInterface =
  createServiceInterface<IPropRenderingService>(
    "IPropRenderingService",
    PropRenderingService,
  );

// Infrastructure services
export const IPersistenceServiceInterface =
  createServiceInterface<IPersistenceService>(
    "IPersistenceService",
    LocalStoragePersistenceService,
  );

export const ISettingsServiceInterface =
  createServiceInterface<ISettingsService>("ISettingsService", SettingsService);

export const IDeviceDetectionServiceInterface =
  createServiceInterface<IDeviceDetectionService>(
    "IDeviceDetectionService",
    DeviceDetectionService,
  );

export const IPanelManagementServiceInterface =
  createServiceInterface<IPanelManagementService>(
    "IPanelManagementService",
    PanelManagementService,
  );

// Application services
export const IApplicationInitializationServiceInterface =
  createServiceInterface<IApplicationInitializationService>(
    "IApplicationInitializationService",
    class extends ApplicationInitializationService {
      constructor(...args: unknown[]) {
        super(args[0] as ISettingsService, args[1] as IPersistenceService);
      }
    },
  );

export const IExportServiceInterface = createServiceInterface<IExportService>(
  "IExportService",
  class extends ExportService {
    constructor(...args: unknown[]) {
      super(args[0] as IPictographService);
    }
  },
);

// Generation services
export const IMotionGenerationServiceInterface =
  createServiceInterface<IMotionGenerationService>(
    "IMotionGenerationService",
    MotionGenerationService,
  );

export const ISequenceGenerationServiceInterface =
  createServiceInterface<ISequenceGenerationService>(
    "ISequenceGenerationService",
    class extends SequenceGenerationService {
      constructor(...args: unknown[]) {
        super(args[0] as IMotionGenerationService);
      }
    },
  );

// Construct tab services
export const IConstructTabCoordinationServiceInterface =
  createServiceInterface<IConstructTabCoordinationService>(
    "IConstructTabCoordinationService",
    class extends ConstructTabCoordinationService {
      constructor(...args: unknown[]) {
        super(args[0] as ISequenceService, args[1] as IStartPositionService);
      }
    },
  );

export const IOptionDataServiceInterface =
  createServiceInterface<IOptionDataService>(
    "IOptionDataService",
    OptionDataService,
  );

export const IStartPositionServiceInterface =
  createServiceInterface<IStartPositionService>(
    "IStartPositionService",
    StartPositionService,
  );
