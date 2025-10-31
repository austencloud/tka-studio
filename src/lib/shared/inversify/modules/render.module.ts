import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  CanvasManagementService,
  DimensionCalculationService,
  FilenameGeneratorService,
  GlyphCacheService,
  ImageCompositionService,
  ImageFormatConverterService,
  LayoutCalculationService,
  SequenceRenderService,
  SVGToCanvasConverterService,
  TextRenderingService,
} from "../../render/services/implementations";
import { TYPES } from "../types";

export const renderModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === MAIN RENDER SERVICE ===
    options.bind(TYPES.ISequenceRenderService).to(SequenceRenderService);

    // === PURE RENDERING SERVICES ===
    options.bind(TYPES.ICanvasManagementService).to(CanvasManagementService);
    options.bind(TYPES.IImageCompositionService).to(ImageCompositionService);
    options.bind(TYPES.ILayoutCalculationService).to(LayoutCalculationService);
    options
      .bind(TYPES.IDimensionCalculationService)
      .to(DimensionCalculationService);
    options
      .bind(TYPES.IImageFormatConverterService)
      .to(ImageFormatConverterService);
    options
      .bind(TYPES.ISVGToCanvasConverterService)
      .to(SVGToCanvasConverterService);
    options.bind(TYPES.ITextRenderingService).to(TextRenderingService);
    options
      .bind(TYPES.IGlyphCacheService)
      .to(GlyphCacheService)
      .inSingletonScope();

    // === UTILITY SERVICES ===
    options.bind(TYPES.IFilenameGeneratorService).to(FilenameGeneratorService);
  }
);
