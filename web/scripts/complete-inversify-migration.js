/**
 * Complete InversifyJS Migration Script
 *
 * This script identifies all missing services and creates the necessary bindings
 * to complete the migration from legacy DI to InversifyJS.
 */

import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the current TYPES file to see what services are defined
function readTypesFile() {
  const typesPath = path.join(
    __dirname,
    "../src/lib/services/inversify/types.ts"
  );
  return fs.readFileSync(typesPath, "utf8");
}

// Read the current container file to see what services are bound
function readContainerFile() {
  const containerPath = path.join(
    __dirname,
    "../src/lib/services/inversify/container.ts"
  );
  return fs.readFileSync(containerPath, "utf8");
}

// Search for all service interfaces in the codebase
function findAllServiceInterfaces() {
  try {
    const result = execSync(
      'Get-ChildItem -Recurse -Include *.ts -Path src | Select-String -Pattern "interface I[A-Z].*Service|interface I[A-Z].*Repository|interface I[A-Z].*Orchestrator|interface I[A-Z].*Calculator|interface I[A-Z].*Deriver|interface I[A-Z].*Mapper" | Select-Object -First 50',
      {
        cwd: path.join(__dirname, ".."),
        shell: "powershell",
        encoding: "utf8",
      }
    );

    return result
      .split("\n")
      .filter((line) => line.trim())
      .map((line) => {
        const match = line.match(/interface (I[A-Z][a-zA-Z]*)/);
        return match ? match[1] : null;
      })
      .filter(Boolean);
  } catch (error) {
    console.error("Error finding interfaces:", error.message);
    return [];
  }
}

// Search for all service implementations
function findAllServiceImplementations() {
  try {
    const result = execSync(
      'Get-ChildItem -Recurse -Include *.ts -Path src | Select-String -Pattern "class.*Service.*implements|class.*Repository.*implements|class.*Orchestrator.*implements|class.*Calculator.*implements|class.*Deriver.*implements|class.*Mapper.*implements" | Select-Object -First 50',
      {
        cwd: path.join(__dirname, ".."),
        shell: "powershell",
        encoding: "utf8",
      }
    );

    return result
      .split("\n")
      .filter((line) => line.trim())
      .map((line) => {
        const match = line.match(/class ([A-Z][a-zA-Z]*) implements/);
        return match ? match[1] : null;
      })
      .filter(Boolean);
  } catch (error) {
    console.error("Error finding implementations:", error.message);
    return [];
  }
}

// Extract service names from TYPES
function extractTypesFromFile(typesContent) {
  const typeMatches = typesContent.match(/(\w+):\s*Symbol\.for\(/g);
  return typeMatches
    ? typeMatches.map((match) => match.replace(/:\s*Symbol\.for\(/, ""))
    : [];
}

// Extract bound services from container
function extractBoundServicesFromContainer(containerContent) {
  // Updated regex to match both patterns:
  // container.bind(TYPES.IServiceName) and container.bind<Type>(TYPES.IServiceName)
  const bindMatches = containerContent.match(
    /\.bind(?:<.*?>)?\(TYPES\.(\w+)\)/g
  );
  return bindMatches
    ? bindMatches
        .map((match) => {
          const typeMatch = match.match(/TYPES\.(\w+)/);
          return typeMatch ? typeMatch[1] : null;
        })
        .filter(Boolean)
    : [];
}

// Main analysis function
function analyzeServices() {
  console.log("🔍 Analyzing InversifyJS migration status...\n");

  const typesContent = readTypesFile();
  const containerContent = readContainerFile();

  const definedTypes = extractTypesFromFile(typesContent);
  const boundServices = extractBoundServicesFromContainer(containerContent);
  const allInterfaces = findAllServiceInterfaces();
  const allImplementations = findAllServiceImplementations();

  console.log(`📊 Analysis Results:`);
  console.log(`   - Defined TYPES: ${definedTypes.length}`);
  console.log(`   - Bound Services: ${boundServices.length}`);
  console.log(`   - Found Interfaces: ${allInterfaces.length}`);
  console.log(`   - Found Implementations: ${allImplementations.length}\n`);

  // Find missing bindings (defined in TYPES but not bound)
  const missingBindings = definedTypes.filter(
    (type) => !boundServices.includes(type)
  );

  // Find missing TYPES (interfaces found but not in TYPES)
  const missingTypes = allInterfaces.filter(
    (iface) => !definedTypes.includes(iface)
  );

  console.log(`❌ Missing Bindings (${missingBindings.length}):`);
  missingBindings.forEach((service) => console.log(`   - ${service}`));

  console.log(`\n❌ Missing TYPES (${missingTypes.length}):`);
  missingTypes.forEach((service) => console.log(`   - ${service}`));

  return {
    definedTypes,
    boundServices,
    allInterfaces,
    allImplementations,
    missingBindings,
    missingTypes,
  };
}

// Generate the missing TYPES
function generateMissingTypes(missingTypes) {
  return missingTypes
    .map((type) => `  ${type}: Symbol.for("${type}"),`)
    .join("\n");
}

// Generate the missing bindings
function generateMissingBindings(missingBindings) {
  return missingBindings
    .map((service) => {
      const interfaceName = service.startsWith("I") ? service : `I${service}`;
      return `  container
    .bind<${interfaceName}>(TYPES.${service})
    .to(${service.replace(/^I/, "")});`;
    })
    .join("\n");
}

// Main execution
// Always run analysis
{
  const analysis = analyzeServices();

  console.log("\n🔧 Generated Code:\n");

  if (analysis.missingTypes.length > 0) {
    console.log("📝 Add to TYPES:");
    console.log(generateMissingTypes(analysis.missingTypes));
    console.log("");
  }

  if (analysis.missingBindings.length > 0) {
    console.log("🔗 Add to Container:");
    console.log(generateMissingBindings(analysis.missingBindings));
  }

  console.log(
    `\n✅ Migration Progress: ${analysis.boundServices.length}/${analysis.definedTypes.length} services bound (${Math.round((analysis.boundServices.length / analysis.definedTypes.length) * 100)}%)`
  );
}

export { analyzeServices, generateMissingTypes, generateMissingBindings };
