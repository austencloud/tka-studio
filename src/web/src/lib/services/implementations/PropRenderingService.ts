/**
 * Prop Rendering Service - Web Implementation
 *
 * This service handles prop rendering for the web app, including:
 * - Loading and caching prop SVG assets
 * - Applying color transformations
 * - Calculating prop positions based on motion data
 * - Rendering props as SVG elements
 */

import { GridMode as DomainGridMode, Orientation } from "../../domain/enums";
import { DefaultPropPositioner } from "../DefaultPropPositioner";
import type {
  GridMode,
  IPropRenderingService,
  MotionData,
  PropPosition,
} from "../interfaces";
import { PropRotAngleManager } from "../PropRotAngleManager";

export class PropRenderingService implements IPropRenderingService {
  private svgCache = new Map<string, string>();
  private readonly SUPPORTED_PROPS = ["staff", "hand", "fan"];

  // Color transformation constants (matching desktop)
  private readonly COLOR_TRANSFORMATIONS = {
    blue: "#2E3192",
    red: "#ED1C24",
  };

  constructor() {
    // PropRenderingService initialized
  }

  /**
   * Render a prop as an SVG element
   * DISABLED: Props are now rendered by Prop.svelte components to avoid duplicates
   */
  async renderProp(
    _propType: string,
    _color: "blue" | "red",
    _motionData: MotionData,
    _gridMode: GridMode = DomainGridMode.DIAMOND,
  ): Promise<SVGElement> {
    // Props are now handled by ModernPictograph.svelte -> Prop.svelte components
    // This service-level rendering is disabled to prevent duplicate CIRCLE_PROP elements

    // Return empty group to prevent errors
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", "prop-service-disabled");
    return group;
  }

  /**
   * Calculate prop position based on motion data using real grid coordinates
   */
  async calculatePropPosition(
    motionData: MotionData,
    color: "blue" | "red",
    gridMode: GridMode = DomainGridMode.DIAMOND,
  ): Promise<PropPosition> {
    try {
      // Use end location for prop positioning (domain uses end_loc)
      const location = (motionData?.end_loc as unknown as string) || "s";

      // Use DefaultPropPositioner for consistent positioning
      const basePosition = DefaultPropPositioner.calculatePosition(
        location,
        gridMode,
      );

      // Calculate rotation using PropRotAngleManager for parity with legacy
      const rotation = this.calculatePropRotation(motionData, location);

      // Apply small offset for color separation
      const offset = this.getColorOffset(color);

      return {
        x: basePosition.x + offset.x,
        y: basePosition.y + offset.y,
        rotation,
      };
    } catch (error) {
      console.error("❌ Error calculating prop position:", error);
      // Return center position as fallback (950x950 scene)
      return { x: 475, y: 475, rotation: 0 };
    }
  }

  /**
   * Load prop SVG with color transformation
   */
  async loadPropSVG(propType: string, color: "blue" | "red"): Promise<string> {
    const cacheKey = `${propType}_${color}`;

    if (this.svgCache.has(cacheKey)) {
      const cached = this.svgCache.get(cacheKey);
      if (cached) return cached;
    }

    try {
      // Load base SVG
      const response = await fetch(`/images/props/${propType}.svg`);
      if (!response.ok) {
        throw new Error(`Failed to load ${propType}.svg: ${response.status}`);
      }

      let svgContent = await response.text();

      // Apply color transformation
      svgContent = this.applyColorTransformation(svgContent, color);

      // Cache the result
      this.svgCache.set(cacheKey, svgContent);

      return svgContent;
    } catch (error) {
      console.error(`❌ Error loading ${propType} SVG:`, error);
      // Return fallback SVG
      return this.createFallbackSVG(propType, color);
    }
  }

  /**
   * Get supported prop types
   */
  getSupportedPropTypes(): string[] {
    return [...this.SUPPORTED_PROPS];
  }

  /**
   * Apply color transformation to SVG content
   */
  private applyColorTransformation(
    svgContent: string,
    color: "blue" | "red",
  ): string {
    const targetColor = this.COLOR_TRANSFORMATIONS[color];

    // Replace common fill patterns
    svgContent = svgContent.replace(/fill="[^"]*"/g, `fill="${targetColor}"`);
    svgContent = svgContent.replace(/fill:[^;]*/g, `fill:${targetColor}`);

    // Replace stroke patterns for outlines
    svgContent = svgContent.replace(
      /stroke="[^"]*"/g,
      `stroke="${targetColor}"`,
    );
    svgContent = svgContent.replace(/stroke:[^;]*/g, `stroke:${targetColor}`);

    return svgContent;
  }

  /**
   * Get coordinates for a location on the grid using real grid data
   */
  // getLocationCoordinates removed (unused)

  /**
   * Calculate prop rotation based on motion data using PropRotAngleManager for parity
   */
  private calculatePropRotation(
    motionData: MotionData,
    location?: string,
  ): number {
    // Use PropRotAngleManager for consistent rotation calculation with legacy
    const endLocation =
      location || (motionData?.end_loc as unknown as string) || "s";
    const endOrientation =
      (motionData as unknown as { end_ori?: string })?.end_ori || "in";

    // Convert string orientation to enum
    let orientation: Orientation;
    switch (endOrientation) {
      case "in":
        orientation = Orientation.IN;
        break;
      case "out":
        orientation = Orientation.OUT;
        break;
      case "clock":
        orientation = Orientation.CLOCK;
        break;
      case "counter":
        orientation = Orientation.COUNTER;
        break;
      default:
        orientation = Orientation.IN;
    }

    // Delegate to angle manager
    return PropRotAngleManager.calculateRotation(endLocation, orientation);
  }

  private getColorOffset(color: "blue" | "red"): { x: number; y: number } {
    // Small offset to prevent props from overlapping
    return color === "blue" ? { x: -8, y: -8 } : { x: 8, y: 8 };
  }

  /**
   * Create fallback SVG for missing props
   */
  private createFallbackSVG(propType: string, color: "blue" | "red"): string {
    const fillColor = this.COLOR_TRANSFORMATIONS[color];
    return `
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
				<rect x="10" y="10" width="80" height="80" fill="${fillColor}" opacity="0.5"/>
				<text x="50" y="55" text-anchor="middle" font-size="12" fill="white">${propType}</text>
			</svg>
		`;
  }
}
