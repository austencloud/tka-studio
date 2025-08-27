/**
 * Add Missing Service Bindings Script
 *
 * This script adds all the missing service bindings to the InversifyJS container
 * based on the analysis from complete-inversify-migration.js
 */

import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);

// Missing services that need bindings (from the analysis)
const missingBindings = [
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
  "IApplicationInitializationService",
  "IValidationService",
];

// Services that need TYPES and bindings (from the analysis)
const newServices = [
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

// Generate import statements for missing services
function generateImports(services) {
  const imports = [];

  services.forEach((serviceName) => {
    const className = serviceName.replace(/^I/, "");

    // Try to find the service file
    const possiblePaths = [
      `../implementations/domain/${className}.ts`,
      `../implementations/data/${className}.ts`,
      `../implementations/positioning/${className}.ts`,
      `../implementations/rendering/${className}.ts`,
      `../implementations/export/${className}.ts`,
      `../implementations/workbench/${className}.ts`,
      `../implementations/construct/${className}.ts`,
      `../implementations/background/${className}.ts`,
      `../implementations/browse/${className}.ts`,
      `../implementations/generation/${className}.ts`,
      `../implementations/application/${className}.ts`,
      `../../repositories/${className}.ts`,
      `../../codex/${className}.ts`,
      `../../animator/core/services/${className}.ts`,
    ];

    // For now, just generate the import structure
    imports.push({
      serviceName,
      className,
      interfaceName: serviceName,
    });
  });

  return imports;
}

// Generate binding statements
function generateBindings(services) {
  return services
    .map((serviceName) => {
      const className = serviceName.replace(/^I/, "");
      return `  container
    .bind<${serviceName}>(TYPES.${serviceName})
    .to(${className});`;
    })
    .join("\n");
}

// Main execution
console.log("🔧 Generating missing service bindings...\n");

const missingImports = generateImports(missingBindings);
const newImports = generateImports(newServices);
const allImports = [...missingImports, ...newImports];

console.log("📦 Required Imports:");
allImports.forEach(({ serviceName, className }) => {
  console.log(
    `import { ${className} } from "../implementations/.../${className}";`
  );
  console.log(`import type { ${serviceName} } from "../interfaces/...";`);
});

console.log("\n🔗 Missing Bindings:");
console.log(generateBindings(missingBindings));

console.log("\n🔗 New Service Bindings:");
console.log(generateBindings(newServices));

console.log(
  "\n✅ Total services to add:",
  missingBindings.length + newServices.length
);
