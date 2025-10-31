#!/usr/bin/env node

/**
 * Modern Metadata Extraction Tool (2025)
 *
 * Extracts metadata from PNG files and creates clean JSON sidecar files.
 * This is the MODERN approach - no more messing with image EXIF!
 *
 * Creates: filename.meta.json alongside each image
 * Benefits: Fast, reliable, debuggable, no size limits
 */

import { promises as fs } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  sourceDir: path.join(__dirname, "..", "..", "desktop", "data", "dictionary"),
  targetDir: path.join(__dirname, "..", "static", "Explore"),
  batchSize: 10,
};

// Statistics
const stats = {
  totalFiles: 0,
  successfulExtractions: 0,
  errors: [],
};

/**
 * Extract JSON metadata from PNG tEXt chunk
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
    console.error(
      `❌ Error extracting from ${path.basename(pngPath)}:`,
      error.message
    );
    throw error;
  }
}

/**
 * Find tEXt chunk in PNG data
 */
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

function readUint32BE(data, offset) {
  return (
    (data[offset] << 24) |
    (data[offset + 1] << 16) |
    (data[offset + 2] << 8) |
    data[offset + 3]
  );
}

function readString(data, offset, length) {
  return new TextDecoder("ascii").decode(data.slice(offset, offset + length));
}

/**
 * Create JSON sidecar file
 */
async function createMetadataSidecar(webpPath, metadata) {
  const sidecarPath = webpPath.replace(".webp", ".meta.json");

  // Add extraction metadata
  const sidecarData = {
    extractedAt: new Date().toISOString(),
    extractedBy: "extract-metadata-to-sidecars.js",
    version: "1.0",
    metadata: metadata,
  };

  await fs.writeFile(sidecarPath, JSON.stringify(sidecarData, null, 2), "utf8");
  console.log(`✅ Created sidecar: ${path.basename(sidecarPath)}`);
}

/**
 * Map PNG path to WebP path
 */
function mapPngToWebpPath(pngPath) {
  const relativeToDictionary = path.relative(CONFIG.sourceDir, pngPath);
  const webpRelativePath = relativeToDictionary.replace(".png", ".webp");
  return path.join(CONFIG.targetDir, webpRelativePath);
}

/**
 * Get all PNG files that have corresponding WebP files
 */
async function getPngWebpPairs() {
  const pairs = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        if (entry.isDirectory()) {
          await scan(fullPath);
        } else if (entry.isFile() && entry.name.endsWith(".png")) {
          const webpPath = mapPngToWebpPath(fullPath);

          try {
            await fs.access(webpPath);
            pairs.push({ png: fullPath, webp: webpPath });
          } catch {
            // WebP doesn't exist, skip
          }
        }
      }
    } catch (error) {
      console.error(`Error scanning ${currentDir}:`, error.message);
    }
  }

  await scan(CONFIG.sourceDir);
  return pairs;
}

/**
 * Process files in batches
 */
async function processBatch(pairs, startIndex) {
  const batch = pairs.slice(startIndex, startIndex + CONFIG.batchSize);

  for (const { png, webp } of batch) {
    try {
      stats.totalFiles++;

      // Extract metadata from PNG
      const metadata = await extractPngMetadata(png);

      // Create JSON sidecar
      await createMetadataSidecar(webp, metadata);

      stats.successfulExtractions++;
    } catch (error) {
      stats.errors.push({ file: path.basename(png), error: error.message });
    }
  }
}

/**
 * Main extraction function
 */
async function extractAllMetadataToSidecars() {
  console.log("🚀 Extracting metadata to modern JSON sidecar files...\n");

  const pairs = await getPngWebpPairs();

  if (pairs.length === 0) {
    console.log("ℹ️  No PNG/WebP pairs found.");
    return;
  }

  console.log(`📊 Found ${pairs.length} PNG/WebP pairs to process\n`);

  const startTime = Date.now();

  // Process in batches
  for (let i = 0; i < pairs.length; i += CONFIG.batchSize) {
    const batchNumber = Math.floor(i / CONFIG.batchSize) + 1;
    const totalBatches = Math.ceil(pairs.length / CONFIG.batchSize);

    console.log(`🔄 Processing batch ${batchNumber}/${totalBatches}...`);
    await processBatch(pairs, i);
  }

  const endTime = Date.now();
  const duration = ((endTime - startTime) / 1000).toFixed(1);

  // Print results
  console.log("\n🎉 Modern metadata extraction completed!\n");
  console.log("📈 EXTRACTION STATISTICS:");
  console.log(`   Total files processed: ${stats.totalFiles}`);
  console.log(`   Successful extractions: ${stats.successfulExtractions}`);
  console.log(`   Errors: ${stats.errors.length}`);
  console.log(`   Processing time: ${duration}s\n`);

  const successRate = (
    (stats.successfulExtractions / stats.totalFiles) *
    100
  ).toFixed(1);
  console.log(`✅ SUCCESS RATE: ${successRate}%\n`);

  if (stats.errors.length > 0) {
    console.log("⚠️  ERRORS:");
    stats.errors.forEach(({ file, error }) => {
      console.log(`   ${file}: ${error}`);
    });
  }

  if (
    stats.successfulExtractions === stats.totalFiles &&
    stats.totalFiles > 0
  ) {
    console.log(
      "🏆 100% SUCCESS! All metadata extracted to clean JSON sidecar files!"
    );
    console.log(
      "🎯 No more EXIF headaches - just clean, fast, reliable JSON files!"
    );
  }
}

// Run the extraction
extractAllMetadataToSidecars().catch((error) => {
  console.error("💥 Fatal error:", error);
  process.exit(1);
});
