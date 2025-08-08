/**
 * 🔲 GRID RENDERER
 *
 * Enterprise-grade grid rendering service for pictograph backgrounds.
 * Based on modern desktop app grid rendering patterns.
 *
 * Source: src/desktop/modern/src/presentation/components/pictograph/renderers/grid_renderer.py
 */

import type {
  IGridRenderer,
  ISVGAssetManager,
  GridPoint,
  GridMode,
  Location
} from '../interfaces/IPictographRenderer.js';

import type { GridData } from '@tka/domain';

// ============================================================================
// GRID RENDERER IMPLEMENTATION
// ============================================================================

export class GridRenderer implements IGridRenderer {
  private readonly assetManager: ISVGAssetManager;
  private readonly SCENE_SIZE = 950;
  private readonly CENTER_X = 475;
  private readonly CENTER_Y = 475;

  constructor(assetManager: ISVGAssetManager) {
    this.assetManager = assetManager;
  }

  // ============================================================================
  // GRID RENDERING METHODS
  // ============================================================================

  async renderGrid(gridData: GridData): Promise<SVGElement> {
    try {
      const gridAssetPath = this.getGridAssetPath(gridData.mode);
      const gridElement = await this.assetManager.loadSVGAsset(gridAssetPath);

      // Configure grid element
      this.configureGridElement(gridElement, gridData);

      return gridElement;

    } catch (error) {
      console.error('Error rendering grid:', error);
      return this.createFallbackGrid(gridData);
    }
  }

  getGridPoints(gridData: GridData): GridPoint[] {
    switch (gridData.mode) {
      case GridMode.DIAMOND:
        return this.getDiamondGridPoints();
      case GridMode.BOX:
        return this.getBoxGridPoints();
      default:
        return this.getDiamondGridPoints();
    }
  }

  updateGridMode(element: SVGElement, mode: GridMode): void {
    // Update the grid element to use a different mode
    // This would typically involve swapping the SVG content
    const newAssetPath = this.getGridAssetPath(mode);

    this.assetManager.loadSVGAsset(newAssetPath).then(newGrid => {
      // Replace the content of the existing element
      element.innerHTML = newGrid.innerHTML;

      // Copy attributes
      Array.from(newGrid.attributes).forEach(attr => {
        element.setAttribute(attr.name, attr.value);
      });
    }).catch(error => {
      console.error('Error updating grid mode:', error);
    });
  }

  // ============================================================================
  // PRIVATE GRID CONFIGURATION METHODS
  // ============================================================================

  private configureGridElement(element: SVGElement, gridData: GridData): void {
    // Set standard pictograph dimensions
    element.setAttribute('width', '100%');
    element.setAttribute('height', '100%');
    element.setAttribute('viewBox', `0 0 ${this.SCENE_SIZE} ${this.SCENE_SIZE}`);

    // Set positioning
    element.style.position = 'absolute';
    element.style.top = '0';
    element.style.left = '0';
    element.style.zIndex = '1';

    // Apply visibility
    element.style.opacity = gridData.visible ? '1' : '0';

    // Apply any grid-specific styling
    this.applyGridStyling(element, gridData);
  }

  private applyGridStyling(element: SVGElement, gridData: GridData): void {
    // Apply grid-specific styling based on mode and size
    const gridLines = element.querySelectorAll('line, path, circle');

    gridLines.forEach(line => {
      // Set grid line styling
      line.setAttribute('stroke', '#ddd');
      line.setAttribute('stroke-width', '1');
      line.setAttribute('fill', 'none');
      line.setAttribute('opacity', '0.6');
    });

    // Apply size scaling if needed
    if (gridData.size && gridData.size !== 8) {
      const scale = gridData.size / 8;
      element.style.transform = `scale(${scale})`;
      element.style.transformOrigin = 'center center';
    }
  }

  // ============================================================================
  // GRID POINT CALCULATION METHODS
  // ============================================================================

  private getDiamondGridPoints(): GridPoint[] {
    // Diamond grid points based on TKA standard positions
    const radius = 143.1; // Hand radius from desktop app
    const points: GridPoint[] = [];

    // 8 primary positions around the diamond
    const positions = [
      { location: Location.NORTH, angle: 0 },
      { location: Location.NORTHEAST, angle: 45 },
      { location: Location.EAST, angle: 90 },
      { location: Location.SOUTHEAST, angle: 135 },
      { location: Location.SOUTH, angle: 180 },
      { location: Location.SOUTHWEST, angle: 225 },
      { location: Location.WEST, angle: 270 },
      { location: Location.NORTHWEST, angle: 315 }
    ];

    positions.forEach(pos => {
      const radians = (pos.angle * Math.PI) / 180;
      const x = this.CENTER_X + radius * Math.cos(radians);
      const y = this.CENTER_Y + radius * Math.sin(radians);

      points.push({
        x,
        y,
        location: pos.location
      });
    });

    return points;
  }

  private getBoxGridPoints(): GridPoint[] {
    // Box grid points for square formation
    const radius = 143.1;
    const points: GridPoint[] = [];

    // 4 primary positions for box formation
    const positions = [
      { location: Location.NORTH, x: 0, y: -radius },
      { location: Location.EAST, x: radius, y: 0 },
      { location: Location.SOUTH, x: 0, y: radius },
      { location: Location.WEST, x: -radius, y: 0 }
    ];

    positions.forEach(pos => {
      points.push({
        x: this.CENTER_X + pos.x,
        y: this.CENTER_Y + pos.y,
        location: pos.location
      });
    });

    return points;
  }

  // ============================================================================
  // ASSET PATH METHODS
  // ============================================================================

  private getGridAssetPath(mode: GridMode): string {
    switch (mode) {
      case GridMode.DIAMOND:
        return 'grid/diamond_grid.svg';
      case GridMode.BOX:
        return 'grid/box_grid.svg';
      default:
        return 'grid/diamond_grid.svg';
    }
  }

  // ============================================================================
  // FALLBACK METHODS
  // ============================================================================

  private createFallbackGrid(gridData: GridData): SVGElement {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${this.SCENE_SIZE} ${this.SCENE_SIZE}`);
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');

    if (gridData.mode === GridMode.DIAMOND) {
      this.createFallbackDiamondGrid(svg);
    } else {
      this.createFallbackBoxGrid(svg);
    }

    return svg;
  }

  private createFallbackDiamondGrid(svg: SVGElement): void {
    const radius = 143.1;

    // Create diamond shape
    const diamond = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const diamondPath = `
      M ${this.CENTER_X} ${this.CENTER_Y - radius}
      L ${this.CENTER_X + radius} ${this.CENTER_Y}
      L ${this.CENTER_X} ${this.CENTER_Y + radius}
      L ${this.CENTER_X - radius} ${this.CENTER_Y}
      Z
    `;

    diamond.setAttribute('d', diamondPath);
    diamond.setAttribute('fill', 'none');
    diamond.setAttribute('stroke', '#ddd');
    diamond.setAttribute('stroke-width', '2');
    diamond.setAttribute('opacity', '0.6');

    svg.appendChild(diamond);

    // Add center point
    const center = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    center.setAttribute('cx', this.CENTER_X.toString());
    center.setAttribute('cy', this.CENTER_Y.toString());
    center.setAttribute('r', '3');
    center.setAttribute('fill', '#999');
    center.setAttribute('opacity', '0.8');

    svg.appendChild(center);
  }

  private createFallbackBoxGrid(svg: SVGElement): void {
    const size = 143.1 * 2;

    // Create box shape
    const box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    box.setAttribute('x', (this.CENTER_X - size / 2).toString());
    box.setAttribute('y', (this.CENTER_Y - size / 2).toString());
    box.setAttribute('width', size.toString());
    box.setAttribute('height', size.toString());
    box.setAttribute('fill', 'none');
    box.setAttribute('stroke', '#ddd');
    box.setAttribute('stroke-width', '2');
    box.setAttribute('opacity', '0.6');

    svg.appendChild(box);

    // Add center point
    const center = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    center.setAttribute('cx', this.CENTER_X.toString());
    center.setAttribute('cy', this.CENTER_Y.toString());
    center.setAttribute('r', '3');
    center.setAttribute('fill', '#999');
    center.setAttribute('opacity', '0.8');

    svg.appendChild(center);
  }
}
