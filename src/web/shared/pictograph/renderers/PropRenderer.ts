/**
 * 🎪 PROP RENDERER
 *
 * Enterprise-grade prop rendering service with positioning, rotation, and color transformation.
 * Based on modern desktop app prop rendering patterns.
 *
 * Source: src/desktop/modern/src/presentation/components/pictograph/renderers/prop_renderer.py
 */

import type {
  IPropRenderer,
  ISVGAssetManager,
  IPropPositioningService,
  PropPosition,
} from "../interfaces/IPictographRenderer.js";

import type { PropData, MotionData } from "@tka/domain";
import { PropType, Location, Orientation } from "@tka/domain";

// ============================================================================
// PROP RENDERER IMPLEMENTATION
// ============================================================================

export class PropRenderer implements IPropRenderer {
  private readonly assetManager: ISVGAssetManager;
  private readonly positioningService: IPropPositioningService;
  private readonly CENTER_X = 475;
  private readonly CENTER_Y = 475;
  private readonly HAND_RADIUS = 143.1;

  constructor(
    assetManager: ISVGAssetManager,
    positioningService: IPropPositioningService
  ) {
    this.assetManager = assetManager;
    this.positioningService = positioningService;
  }

  // ============================================================================
  // PROP RENDERING METHODS
  // ============================================================================

  async renderProp(propData: PropData): Promise<SVGElement> {
    try {
      // Skip rendering if prop is not visible
      if (!propData.isVisible) {
        return this.createEmptyElement();
      }

      // Get the appropriate prop SVG asset
      const assetPath = this.getPropAssetPath(propData.propType);
      let propElement = await this.assetManager.loadSVGAsset(assetPath);

      // Apply color transformation
      this.applyPropColor(propElement, propData.color);

      // Calculate and apply positioning
      const position = this.calculatePropPosition(propData);
      this.applyPositioning(propElement, position);

      // Set prop metadata
      this.setPropMetadata(propElement, propData);

      return propElement;
    } catch (error) {
      console.error("Error rendering prop:", error);
      return this.createFallbackProp(propData);
    }
  }

  calculatePropPosition(propData: PropData): PropPosition {
    if (!propData.motionData) {
      return {
        x: this.CENTER_X,
        y: this.CENTER_Y,
        rotation: 0,
        handPointX: this.CENTER_X,
        handPointY: this.CENTER_Y,
      };
    }

    // Use the positioning service for sophisticated positioning
    return this.positioningService.calculatePropPosition(propData.motionData);
  }

  applyPropColor(element: SVGElement, color: string): void {
    // Get the SVG content as string for transformation
    const svgContent = element.outerHTML;
    const transformedContent = this.assetManager.applyColorTransformation(
      svgContent,
      color
    );

    // Parse the transformed content back to element
    const parser = new DOMParser();
    const doc = parser.parseFromString(transformedContent, "image/svg+xml");
    const transformedElement = doc.querySelector("svg");

    if (transformedElement) {
      // Replace the element's content with transformed content
      element.innerHTML = transformedElement.innerHTML;

      // Copy any new attributes
      Array.from(transformedElement.attributes).forEach((attr) => {
        if (attr.name !== "xmlns") {
          element.setAttribute(attr.name, attr.value);
        }
      });
    }
  }

  getPropAssetPath(propType: PropType): string {
    return this.assetManager.getAssetPath("prop", propType.toString());
  }

  // ============================================================================
  // PRIVATE POSITIONING METHODS
  // ============================================================================

  private applyPositioning(element: SVGElement, position: PropPosition): void {
    // Set transform origin to center of prop for proper rotation
    element.style.transformOrigin = "center center";

    // Apply position and rotation
    const transform = `translate(${position.x}px, ${position.y}px) rotate(${position.rotation}deg)`;
    element.style.transform = transform;

    // Ensure proper positioning context
    element.style.position = "absolute";
    element.style.top = "0";
    element.style.left = "0";
    element.style.zIndex = "3"; // Props should be above grid and arrows
  }

  private setPropMetadata(element: SVGElement, propData: PropData): void {
    // Set data attributes for debugging and interaction
    element.setAttribute("data-prop-id", propData.id);
    element.setAttribute("data-prop-color", propData.color);
    element.setAttribute("data-prop-type", propData.propType.toString());

    if (propData.motionData) {
      element.setAttribute("data-motion-type", propData.motionData.motionType);
      element.setAttribute("data-start-loc", propData.motionData.startLoc);
      element.setAttribute("data-end-loc", propData.motionData.endLoc);
      element.setAttribute(
        "data-prop-rot-dir",
        propData.motionData.propRotDir || ""
      );
    }

    // Add CSS classes for styling and interaction
    element.classList.add("pictograph-prop");
    element.classList.add(`prop-${propData.color}`);
    element.classList.add(`prop-${propData.propType}`);

    if (propData.isSelected) {
      element.classList.add("prop-selected");
    }
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  private createEmptyElement(): SVGElement {
    // Create an empty SVG element for invisible props
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "0");
    svg.setAttribute("height", "0");
    svg.style.display = "none";
    return svg;
  }

  private createFallbackProp(propData: PropData): SVGElement {
    // Create a simple fallback prop when asset loading fails
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 100 100");
    svg.setAttribute("width", "80");
    svg.setAttribute("height", "80");

    // Create a simple prop shape based on type
    const shape = this.createFallbackShape(propData.propType);
    shape.setAttribute("fill", this.getFallbackColor(propData.color));
    shape.setAttribute("stroke", this.getFallbackStrokeColor(propData.color));
    shape.setAttribute("stroke-width", "2");

    svg.appendChild(shape);

    // Apply positioning
    const position = this.calculatePropPosition(propData);
    this.applyPositioning(svg, position);

    // Set metadata
    this.setPropMetadata(svg, propData);

    console.warn(`Using fallback prop for ${propData.propType} prop`);
    return svg;
  }

  private createFallbackShape(propType: PropType): SVGElement {
    switch (propType) {
      case PropType.STAFF:
        return this.createStaffShape();
      case PropType.CLUB:
        return this.createClubShape();
      case PropType.HAND:
        return this.createHandShape();
      case PropType.BUUGENG:
        return this.createBuugengShape();
      default:
        return this.createStaffShape();
    }
  }

  private createStaffShape(): SVGElement {
    // Create a simple staff shape
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", "50");
    line.setAttribute("y1", "10");
    line.setAttribute("x2", "50");
    line.setAttribute("y2", "90");
    line.setAttribute("stroke-width", "6");
    line.setAttribute("stroke-linecap", "round");
    return line;
  }

  private createClubShape(): SVGElement {
    // Create a simple club shape
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");

    // Handle
    const handle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "line"
    );
    handle.setAttribute("x1", "50");
    handle.setAttribute("y1", "40");
    handle.setAttribute("x2", "50");
    handle.setAttribute("y2", "90");
    handle.setAttribute("stroke-width", "4");

    // Head
    const head = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "ellipse"
    );
    head.setAttribute("cx", "50");
    head.setAttribute("cy", "25");
    head.setAttribute("rx", "15");
    head.setAttribute("ry", "20");

    group.appendChild(handle);
    group.appendChild(head);
    return group;
  }

  private createHandShape(): SVGElement {
    // Create a simple hand shape
    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "circle"
    );
    circle.setAttribute("cx", "50");
    circle.setAttribute("cy", "50");
    circle.setAttribute("r", "20");
    return circle;
  }

  private createBuugengShape(): SVGElement {
    // Create a simple buugeng shape
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M30,50 Q50,20 70,50 Q50,80 30,50 Z");
    return path;
  }

  private getFallbackColor(color: string): string {
    const colorMap: Record<string, string> = {
      blue: "#0066cc",
      red: "#cc0000",
    };
    return colorMap[color.toLowerCase()] || "#666666";
  }

  private getFallbackStrokeColor(color: string): string {
    const colorMap: Record<string, string> = {
      blue: "#004499",
      red: "#990000",
    };
    return colorMap[color.toLowerCase()] || "#444444";
  }

  // ============================================================================
  // PROP TYPE VALIDATION
  // ============================================================================

  private isValidPropType(propType: string): boolean {
    const validTypes = Object.values(PropType);
    return validTypes.includes(propType as PropType);
  }

  private normalizePropType(propType: string): PropType {
    const normalized = propType.toLowerCase();

    switch (normalized) {
      case "staff":
      case "simplestaff":
        return PropType.STAFF;
      case "club":
        return PropType.CLUB;
      case "hand":
        return PropType.HAND;
      case "buugeng":
        return PropType.BUUGENG;
      default:
        console.warn(`Unknown prop type: ${propType}, defaulting to staff`);
        return PropType.STAFF;
    }
  }

  // ============================================================================
  // PERFORMANCE OPTIMIZATION
  // ============================================================================

  private shouldUseCache(propData: PropData): boolean {
    // Determine if this prop configuration should be cached
    // Cache common prop types and static configurations
    return (
      propData.propType === PropType.STAFF ||
      propData.propType === PropType.HAND
    );
  }

  private getCacheKey(propData: PropData): string {
    // Generate a cache key for this prop configuration
    const propType = propData.propType;
    const color = propData.color;
    const rotation = Math.round(propData.rotationAngle / 10) * 10; // Round to nearest 10 degrees

    return `prop_${propType}_${color}_${rotation}`;
  }
}
