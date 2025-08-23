/**
 * Image Export Service Interface Definitions
 *
 * Proper ServiceInterface definitions for the TKA image export system,
 * following the established DI container patterns used by core services.
 */

import type {
  IBeatRenderingService,
  ICanvasManagementService,
  IDimensionCalculationService,
  IFileExportService,
  IGridOverlayService,
  IImageCompositionService,
  ILayoutCalculationService,
  ITextRenderingService,
  ITKAImageExportService,
} from "../../interfaces/image-export-interfaces";

import type {
  IWordTextRenderer,
  IUserInfoRenderer,
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
} from "../../interfaces/text-rendering-interfaces";

import { createServiceInterface } from "../types";

// Import service implementations
import { BeatRenderingService } from "../../implementations/image-export/BeatRenderingService";
import { CanvasManagementService } from "../../implementations/image-export/CanvasManagementService";
import { DimensionCalculationService } from "../../implementations/image-export/DimensionCalculationService";
import { FileExportService } from "../../implementations/image-export/FileExportService";
import { GridOverlayService } from "../../implementations/image-export/GridOverlayService";
import { ImageCompositionService } from "../../implementations/image-export/ImageCompositionService";
import { LayoutCalculationService } from "../../implementations/image-export/LayoutCalculationService";
import { TextRenderingService } from "../../implementations/image-export/TextRenderingService";
import { TKAImageExportService } from "../../implementations/image-export/TKAImageExportService";

// Import text rendering component implementations
import { WordTextRenderer } from "../../implementations/image-export/text-rendering/internal/WordTextRenderer";
import { UserInfoRenderer } from "../../implementations/image-export/text-rendering/internal/UserInfoRenderer";
import { DifficultyBadgeRenderer } from "../../implementations/image-export/text-rendering/internal/DifficultyBadgeRenderer";
import { TextRenderingUtils } from "../../implementations/image-export/text-rendering/internal/TextRenderingUtils";
import type { IPictographService } from "../../interfaces/pictograph-interfaces";
import type { ISVGToCanvasConverterService } from "../../interfaces/svg-conversion-interfaces";
import type { IBeatGridService } from "../../interfaces/beat-grid-interfaces";
import type { IBeatFallbackRenderingService } from "../../interfaces/beat-fallback-interfaces";

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
    class extends BeatRenderingService {
      constructor(...args: unknown[]) {
        super(
          args[0] as IPictographService,
          args[1] as ISVGToCanvasConverterService,
          args[2] as IBeatGridService,
          args[3] as IBeatFallbackRenderingService,
          args[4] as ICanvasManagementService
        );
      }
    }
  );

// Text rendering component interfaces
export const IWordTextRendererInterface =
  createServiceInterface<IWordTextRenderer>(
    "IWordTextRenderer",
    WordTextRenderer
  );

export const IUserInfoRendererInterface =
  createServiceInterface<IUserInfoRenderer>(
    "IUserInfoRenderer",
    UserInfoRenderer
  );

export const IDifficultyBadgeRendererInterface =
  createServiceInterface<IDifficultyBadgeRenderer>(
    "IDifficultyBadgeRenderer",
    DifficultyBadgeRenderer
  );

export const ITextRenderingUtilsInterface =
  createServiceInterface<ITextRenderingUtils>(
    "ITextRenderingUtils",
    TextRenderingUtils
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
