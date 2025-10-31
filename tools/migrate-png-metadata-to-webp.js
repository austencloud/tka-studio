#!/usr/bin/env node

/**
 * PNG to WebP Metadata Migration Tool
 *
 * Migrates sequence metadata from PNG tEXt chunks to WebP EXIF UserComment fields.
 * This tool:
 * 1. Reads existing PNG files and extracts JSON metadata from tEXt chunks
 * 2. Embeds that metadata into WebP EXIF UserComment fields
 * 3. Validates that metadata can be extracted from the new WebP files
 * 4. Provides 100% accuracy verification
 *
 * Usage:
 *   npm run migrate:metadata
 *   node tools/migrate-png-metadata-to-webp.js
 */

import { promises as fs } from "fs";
import path from "path";
import sharp from "sharp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  sourceDir: path.join(__dirname, "..", "..", "desktop", "data", "dictionary"), // Desktop PNG source
  targetDir: path.join(__dirname, "..", "static", "Explore"), // Web WebP target
  batchSize: 5, // Smaller batches for metadata operations
  validateAfterMigration: true,
  backupOriginalWebP: true,
};

// Statistics tracking
const stats = {
  totalPngFiles: 0,
  migratedFiles: 0,
  validationSuccesses: 0,
  validationFailures: 0,
  errors: [],
};

/**
 * Extract JSON metadata from PNG tEXt chunk (replicating PngMetadataExtractor logic)
 */
async function extractPngMetadata(pngPath) {
  try {
    const data = await fs.readFile(pngPath);
    const uint8Array = new Uint8Array(data.buffer);

    // Find "metadata" tEXt chunk
    const metadataJson = findTextChunk(uint8Array, "metadata");

    if (!metadataJson) {
      throw new Error("No metadata tEXt chunk found");
    }

    return JSON.parse(metadataJson);
  } catch (error) {
    console.error(
      `Error extracting PNG metadata from ${path.basename(pngPath)}:`,
      error.message
    );
    throw error;
  }
}

/**
 * Find tEXt chunk in PNG data (replicated from PngMetadataExtractor)
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

    offset += 8 + length + 4; // Length + type + data + CRC
  }

  return null;
}

/**
 * Binary reading utilities
 */
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
 * Migrate metadata from PNG to WebP using Sharp with EXIF injection
 */
async function migrateMetadataPngToWebP(pngPath, webpPath, metadata) {
  try {
    // Prepare EXIF data with UserComment containing JSON metadata
    const metadataJson = JSON.stringify(metadata);

    // For Sharp's EXIF, we need to include the character code prefix as part of the string
    // The browser extraction will handle finding the JSON within the UserComment
    const characterCodePrefix = "ASCII\x00\x00\x00"; // ASCII character code + 3 nulls
    const userCommentString = characterCodePrefix + metadataJson;

    // Create EXIF data object (Sharp expects string format for UserComment)
    const exifData = {
      IFD0: {
        UserComment: userCommentString, // Store complete UserComment as string
      },
    };

    // Check if WebP exists and backup if requested
    if (CONFIG.backupOriginalWebP) {
      try {
        await fs.access(webpPath);
        const backupPath = webpPath.replace(".webp", ".webp.backup");
        await fs.copyFile(webpPath, backupPath);
      } catch {
        // WebP doesn't exist, no backup needed
      }
    }

    // Read the PNG and convert to WebP with embedded EXIF
    await sharp(pngPath)
      .webp({
        quality: 85,
        effort: 6,
        lossless: false,
      })
      .withMetadata({
        exif: exifData, // Add our custom EXIF data
      })
      .toFile(webpPath);

    console.log(
      `✅ Migrated metadata: ${path.basename(pngPath)} → ${path.basename(webpPath)}`
    );
    stats.migratedFiles++;
  } catch (error) {
    console.error(
      `❌ Failed to migrate ${path.basename(pngPath)}:`,
      error.message
    );
    stats.errors.push({ file: pngPath, error: error.message });
    throw error;
  }
}

/**
 * Create EXIF buffer with UserComment field containing JSON metadata
 * This creates a minimal EXIF structure with just the UserComment tag
 */
function createExifWithUserComment(jsonString) {
  // EXIF data structure:
  // - TIFF header (8 bytes)
  // - IFD0 with UserComment entry (varies)

  const jsonBytes = Buffer.from(jsonString, "utf8");
  const commentBytes = Buffer.concat([
    Buffer.alloc(8, 0), // 8-byte character code (ASCII = all zeros)
    jsonBytes,
  ]);

  // Create EXIF buffer with UserComment
  const exifBuffer = Buffer.alloc(1024); // Generous size
  let offset = 0;

  // TIFF header (little endian)
  exifBuffer.write("II", offset, "ascii");
  offset += 2; // Little endian marker
  exifBuffer.writeUInt16LE(42, offset);
  offset += 2; // TIFF magic number
  exifBuffer.writeUInt32LE(8, offset);
  offset += 4; // IFD0 offset

  // IFD0
  exifBuffer.writeUInt16LE(1, offset);
  offset += 2; // Number of entries

  // UserComment entry
  exifBuffer.writeUInt16LE(0x9286, offset);
  offset += 2; // UserComment tag
  exifBuffer.writeUInt16LE(7, offset);
  offset += 2; // UNDEFINED type
  exifBuffer.writeUInt32LE(commentBytes.length, offset);
  offset += 4; // Count

  if (commentBytes.length <= 4) {
    // Data fits in value field
    commentBytes.copy(exifBuffer, offset);
    offset += 4;
  } else {
    // Data stored at offset
    const dataOffset = 8 + 2 + 12 + 4; // After IFD
    exifBuffer.writeUInt32LE(dataOffset, offset);
    offset += 4;
    commentBytes.copy(exifBuffer, dataOffset);
  }

  // Next IFD offset (none)
  exifBuffer.writeUInt32LE(0, offset);
  offset += 4;

  // Copy comment data if it's stored at offset
  if (commentBytes.length > 4) {
    const dataOffset = 8 + 2 + 12 + 4;
    commentBytes.copy(exifBuffer, dataOffset);
    offset = dataOffset + commentBytes.length;
  }

  return exifBuffer.slice(0, offset);
}

/**
 * Validate that metadata can be extracted from WebP file
 */
async function validateWebPMetadata(webpPath, originalMetadata) {
  try {
    // Use our WebpMetadataExtractor logic to validate
    const data = await fs.readFile(webpPath);
    const uint8Array = new Uint8Array(data.buffer);

    const exifData = extractExifFromWebP(uint8Array);
    if (!exifData) {
      throw new Error("No EXIF data found in WebP");
    }

    const extractedJson = extractUserComment(exifData);
    if (!extractedJson) {
      throw new Error("No UserComment found in WebP EXIF");
    }

    const extractedMetadata = JSON.parse(extractedJson);

    // Compare critical fields
    const original = originalMetadata.sequence || originalMetadata;
    const extracted = extractedMetadata.sequence || extractedMetadata;

    if (Array.isArray(original) && Array.isArray(extracted)) {
      if (JSON.stringify(original) === JSON.stringify(extracted)) {
        stats.validationSuccesses++;
        return true;
      }
    }

    throw new Error("Metadata mismatch after extraction");
  } catch (error) {
    console.error(
      `❌ Validation failed for ${path.basename(webpPath)}:`,
      error.message
    );
    stats.validationFailures++;
    stats.errors.push({
      file: webpPath,
      error: `Validation: ${error.message}`,
    });
    return false;
  }
}

/**
 * Extract EXIF from WebP (simplified version of WebpMetadataExtractor)
 */
function extractExifFromWebP(data) {
  let offset = 0;

  if (readString(data, offset, 4) !== "RIFF") return null;
  offset += 8; // Skip RIFF header and size

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

function readUint32LE(data, offset) {
  return (
    data[offset] |
    (data[offset + 1] << 8) |
    (data[offset + 2] << 16) |
    (data[offset + 3] << 24)
  );
}

/**
 * Extract UserComment from EXIF (fixed to handle character code prefix)
 */
function extractUserComment(exifData) {
  try {
    let offset = 0;

    // Skip to IFD0
    const endian = readString(exifData, offset, 2);
    const isLittleEndian = endian === "II";
    offset += 4; // Skip endian marker and magic

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
        // UserComment, UNDEFINED type
        let dataOffset = count <= 4 ? offset + 8 : valueOffset;
        const rawData = exifData.slice(dataOffset, dataOffset + count);

        // Find JSON start by looking for opening brace (skip character code prefix)
        let jsonStart = -1;
        for (let i = 0; i < rawData.length; i++) {
          if (rawData[i] === 123) {
            // ASCII for '{'
            jsonStart = i;
            break;
          }
        }

        if (jsonStart >= 0) {
          const jsonData = rawData.slice(jsonStart);
          return new TextDecoder("utf-8").decode(jsonData);
        }

        return null; // No JSON found
      }

      offset += 12;
    }

    return null;
  } catch (error) {
    return null;
  }
}

function readUint16LE(data, offset) {
  return data[offset] | (data[offset + 1] << 8);
}

function readUint16BE(data, offset) {
  return (data[offset] << 8) | data[offset + 1];
}

/**
 * Get all PNG/WebP file pairs for migration (cross-directory mapping)
 */
async function getPngWebpPairs(sourceDir) {
  const pairs = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        if (entry.isDirectory()) {
          await scan(fullPath);
        } else if (entry.isFile() && entry.name.endsWith(".png")) {
          // Map desktop PNG to web WebP
          const webpPath = mapPngToWebpPath(fullPath);

          try {
            await fs.access(webpPath);
            pairs.push({ png: fullPath, webp: webpPath });
            console.log(
              `✅ Found pair: ${path.basename(fullPath)} → ${path.relative(CONFIG.targetDir, webpPath)}`
            );
          } catch {
            console.log(
              `⚠️  No WebP found for ${path.basename(fullPath)} at ${path.relative(CONFIG.targetDir, webpPath)}`
            );
          }
        }
      }
    } catch (error) {
      console.error(`Error scanning ${currentDir}:`, error.message);
    }
  }

  await scan(sourceDir);
  return pairs;
}

/**
 * Map desktop PNG path to web WebP path
 */
function mapPngToWebpPath(pngPath) {
  // Extract relative path from desktop dictionary
  const relativeToDictionary = path.relative(CONFIG.sourceDir, pngPath);

  // Convert PNG to WebP filename
  const webpRelativePath = relativeToDictionary.replace(".png", ".webp");

  // Build target path in web Explore
  const webpPath = path.join(CONFIG.targetDir, webpRelativePath);

  return webpPath;
}

/**
 * Process files in batches
 */
async function processBatch(pairs, startIndex) {
  const batch = pairs.slice(startIndex, startIndex + CONFIG.batchSize);

  for (const { png, webp } of batch) {
    try {
      // Extract metadata from PNG
      const metadata = await extractPngMetadata(png);

      // Migrate to WebP
      await migrateMetadataPngToWebP(png, webp, metadata);

      // Validate if requested
      if (CONFIG.validateAfterMigration) {
        await validateWebPMetadata(webp, metadata);
      }
    } catch (error) {
      console.error(
        `❌ Failed processing ${path.basename(png)}:`,
        error.message
      );
    }
  }
}

/**
 * Main migration function
 */
async function migrateAllMetadata() {
  console.log("🚀 Starting PNG to WebP metadata migration...\n");

  // Get all PNG/WebP pairs
  console.log("📁 Scanning for PNG/WebP pairs...");
  const pairs = await getPngWebpPairs(CONFIG.sourceDir);
  stats.totalPngFiles = pairs.length;

  if (pairs.length === 0) {
    console.log("ℹ️  No PNG/WebP pairs found for migration.");
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
  console.log("\n🎉 Metadata migration completed!\n");
  console.log("📈 MIGRATION STATISTICS:");
  console.log(`   Total PNG files: ${stats.totalPngFiles}`);
  console.log(`   Successfully migrated: ${stats.migratedFiles}`);
  console.log(`   Validation successes: ${stats.validationSuccesses}`);
  console.log(`   Validation failures: ${stats.validationFailures}`);
  console.log(`   Errors: ${stats.errors.length}`);
  console.log(`   Processing time: ${duration}s\n`);

  // Calculate success rate
  const successRate = (
    (stats.validationSuccesses / stats.migratedFiles) *
    100
  ).toFixed(1);
  console.log(`✅ METADATA ACCURACY: ${successRate}% verified success rate\n`);

  if (stats.errors.length > 0) {
    console.log("⚠️  ERRORS:");
    stats.errors.forEach(({ file, error }) => {
      console.log(`   ${path.basename(file)}: ${error}`);
    });
  }

  if (
    stats.validationSuccesses === stats.migratedFiles &&
    stats.migratedFiles > 0
  ) {
    console.log(
      "🏆 100% SUCCESS! All metadata migrated and validated perfectly!"
    );
  }
}

// Run the migration
migrateAllMetadata().catch((error) => {
  console.error("💥 Fatal error:", error);
  process.exit(1);
});
