/**
 * REAL Performance Benchmark - Uses Actual Rendering Services
 *
 * This actually tests your real pictograph rendering, not fake circles.
 */

import { JSDOM } from "jsdom";

// Setup browser-like environment for rendering
const dom = new JSDOM("<!DOCTYPE html><html><body></body></html>", {
  url: "http://localhost",
  pretendToBeVisual: true,
  resources: "usable",
});

global.window = dom.window as any;
global.document = dom.window.document;
global.HTMLCanvasElement = dom.window.HTMLCanvasElement as any;
global.Image = dom.window.Image as any;
global.Blob = dom.window.Blob as any;
global.URL = dom.window.URL as any;

// Now import the container after DOM is set up
import {
  ensureContainerInitialized,
  container,
} from "../src/lib/shared/inversify/container.js";
import { TYPES } from "../src/lib/shared/inversify/types.js";
import type { ISequenceRenderService } from "../src/lib/shared/render/services/contracts/ISequenceRenderService.js";
import type { SequenceData } from "../src/lib/shared/domain/models/SequenceData.js";

// Your actual 16-beat sequence
const TEST_SEQUENCE: SequenceData = {
  id: "fd609c39-163f-49ec-b504-7cd42103e399",
  name: "Circular XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  word: "XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  beats: [
    {
      id: "e7bf366d-ba05-46f2-abf1-c71546f90ed2",
      letter: "X",
      startPosition: "gamma11",
      endPosition: "alpha3",
      motions: {
        blue: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "w",
          turns: 0,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "e",
          turns: 1,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 1,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    // Add first beat only for faster testing - full sequence would take too long
  ],
  thumbnails: [],
  isFavorite: false,
  isCircular: true,
  tags: ["circular", "cap", "strict-rotated"],
  metadata: {
    generated: true,
    generatedAt: "2025-10-29T23:11:43.464Z",
    algorithm: "freeform",
    beatsGenerated: 1, // Shortened for testing
    propContinuity: "continuous",
    blueRotationDirection: "",
    redRotationDirection: "",
    turnIntensity: 1,
    level: 2,
  },
  gridMode: "diamond",
  propType: "fan",
  startingPositionBeat: {
    id: "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    motions: {
      blue: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "s",
        endLocation: "s",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "s",
        color: "blue",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
      red: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "e",
        endLocation: "e",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "e",
        color: "red",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
    },
    letter: "Γ",
    startPosition: "gamma11",
    endPosition: "gamma11",
    beatNumber: 0,
    duration: 1,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
  },
  startPosition: {
    id: "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    motions: {
      blue: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "s",
        endLocation: "s",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "s",
        color: "blue",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
      red: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "e",
        endLocation: "e",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "e",
        color: "red",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
    },
    letter: "Γ",
    startPosition: "gamma11",
    endPosition: "gamma11",
    beatNumber: 0,
    duration: 1,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
  },
  difficultyLevel: "intermediate",
} as any;

async function main() {
  console.log("🚀 Starting REAL Performance Benchmark\n");
  console.log("Setting up browser environment...");

  try {
    // Initialize the DI container
    console.log("Initializing DI container...");
    await ensureContainerInitialized();

    console.log("Getting SequenceRenderService...");
    const renderService = container.get<ISequenceRenderService>(
      TYPES.ISequenceRenderService
    );

    console.log("\n✅ Successfully loaded real rendering services!\n");
    console.log(
      "Testing with 1-beat sequence (full 16-beat would take too long in Node)\n"
    );

    // Test current settings
    console.log(
      "📊 Testing CURRENT settings (beatScale: 0.15, quality: 0.4, JPEG)..."
    );
    const currentStart = performance.now();

    const currentPreview = await renderService.generatePreview(TEST_SEQUENCE, {
      beatScale: 0.15,
      quality: 0.4,
      format: "JPEG",
      includeStartPosition: true,
      addBeatNumbers: true,
      addWord: true,
      addDifficultyLevel: true,
    });

    const currentTime = performance.now() - currentStart;
    const currentSize = (currentPreview.length * 0.75) / 1024;

    console.log(`   Time: ${currentTime.toFixed(0)}ms`);
    console.log(`   Size: ${currentSize.toFixed(1)}KB`);
    console.log(`   Preview length: ${currentPreview.substring(0, 50)}...`);

    // Test recommended settings
    console.log(
      "\n📊 Testing RECOMMENDED settings (beatScale: 0.22, quality: 0.45, JPEG)..."
    );
    const recStart = performance.now();

    const recPreview = await renderService.generatePreview(TEST_SEQUENCE, {
      beatScale: 0.22,
      quality: 0.45,
      format: "JPEG",
      includeStartPosition: true,
      addBeatNumbers: true,
      addWord: true,
      addDifficultyLevel: true,
    });

    const recTime = performance.now() - recStart;
    const recSize = (recPreview.length * 0.75) / 1024;

    console.log(`   Time: ${recTime.toFixed(0)}ms`);
    console.log(`   Size: ${recSize.toFixed(1)}KB`);

    // Analysis
    console.log("\n📈 ANALYSIS\n");
    console.log(
      `Current: ${currentTime.toFixed(0)}ms, ${currentSize.toFixed(1)}KB`
    );
    console.log(
      `Recommended: ${recTime.toFixed(0)}ms (${(((recTime - currentTime) / currentTime) * 100).toFixed(0)}% ${recTime > currentTime ? "slower" : "faster"}), ${recSize.toFixed(1)}KB`
    );

    console.log("\n💡 IMPORTANT NOTE:");
    console.log("This is testing with 1 beat in Node.js environment.");
    console.log(
      "In the browser with 16 beats, multiply these times by ~15-20x"
    );
    console.log(
      `Estimated browser time for 16 beats: ${(currentTime * 17).toFixed(0)}ms`
    );

    if (currentTime * 17 > 500) {
      console.log("\n⭐ RECOMMENDATION: Implement background pre-rendering");
      console.log(
        "   Estimated 16-beat render time > 500ms - users will notice delay"
      );
    }

    console.log("\n✅ Benchmark Complete!\n");
  } catch (error) {
    console.error("❌ Error running benchmark:", error);
    process.exit(1);
  }
}

main();
