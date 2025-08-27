/**
 * Validate sequence-index.json to ensure no fake sequences exist
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function validateSequenceIndex() {
  console.log("🔍 Validating sequence-index.json...");

  try {
    const indexPath = path.join(__dirname, "static", "sequence-index.json");
    const indexData = JSON.parse(fs.readFileSync(indexPath, "utf8"));

    console.log(
      `📦 Found ${indexData.totalSequences} total sequences in index`
    );
    console.log(
      `📦 Sequences array length: ${indexData.sequences?.length || 0}`
    );

    // Check for fake Greek letter sequences
    const fakeSequences = [
      "ALPHA",
      "BETA",
      "GAMMA",
      "DELTA",
      "EPSILON",
      "ZETA",
      "ETA",
      "THETA",
      "IOTA",
      "KAPPA",
      "LAMBDA",
      "MU",
      "NU",
      "XI",
      "OMICRON",
      "PI",
      "RHO",
      "SIGMA",
    ];
    const foundFakeSequences = indexData.sequences.filter((seq) =>
      fakeSequences.includes(seq.word)
    );

    if (foundFakeSequences.length > 0) {
      console.error(
        "❌ Found fake sequences in index:",
        foundFakeSequences.map((s) => s.word)
      );
      return false;
    } else {
      console.log("✅ No fake Greek letter sequences found in index");
    }

    // Check for some real sequences
    const realSequences = ["A", "AABB", "AAKE", "AB", "ABC"];
    const foundRealSequences = indexData.sequences.filter((seq) =>
      realSequences.includes(seq.word)
    );

    console.log(
      `✅ Found ${foundRealSequences.length} expected real sequences`
    );
    console.log(
      "Real sequences found:",
      foundRealSequences.map((s) => s.word)
    );

    // Show first 10 sequences
    console.log("📋 First 10 sequences in index:");
    indexData.sequences.slice(0, 10).forEach((seq, index) => {
      console.log(
        `  ${index + 1}. ${seq.word} (${seq.thumbnails?.[0] || "no thumbnail"})`
      );
    });

    console.log("✅ Sequence index validation completed successfully");
    return true;
  } catch (error) {
    console.error("❌ Sequence index validation failed:", error);
    return false;
  }
}

// Run the validation
validateSequenceIndex();
