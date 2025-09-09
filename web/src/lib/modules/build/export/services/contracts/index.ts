/**
 * Export Services Contracts
 * 
 * Clean, focused interfaces for TKA image export functionality.
 * Each interface has a 1:1 relationship with an implementation.
 */

// Main export service
export type { IImageExportService, IImageExportService as ITKAImageExportService } from './IImageExportService';

// Layout and positioning
export type { IDimensionCalculationService, ILayoutCalculationService } from './image-export-layout-interfaces';

// Beat and canvas rendering
export type {
  IBeatRenderingService,
  ICanvasManagementService,
  IImageCompositionService
} from './image-export-rendering-interfaces';

// Text rendering
export type {
  IDifficultyBadgeRenderer,
  ITextRenderingUtils, IUserInfoRenderer, IWordTextRenderer
} from './text-rendering-interfaces';

// File operations
export type { IFileExportService } from './image-export-file-interfaces';
export type { IImageFormatConverterService } from './image-format-interfaces';

// SVG conversion
export type { ISVGToCanvasConverterService, RenderQualitySettings, SVGConversionOptions } from './svg-conversion-interfaces';

// Grid overlay
export type { IGridService as IBeatGridService } from '../../../../../shared/pictograph/grid/services/contracts/IGridService';
export type { IBeatGridDrawingService } from './beat-grid-draw-contracts';

// Fallback rendering
export type { EmptyBeatOptions, ErrorBeatOptions, FallbackRenderOptions, FallbackRenderResult, IBeatFallbackRenderer } from './beat-fallback-interfaces';

// Word card services (aliases for compatibility)
export type { IImageCompositionService as IWordCardMetadataOverlayService, IImageCompositionService as IWordCardSVGCompositionService } from './image-export-rendering-interfaces';

// Configuration and validation services
export type { IExportConfigManager } from '../implementations/ExportConfig';
export type { IExportMemoryCalculator } from '../implementations/ExportMemoryCalculator';
export type { IExportOptionsValidator } from '../implementations/ExportOptionsValidator';
export type { IFilenameGeneratorService } from '../implementations/FilenameGeneratorService';
export type { IImagePreviewGenerator } from '../implementations/ImagePreviewGenerator';
export type { ISequenceExportService } from '../implementations/SequenceExportService';
export type { ITextRenderingService } from '../implementations/TextRenderingService';

