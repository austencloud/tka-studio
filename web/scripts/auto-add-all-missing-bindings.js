#!/usr/bin/env node

/**
 * Auto-Add All Missing Bindings Script
 *
 * This script automatically finds all service implementations and adds them to the InversifyJS container.
 * It will find the actual file paths and add proper imports and bindings.
 */

import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Services that need to be added (from the missing services list)
const MISSING_SERVICES = [
  "ISequenceDeletionService",
  "IArrowPositioningOrchestrator",
  "IPositionMapper",
  "IPositionCalculatorService",
  "IBetaOffsetCalculator",
  "IPictographGenerator",
  "IWorkbenchBeatOperationsService",
  "IConstructTabCoordinationService",
  "IPageImageExportService",
  "IPageFactoryService",
  "IPrintablePageLayoutService",
  "ISequenceCardExportIntegrationService",
  "IImageFormatConverterService",
  "ISVGToCanvasConverterService",
  "ITKAImageExportService",
  "ICanvasManagementService",
  "IImageCompositionService",
  "IFileExportService",
  "IImagePreviewGenerator",
  "IBeatRenderingService",
  "IGridOverlayService",
  "IPictographTransformationService",
  "IAnimatorService",
  "IValidationService",
  "IMotionQueryService",
  "IExampleSequenceService",
  "ILessonRepository",
  "ICodexService",
  "IPictographOperationsService",
  "IBeatCalculationService",
  "IPropInterpolationService",
  "IAnimationStateService",
  "ISequenceAnimationOrchestrator",
  "IAngleCalculationService",
  "IMotionCalculationService",
  "IEndpointCalculationService",
  "ICoordinateUpdateService",
  "IImageExportServices",
  "IAnimatedPictographDataService",
  "IBackgroundService",
  "IBrowseStatePersistenceService",
  "IArrowPlacementService",
  "ICSVParserService",
  "IMotionParameterService",
  "IAnimationControlService",
  "IMotionLetterIdentificationService",
  "ICSVPictographLoaderService",
  "IArrowLocationService",
  "IArrowPlacementKeyService",
  "IPropPlacementService",
];

/**
 * Find the actual implementation file for a service
 */
async function findServiceImplementation(serviceName) {
  const implementationName = serviceName.replace(/^I/, ""); // Remove 'I' prefix

  try {
    const result = execSync(
      `Get-ChildItem -Recurse -Include *.ts -Path src | Select-String -Pattern "export class ${implementationName}" | Select-Object -First 1`,
      {
        cwd: path.join(__dirname, ".."),
        shell: "powershell",
        encoding: "utf8",
      }
    );

    if (result.trim()) {
      const filePath = result.split(":")[0].trim();
      const relativePath = filePath
        .replace(/^.*\\src\\/, "src/")
        .replace(/\\/g, "/");
      return {
        name: implementationName,
        interface: serviceName,
        path: relativePath,
        importPath: relativePath
          .replace("src/lib/services/", "../")
          .replace(".ts", ""),
      };
    }
  } catch (error) {
    console.warn(`⚠️ Could not find implementation for ${serviceName}`);
  }

  return null;
}

/**
 * Find all service implementations
 */
async function findAllServiceImplementations() {
  console.log("🔍 Finding service implementations...");

  const services = [];
  for (const serviceName of MISSING_SERVICES) {
    const service = await findServiceImplementation(serviceName);
    if (service) {
      services.push(service);
      console.log(`✅ Found: ${service.name} at ${service.path}`);
    } else {
      console.log(`❌ Missing: ${serviceName}`);
    }
  }

  return services;
}

/**
 * Generate import statements
 */
function generateImports(services) {
  const interfaceImports = services
    .map(
      (service) =>
        `import type { ${service.interface} } from "../interfaces/application-interfaces";`
    )
    .join("\n");

  const implementationImports = services
    .map(
      (service) => `import { ${service.name} } from "${service.importPath}";`
    )
    .join("\n");

  return { interfaceImports, implementationImports };
}

/**
 * Generate binding statements
 */
function generateBindings(services) {
  return services
    .map(
      (service) =>
        `  container.bind<${service.interface}>(TYPES.${service.interface}).to(${service.name});`
    )
    .join("\n");
}

/**
 * Update the container.ts file
 */
async function updateContainer(services) {
  const containerPath = path.join(
    __dirname,
    "..",
    "src/lib/services/inversify/container.ts"
  );

  try {
    let content = await fs.readFile(containerPath, "utf8");

    const { interfaceImports, implementationImports } =
      generateImports(services);
    const bindings = generateBindings(services);

    // Add interface imports after existing interface imports
    const interfaceImportRegex =
      /(import type \{[^}]+\} from ["'][^"']+["'];?\s*)+/;
    content = content.replace(
      interfaceImportRegex,
      `$&\n${interfaceImports}\n`
    );

    // Add implementation imports after existing implementation imports
    const implementationImportRegex =
      /(import \{ [^}]+\} from ["'][^"']+["'];?\s*)+/;
    content = content.replace(
      implementationImportRegex,
      `$&\n${implementationImports}\n`
    );

    // Add bindings before the return statement
    const returnRegex = /(\s+return container;)/;
    content = content.replace(
      returnRegex,
      `\n  // === MISSING SERVICES BINDINGS ===\n${bindings}\n$1`
    );

    await fs.writeFile(containerPath, content);
    console.log(`✅ Updated container.ts with ${services.length} new bindings`);
  } catch (error) {
    console.error("❌ Failed to update container:", error.message);
    throw error;
  }
}

/**
 * Main function
 */
async function addAllMissingBindings() {
  console.log("🚀 Starting auto-add missing bindings...\n");

  // Find all service implementations
  const services = await findAllServiceImplementations();

  console.log(
    `\n📊 Found ${services.length} service implementations out of ${MISSING_SERVICES.length} missing services`
  );

  if (services.length === 0) {
    console.log("❌ No services found to add");
    return;
  }

  // Update the container
  await updateContainer(services);

  console.log("\n🎉 Successfully added all missing service bindings!");
  console.log(
    `📈 Container should now have ${53 + services.length} total services bound`
  );
  console.log("\n🔄 Restart the dev server to see the changes");
}

// Run the script
if (import.meta.url === `file://${process.argv[1]}`) {
  addAllMissingBindings().catch(console.error);
}

export { addAllMissingBindings };
