/**
 * Prop Coordinator Service
 *
 * Orchestrates prop rendering by coordinating placement calculation and SVG loading.
 * Focuses on rendering coordination rather than placement calculation logic.
 * Uses PropPlacementService for placement calculations following separation of concerns.
 */

import type {
  PropPlacementData,
  MotionData,
  PictographData,
} from "$lib/domain";
import { MotionColor } from "$lib/domain/enums";
import { PropPlacementService } from "../positioning/PropPlacementService";
import type { IPropPlacementService } from "../positioning/PropPlacementService";

export interface PropRenderData {
  position: { x: number; y: number };
  rotation: number;
  svgData: {
    svgContent: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } | null;
  loaded: boolean;
  error: string | null;
}

export interface IPropCoordinatorService {
  calculatePropRenderData(
    PropPlacementData: PropPlacementData,
    motionData?: MotionData,
    pictographData?: PictographData // ✅ SIMPLIFIED: Complete pictograph data contains gridMode
  ): Promise<PropRenderData>;
}

export class PropCoordinatorService implements IPropCoordinatorService {
  private svgCache = new Map<
    string,
    {
      svgContent: string;
      viewBox: { width: number; height: number };
      center: { x: number; y: number };
    }
  >();
  private placementService: IPropPlacementService;

  constructor() {
    this.placementService = new PropPlacementService();
  }

  async calculatePropRenderData(
    PropPlacementData: PropPlacementData,
    motionData?: MotionData,
    pictographData?: PictographData
  ): Promise<PropRenderData> {
    // Debug logging removed for performance

    try {
      // ✅ SIMPLIFIED: Only need pictographData and motionData for placement calculation
      if (!pictographData) {
        throw new Error(
          "PictographData is required for prop placement calculation"
        );
      }

      if (!motionData) {
        throw new Error(
          "MotionData is required for prop placement calculation"
        );
      }

      const placementData = this.placementService.calculatePlacement(
        pictographData,
        motionData
      );

      // Load SVG data using motion data for color (single source of truth)
      console.log("✅ About to load SVG data");
      const svgData = await this.loadSvgData(PropPlacementData, motionData);
      console.log("✅ SVG data loaded:", svgData);

      const result = {
        position: { x: placementData.positionX, y: placementData.positionY },
        rotation: placementData.rotationAngle,
        svgData,
        loaded: true,
        error: null,
      };

      console.log(
        "✅ PropCoordinatorService.calculatePropRenderData returning:",
        result
      );
      return result;
    } catch (error) {
      console.error(
        "❌ PropCoordinatorService.calculatePropRenderData error:",
        error
      );
      return {
        position: { x: 475, y: 475 },
        rotation: 0,
        svgData: null,
        loaded: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  private async loadSvgData(
    propData: PropPlacementData,
    motionData?: MotionData
  ): Promise<{
    svgContent: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }> {
    // Use motionData.color as source of truth, fallback to blue
    const color = motionData?.color || MotionColor.BLUE;
    const cacheKey = `${motionData?.propType || "staff"}_${color}`;

    if (this.svgCache.has(cacheKey)) {
      console.log(
        `✅ PropCoordinatorService: Using cached SVG for ${cacheKey}`
      );
      const cachedData = this.svgCache.get(cacheKey);
      if (cachedData) {
        return cachedData;
      }
    }

    console.log(`🔄 PropCoordinatorService: Creating new SVG for ${cacheKey}`);

    const response = await fetch(
      `/images/props/${motionData?.propType || "staff"}.svg`
    );
    if (!response.ok) throw new Error("Failed to fetch SVG");

    const originalSvgText = await response.text();
    const { viewBox, center } = this.parsePropSvg(originalSvgText);
    const coloredSvgText = this.applyColorToSvg(originalSvgText, color);

    // Extract just the inner SVG content (no scaling needed - props are already correctly sized)
    const svgContent = this.extractSvgContent(coloredSvgText);

    const svgData = {
      svgContent,
      viewBox,
      center,
    };

    console.log(`💾 PropCoordinatorService: Caching SVG for ${cacheKey}`);
    this.svgCache.set(cacheKey, svgData);
    return svgData;
  }

  private parsePropSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    const doc = new DOMParser().parseFromString(svgText, "image/svg+xml");
    const svg = doc.documentElement;

    const viewBoxValues = svg.getAttribute("viewBox")?.split(/\s+/) || [
      "0",
      "0",
      "252.8",
      "77.8",
    ];
    const viewBox = {
      width: parseFloat(viewBoxValues[2] || "252.8") || 252.8,
      height: parseFloat(viewBoxValues[3] || "77.8") || 77.8,
    };

    let center = { x: viewBox.width / 2, y: viewBox.height / 2 };

    try {
      const centerElement = doc.getElementById("centerPoint");
      if (centerElement) {
        center = {
          x: parseFloat(centerElement.getAttribute("cx") || "0") || center.x,
          y: parseFloat(centerElement.getAttribute("cy") || "0") || center.y,
        };
      }
    } catch {
      // Use default center
    }

    return { viewBox, center };
  }

  private applyColorToSvg(svgText: string, color: MotionColor): string {
    const colorMap = new Map([
      [MotionColor.BLUE, "#2E3192"],
      [MotionColor.RED, "#ED1C24"],
    ]);

    const targetColor = colorMap.get(color) || "#2E3192";

    let coloredSvg = svgText.replace(
      /fill="#[0-9A-Fa-f]{6}"/g,
      `fill="${targetColor}"`
    );
    coloredSvg = coloredSvg.replace(
      /fill:\s*#[0-9A-Fa-f]{6}/g,
      `fill:${targetColor}`
    );

    // Make CSS class names unique for each color to prevent conflicts
    // Replace .st0, .st1, etc. with .st0-blue, .st1-blue, etc.
    const colorSuffix = color.toLowerCase();
    coloredSvg = coloredSvg.replace(/\.st(\d+)/g, `.st$1-${colorSuffix}`);

    // Also update class references in elements
    coloredSvg = coloredSvg.replace(
      /class="st(\d+)"/g,
      `class="st$1-${colorSuffix}"`
    );

    // Remove centerPoint circle to prevent detection issues
    coloredSvg = coloredSvg.replace(
      /<circle[^>]*id="centerPoint"[^>]*\/?>/g,
      ""
    );

    console.log(
      `🔧 PropCoordinatorService: Applied unique class names with suffix -${colorSuffix}`
    );
    return coloredSvg;
  }

  private extractSvgContent(svgText: string): string {
    // Extract SVG content (everything inside the <svg> tags)
    // Props are already correctly sized for 950x950 coordinate system
    console.log(
      `🔍 PropCoordinatorService: Extracting SVG content from: ${svgText.substring(0, 200)}...`
    );

    const svgContentMatch = svgText.match(/<svg[^>]*>(.*)<\/svg>/s);
    if (!svgContentMatch) {
      console.warn("Could not extract SVG content");
      console.log(
        `🚫 PropCoordinatorService: SVG text that failed to match: ${svgText}`
      );
      return svgText;
    }

    const extractedContent = svgContentMatch[1];
    console.log(
      `✅ PropCoordinatorService: Extracted SVG content: ${extractedContent.substring(0, 200)}...`
    );
    return extractedContent;
  }
}
