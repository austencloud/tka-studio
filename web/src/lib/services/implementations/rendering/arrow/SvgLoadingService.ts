/**
 * SVG Loading Service
 *
 * Handles fetching and loading SVG files.
 * Extracted from ArrowRenderingService to improve modularity and reusability.
 */

import type { MotionData } from "$lib/domain";
import type { ArrowPlacementData } from "$lib/domain/ArrowPlacementData";
import type {
  ArrowSvgData,
  IArrowPathResolutionService,
  ISvgColorTransformationService,
  ISvgLoadingService,
  ISvgParsingService,
} from "$lib/services/interfaces/pictograph-interfaces";

export class SvgLoadingService implements ISvgLoadingService {
  constructor(
    private pathResolver: IArrowPathResolutionService,
    private svgParser: ISvgParsingService,
    private colorTransformer: ISvgColorTransformationService
  ) {}

  /**
   * Load arrow SVG data with color transformation (extracted from Arrow.svelte)
   */
  async loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<ArrowSvgData> {
    console.log("🔄 SvgLoadingService: Starting loadArrowPlacementData", {
      arrowData,
      motionData,
    });

    const path = this.pathResolver.getArrowPath(arrowData, motionData);
    console.log("📍 SvgLoadingService: Path resolved:", path);

    if (!path) {
      console.error(
        "❌ SvgLoadingService: No arrow path available - missing motion data"
      );
      throw new Error("No arrow path available - missing motion data");
    }

    console.log("🌐 SvgLoadingService: Fetching SVG content from:", path);
    const originalSvgText = await this.fetchSvgContent(path);
    console.log(
      "✅ SvgLoadingService: SVG content fetched, length:",
      originalSvgText.length
    );
    console.log(
      "📄 SvgLoadingService: SVG content preview:",
      originalSvgText.substring(0, 200) + "..."
    );

    const { viewBox, center } = this.svgParser.parseArrowSvg(originalSvgText);
    console.log("📐 SvgLoadingService: Parsed viewBox and center:", {
      viewBox,
      center,
    });

    // Apply color transformation to the SVG
    const coloredSvgText = this.colorTransformer.applyColorToSvg(
      originalSvgText,
      motionData.color
    );
    console.log(
      "🎨 SvgLoadingService: Color applied, length:",
      coloredSvgText.length
    );

    // Extract just the inner SVG content (no scaling needed - arrows are already correctly sized)
    const svgContent = this.svgParser.extractSvgContent(coloredSvgText);
    console.log(
      "✂️ SvgLoadingService: SVG content extracted, length:",
      svgContent.length
    );
    console.log(
      "📄 SvgLoadingService: Final SVG content:",
      svgContent.substring(0, 100) + "..."
    );

    const result = {
      imageSrc: svgContent,
      viewBox,
      center,
    };

    console.log("🎯 SvgLoadingService: Final result:", result);
    return result;
  }

  /**
   * Fetch SVG content from a given path
   */
  async fetchSvgContent(path: string): Promise<string> {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch SVG: ${response.status}`);
    }
    return await response.text();
  }
}
