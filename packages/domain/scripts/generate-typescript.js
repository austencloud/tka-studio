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
 * Post-process generated TypeScript to convert property names to camelCase
 */
function convertSnakeCaseToCamelCase(typescript) {
  // Convert property names in interface definitions
  // Pattern: "  property_name:" -> "  propertyName:"
  // Also handle optional properties: "  property_name?:" -> "  propertyName?:"
  return typescript.replace(
    /^(\s+)([a-z][a-z0-9_]*\??):(\s)/gm,
    (match, indent, propNameWithOptional, colon) => {
      // Check if property is optional
      const isOptional = propNameWithOptional.endsWith("?");
      const propName = isOptional
        ? propNameWithOptional.slice(0, -1)
        : propNameWithOptional;
      const camelCaseName = toCamelCase(propName);
      const optionalSuffix = isOptional ? "?" : "";
      return `${indent}${camelCaseName}${optionalSuffix}:${colon}`;
    }
  );
}

/**
 * Generate TypeScript from a schema file
 */
async function generateTypeScript(schemaPath, outputPath) {
  console.log(`🔄 Generating TypeScript from ${schemaPath}...`);

  try {
    // Generate TypeScript first
    let typescript = await compileFromFile(schemaPath, {
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

    // Post-process to convert snake_case to camelCase
    typescript = convertSnakeCaseToCamelCase(typescript);

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
