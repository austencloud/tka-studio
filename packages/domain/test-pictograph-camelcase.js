import { compileFromFile } from "json-schema-to-typescript";
import { writeFileSync } from "fs";

function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function convertSnakeCaseToCamelCase(typescript) {
  return typescript.replace(
    /^(\s+)([a-z][a-z0-9_]*\??):(\s)/gm,
    (match, indent, propNameWithOptional, colon) => {
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

async function test() {
  try {
    console.log("🔄 Testing pictograph camelCase generation...");
    let typescript = await compileFromFile("schemas/pictograph-data.json", {
      style: { singleQuote: true, semi: true }
    });
    
    console.log("📋 Before camelCase conversion:");
    const beforeLines = typescript.split('\n');
    const beforeStart = beforeLines.findIndex(line => line.includes('start_pos'));
    if (beforeStart !== -1) {
      console.log(beforeLines[beforeStart]);
    }
    
    // Post-process to convert snake_case to camelCase
    typescript = convertSnakeCaseToCamelCase(typescript);
    
    console.log("📋 After camelCase conversion:");
    const afterLines = typescript.split('\n');
    const afterStart = afterLines.findIndex(line => line.includes('startPos'));
    if (afterStart !== -1) {
      console.log(afterLines[afterStart]);
    }
    
    writeFileSync("generated/typescript/pictograph-data.ts", typescript);
    console.log("✅ Generated pictograph-data.ts with camelCase");
    
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

test();
