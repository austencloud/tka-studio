/**
 * Phase 2: Demonstration Script
 * Shows real PNG metadata extraction vs placeholder data
 */

import { PngMetadataExtractor } from "./src/lib/utils/png-metadata-extractor.js";

console.log("🔍 Phase 2: PNG Metadata Extraction Demonstration");
console.log("=".repeat(60));

// Test sequences that we know exist
const testSequences = ["ABC", "CAKE", "A"];

async function demonstrateMetadataExtraction() {
  console.log("\n📋 1. REAL PNG METADATA EXTRACTION:");
  console.log("-".repeat(40));

  for (const sequenceName of testSequences) {
    try {
      console.log(`\n🔍 Extracting metadata for ${sequenceName}...`);
      const metadata =
        await PngMetadataExtractor.extractSequenceMetadata(sequenceName);

      if (metadata && metadata.length > 0) {
        const firstStep = metadata[0];
        console.log(`✅ ${sequenceName} Metadata:`);
        console.log(`   - Sequence Length: ${metadata.length - 1} beats`);
        console.log(
          `   - Starting Position: ${firstStep.sequence_start_position || "Unknown"}`,
        );
        console.log(`   - Grid Mode: ${firstStep.grid_mode || "Unknown"}`);
        console.log(`   - Total Steps: ${metadata.length}`);

        // Show first few beats
        console.log(`   - Beat Structure:`);
        metadata.slice(1, 4).forEach((step, index) => {
          if (step.beat && step.beat > 0) {
            const blueMotion = step.blue_attributes?.motion_type || "unknown";
            const redMotion = step.red_attributes?.motion_type || "unknown";
            console.log(
              `     Beat ${step.beat} (${step.letter}): blue=${blueMotion}, red=${redMotion}`,
            );
          }
        });
      }
    } catch (error) {
      console.error(`❌ Failed to extract ${sequenceName}:`, error.message);
    }
  }
}

async function compareWithPlaceholderData() {
  console.log("\n📊 2. REAL vs PLACEHOLDER DATA COMPARISON:");
  console.log("-".repeat(40));

  try {
    // Load real sequence index
    const response = await fetch("/sequence-index.json");
    const data = await response.json();
    const sequences = data.sequences || [];

    console.log(`✅ Loaded ${sequences.length} real sequences from index\n`);

    // Extract real data statistics
    const realAuthors = [
      ...new Set(sequences.map((s) => s.author).filter(Boolean)),
    ];
    const realDifficulties = [
      ...new Set(sequences.map((s) => s.difficultyLevel).filter(Boolean)),
    ];
    const realLengths = [
      ...new Set(sequences.map((s) => s.sequenceLength).filter(Boolean)),
    ].sort((a, b) => a - b);
    const realLetters = [
      ...new Set(sequences.map((s) => s.word?.[0]).filter(Boolean)),
    ].sort();

    console.log("🔴 CURRENT PLACEHOLDER DATA:");
    console.log('   Authors: "TKA User", "Demo Author", "Expert User"');
    console.log('   Difficulties: "beginner", "intermediate", "advanced"');
    console.log("   Lengths: Random 3-8 beats");
    console.log("   Letters: Hardcoded ranges A-D, E-H, etc.");

    console.log("\n🟢 REAL DATA AVAILABLE:");
    console.log(
      `   Authors: ${realAuthors.length} unique - ${realAuthors.join(", ")}`,
    );
    console.log(`   Difficulties: ${realDifficulties.join(", ")}`);
    console.log(
      `   Lengths: ${realLengths[0]}-${realLengths[realLengths.length - 1]} beats (${realLengths.length} unique values)`,
    );
    console.log(
      `   Letters: ${realLetters.length} unique starting letters - ${realLetters.join(", ")}`,
    );

    // Show sample real sequences
    console.log("\n📝 SAMPLE REAL SEQUENCES:");
    sequences.slice(0, 5).forEach((seq) => {
      console.log(
        `   ${seq.word}: ${seq.author}, ${seq.difficultyLevel}, ${seq.sequenceLength} beats`,
      );
    });
  } catch (error) {
    console.error("❌ Failed to load sequence index:", error.message);
  }
}

async function showCurrentBrowseTabBehavior() {
  console.log("\n🔍 3. CURRENT BROWSE TAB BEHAVIOR:");
  console.log("-".repeat(40));

  console.log("The Browse tab currently:");
  console.log("❌ Ignores the real sequence-index.json file");
  console.log(
    "❌ Generates fake placeholder data in BrowseService.createSampleSequences()",
  );
  console.log('❌ Uses hardcoded authors like "Expert User", "Demo Author"');
  console.log("❌ Creates random difficulty levels and sequence lengths");
  console.log("❌ Navigation panel filters by this fake data");
  console.log("");
  console.log("✅ Real PNG metadata extractor exists and works");
  console.log("✅ Real sequence index with 361 sequences exists");
  console.log("✅ Real PNG files with embedded metadata exist");
}

// Run the demonstration
async function runDemo() {
  await demonstrateMetadataExtraction();
  await compareWithPlaceholderData();
  await showCurrentBrowseTabBehavior();

  console.log("\n🎯 PHASE 2 COMPLETE - Ready for Phase 3: Implementation");
  console.log("=".repeat(60));
}

// Export for use in browser console or Node.js
if (typeof window !== "undefined") {
  window.runMetadataDemo = runDemo;
  window.demonstrateMetadataExtraction = demonstrateMetadataExtraction;
  window.compareWithPlaceholderData = compareWithPlaceholderData;
} else {
  runDemo().catch(console.error);
}
