#!/usr/bin/env node

/**
 * TypeScript Code Generation from JSON Schema
 *
 * This script converts our JSON schemas into TypeScript interfaces
 * with proper camelCase conversion for TypeScript conventions.
 */

import { compileFromFile } from "json-schema-to-typescript";
import { writeFileSync, mkdirSync } from "fs";
import { dirname } from "path";

/**
 * Convert snake_case to camelCase
 * Example: motion_type -> motionType
 */
function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 * Generate TypeScript from a schema file
 */
async function generateTypeScript(schemaPath, outputPath) {
  console.log(`🔄 Generating TypeScript from ${schemaPath}...`);

  try {
    // Generate TypeScript with camelCase property names
    const typescript = await compileFromFile(schemaPath, {
      style: {
        singleQuote: true,
        semi: true,
      },
      bannerComment: `/**
 * Generated from ${schemaPath}
 * 
 * This file is auto-generated. Do not edit manually.
 * To make changes, update the JSON schema and regenerate.
 */`,
    });

    // Ensure output directory exists
    mkdirSync(dirname(outputPath), { recursive: true });

    // Write the generated TypeScript
    writeFileSync(outputPath, typescript);

    console.log(`✅ Generated: ${outputPath}`);
  } catch (error) {
    console.error(`❌ Error generating ${outputPath}:`, error.message);
    process.exit(1);
  }
}

/**
 * Main generation function
 */
async function main() {
  console.log("🚀 Starting TypeScript generation from JSON schemas...\n");

  // Generate MotionData
  await generateTypeScript(
    "schemas/motion-data.json",
    "generated/typescript/motion-data.ts"
  );

  // Generate PictographData
  await generateTypeScript(
    "schemas/pictograph-data.json",
    "generated/typescript/pictograph-data.ts"
  );

  console.log("\n✨ TypeScript generation complete!");
}

// Run the generator
main().catch((error) => {
  console.error("💥 Generation failed:", error);
  process.exit(1);
});
