import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { PageFactoryService, PageImageExportService } from "../../../modules";
import {
    ExportMemoryCalculator,
    ExportOptionsValidator,
    FilenameGeneratorService,
    ImagePreviewGenerator,
    TextRenderingService,
    TKAImageExportService
} from "../../../modules/build/export/services/implementations";
import { BeatRenderingService } from "../../../modules/build/export/services/implementations/BeatRenderingService";
import { CanvasManagementService } from "../../../modules/build/export/services/implementations/CanvasManagementService";
import { DifficultyBadgeRenderer } from "../../../modules/build/export/services/implementations/DifficultyBadgeRenderer";
import { DimensionCalculationService } from "../../../modules/build/export/services/implementations/DimensionCalculationService";
import { ExportConfig } from "../../../modules/build/export/services/implementations/ExportConfig";
import { FileExportService } from "../../../modules/build/export/services/implementations/FileExportService";
import { GridOverlayService } from "../../../modules/build/export/services/implementations/GridOverlayService";
import { ImageCompositionService } from "../../../modules/build/export/services/implementations/ImageCompositionService";
import { ImageFormatConverterService } from "../../../modules/build/export/services/implementations/ImageFormatConverterService";
import { LayoutCalculationService } from "../../../modules/build/export/services/implementations/LayoutCalculationService";
import { SequenceExportService } from "../../../modules/build/export/services/implementations/SequenceExportService";
import { SVGToCanvasConverterService } from "../../../modules/build/export/services/implementations/SVGToCanvasConverterService";
import { TextRenderingUtils } from "../../../modules/build/export/services/implementations/TextRenderingUtils";
import { UserInfoRenderer } from "../../../modules/build/export/services/implementations/UserInfoRenderer";
import { WordTextRenderer } from "../../../modules/build/export/services/implementations/WordTextRenderer";
import { TYPES } from "../types";

export const exportModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === EXPORT CORE SERVICES ===
    options.bind(TYPES.IExportConfigManager).to(ExportConfig);
    options.bind(TYPES.IFileExportService).to(FileExportService);
    options.bind(TYPES.IExportMemoryCalculator).to(ExportMemoryCalculator);
    options.bind(TYPES.IExportOptionsValidator).to(ExportOptionsValidator);
    options.bind(TYPES.IFilenameGeneratorService).to(FilenameGeneratorService);
    options.bind(TYPES.IImagePreviewGenerator).to(ImagePreviewGenerator);
    options.bind(TYPES.ISequenceExportService).to(SequenceExportService);

    // === IMAGE EXPORT SERVICES ===
    options.bind(TYPES.ITKAImageExportService).to(TKAImageExportService);
    options.bind(TYPES.ICanvasManagementService).to(CanvasManagementService);
    options.bind(TYPES.IImageCompositionService).to(ImageCompositionService);
    options.bind(TYPES.ILayoutCalculationService).to(LayoutCalculationService);
    options.bind(TYPES.IDimensionCalculationService).to(DimensionCalculationService);
    options.bind(TYPES.IImageFormatConverterService).to(ImageFormatConverterService);
    options.bind(TYPES.ISVGToCanvasConverterService).to(SVGToCanvasConverterService);
    options.bind(TYPES.IGridOverlayService).to(GridOverlayService);

    // === RENDERING SERVICES ===
    options.bind(TYPES.IBeatRenderingService).to(BeatRenderingService);
    options.bind(TYPES.ITextRenderingService).to(TextRenderingService);
    options.bind(TYPES.IWordTextRenderer).to(WordTextRenderer);
    options.bind(TYPES.IUserInfoRenderer).to(UserInfoRenderer);
    options.bind(TYPES.IDifficultyBadgeRenderer).to(DifficultyBadgeRenderer);
    options.bind(TYPES.ITextRenderingUtils).to(TextRenderingUtils);

    // === PAGE SERVICES ===
    options.bind(TYPES.IPageFactoryService).to(PageFactoryService);
    options.bind(TYPES.IPageImageExportService).to(PageImageExportService);
  }
);
