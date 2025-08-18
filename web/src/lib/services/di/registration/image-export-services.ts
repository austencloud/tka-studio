/**
 * Image Export Services Registration
 * 
 * Registers all TKA image export services with the DI container.
 * This module sets up the complete image export pipeline with proper
 * dependency injection following the established patterns.
 */

import type { ServiceContainer } from '../ServiceContainer';

// Import service interfaces
import {
  ITKAImageExportServiceInterface,
  ILayoutCalculationServiceInterface,
  IDimensionCalculationServiceInterface,
  IFileExportServiceInterface,
  IBeatRenderingServiceInterface,
  ITextRenderingServiceInterface,
  IImageCompositionServiceInterface,
  IGridOverlayServiceInterface,
  ICanvasManagementServiceInterface
} from '../../interfaces/image-export-interfaces';

// Import service implementations
import { TKAImageExportService } from '../../implementations/image-export/TKAImageExportService';
import { LayoutCalculationService } from '../../implementations/image-export/LayoutCalculationService';
import { DimensionCalculationService } from '../../implementations/image-export/DimensionCalculationService';
import { FileExportService } from '../../implementations/image-export/FileExportService';
import { BeatRenderingService } from '../../implementations/image-export/BeatRenderingService';
import { TextRenderingService } from '../../implementations/image-export/TextRenderingService';
import { ImageCompositionService } from '../../implementations/image-export/ImageCompositionService';
import { GridOverlayService } from '../../implementations/image-export/GridOverlayService';
import { CanvasManagementService } from '../../implementations/image-export/CanvasManagementService';

/**
 * Register all TKA image export services with the DI container
 * Services are registered in dependency order to ensure proper resolution
 */
export async function registerImageExportServices(
  container: ServiceContainer
): Promise<void> {
  console.log('🖼️ Registering TKA image export services...');

  try {
    // Register foundation services (no dependencies)
    console.log('📐 Registering layout and dimension services...');
    container.registerSingletonFactory(ILayoutCalculationServiceInterface, () => {
      return new LayoutCalculationService();
    });

    container.registerSingletonFactory(IDimensionCalculationServiceInterface, () => {
      return new DimensionCalculationService();
    });

    container.registerSingletonFactory(IFileExportServiceInterface, () => {
      return new FileExportService();
    });

    console.log('🎨 Registering rendering services...');
    container.registerSingletonFactory(ICanvasManagementServiceInterface, () => {
      return new CanvasManagementService();
    });

    container.registerSingletonFactory(IGridOverlayServiceInterface, () => {
      return new GridOverlayService();
    });

    container.registerSingletonFactory(IBeatRenderingServiceInterface, () => {
      return new BeatRenderingService();
    });

    container.registerSingletonFactory(ITextRenderingServiceInterface, () => {
      return new TextRenderingService();
    });

    // Register composition service (depends on layout, dimension, beat rendering, and text rendering)
    console.log('🏗️ Registering composition service...');
    container.registerSingletonFactory(IImageCompositionServiceInterface, () => {
      const layoutService = container.resolve(ILayoutCalculationServiceInterface);
      const dimensionService = container.resolve(IDimensionCalculationServiceInterface);
      const beatRenderer = container.resolve(IBeatRenderingServiceInterface);
      const textRenderer = container.resolve(ITextRenderingServiceInterface);
      
      return new ImageCompositionService(
        layoutService,
        dimensionService,
        beatRenderer,
        textRenderer
      );
    });

    // Register main TKA image export service (depends on composition and file services)
    console.log('📸 Registering main TKA image export service...');
    container.registerSingletonFactory(ITKAImageExportServiceInterface, () => {
      const compositionService = container.resolve(IImageCompositionServiceInterface);
      const fileService = container.resolve(IFileExportServiceInterface);
      const layoutService = container.resolve(ILayoutCalculationServiceInterface);
      const dimensionService = container.resolve(IDimensionCalculationServiceInterface);
      
      return new TKAImageExportService(
        compositionService,
        fileService,
        layoutService,
        dimensionService
      );
    });

    console.log('✅ TKA image export services registered successfully');

    // Validate registrations
    await validateImageExportServices(container);
    
  } catch (error) {
    console.error('❌ Failed to register TKA image export services:', error);
    throw new Error(`Image export service registration failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Validate that all image export services can be resolved
 */
async function validateImageExportServices(container: ServiceContainer): Promise<void> {
  console.log('🔍 Validating TKA image export service registrations...');
  
  const servicesToValidate = [
    { interface: ILayoutCalculationServiceInterface, name: 'LayoutCalculationService' },
    { interface: IDimensionCalculationServiceInterface, name: 'DimensionCalculationService' },
    { interface: IFileExportServiceInterface, name: 'FileExportService' },
    { interface: IBeatRenderingServiceInterface, name: 'BeatRenderingService' },
    { interface: ITextRenderingServiceInterface, name: 'TextRenderingService' },
    { interface: IImageCompositionServiceInterface, name: 'ImageCompositionService' },
    { interface: IGridOverlayServiceInterface, name: 'GridOverlayService' },
    { interface: ICanvasManagementServiceInterface, name: 'CanvasManagementService' },
    { interface: ITKAImageExportServiceInterface, name: 'TKAImageExportService' }
  ];

  const validationErrors: string[] = [];

  for (const { interface: serviceInterface, name } of servicesToValidate) {
    try {
      const service = container.resolve(serviceInterface);
      if (!service) {
        validationErrors.push(`${name} resolved to null/undefined`);
      } else {
        console.log(`✓ ${name} resolved successfully`);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      validationErrors.push(`${name} resolution failed: ${errorMessage}`);
    }
  }

  if (validationErrors.length > 0) {
    console.error('❌ Service validation failed:');
    validationErrors.forEach(error => console.error(`  - ${error}`));
    throw new Error(`Service validation failed: ${validationErrors.join(', ')}`);
  }

  console.log('✅ All TKA image export services validated successfully');
}

/**
 * Test image export service pipeline
 * Quick smoke test to ensure the services work together
 */
export async function testImageExportPipeline(container: ServiceContainer): Promise<boolean> {
  console.log('🧪 Testing TKA image export pipeline...');
  
  try {
    // Test layout calculation
    const layoutService = container.resolve(ILayoutCalculationServiceInterface);
    const layout = layoutService.calculateLayout(4, true);
    if (!layout || layout.length !== 2) {
      throw new Error('Layout calculation test failed');
    }
    console.log('✓ Layout calculation test passed');

    // Test dimension calculation
    const dimensionService = container.resolve(IDimensionCalculationServiceInterface);
    const testOptions = {
      addWord: true,
      addUserInfo: true,
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      combinedGrids: false,
      beatScale: 1,
      beatSize: 144,
      margin: 50,
      redVisible: true,
      blueVisible: true,
      userName: 'Test',
      exportDate: '1-1-2024',
      notes: 'Test',
      format: 'PNG' as const,
      quality: 1.0
    };
    const dimensions = dimensionService.determineAdditionalHeights(testOptions, 4, 1);
    if (!dimensions || dimensions.length !== 2) {
      throw new Error('Dimension calculation test failed');
    }
    console.log('✓ Dimension calculation test passed');

    // Test file export service
    const fileService = container.resolve(IFileExportServiceInterface);
    const formats = fileService.getSupportedFormats();
    if (!formats.includes('PNG') || !formats.includes('JPEG')) {
      throw new Error('File export service test failed');
    }
    console.log('✓ File export service test passed');

    // Test text rendering service
    const textService = container.resolve(ITextRenderingServiceInterface);
    const fontValidation = await textService.validateFonts();
    if (typeof fontValidation.available !== 'boolean') {
      throw new Error('Text rendering service test failed');
    }
    console.log('✓ Text rendering service test passed');

    // Test main export service
    const exportService = container.resolve(ITKAImageExportServiceInterface);
    const capabilities = exportService.getExportCapabilities();
    if (!capabilities.supportedFormats.includes('PNG')) {
      throw new Error('Main export service test failed');
    }
    console.log('✓ Main export service test passed');

    console.log('✅ TKA image export pipeline test completed successfully');
    return true;
    
  } catch (error) {
    console.error('❌ Image export pipeline test failed:', error);
    return false;
  }
}

/**
 * Get image export service metrics
 */
export function getImageExportServiceMetrics(container: ServiceContainer): {
  servicesRegistered: number;
  memoryUsage?: number;
  cacheStats?: any;
} {
  const servicesToCount = [
    ILayoutCalculationServiceInterface,
    IDimensionCalculationServiceInterface,
    IFileExportServiceInterface,
    IBeatRenderingServiceInterface,
    ITextRenderingServiceInterface,
    IImageCompositionServiceInterface,
    IGridOverlayServiceInterface,
    ICanvasManagementServiceInterface,
    ITKAImageExportServiceInterface
  ];

  let registeredCount = 0;
  let memoryUsage: number | undefined;
  let cacheStats: any;

  for (const serviceInterface of servicesToCount) {
    try {
      const service = container.resolve(serviceInterface);
      if (service) {
        registeredCount++;
        
        // Get memory usage from canvas management service
        if (serviceInterface === ICanvasManagementServiceInterface) {
          memoryUsage = service.getMemoryUsage();
          cacheStats = service.getCacheStats();
        }
      }
    } catch {
      // Service not registered or failed to resolve
    }
  }

  return {
    servicesRegistered: registeredCount,
    memoryUsage,
    cacheStats
  };
}

/**
 * Cleanup image export services
 * Should be called when shutting down the application
 */
export function cleanupImageExportServices(container: ServiceContainer): void {
  console.log('🧹 Cleaning up TKA image export services...');
  
  try {
    // Cleanup canvas management service
    const canvasService = container.resolve(ICanvasManagementServiceInterface);
    if (canvasService && typeof canvasService.dispose === 'function') {
      canvasService.dispose();
    }

    // Cleanup beat rendering service
    const beatService = container.resolve(IBeatRenderingServiceInterface);
    if (beatService && typeof beatService.dispose === 'function') {
      beatService.dispose();
    }

    console.log('✅ TKA image export services cleaned up successfully');
  } catch (error) {
    console.warn('⚠️ Some cleanup operations failed:', error);
  }
}
