/**
 * 🏭 PICTOGRAPH SERVICE REGISTRATION
 *
 * Enterprise DI container registration for pictograph services.
 * Integrates sophisticated pictograph architecture with the TKA enterprise DI system.
 *
 * Based on: src/desktop/modern/src/application/services/core/service_registration_manager.py
 */

import type { ServiceContainer } from '../../di/core/ServiceContainer.js';

// Import service interfaces
import type {
  IPictographRenderer,
  IGridRenderer,
  IArrowRenderer,
  IPropRenderer,
  IGlyphRenderer,
  ISVGAssetManager,
  IArrowPositioningOrchestrator,
  IPropPositioningService,
  IPictographOrchestrator
} from '../interfaces/IPictographRenderer.js';

// Import service implementations
import { PictographOrchestrator } from '../services/PictographOrchestrator.js';
import { SVGAssetManager } from '../services/SVGAssetManager.js';
import { GridRenderer } from '../renderers/GridRenderer.js';
import { ArrowRenderer } from '../renderers/ArrowRenderer.js';
import { PropRenderer } from '../renderers/PropRenderer.js';
import { ArrowPositioningOrchestrator } from '../services/ArrowPositioningOrchestrator.js';
import { PropPositioningService } from '../services/PropPositioningService.js';

// ============================================================================
// PICTOGRAPH SERVICE REGISTRATION
// ============================================================================

export class PictographServiceRegistration {

  /**
   * Register all pictograph services with the DI container
   */
  static registerServices(container: ServiceContainer): void {
    console.log('🎨 Registering pictograph services...');

    try {
      // Register core services first (dependencies)
      this.registerCoreServices(container);

      // Register positioning services
      this.registerPositioningServices(container);

      // Register renderers
      this.registerRenderers(container);

      // Register orchestrator (depends on all others)
      this.registerOrchestrator(container);

      console.log('✅ Pictograph services registered successfully');

    } catch (error) {
      console.error('❌ Failed to register pictograph services:', error);
      throw error;
    }
  }

  /**
   * Register core infrastructure services
   */
  private static registerCoreServices(container: ServiceContainer): void {
    // SVG Asset Manager - singleton for caching
    container.registerSingleton(
      'ISVGAssetManager',
      () => new SVGAssetManager('/assets/pictograph')
    );

    console.log('  📦 Registered SVG Asset Manager');
  }

  /**
   * Register positioning calculation services
   */
  private static registerPositioningServices(container: ServiceContainer): void {
    // Arrow Positioning Orchestrator - singleton for consistency
    container.registerSingleton(
      'IArrowPositioningOrchestrator',
      () => new ArrowPositioningOrchestrator()
    );

    // Prop Positioning Service - singleton for consistency
    container.registerSingleton(
      'IPropPositioningService',
      () => new PropPositioningService()
    );

    console.log('  🎯 Registered positioning services');
  }

  /**
   * Register specialized renderers
   */
  private static registerRenderers(container: ServiceContainer): void {
    // Grid Renderer
    container.registerSingleton(
      'IGridRenderer',
      () => {
        const assetManager = container.resolve<ISVGAssetManager>('ISVGAssetManager');
        return new GridRenderer(assetManager);
      }
    );

    // Arrow Renderer
    container.registerSingleton(
      'IArrowRenderer',
      () => {
        const assetManager = container.resolve<ISVGAssetManager>('ISVGAssetManager');
        const positioning = container.resolve<IArrowPositioningOrchestrator>('IArrowPositioningOrchestrator');
        return new ArrowRenderer(assetManager, positioning);
      }
    );

    // Prop Renderer
    container.registerSingleton(
      'IPropRenderer',
      () => {
        const assetManager = container.resolve<ISVGAssetManager>('ISVGAssetManager');
        const positioning = container.resolve<IPropPositioningService>('IPropPositioningService');
        return new PropRenderer(assetManager, positioning);
      }
    );

    // TODO: Glyph Renderer (will be implemented in next phase)
    container.registerSingleton(
      'IGlyphRenderer',
      () => {
        // Placeholder implementation
        return {
          renderTKAGlyph: async () => document.createElementNS('http://www.w3.org/2000/svg', 'svg'),
          renderVTGGlyph: async () => document.createElementNS('http://www.w3.org/2000/svg', 'svg'),
          renderElementalGlyph: async () => document.createElementNS('http://www.w3.org/2000/svg', 'svg'),
          renderPositionGlyph: async () => document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        } as IGlyphRenderer;
      }
    );

    console.log('  🎨 Registered specialized renderers');
  }

  /**
   * Register main orchestrator service
   */
  private static registerOrchestrator(container: ServiceContainer): void {
    // Pictograph Orchestrator - coordinates all rendering
    container.registerSingleton(
      'IPictographOrchestrator',
      () => {
        const gridRenderer = container.resolve<IGridRenderer>('IGridRenderer');
        const arrowRenderer = container.resolve<IArrowRenderer>('IArrowRenderer');
        const propRenderer = container.resolve<IPropRenderer>('IPropRenderer');
        const glyphRenderer = container.resolve<IGlyphRenderer>('IGlyphRenderer');
        const assetManager = container.resolve<ISVGAssetManager>('ISVGAssetManager');
        const arrowPositioning = container.resolve<IArrowPositioningOrchestrator>('IArrowPositioningOrchestrator');
        const propPositioning = container.resolve<IPropPositioningService>('IPropPositioningService');

        return new PictographOrchestrator(
          gridRenderer,
          arrowRenderer,
          propRenderer,
          glyphRenderer,
          assetManager,
          arrowPositioning,
          propPositioning
        );
      }
    );

    // Main Pictograph Renderer interface (alias to orchestrator)
    container.registerSingleton(
      'IPictographRenderer',
      () => {
        const orchestrator = container.resolve<IPictographOrchestrator>('IPictographOrchestrator');
        return {
          renderPictograph: orchestrator.renderPictograph.bind(orchestrator),
          updatePictograph: async (element: SVGElement, data: any) => {
            // Clear and re-render for updates
            element.innerHTML = '';
            const newElement = await orchestrator.renderPictograph(data);
            element.innerHTML = newElement.innerHTML;
          },
          clearPictograph: (element: SVGElement) => {
            element.innerHTML = '';
          },
          setVisibility: orchestrator.setVisibility.bind(orchestrator)
        } as IPictographRenderer;
      }
    );

    console.log('  🎭 Registered pictograph orchestrator');
  }

  /**
   * Validate service registration
   */
  static validateRegistration(container: ServiceContainer): boolean {
    try {
      const requiredServices = [
        'ISVGAssetManager',
        'IArrowPositioningOrchestrator',
        'IPropPositioningService',
        'IGridRenderer',
        'IArrowRenderer',
        'IPropRenderer',
        'IGlyphRenderer',
        'IPictographOrchestrator',
        'IPictographRenderer'
      ];

      for (const service of requiredServices) {
        const instance = container.resolve(service);
        if (!instance) {
          console.error(`❌ Service not registered: ${service}`);
          return false;
        }
      }

      console.log('✅ All pictograph services validated successfully');
      return true;

    } catch (error) {
      console.error('❌ Service validation failed:', error);
      return false;
    }
  }

  /**
   * Get service dependency graph for debugging
   */
  static getServiceDependencyGraph(): Record<string, string[]> {
    return {
      'ISVGAssetManager': [],
      'IArrowPositioningOrchestrator': [],
      'IPropPositioningService': [],
      'IGridRenderer': ['ISVGAssetManager'],
      'IArrowRenderer': ['ISVGAssetManager', 'IArrowPositioningOrchestrator'],
      'IPropRenderer': ['ISVGAssetManager', 'IPropPositioningService'],
      'IGlyphRenderer': ['ISVGAssetManager'],
      'IPictographOrchestrator': [
        'IGridRenderer',
        'IArrowRenderer',
        'IPropRenderer',
        'IGlyphRenderer',
        'ISVGAssetManager',
        'IArrowPositioningOrchestrator',
        'IPropPositioningService'
      ],
      'IPictographRenderer': ['IPictographOrchestrator']
    };
  }

  /**
   * Preload essential assets for better performance
   */
  static async preloadAssets(container: ServiceContainer): Promise<void> {
    try {
      const assetManager = container.resolve<ISVGAssetManager>('ISVGAssetManager');

      const essentialAssets = [
        'grid/diamond_grid.svg',
        'grid/box_grid.svg',
        'arrows/static/from_radial/static_0.svg',
        'arrows/static/from_radial/static_1.svg',
        'arrows/pro/from_radial/pro_1.svg',
        'arrows/anti/from_radial/anti_1.svg',
        'props/staff.svg',
        'props/hand.svg'
      ];

      console.log('🚀 Preloading essential pictograph assets...');
      await assetManager.preloadAssets(essentialAssets);
      console.log('✅ Essential assets preloaded');

    } catch (error) {
      console.warn('⚠️ Asset preloading failed (non-critical):', error);
    }
  }

  /**
   * Create start position pictographs for the picker
   */
  static createStartPositionPictographs(container: ServiceContainer): any[] {
    const orchestrator = container.resolve<IPictographOrchestrator>('IPictographOrchestrator');

    // Create the three standard start positions
    const startPositions = [
      {
        id: 'alpha',
        name: 'Alpha',
        letter: 'α',
        gridMode: 'diamond',
        startPosition: 'alpha',
        description: 'Alpha start position'
      },
      {
        id: 'beta',
        name: 'Beta',
        letter: 'β',
        gridMode: 'diamond',
        startPosition: 'beta',
        description: 'Beta start position'
      },
      {
        id: 'gamma',
        name: 'Gamma',
        letter: 'γ',
        gridMode: 'diamond',
        startPosition: 'gamma',
        description: 'Gamma start position'
      }
    ];

    return startPositions.map(pos => ({
      ...pos,
      pictographData: orchestrator.createPictograph(pos.gridMode as any)
    }));
  }
}

// ============================================================================
// CONVENIENCE FUNCTIONS
// ============================================================================

/**
 * Quick registration function for use in ApplicationFactory
 */
export function registerPictographServices(container: ServiceContainer): void {
  PictographServiceRegistration.registerServices(container);
}

/**
 * Validate pictograph services are properly registered
 */
export function validatePictographServices(container: ServiceContainer): boolean {
  return PictographServiceRegistration.validateRegistration(container);
}

/**
 * Preload pictograph assets
 */
export async function preloadPictographAssets(container: ServiceContainer): Promise<void> {
  await PictographServiceRegistration.preloadAssets(container);
}

/**
 * Create start position data for picker
 */
export function createStartPositionData(container: ServiceContainer): any[] {
  return PictographServiceRegistration.createStartPositionPictographs(container);
}
