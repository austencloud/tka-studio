/**
 * TKA Image Export Service Interfaces
 *
 * Service contracts for the TKA image export system, providing pixel-perfect
 * compatibility with the desktop application's image export functionality.
 *
 * This system converts TKA sequences into high-quality images for sharing,
 * printing, and archival purposes.
 *
 * ============================================================================
 * REFACTORED STRUCTURE: This file now re-exports from focused interface files
 * ============================================================================
 */

// ============================================================================
// RE-EXPORTS FROM SPLIT INTERFACE FILES
// ============================================================================

// Core interfaces (main orchestrator & fundamental types)
export type { ITKAImageExportService } from "./image-export-core-interfaces";

// Rendering interfaces (beat, image, canvas, visual effects)
export type {
  IBeatRenderingService,
  ICanvasManagementService,
  IFontManagementService,
  IGridOverlayService,
  IImageCompositionService,
  IReversalDetectionService,
  ITextRenderingService,
} from "./image-export-rendering-interfaces";

export {
  IBeatRenderingServiceInterface,
  ICanvasManagementServiceInterface,
  IFontManagementServiceInterface,
  IGridOverlayServiceInterface,
  IImageCompositionServiceInterface,
  IReversalDetectionServiceInterface,
  ITextRenderingServiceInterface,
} from "./image-export-rendering-interfaces";

// Layout interfaces (grid positioning, dimensions)
export type {
  IDimensionCalculationService,
  ILayoutCalculationService,
} from "./image-export-layout-interfaces";

export {
  IDimensionCalculationServiceInterface,
  ILayoutCalculationServiceInterface,
} from "./image-export-layout-interfaces";

// File interfaces (downloads, browser export)
export type { IFileExportService } from "./image-export-file-interfaces";

export { IFileExportServiceInterface } from "./image-export-file-interfaces";

// Utility interfaces (configuration, memory, validation)
export type {
  ExportValidationResult,
  IExportConfigurationManager as IExportConfig,
  IExportMemoryCalculator,
  IExportOptionsValidator,
  IExportSettingsService,
  IFilenameGeneratorService,
  IImagePreviewGenerator,
} from "./image-export-utility-interfaces";

// Text rendering component interface symbols (from existing text-rendering-interfaces.ts)
export const IWordTextRendererInterface = Symbol.for("IWordTextRenderer");
export const IUserInfoRendererInterface = Symbol.for("IUserInfoRenderer");
export const IDifficultyBadgeRendererInterface = Symbol.for(
  "IDifficultyBadgeRenderer"
);
export const ITextRenderingUtilsInterface = Symbol.for("ITextRenderingUtils");
