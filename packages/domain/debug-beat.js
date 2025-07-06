import { compileFromFile } from "json-schema-to-typescript";
import { writeFileSync } from "fs";

async function test() {
  try {
    console.log("Generating beat-data...");
    const ts = await compileFromFile("schemas/beat-data.json");
    writeFileSync("generated/typescript/beat-data.ts", ts);
    console.log("✅ Beat data generated successfully");
  } catch (error) {
    console.error("❌ Error:", error.message);
    console.error("Full error:", error);
  }
}

test();
