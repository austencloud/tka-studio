import { compileFromFile } from "json-schema-to-typescript";
import { writeFileSync } from "fs";

async function test() {
  try {
    console.log("Generating beat-data-simple...");
    const ts = await compileFromFile("schemas/beat-data-simple.json");
    writeFileSync("generated/typescript/beat-data-simple.ts", ts);
    console.log("✅ Beat data simple generated successfully");
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

test();
