/**
 * 🏹 ARROW RENDERER
 *
 * Enterprise-grade arrow rendering service with positioning, rotation, and color transformation.
 * Based on modern desktop app arrow rendering patterns.
 *
 * Source: src/desktop/modern/src/presentation/components/pictograph/renderers/arrow_renderer.py
 */

import type {
  IArrowRenderer,
  ISVGAssetManager,
  IArrowPositioningOrchestrator,
  ArrowPosition,
  MotionType,
  MotionData
} from '../interfaces/IPictographRenderer.js';

import type { ArrowData, PictographData } from '@tka/domain';

// ============================================================================
// ARROW RENDERER IMPLEMENTATION
// ============================================================================

export class ArrowRenderer implements IArrowRenderer {
  private readonly assetManager: ISVGAssetManager;
  private readonly positioningOrchestrator: IArrowPositioningOrchestrator;
  private readonly CENTER_X = 475;
  private readonly CENTER_Y = 475;
  private readonly HAND_RADIUS = 143.1;

  constructor(
    assetManager: ISVGAssetManager,
    positioningOrchestrator: IArrowPositioningOrchestrator
  ) {
    this.assetManager = assetManager;
    this.positioningOrchestrator = positioningOrchestrator;
  }

  // ============================================================================
  // ARROW RENDERING METHODS
  // ============================================================================

  async renderArrow(arrowData: ArrowData): Promise<SVGElement> {
    try {
      // Skip rendering if arrow is not visible
      if (!arrowData.isVisible) {
        return this.createEmptyElement();
      }

      // Get the appropriate arrow SVG asset
      const assetPath = this.getArrowAssetPath(arrowData.motionData);
      const arrowElement = await this.assetManager.loadSVGAsset(assetPath);

      // Apply color transformation
      this.applyColorTransformation(arrowElement, arrowData.color);

      // Calculate and apply positioning
      const position = this.calculateArrowPosition(arrowData);
      this.applyPositioning(arrowElement, position);

      // Apply mirroring if needed
      if (arrowData.isMirrored) {
        this.applyMirroring(arrowElement);
      }

      // Set arrow metadata
      this.setArrowMetadata(arrowElement, arrowData);

      return arrowElement;

    } catch (error) {
      console.error('Error rendering arrow:', error);
      return this.createFallbackArrow(arrowData);
    }
  }

  calculateArrowPosition(arrowData: ArrowData, pictographData?: PictographData): ArrowPosition {
    if (!arrowData.motionData) {
      return { x: this.CENTER_X, y: this.CENTER_Y, rotation: 0 };
    }

    // Use the positioning orchestrator for sophisticated positioning
    return this.positioningOrchestrator.calculateArrowPosition(
      arrowData.color,
      arrowData.motionData,
      pictographData
    );
  }

  applyColorTransformation(element: SVGElement, color: string): void {
    // Get the SVG content as string for transformation
    const svgContent = element.outerHTML;
    const transformedContent = this.assetManager.applyColorTransformation(svgContent, color);

    // Parse the transformed content back to element
    const parser = new DOMParser();
    const doc = parser.parseFromString(transformedContent, 'image/svg+xml');
    const transformedElement = doc.querySelector('svg');

    if (transformedElement) {
      // Replace the element's content with transformed content
      element.innerHTML = transformedElement.innerHTML;

      // Copy any new attributes
      Array.from(transformedElement.attributes).forEach(attr => {
        if (attr.name !== 'xmlns') {
          element.setAttribute(attr.name, attr.value);
        }
      });
    }
  }

  getArrowAssetPath(motionData: MotionData): string {
    if (!motionData) {
      return this.assetManager.getAssetPath('arrow', 'static_0');
    }

    const turns = this.formatTurns(motionData.turns);
    const identifier = `${motionData.motionType}_${turns}`;

    return this.assetManager.getAssetPath('arrow', identifier);
  }

  // ============================================================================
  // PRIVATE POSITIONING METHODS
  // ============================================================================

  private applyPositioning(element: SVGElement, position: ArrowPosition): void {
    // Set transform origin to center of arrow for proper rotation
    element.style.transformOrigin = 'center center';

    // Apply position and rotation
    const transform = `translate(${position.x}px, ${position.y}px) rotate(${position.rotation}deg)`;
    element.style.transform = transform;

    // Ensure proper positioning context
    element.style.position = 'absolute';
    element.style.top = '0';
    element.style.left = '0';
  }

  private applyMirroring(element: SVGElement): void {
    // Apply horizontal mirroring
    const currentTransform = element.style.transform || '';
    element.style.transform = `${currentTransform} scaleX(-1)`;
  }

  private setArrowMetadata(element: SVGElement, arrowData: ArrowData): void {
    // Set data attributes for debugging and interaction
    element.setAttribute('data-arrow-id', arrowData.id);
    element.setAttribute('data-arrow-color', arrowData.color);
    element.setAttribute('data-arrow-turns', arrowData.turns.toString());

    if (arrowData.motionData) {
      element.setAttribute('data-motion-type', arrowData.motionData.motionType);
      element.setAttribute('data-start-loc', arrowData.motionData.startLoc);
      element.setAttribute('data-end-loc', arrowData.motionData.endLoc);
    }

    // Add CSS classes for styling and interaction
    element.classList.add('pictograph-arrow');
    element.classList.add(`arrow-${arrowData.color}`);

    if (arrowData.isSelected) {
      element.classList.add('arrow-selected');
    }
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  private formatTurns(turns: number): string {
    // Format turns for asset path (e.g., 0, 1, 2, 3, etc.)
    return Math.abs(turns).toString();
  }

  private createEmptyElement(): SVGElement {
    // Create an empty SVG element for invisible arrows
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '0');
    svg.setAttribute('height', '0');
    svg.style.display = 'none';
    return svg;
  }

  private createFallbackArrow(arrowData: ArrowData): SVGElement {
    // Create a simple fallback arrow when asset loading fails
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('width', '60');
    svg.setAttribute('height', '60');

    // Create a simple arrow shape
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M20,50 L60,30 L60,40 L80,40 L80,60 L60,60 L60,70 Z');
    path.setAttribute('fill', this.getFallbackColor(arrowData.color));
    path.setAttribute('stroke', this.getFallbackStrokeColor(arrowData.color));
    path.setAttribute('stroke-width', '2');

    svg.appendChild(path);

    // Apply positioning
    const position = this.calculateArrowPosition(arrowData);
    this.applyPositioning(svg, position);

    // Set metadata
    this.setArrowMetadata(svg, arrowData);

    console.warn(`Using fallback arrow for ${arrowData.color} arrow`);
    return svg;
  }

  private getFallbackColor(color: string): string {
    const colorMap: Record<string, string> = {
      'blue': '#0066cc',
      'red': '#cc0000'
    };
    return colorMap[color.toLowerCase()] || '#666666';
  }

  private getFallbackStrokeColor(color: string): string {
    const colorMap: Record<string, string> = {
      'blue': '#004499',
      'red': '#990000'
    };
    return colorMap[color.toLowerCase()] || '#444444';
  }

  // ============================================================================
  // MOTION TYPE VALIDATION
  // ============================================================================

  private isValidMotionType(motionType: string): boolean {
    const validTypes = ['static', 'pro', 'anti', 'dash', 'float'];
    return validTypes.includes(motionType.toLowerCase());
  }

  private normalizeMotionType(motionType: string): MotionType {
    const normalized = motionType.toLowerCase();

    switch (normalized) {
      case 'static':
        return MotionType.STATIC;
      case 'pro':
        return MotionType.PRO;
      case 'anti':
        return MotionType.ANTI;
      case 'dash':
        return MotionType.DASH;
      case 'float':
        return MotionType.FLOAT;
      default:
        console.warn(`Unknown motion type: ${motionType}, defaulting to static`);
        return MotionType.STATIC;
    }
  }

  // ============================================================================
  // PERFORMANCE OPTIMIZATION
  // ============================================================================

  private shouldUseCache(arrowData: ArrowData): boolean {
    // Determine if this arrow configuration should be cached
    // Cache static arrows and common configurations
    return arrowData.motionData?.motionType === 'static' ||
           arrowData.turns === 0;
  }

  private getCacheKey(arrowData: ArrowData): string {
    // Generate a cache key for this arrow configuration
    const motionType = arrowData.motionData?.motionType || 'static';
    const turns = arrowData.turns;
    const color = arrowData.color;
    const mirrored = arrowData.isMirrored ? 'mirrored' : 'normal';

    return `arrow_${motionType}_${turns}_${color}_${mirrored}`;
  }
}
