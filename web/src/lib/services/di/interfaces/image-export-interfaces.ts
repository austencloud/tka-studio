/**
 * Image Export Service Interface Definitions
 *
 * Proper ServiceInterface definitions for the TKA image export system,
 * following the established DI container patterns used by core services.
 */

import type {
  ITKAImageExportService,
  ILayoutCalculationService,
  IDimensionCalculationService,
  IFileExportService,
  IBeatRenderingService,
  ITextRenderingService,
  IImageCompositionService,
  IGridOverlayService,
  ICanvasManagementService,
} from "../../interfaces/image-export-interfaces";

import { createServiceInterface } from "../types";

// Import service implementations
import { TKAImageExportService } from "../../implementations/image-export/TKAImageExportService";
import { LayoutCalculationService } from "../../implementations/image-export/LayoutCalculationService";
import { DimensionCalculationService } from "../../implementations/image-export/DimensionCalculationService";
import { FileExportService } from "../../implementations/image-export/FileExportService";
import { BeatRenderingService } from "../../implementations/image-export/BeatRenderingService";
import { TextRenderingService } from "../../implementations/image-export/TextRenderingService";
import { ImageCompositionService } from "../../implementations/image-export/ImageCompositionService";
import { GridOverlayService } from "../../implementations/image-export/GridOverlayService";
import { CanvasManagementService } from "../../implementations/image-export/CanvasManagementService";

// Foundation services (no dependencies)
export const ILayoutCalculationServiceInterface =
  createServiceInterface<ILayoutCalculationService>(
    "ILayoutCalculationService",
    LayoutCalculationService
  );

export const IDimensionCalculationServiceInterface =
  createServiceInterface<IDimensionCalculationService>(
    "IDimensionCalculationService",
    DimensionCalculationService
  );

export const IFileExportServiceInterface =
  createServiceInterface<IFileExportService>(
    "IFileExportService",
    FileExportService
  );

export const ICanvasManagementServiceInterface =
  createServiceInterface<ICanvasManagementService>(
    "ICanvasManagementService",
    CanvasManagementService
  );

export const IGridOverlayServiceInterface =
  createServiceInterface<IGridOverlayService>(
    "IGridOverlayService",
    GridOverlayService
  );

export const IBeatRenderingServiceInterface =
  createServiceInterface<IBeatRenderingService>(
    "IBeatRenderingService",
    BeatRenderingService
  );

export const ITextRenderingServiceInterface =
  createServiceInterface<ITextRenderingService>(
    "ITextRenderingService",
    TextRenderingService
  );

// Composition service (depends on layout, dimension, beat rendering, and text rendering)
export const IImageCompositionServiceInterface =
  createServiceInterface<IImageCompositionService>(
    "IImageCompositionService",
    class extends ImageCompositionService {
      constructor(...args: unknown[]) {
        super(
          args[0] as ILayoutCalculationService,
          args[1] as IDimensionCalculationService,
          args[2] as IBeatRenderingService,
          args[3] as ITextRenderingService
        );
      }
    }
  );

// Main TKA image export service (depends on composition and file services)
export const ITKAImageExportServiceInterface =
  createServiceInterface<ITKAImageExportService>(
    "ITKAImageExportService",
    class extends TKAImageExportService {
      constructor(...args: unknown[]) {
        super(
          args[0] as IImageCompositionService,
          args[1] as IFileExportService,
          args[2] as ILayoutCalculationService,
          args[3] as IDimensionCalculationService
        );
      }
    }
  );
