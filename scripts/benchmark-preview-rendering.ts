/**
 * Standalone Benchmark Script for Sequence Preview Rendering
 *
 * Run this script to get immediate performance metrics:
 * npx tsx scripts/benchmark-preview-rendering.ts
 */

import { container } from "../src/lib/shared/inversify/container";
import { TYPES } from "../src/lib/shared/inversify/types";
import type { ISequenceRenderService } from "../src/lib/shared/render";
import type { SequenceData } from "../src/lib/shared";

// Test sequence (simplified for this benchmark)
const SIMPLE_SEQUENCE: Partial<SequenceData> = {
  id: "benchmark-test",
  name: "Test Sequence",
  word: "TEST",
  beats: Array(16)
    .fill(null)
    .map((_, i) => ({
      id: `beat-${i}`,
      letter: i % 2 === 0 ? "X" : "Δ",
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
      beatNumber: i + 1,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    })),
  startingPositionBeat: {
    id: "start",
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
    id: "start",
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
} as SequenceData;

interface BenchmarkResult {
  config: string;
  avgTime: number;
  minTime: number;
  maxTime: number;
  sizeKB: number;
}

async function benchmark(
  renderService: ISequenceRenderService,
  config: {
    beatScale: number;
    quality: number;
    format: "PNG" | "JPEG" | "WebP";
  },
  runs = 5
): Promise<BenchmarkResult> {
  const times: number[] = [];
  let dataUrl = "";

  for (let i = 0; i < runs; i++) {
    const start = performance.now();

    dataUrl = await renderService.generatePreview(SIMPLE_SEQUENCE, {
      beatScale: config.beatScale,
      quality: config.quality,
      format: config.format,
      includeStartPosition: true,
      addBeatNumbers: true,
      addWord: true,
      addDifficultyLevel: true,
    });

    const end = performance.now();
    times.push(end - start);
  }

  const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
  const minTime = Math.min(...times);
  const maxTime = Math.max(...times);
  const sizeKB = (dataUrl.length * 0.75) / 1024;

  return {
    config: `scale=${config.beatScale}, q=${config.quality}, ${config.format}`,
    avgTime,
    minTime,
    maxTime,
    sizeKB,
  };
}

async function main() {
  console.log("🚀 Starting Sequence Preview Rendering Benchmark\n");

  const renderService = container.get<ISequenceRenderService>(
    TYPES.ISequenceRenderService
  );

  // Test configurations
  const configs = [
    // Current settings
    {
      beatScale: 0.15,
      quality: 0.4,
      format: "JPEG" as const,
      name: "CURRENT (Share Preview)",
    },

    // Potential optimizations
    {
      beatScale: 0.12,
      quality: 0.4,
      format: "JPEG" as const,
      name: "Lower Scale",
    },
    {
      beatScale: 0.15,
      quality: 0.3,
      format: "JPEG" as const,
      name: "Lower Quality",
    },
    {
      beatScale: 0.1,
      quality: 0.3,
      format: "JPEG" as const,
      name: "Aggressive Optimization",
    },
    {
      beatScale: 0.08,
      quality: 0.2,
      format: "JPEG" as const,
      name: "Ultra Low",
    },

    // Format comparison
    {
      beatScale: 0.15,
      quality: 0.4,
      format: "PNG" as const,
      name: "PNG Format",
    },
    {
      beatScale: 0.15,
      quality: 0.4,
      format: "WebP" as const,
      name: "WebP Format",
    },

    // Higher quality for comparison
    {
      beatScale: 0.2,
      quality: 0.6,
      format: "JPEG" as const,
      name: "Higher Quality",
    },
  ];

  const results: (BenchmarkResult & { name: string })[] = [];

  for (const config of configs) {
    console.log(`Testing: ${config.name}...`);
    const result = await benchmark(renderService, config);
    results.push({ ...result, name: config.name });
  }

  // Print results table
  console.log("\n📊 BENCHMARK RESULTS\n");
  console.log(
    "┌─────────────────────────────┬──────────┬──────────┬──────────┬──────────┐"
  );
  console.log(
    "│ Configuration               │ Avg (ms) │ Min (ms) │ Max (ms) │ Size (KB)│"
  );
  console.log(
    "├─────────────────────────────┼──────────┼──────────┼──────────┼──────────┤"
  );

  results.forEach((result) => {
    const name = result.name.padEnd(27);
    const avg = result.avgTime.toFixed(0).padStart(8);
    const min = result.minTime.toFixed(0).padStart(8);
    const max = result.maxTime.toFixed(0).padStart(8);
    const size = result.sizeKB.toFixed(1).padStart(8);

    console.log(`│ ${name} │ ${avg} │ ${min} │ ${max} │ ${size} │`);
  });

  console.log(
    "└─────────────────────────────┴──────────┴──────────┴──────────┴──────────┘"
  );

  // Analysis
  console.log("\n📈 ANALYSIS\n");

  const current = results[0];
  const fastest = results.reduce((prev, curr) =>
    curr.avgTime < prev.avgTime ? curr : prev
  );
  const smallest = results.reduce((prev, curr) =>
    curr.sizeKB < prev.sizeKB ? curr : prev
  );

  console.log(
    `Current Settings: ${current.avgTime.toFixed(0)}ms, ${current.sizeKB.toFixed(1)}KB`
  );
  console.log(
    `Fastest Config: ${fastest.name} - ${fastest.avgTime.toFixed(0)}ms (${(((current.avgTime - fastest.avgTime) / current.avgTime) * 100).toFixed(1)}% faster)`
  );
  console.log(
    `Smallest Size: ${smallest.name} - ${smallest.sizeKB.toFixed(1)}KB (${(((current.sizeKB - smallest.sizeKB) / current.sizeKB) * 100).toFixed(1)}% smaller)`
  );

  // Recommendations
  console.log("\n💡 RECOMMENDATIONS\n");

  if (fastest.avgTime < current.avgTime * 0.7) {
    console.log(
      `✅ RECOMMENDATION: Switch to "${fastest.name}" for ${(((current.avgTime - fastest.avgTime) / current.avgTime) * 100).toFixed(0)}% faster rendering`
    );
  } else {
    console.log("✅ Current settings are already well-optimized");
  }

  if (current.avgTime > 1000) {
    console.log(
      "⚠️  WARNING: Preview generation takes >1s - consider background pre-rendering"
    );
  } else if (current.avgTime > 500) {
    console.log(
      "⚠️  WARNING: Preview generation takes >500ms - users may notice delay"
    );
  } else {
    console.log("✅ Preview generation time is acceptable for real-time use");
  }

  if (current.sizeKB > 200) {
    console.log(
      "⚠️  WARNING: Preview size is >200KB - may be slow on poor connections"
    );
  } else {
    console.log("✅ Preview size is acceptable for phone screens");
  }

  console.log("\n🎯 OPTIMIZATION STRATEGIES:\n");
  console.log(
    "1. Background Pre-rendering: Generate preview when sequence is opened, not when share button is clicked"
  );
  console.log(
    "2. Caching: Cache generated previews in memory to avoid regeneration"
  );
  console.log(
    "3. Progressive Loading: Show a low-quality placeholder immediately, then enhance"
  );
  console.log(
    "4. Lazy Generation: Only generate preview when share panel is actually opened"
  );
  console.log(
    "5. Web Workers: Move rendering to a background thread (if supported by your rendering library)"
  );

  console.log("\n✅ Benchmark Complete!\n");
}

// Run if executed directly (ES module compatible)
const isMainModule =
  import.meta.url === `file://${process.argv[1].replace(/\\/g, "/")}`;
if (isMainModule) {
  main().catch(console.error);
}

export { benchmark, main };
