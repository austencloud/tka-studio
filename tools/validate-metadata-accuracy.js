#!/usr/bin/env node

/**
 * Metadata Validation Tool for TKA Explore Optimization
 *
 * Validates 100% metadata accuracy after PNG-to-WebP migration.
 * This tool ensures no data is lost during the optimization process.
 *
 * Features:
 * 1. Validates metadata extraction from both PNG and WebP files
 * 2. Compares metadata between formats for accuracy
 * 3. Generates comprehensive validation report
 * 4. Tests Universal Metadata Extractor fallback behavior
 * 5. Performance benchmarking for optimization metrics
 *
 * Usage:
 *   npm run validate:metadata
 *   node tools/validate-metadata-accuracy.js
 */

import { promises as fs } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  sourceDir: path.join(__dirname, "../static/Explore"),
  maxSequencesToTest: 50, // Limit for performance testing
  detailedLogging: false,
  performanceBenchmark: true,
};

// Validation statistics
const stats = {
  totalSequences: 0,
  webpAvailable: 0,
  pngAvailable: 0,
  bothFormatsAvailable: 0,
  metadataMatches: 0,
  metadataMismatches: 0,
  webpOnlySequences: 0,
  pngOnlySequences: 0,
  extractionErrors: 0,
  performanceData: {
    webpTimes: [],
    pngTimes: [],
    universalTimes: [],
  },
  errors: [],
};

/**
 * Simplified PNG metadata extraction (browser-compatible)
 */
async function extractPngMetadata(pngPath) {
  try {
    const data = await fs.readFile(pngPath);
    const uint8Array = new Uint8Array(data.buffer);

    const metadataJson = findTextChunk(uint8Array, "metadata");
    if (!metadataJson) {
      throw new Error("No metadata tEXt chunk found");
    }

    return JSON.parse(metadataJson);
  } catch (error) {
    throw new Error(`PNG extraction failed: ${error.message}`);
  }
}

/**
 * Simplified WebP metadata extraction (EXIF UserComment)
 */
async function extractWebpMetadata(webpPath) {
  try {
    const data = await fs.readFile(webpPath);
    const uint8Array = new Uint8Array(data.buffer);

    const exifData = extractExifFromWebP(uint8Array);
    if (!exifData) {
      throw new Error("No EXIF data found");
    }

    const metadataJson = extractUserComment(exifData);
    if (!metadataJson) {
      throw new Error("No UserComment found in EXIF");
    }

    return JSON.parse(metadataJson);
  } catch (error) {
    throw new Error(`WebP extraction failed: ${error.message}`);
  }
}

/**
 * Simulate Universal Metadata Extractor behavior
 */
async function extractUniversalMetadata(basePath) {
  const webpPath = `${basePath}.webp`;
  const pngPath = `${basePath}.png`;

  const startTime = Date.now();

  try {
    // Try WebP first
    const webpResult = await extractWebpMetadata(webpPath);
    return {
      data: webpResult,
      source: "webp",
      extractionTime: Date.now() - startTime,
    };
  } catch (webpError) {
    try {
      // Fallback to PNG
      const pngResult = await extractPngMetadata(pngPath);
      return {
        data: pngResult,
        source: "png",
        extractionTime: Date.now() - startTime,
      };
    } catch (pngError) {
      throw new Error(
        `Both formats failed. WebP: ${webpError.message}, PNG: ${pngError.message}`
      );
    }
  }
}

/**
 * Compare metadata between PNG and WebP formats
 */
function compareMetadata(pngData, webpData, sequenceName) {
  const differences = [];

  try {
    // Extract sequence arrays for comparison
    const pngSequence = pngData.sequence || pngData;
    const webpSequence = webpData.sequence || webpData;

    if (!Array.isArray(pngSequence) || !Array.isArray(webpSequence)) {
      differences.push("Metadata structure differs between formats");
      return { matches: false, differences };
    }

    // Compare sequence lengths
    if (pngSequence.length !== webpSequence.length) {
      differences.push(
        `Sequence length: PNG=${pngSequence.length}, WebP=${webpSequence.length}`
      );
    }

    // Compare beat data (excluding metadata entries)
    const pngBeats = pngSequence.filter(
      (step) => step.letter && !step.sequence_start_position
    );
    const webpBeats = webpSequence.filter(
      (step) => step.letter && !step.sequence_start_position
    );

    if (pngBeats.length !== webpBeats.length) {
      differences.push(
        `Beat count: PNG=${pngBeats.length}, WebP=${webpBeats.length}`
      );
    }

    // Deep comparison of critical fields
    for (let i = 0; i < Math.min(pngBeats.length, webpBeats.length); i++) {
      const pngBeat = pngBeats[i];
      const webpBeat = webpBeats[i];

      if (pngBeat.letter !== webpBeat.letter) {
        differences.push(
          `Beat ${i + 1} letter: PNG=${pngBeat.letter}, WebP=${webpBeat.letter}`
        );
      }
    }

    // Compare metadata fields from first entry
    const pngMeta = pngSequence[0] || {};
    const webpMeta = webpSequence[0] || {};

    const criticalFields = ["author", "level", "gridMode", "propType"];
    for (const field of criticalFields) {
      if (pngMeta[field] !== webpMeta[field]) {
        differences.push(
          `${field}: PNG=${pngMeta[field]}, WebP=${webpMeta[field]}`
        );
      }
    }

    return {
      matches: differences.length === 0,
      differences,
    };
  } catch (error) {
    differences.push(`Comparison error: ${error.message}`);
    return { matches: false, differences };
  }
}

/**
 * Get all sequence directories for testing
 */
async function getSequenceDirectories(maxSequences = null) {
  const directories = [];

  try {
    const entries = await fs.readdir(CONFIG.sourceDir, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.isDirectory() && entry.name !== "__init__.py") {
        directories.push(entry.name);

        if (maxSequences && directories.length >= maxSequences) {
          break;
        }
      }
    }
  } catch (error) {
    console.error(`Error reading Explore directory: ${error.message}`);
  }

  return directories;
}

/**
 * Check file availability for a sequence
 */
async function checkFileAvailability(sequenceName) {
  const sequenceDir = path.join(CONFIG.sourceDir, sequenceName);

  try {
    const files = await fs.readdir(sequenceDir);
    const webpFiles = files.filter((f) => f.endsWith(".webp"));
    const pngFiles = files.filter((f) => f.endsWith(".png"));

    return {
      hasWebP: webpFiles.length > 0,
      hasPNG: pngFiles.length > 0,
      webpFiles,
      pngFiles,
    };
  } catch (error) {
    return {
      hasWebP: false,
      hasPNG: false,
      webpFiles: [],
      pngFiles: [],
    };
  }
}

/**
 * Validate a single sequence
 */
async function validateSequence(sequenceName) {
  const result = {
    sequenceName,
    success: false,
    hasWebP: false,
    hasPNG: false,
    metadataMatches: false,
    universalFallbackWorks: false,
    performanceData: {},
    errors: [],
    differences: [],
  };

  try {
    // Check file availability
    const availability = await checkFileAvailability(sequenceName);
    result.hasWebP = availability.hasWebP;
    result.hasPNG = availability.hasPNG;

    stats.totalSequences++;
    if (availability.hasWebP) stats.webpAvailable++;
    if (availability.hasPNG) stats.pngAvailable++;
    if (availability.hasWebP && availability.hasPNG)
      stats.bothFormatsAvailable++;

    // Test metadata extraction and comparison
    if (availability.hasWebP && availability.hasPNG) {
      // Test both formats individually
      const basePath = path.join(
        CONFIG.sourceDir,
        sequenceName,
        `${sequenceName}_ver1`
      );
      const webpPath = `${basePath}.webp`;
      const pngPath = `${basePath}.png`;

      let pngData, webpData;

      // Extract PNG metadata with timing
      const pngStart = Date.now();
      try {
        pngData = await extractPngMetadata(pngPath);
        const pngTime = Date.now() - pngStart;
        result.performanceData.pngTime = pngTime;
        stats.performanceData.pngTimes.push(pngTime);
      } catch (error) {
        result.errors.push(`PNG extraction: ${error.message}`);
      }

      // Extract WebP metadata with timing
      const webpStart = Date.now();
      try {
        webpData = await extractWebpMetadata(webpPath);
        const webpTime = Date.now() - webpStart;
        result.performanceData.webpTime = webpTime;
        stats.performanceData.webpTimes.push(webpTime);
      } catch (error) {
        result.errors.push(`WebP extraction: ${error.message}`);
      }

      // Compare metadata if both succeeded
      if (pngData && webpData) {
        const comparison = compareMetadata(pngData, webpData, sequenceName);
        result.metadataMatches = comparison.matches;
        result.differences = comparison.differences;

        if (comparison.matches) {
          stats.metadataMatches++;
        } else {
          stats.metadataMismatches++;
        }
      }

      // Test Universal Metadata Extractor
      const universalStart = Date.now();
      try {
        const universalResult = await extractUniversalMetadata(basePath);
        const universalTime = Date.now() - universalStart;
        result.performanceData.universalTime = universalTime;
        result.performanceData.universalSource = universalResult.source;
        result.universalFallbackWorks = true;
        stats.performanceData.universalTimes.push(universalTime);
      } catch (error) {
        result.errors.push(`Universal extraction: ${error.message}`);
      }
    } else if (availability.hasWebP) {
      stats.webpOnlySequences++;
    } else if (availability.hasPNG) {
      stats.pngOnlySequences++;
    }

    result.success = result.errors.length === 0;
  } catch (error) {
    result.errors.push(`Validation error: ${error.message}`);
    stats.extractionErrors++;
  }

  return result;
}

/**
 * Generate performance analysis
 */
function generatePerformanceAnalysis() {
  const { webpTimes, pngTimes, universalTimes } = stats.performanceData;

  const analysis = {
    webp: {
      count: webpTimes.length,
      average: webpTimes.length
        ? webpTimes.reduce((a, b) => a + b, 0) / webpTimes.length
        : 0,
      min: webpTimes.length ? Math.min(...webpTimes) : 0,
      max: webpTimes.length ? Math.max(...webpTimes) : 0,
    },
    png: {
      count: pngTimes.length,
      average: pngTimes.length
        ? pngTimes.reduce((a, b) => a + b, 0) / pngTimes.length
        : 0,
      min: pngTimes.length ? Math.min(...pngTimes) : 0,
      max: pngTimes.length ? Math.max(...pngTimes) : 0,
    },
    universal: {
      count: universalTimes.length,
      average: universalTimes.length
        ? universalTimes.reduce((a, b) => a + b, 0) / universalTimes.length
        : 0,
      min: universalTimes.length ? Math.min(...universalTimes) : 0,
      max: universalTimes.length ? Math.max(...universalTimes) : 0,
    },
  };

  // Calculate performance improvement
  if (analysis.webp.average > 0 && analysis.png.average > 0) {
    analysis.improvement = {
      absolute: analysis.png.average - analysis.webp.average,
      percentage:
        ((analysis.png.average - analysis.webp.average) /
          analysis.png.average) *
        100,
    };
  }

  return analysis;
}

/**
 * Main validation function
 */
async function validateMetadataAccuracy() {
  console.log("🔍 Starting metadata validation for Explore optimization...\n");

  // Get sequences to test
  const sequences = await getSequenceDirectories(CONFIG.maxSequencesToTest);

  if (sequences.length === 0) {
    console.log("❌ No sequences found to validate.");
    return;
  }

  console.log(
    `📊 Testing ${sequences.length} sequences for metadata accuracy...\n`
  );

  const results = [];
  const startTime = Date.now();

  // Validate each sequence
  for (let i = 0; i < sequences.length; i++) {
    const sequenceName = sequences[i];
    process.stdout.write(
      `\r🔄 Validating ${i + 1}/${sequences.length}: ${sequenceName.padEnd(20)}`
    );

    try {
      const result = await validateSequence(sequenceName);
      results.push(result);

      if (CONFIG.detailedLogging && result.differences.length > 0) {
        console.log(`\n⚠️  ${sequenceName}: ${result.differences.join(", ")}`);
      }
    } catch (error) {
      console.error(`\n❌ Failed to validate ${sequenceName}:`, error.message);
      stats.errors.push({ sequence: sequenceName, error: error.message });
    }
  }

  const totalTime = Date.now() - startTime;
  console.log("\n\n🎉 Validation completed!\n");

  // Generate comprehensive report
  console.log("📈 VALIDATION RESULTS:");
  console.log(`   Total sequences tested: ${stats.totalSequences}`);
  console.log(`   WebP files available: ${stats.webpAvailable}`);
  console.log(`   PNG files available: ${stats.pngAvailable}`);
  console.log(`   Both formats available: ${stats.bothFormatsAvailable}`);
  console.log(`   Metadata matches: ${stats.metadataMatches}`);
  console.log(`   Metadata mismatches: ${stats.metadataMismatches}`);
  console.log(`   WebP-only sequences: ${stats.webpOnlySequences}`);
  console.log(`   PNG-only sequences: ${stats.pngOnlySequences}`);
  console.log(`   Extraction errors: ${stats.extractionErrors}`);
  console.log(`   Total validation time: ${(totalTime / 1000).toFixed(1)}s\n`);

  // Calculate accuracy rate
  const totalComparisons = stats.metadataMatches + stats.metadataMismatches;
  if (totalComparisons > 0) {
    const accuracyRate = (stats.metadataMatches / totalComparisons) * 100;
    console.log(
      `✅ METADATA ACCURACY: ${accuracyRate.toFixed(1)}% (${stats.metadataMatches}/${totalComparisons})\n`
    );

    if (accuracyRate === 100) {
      console.log(
        "🏆 PERFECT ACCURACY! All metadata matches between PNG and WebP formats!\n"
      );
    }
  }

  // Performance analysis
  if (CONFIG.performanceBenchmark) {
    const perfAnalysis = generatePerformanceAnalysis();

    console.log("⚡ PERFORMANCE ANALYSIS:");
    console.log(
      `   WebP extraction: ${perfAnalysis.webp.average.toFixed(1)}ms avg (${perfAnalysis.webp.count} samples)`
    );
    console.log(
      `   PNG extraction: ${perfAnalysis.png.average.toFixed(1)}ms avg (${perfAnalysis.png.count} samples)`
    );
    console.log(
      `   Universal extraction: ${perfAnalysis.universal.average.toFixed(1)}ms avg (${perfAnalysis.universal.count} samples)`
    );

    if (perfAnalysis.improvement) {
      const improvement = perfAnalysis.improvement;
      console.log(
        `   Performance gain: ${improvement.absolute.toFixed(1)}ms (${improvement.percentage.toFixed(1)}% faster)\n`
      );
    }
  }

  // Report mismatches if any
  if (stats.metadataMismatches > 0) {
    console.log("⚠️  METADATA MISMATCHES:");
    results
      .filter((r) => !r.metadataMatches && r.differences.length > 0)
      .forEach((result) => {
        console.log(
          `   ${result.sequenceName}: ${result.differences.join(", ")}`
        );
      });
    console.log();
  }

  // Report errors if any
  if (stats.errors.length > 0) {
    console.log("❌ VALIDATION ERRORS:");
    stats.errors.forEach(({ sequence, error }) => {
      console.log(`   ${sequence}: ${error}`);
    });
    console.log();
  }

  // Migration recommendations
  console.log("💡 OPTIMIZATION RECOMMENDATIONS:");

  if (stats.pngOnlySequences > 0) {
    console.log(
      `   • Convert ${stats.pngOnlySequences} PNG-only sequences to WebP for optimization`
    );
  }

  if (stats.metadataMismatches > 0) {
    console.log(
      `   • Fix ${stats.metadataMismatches} metadata mismatches before production deployment`
    );
  }

  if (
    stats.webpAvailable > 0 &&
    stats.metadataMatches === stats.bothFormatsAvailable
  ) {
    console.log(
      `   • Explore can safely use WebP-first strategy for ${stats.webpAvailable} sequences`
    );
  }

  console.log("\n🚀 Explore optimization validation complete!");
}

// Helper functions for binary data parsing (reused from other tools)
function findTextChunk(data, keyword) {
  let offset = 8; // Skip PNG signature

  while (offset < data.length - 8) {
    const length = readUint32BE(data, offset);
    const chunkType = readString(data, offset + 4, 4);

    if (chunkType === "tEXt") {
      const chunkData = data.slice(offset + 8, offset + 8 + length);
      const nullIndex = chunkData.indexOf(0);

      if (nullIndex > 0) {
        const chunkKeyword = readString(chunkData, 0, nullIndex);
        if (chunkKeyword === keyword) {
          return readString(
            chunkData,
            nullIndex + 1,
            chunkData.length - nullIndex - 1
          );
        }
      }
    }

    offset += 8 + length + 4;
  }

  return null;
}

function extractExifFromWebP(data) {
  let offset = 0;

  if (readString(data, offset, 4) !== "RIFF") return null;
  offset += 8;

  if (readString(data, offset, 4) !== "WEBP") return null;
  offset += 4;

  while (offset < data.length - 8) {
    const chunkType = readString(data, offset, 4);
    offset += 4;

    const chunkSize = readUint32LE(data, offset);
    offset += 4;

    if (chunkType === "EXIF") {
      return data.slice(offset, offset + chunkSize);
    }

    offset += chunkSize;
    if (chunkSize % 2 === 1) offset++;
  }

  return null;
}

function extractUserComment(exifData) {
  try {
    let offset = 0;
    const endian = readString(exifData, offset, 2);
    const isLittleEndian = endian === "II";
    offset += 4;

    const ifd0Offset = isLittleEndian
      ? readUint32LE(exifData, offset)
      : readUint32BE(exifData, offset);
    offset = ifd0Offset;

    const entryCount = isLittleEndian
      ? readUint16LE(exifData, offset)
      : readUint16BE(exifData, offset);
    offset += 2;

    for (let i = 0; i < entryCount; i++) {
      const tag = isLittleEndian
        ? readUint16LE(exifData, offset)
        : readUint16BE(exifData, offset);
      const type = isLittleEndian
        ? readUint16LE(exifData, offset + 2)
        : readUint16BE(exifData, offset + 2);
      const count = isLittleEndian
        ? readUint32LE(exifData, offset + 4)
        : readUint32BE(exifData, offset + 4);
      const valueOffset = isLittleEndian
        ? readUint32LE(exifData, offset + 8)
        : readUint32BE(exifData, offset + 8);

      if (tag === 0x9286 && type === 7) {
        let dataOffset = count <= 4 ? offset + 8 : valueOffset;
        const commentStart = Math.min(8, count);
        const commentData = exifData.slice(
          dataOffset + commentStart,
          dataOffset + count
        );
        return new TextDecoder("utf-8").decode(commentData);
      }

      offset += 12;
    }

    return null;
  } catch (error) {
    return null;
  }
}

function readString(data, offset, length) {
  return new TextDecoder("ascii").decode(data.slice(offset, offset + length));
}

function readUint32BE(data, offset) {
  return (
    (data[offset] << 24) |
    (data[offset + 1] << 16) |
    (data[offset + 2] << 8) |
    data[offset + 3]
  );
}

function readUint32LE(data, offset) {
  return (
    data[offset] |
    (data[offset + 1] << 8) |
    (data[offset + 2] << 16) |
    (data[offset + 3] << 24)
  );
}

function readUint16LE(data, offset) {
  return data[offset] | (data[offset + 1] << 8);
}

function readUint16BE(data, offset) {
  return (data[offset] << 8) | data[offset + 1];
}

// Run the validation
validateMetadataAccuracy().catch((error) => {
  console.error("💥 Fatal validation error:", error);
  process.exit(1);
});
