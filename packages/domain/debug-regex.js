// Test the regex pattern
const testInput = `
  start_pos?:
    | null
    | 'alpha1'
  end_pos?:
    | null
    | 'beta1'
  grid_data?: {
    center_x?: number;
  } | null;
  is_start_position?: boolean;
  gridMode: 'diamond' | 'box';
`;

function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function convertSnakeCaseToCamelCase(typescript) {
  console.log("Input:");
  console.log(typescript);
  
  // Convert property names in interface definitions
  const result = typescript.replace(
    /^(\s+)([a-z][a-z0-9_]*\??):(\s)/gm,
    (match, indent, propNameWithOptional, colon) => {
      console.log(`Match: "${match}" -> propName: "${propNameWithOptional}"`);
      
      // Check if property is optional
      const isOptional = propNameWithOptional.endsWith("?");
      const propName = isOptional
        ? propNameWithOptional.slice(0, -1)
        : propNameWithOptional;
      const camelCaseName = toCamelCase(propName);
      const optionalSuffix = isOptional ? "?" : "";
      const replacement = `${indent}${camelCaseName}${optionalSuffix}:${colon}`;
      
      console.log(`  -> "${replacement}"`);
      return replacement;
    }
  );
  
  console.log("\nOutput:");
  console.log(result);
  return result;
}

convertSnakeCaseToCamelCase(testInput);
