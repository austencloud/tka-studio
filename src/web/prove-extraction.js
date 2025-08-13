/**
 * Proof of PNG Metadata Extraction
 * Using the existing PngMetadataExtractor class
 */

// Import the existing extractor
import { PngMetadataExtractor } from "./src/lib/utils/png-metadata-extractor.js";

console.log("🔍 PROOF: I can use the PNG Metadata Extractor");
console.log("=".repeat(60));

async function proveExtraction() {
  const sequences = ["ABC", "CAKE", "A"];
  const results = [];

  for (const sequenceName of sequences) {
    try {
      console.log(
        `\n📋 Extracting ${sequenceName} using PngMetadataExtractor...`,
      );

      // Use the existing extractor class
      const metadata =
        await PngMetadataExtractor.extractSequenceMetadata(sequenceName);

      if (metadata && metadata.length > 0) {
        const firstStep = metadata[0];
        const realBeats = metadata.filter((step) => step.beat && step.beat > 0);

        const extractedData = {
          sequence: sequenceName,
          author: firstStep.author,
          level: firstStep.level,
          gridMode: firstStep.grid_mode,
          isCircular: firstStep.is_circular,
          propType: firstStep.prop_type,
          realBeatCount: realBeats.length,
          totalSteps: metadata.length,
          dateAdded: firstStep.date_added || "unknown",
        };

        results.push(extractedData);

        console.log(`✅ ${sequenceName} Extracted Data:`);
        console.log(`   Author: "${extractedData.author}"`);
        console.log(`   Level: ${extractedData.level}`);
        console.log(`   Grid Mode: ${extractedData.gridMode}`);
        console.log(`   Is Circular: ${extractedData.isCircular}`);
        console.log(`   Prop Type: ${extractedData.propType}`);
        console.log(`   Real Beat Count: ${extractedData.realBeatCount}`);
        console.log(`   Total Steps: ${extractedData.totalSteps}`);

        // Show motion types for first 3 beats
        console.log(`   Motion Types:`);
        realBeats.slice(0, 3).forEach((step) => {
          const blueMotion = step.blue_attributes?.motion_type || "unknown";
          const redMotion = step.red_attributes?.motion_type || "unknown";
          console.log(
            `     Beat ${step.beat} (${step.letter}): blue=${blueMotion}, red=${redMotion}`,
          );
        });
      } else {
        console.log(`❌ No metadata found for ${sequenceName}`);
      }
    } catch (error) {
      console.error(`❌ Failed to extract ${sequenceName}:`, error.message);
    }
  }

  console.log("\n🎯 EXTRACTION SUMMARY:");
  console.log("=".repeat(40));

  if (results.length > 0) {
    // Show unique authors found
    const uniqueAuthors = [...new Set(results.map((r) => r.author))];
    console.log(`📝 Real Authors Found: ${uniqueAuthors.join(", ")}`);

    // Show level range
    const levels = results.map((r) => r.level).filter((l) => l !== undefined);
    console.log(
      `📊 Levels Found: ${Math.min(...levels)} - ${Math.max(...levels)}`,
    );

    // Show grid modes
    const gridModes = [...new Set(results.map((r) => r.gridMode))];
    console.log(`🔲 Grid Modes: ${gridModes.join(", ")}`);

    // Show beat count range
    const beatCounts = results.map((r) => r.realBeatCount);
    console.log(
      `🎵 Beat Counts: ${Math.min(...beatCounts)} - ${Math.max(...beatCounts)}`,
    );

    console.log(
      "\n✅ PROOF COMPLETE: I can successfully extract real PNG metadata!",
    );
    console.log("🚀 Ready to implement Phase 3 using this real data.");

    return results;
  } else {
    console.log("❌ No successful extractions");
    return [];
  }
}

// Run the proof
proveExtraction()
  .then((results) => {
    console.log("\n📋 Final Results:", results);
  })
  .catch((error) => {
    console.error("❌ Proof failed:", error);
  });

// Make available for browser console
if (typeof window !== "undefined") {
  window.proveExtraction = proveExtraction;
  window.PngMetadataExtractor = PngMetadataExtractor;
}
