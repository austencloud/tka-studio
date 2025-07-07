import { compileFromFile } from "json-schema-to-typescript";
import { writeFileSync } from "fs";

function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function convertSnakeCaseToCamelCase(typescript) {
  // Convert property names in interface definitions
  // Pattern: "  property_name:" -> "  propertyName:"
  return typescript.replace(
    /^(\s+)([a-z][a-z0-9_]*):(\s)/gm,
    (match, indent, propName, colon) => {
      const camelCaseName = toCamelCase(propName);
      return `${indent}${camelCaseName}:${colon}`;
    }
  );
}

async function test() {
  try {
    console.log("🔄 Testing camelCase generation...");
    let typescript = await compileFromFile("schemas/motion-data.json", {
      style: { singleQuote: true, semi: true },
    });

    // Post-process to convert snake_case to camelCase
    typescript = convertSnakeCaseToCamelCase(typescript);

    writeFileSync("generated/typescript/motion-data.ts", typescript);
    console.log("✅ Generated motion-data.ts with camelCase");

    // Show a preview of the generated interface
    const lines = typescript.split("\n");
    const interfaceStart = lines.findIndex((line) =>
      line.includes("export interface")
    );
    if (interfaceStart !== -1) {
      console.log("\n📋 Generated interface preview:");
      for (
        let i = interfaceStart;
        i < Math.min(interfaceStart + 10, lines.length);
        i++
      ) {
        console.log(lines[i]);
      }
    }
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

test();
