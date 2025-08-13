/**
 * Direct PNG Metadata Extraction Test
 * Proving I can use the extractor to get real data
 */

// Test the PNG metadata extractor directly
async function testPngExtraction() {
  console.log("🔍 Testing PNG Metadata Extraction...");
  console.log("=".repeat(50));

  // Test sequences we know exist
  const testSequences = ["ABC", "CAKE", "A"];

  for (const sequenceName of testSequences) {
    try {
      console.log(`\n📋 Extracting ${sequenceName}...`);

      // Use the extractor directly
      const response = await fetch(
        `/dictionary/${sequenceName}/${sequenceName}_ver1.png`,
      );
      if (!response.ok) {
        throw new Error(`Failed to fetch PNG: ${response.status}`);
      }

      const arrayBuffer = await response.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);

      // Find the tEXt chunk with metadata
      const metadata = findTextChunk(uint8Array, "metadata");
      if (!metadata) {
        throw new Error("No metadata found in PNG");
      }

      const parsed = JSON.parse(metadata);
      const sequence = parsed.sequence || parsed;

      // Extract key information
      const firstStep = sequence[0];
      const realBeats = sequence.filter((step) => step.beat && step.beat > 0);

      console.log(`✅ ${sequenceName} Real Metadata:`);
      console.log(`   Author: "${firstStep.author}"`);
      console.log(`   Level: ${firstStep.level}`);
      console.log(`   Grid Mode: ${firstStep.grid_mode}`);
      console.log(`   Is Circular: ${firstStep.is_circular}`);
      console.log(`   Prop Type: ${firstStep.prop_type}`);
      console.log(`   Real Beat Count: ${realBeats.length}`);
      console.log(`   Total Steps: ${sequence.length}`);

      // Show first few beats
      console.log(`   Beat Structure:`);
      realBeats.slice(0, 3).forEach((step) => {
        const blueMotion = step.blue_attributes?.motion_type || "unknown";
        const redMotion = step.red_attributes?.motion_type || "unknown";
        console.log(
          `     Beat ${step.beat} (${step.letter}): blue=${blueMotion}, red=${redMotion}`,
        );
      });
    } catch (error) {
      console.error(`❌ Failed to extract ${sequenceName}:`, error.message);
    }
  }
}

// PNG parsing function (copied from the extractor)
function findTextChunk(data, keyword) {
  let offset = 8; // Skip PNG signature

  while (offset < data.length) {
    // Read chunk length (4 bytes, big-endian)
    const length =
      (data[offset] << 24) |
      (data[offset + 1] << 16) |
      (data[offset + 2] << 8) |
      data[offset + 3];
    offset += 4;

    // Read chunk type (4 bytes)
    const type = String.fromCharCode(
      data[offset],
      data[offset + 1],
      data[offset + 2],
      data[offset + 3],
    );
    offset += 4;

    if (type === "tEXt") {
      // Parse text chunk
      const textData = data.slice(offset, offset + length);
      const textString = new TextDecoder("latin1").decode(textData);
      const nullIndex = textString.indexOf("\0");

      if (nullIndex !== -1) {
        const chunkKeyword = textString.substring(0, nullIndex);
        const text = textString.substring(nullIndex + 1);

        if (chunkKeyword === keyword) {
          return text;
        }
      }
    }

    // Skip chunk data and CRC (4 bytes)
    offset += length + 4;

    // Stop at IEND chunk
    if (type === "IEND") {
      break;
    }
  }

  return null;
}

// Run the test
testPngExtraction().catch(console.error);

// Also make it available in browser console
if (typeof window !== "undefined") {
  window.testPngExtraction = testPngExtraction;
  console.log(
    "🚀 PNG extraction test loaded. Run testPngExtraction() in console.",
  );
}
