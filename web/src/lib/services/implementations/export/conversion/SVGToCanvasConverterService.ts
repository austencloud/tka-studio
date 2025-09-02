/**
 * SVG to Canvas Converter Service - SIMPLIFIED
 *
 * Uses fabric.js for clean, reliable SVG-to-Canvas conversion.
 * Replaces 300+ lines of over-engineered conversion logic with ~50 lines.
 */

import type {
  ISVGToCanvasConverterService,
  RenderQualitySettings,
  SVGConversionOptions,
} from "$contracts";
import { Canvas, loadSVGFromString, util } from "fabric";
import { injectable } from "inversify";

@injectable()
export class SVGToCanvasConverterService
  implements ISVGToCanvasConverterService
{
  private defaultQuality: RenderQualitySettings = {
    antialiasing: true,
    smoothScaling: true,
    imageSmoothingQuality: "high",
    scale: 1,
  };

  /**
   * Convert SVG string to Canvas using fabric.js
   */
  async convertSVGStringToCanvas(
    svgString: string,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement> {
    if (!svgString?.trim()) {
      throw new Error("SVG string cannot be empty");
    }

    return new Promise((resolve, reject) => {
      loadSVGFromString(svgString).then(({ objects, options: svgOptions }) => {
        try {
          // Create fabric canvas
          const fabricCanvas = new Canvas(document.createElement("canvas"), {
            width: options.width,
            height: options.height,
            backgroundColor: options.backgroundColor || "transparent",
          });

          // Add SVG objects to canvas
          const validObjects = objects.filter((obj) => obj !== null);
          if (validObjects.length > 0) {
            const svgGroup = util.groupSVGElements(validObjects, svgOptions);

            // Scale to fit if needed
            if (svgGroup && svgGroup.width && svgGroup.height) {
              const scaleX = options.width / svgGroup.width;
              const scaleY = options.height / svgGroup.height;
              const scale = Math.min(scaleX, scaleY);

              svgGroup.scale(scale);
              // Center the group on the canvas
              svgGroup.set({
                left: options.width / 2,
                top: options.height / 2,
                originX: "center",
                originY: "center",
              });
              fabricCanvas.add(svgGroup);
            }
          }

          fabricCanvas.renderAll();
          resolve(fabricCanvas.getElement());
        } catch (error) {
          reject(new Error(`SVG conversion failed: ${error}`));
        }
      });
    });
  }

  /**
   * Convert SVG element to Canvas
   */
  async convertSVGElementToCanvas(
    svgElement: SVGElement,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement> {
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgElement);
    return this.convertSVGStringToCanvas(svgString, options);
  }

  /**
   * Batch convert multiple SVG strings
   */
  async convertMultipleSVGsToCanvases(
    svgStrings: string[],
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement[]> {
    return Promise.all(
      svgStrings.map((svg) => this.convertSVGStringToCanvas(svg, options))
    );
  }

  // Simple implementations of required interface methods
  setDefaultQuality(settings: RenderQualitySettings): void {
    this.defaultQuality = { ...settings };
  }

  getQualitySettings(): RenderQualitySettings {
    return { ...this.defaultQuality };
  }

  validateSVG(svgContent: string | SVGElement): boolean {
    if (typeof svgContent === "string") {
      return (
        svgContent.trim().includes("<svg") && svgContent.includes("</svg>")
      );
    }
    return svgContent instanceof SVGElement;
  }

  getMemoryUsage() {
    return { activeConversions: 0, totalMemoryUsed: 0, peakMemoryUsed: 0 };
  }

  cleanup(): void {
    // No cleanup needed with fabric.js approach
  }
}
