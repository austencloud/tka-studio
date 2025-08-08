/**
 * Arrow SVG Loader Service
 *
 * Handles loading and managing SVG assets for arrows in the legacy web app.
 */

import type SvgManager from '../../../SvgManager/SvgManager';
import type { ArrowSvgData } from '../../../SvgManager/ArrowSvgData';

// Interface for arrow loading parameters
interface ArrowLoadParams {
  motionType: string;
  turns: number | string;
  startOrientation: string;
  color: string;
}

export class ArrowSvgLoader {
  private svgManager: SvgManager;
  private cache: Map<string, string> = new Map();

  constructor(svgManager: SvgManager) {
    this.svgManager = svgManager;
  }

  /**
   * Load arrow SVG data based on motion type and properties
   */
  public async loadArrowSvg(arrowParams: ArrowLoadParams): Promise<string> {
    const cacheKey = this.generateCacheKey(arrowParams);

    // Check cache first
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    try {
      const svgPath = this.getArrowSvgPath(arrowParams);
      const svgContent = await this.loadSvgFromPath(svgPath);

      // Cache the result
      this.cache.set(cacheKey, svgContent);

      return svgContent;
    } catch (error) {
      console.warn(`Failed to load arrow SVG for ${cacheKey}:`, error);
      return this.getDefaultArrowSvg(arrowParams.color);
    }
  }

  /**
   * Get the appropriate SVG path based on arrow data
   */
  private getArrowSvgPath(arrowParams: ArrowLoadParams): string {
    const { motionType, turns, startOrientation } = arrowParams;

    // Handle float motion type
    if (motionType === 'float') {
      return '/images/arrows/float.svg';
    }

    // Handle other motion types
    // Convert turns to proper decimal format (e.g., 0 -> 0.0, 1 -> 1.0)
    const turnsNum = typeof turns === 'string' ? parseFloat(turns) : turns;
    const turnsStr = turnsNum.toFixed(1); // This will give us 0.0, 1.0, etc.

    if (startOrientation === 'in' || startOrientation === 'out') {
      return `/images/arrows/${motionType}/from_radial/${motionType}_${turnsStr}.svg`;
    } else if (startOrientation === 'clock' || startOrientation === 'counter') {
      return `/images/arrows/${motionType}/from_nonradial/${motionType}_${turnsStr}.svg`;
    }

    // Fallback to default arrow
    return '/images/arrows/dash.svg';
  }

  /**
   * Load SVG content from a path
   */
  private async loadSvgFromPath(path: string): Promise<string> {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.text();
    } catch (error) {
      throw new Error(`Failed to load SVG from ${path}: ${error}`);
    }
  }

  /**
   * Generate a cache key for the arrow data
   */
  private generateCacheKey(arrowParams: ArrowLoadParams): string {
    const { motionType, turns, startOrientation, color } = arrowParams;
    return `${motionType}_${turns}_${startOrientation}_${color}`;
  }

  /**
   * Get default arrow SVG when loading fails
   */
  private getDefaultArrowSvg(color?: string): string {
    // Define colors for red and blue arrows
    const fillColor = color === 'blue' ? '#2E3192' : color === 'red' ? '#ED1C24' : '#231F20';
    const strokeColor = color === 'blue' ? '#1E2082' : color === 'red' ? '#DD0C14' : '#231F20';

    return `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88.9 34.8">
        <style>
          .st0{fill:none;stroke:${strokeColor};stroke-width:4;stroke-miterlimit:10;}
          .st1{fill:${fillColor};}
        </style>
        <g>
          <line class="st0" x1="0" y1="17.4" x2="63.9" y2="17.4"/>
          <polygon class="st1" points="58.8,34.8 88.9,17.4 58.8,0"/>
        </g>
      </svg>
    `;
  }

  /**
   * Clear the SVG cache
   */
  public clearCache(): void {
    this.cache.clear();
  }

  /**
   * Get cache size for debugging
   */
  public getCacheSize(): number {
    return this.cache.size;
  }

  /**
   * Preload common arrow SVGs
   */
  public async preloadCommonArrows(): Promise<void> {
    const commonArrows = [
      { motionType: 'dash', turns: 1, startOrientation: 'in', color: 'blue' },
      { motionType: 'static', turns: 1, startOrientation: 'in', color: 'blue' },
      { motionType: 'float', turns: 1, startOrientation: 'in', color: 'blue' }
    ];

    const loadPromises = commonArrows.map(arrow =>
      this.loadArrowSvg(arrow as ArrowLoadParams).catch(error =>
        console.warn('Failed to preload arrow:', arrow, error)
      )
    );

    await Promise.all(loadPromises);
  }

  /**
   * Load SVG with the signature expected by Arrow.svelte
   */
  public async loadSvg(
    motionType: string,
    startOri: string,
    turns: number | string,
    color: string,
    svgMirrored: boolean = false
  ): Promise<ArrowSvgData> {
    const arrowParams: ArrowLoadParams = {
      motionType,
      startOrientation: startOri,
      turns,
      color
    };

    let svgContent = await this.loadArrowSvg(arrowParams);

    // Apply color transformation using SvgManager
    svgContent = this.svgManager.applyColor(svgContent, color as 'red' | 'blue');

    return this.parseSvgToArrowData(svgContent, arrowParams);
  }



  /**
   * Parse SVG content to ArrowSvgData format
   */
  private parseSvgToArrowData(svgContent: string, arrowParams: ArrowLoadParams): ArrowSvgData {
    // Create a data URL for the SVG content
    const imageSrc = `data:image/svg+xml;base64,${btoa(svgContent)}`;

    // Parse viewBox from SVG content
    const viewBoxMatch = svgContent.match(/viewBox="([^"]+)"/);
    let viewBox = { x: 0, y: 0, width: 88.9, height: 34.8 }; // Default values

    if (viewBoxMatch) {
      const [x, y, width, height] = viewBoxMatch[1].split(' ').map(Number);
      viewBox = { x, y, width, height };
    }

    // Calculate center point (usually half of width/height)
    const center = {
      x: viewBox.width / 2,
      y: viewBox.height / 2
    };

    return {
      imageSrc,
      viewBox,
      center
    };
  }
}
