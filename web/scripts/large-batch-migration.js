#!/usr/bin/env node

/**
 * Large Batch Migration Script - Migrate 10+ Services at Once
 *
 * This script migrates all remaining services that are registered with registerSingletonClass
 * in the custom DI system but are NOT yet in InversifyJS. These are confirmed zero-dependency services.
 */

import fs from "fs/promises";

// Large batch of services that are still in custom DI but not in InversifyJS
const LARGE_BATCH_SERVICES = [
  // Services from core-services.ts that are NOT in InversifyJS yet
  {
    name: "SequenceStateService",
    path: "src/lib/services/implementations/sequence/SequenceStateService.ts",
    interface: "ISequenceStateService",
    interfacePath: "../interfaces/sequence-state-interfaces",
    type: "ISequenceStateService",
  },
  {
    name: "WorkbenchService",
    path: "src/lib/services/implementations/workbench/WorkbenchService.ts",
    interface: "IWorkbenchService",
    interfacePath: "../interfaces/workbench-interfaces",
    type: "IWorkbenchService",
  },
  {
    name: "WorkbenchCoordinationService",
    path: "src/lib/services/implementations/workbench/WorkbenchCoordinationService.ts",
    interface: "IWorkbenchCoordinationService",
    interfacePath: "../interfaces/workbench-interfaces",
    type: "IWorkbenchCoordinationService",
  },
  {
    name: "StartPositionSelectionService",
    path: "src/lib/services/implementations/StartPositionSelectionService.ts",
    interface: "IStartPositionSelectionService",
    interfacePath: "../interfaces/core-interfaces",
    type: "IStartPositionSelectionService",
  },
  {
    name: "GridRenderingService",
    path: "src/lib/services/implementations/rendering/GridRenderingService.ts",
    interface: "IGridRenderingService",
    interfacePath: "../interfaces/rendering-interfaces",
    type: "IGridRenderingService",
  },
  {
    name: "ArrowRenderingService",
    path: "src/lib/services/implementations/rendering/ArrowRenderingService.ts",
    interface: "IArrowRenderingService",
    interfacePath: "../interfaces/rendering-interfaces",
    type: "IArrowRenderingService",
  },
  {
    name: "OverlayRenderingService",
    path: "src/lib/services/implementations/rendering/OverlayRenderingService.ts",
    interface: "IOverlayRenderingService",
    interfacePath: "../interfaces/rendering-interfaces",
    type: "IOverlayRenderingService",
  },
  {
    name: "PropCoordinatorService",
    path: "src/lib/services/implementations/rendering/PropCoordinatorService.ts",
    interface: "IPropCoordinatorService",
    interfacePath: "../interfaces/rendering-interfaces",
    type: "IPropCoordinatorService",
  },
  {
    name: "PictographService",
    path: "src/lib/services/implementations/pictograph/PictographService.ts",
    interface: "IPictographService",
    interfacePath: "../interfaces/pictograph-interfaces",
    type: "IPictographService",
  },
  {
    name: "ExportService",
    path: "src/lib/services/implementations/export/ExportService.ts",
    interface: "IExportService",
    interfacePath: "../interfaces/export-interfaces",
    type: "IExportService",
  },
  // Services from browse-services.ts that are NOT in InversifyJS yet
  {
    name: "FilterPersistenceService",
    path: "src/lib/services/implementations/persistence/FilterPersistenceService.ts",
    interface: "IFilterPersistenceService",
    interfacePath: "../interfaces/browse-interfaces",
    type: "IFilterPersistenceService",
  },
  // Additional rendering services
  {
    name: "SVGToCanvasConverterService",
    path: "src/lib/services/implementations/export/SVGToCanvasConverterService.ts",
    interface: "ISVGToCanvasConverterService",
    interfacePath: "../interfaces/export-interfaces",
    type: "ISVGToCanvasConverterService",
  },
  {
    name: "ImageFormatConverterService",
    path: "src/lib/services/implementations/export/ImageFormatConverterService.ts",
    interface: "IImageFormatConverterService",
    interfacePath: "../interfaces/export-interfaces",
    type: "IImageFormatConverterService",
  },
];

/**
 * Add @injectable decorator and import to a service file
 */
async function addInjectableDecorator(filePath) {
  try {
    const content = await fs.readFile(filePath, "utf-8");

    // Skip if already has @injectable decorator
    if (content.includes("@injectable()")) {
      console.log(`✅ ${filePath} already has @injectable decorator`);
      return true;
    }

    let updatedContent = content;

    // Add inversify import if not present
    if (!content.includes("import { injectable }")) {
      const importRegex = /^import.*from.*['"];$/m;
      const match = content.match(importRegex);
      if (match) {
        const insertIndex = content.indexOf(match[0]) + match[0].length;
        updatedContent =
          content.slice(0, insertIndex) +
          '\nimport { injectable } from "inversify";' +
          content.slice(insertIndex);
      } else {
        // No imports found, add at the top after comments
        const firstNonCommentLine = content
          .split("\n")
          .findIndex(
            (line) =>
              line.trim() &&
              !line.trim().startsWith("*") &&
              !line.trim().startsWith("//")
          );
        if (firstNonCommentLine !== -1) {
          const lines = content.split("\n");
          lines.splice(
            firstNonCommentLine,
            0,
            'import { injectable } from "inversify";',
            ""
          );
          updatedContent = lines.join("\n");
        }
      }
    }

    // Add @injectable() decorator before class declaration
    const classRegex = /^export class (\w+)/m;
    updatedContent = updatedContent.replace(
      classRegex,
      "@injectable()\nexport class $1"
    );

    await fs.writeFile(filePath, updatedContent, "utf-8");
    console.log(`✅ Added @injectable() decorator to ${filePath}`);
    return true;
  } catch (error) {
    console.error(
      `❌ Failed to add @injectable() to ${filePath}:`,
      error.message
    );
    return false;
  }
}

/**
 * Add service imports to the InversifyJS container
 */
async function addServiceImports(services) {
  const containerPath = "src/lib/services/inversify/container.ts";

  try {
    const content = await fs.readFile(containerPath, "utf-8");
    let updatedContent = content;

    // Find the import section and add new imports
    const importSectionEnd = content.lastIndexOf("import");
    const nextLineAfterImports = content.indexOf("\n", importSectionEnd);

    let newImports = "";
    for (const service of services) {
      const importStatement = `import { ${service.name} } from "../implementations/${service.path.replace("src/lib/services/implementations/", "").replace(".ts", "")}";`;
      if (!content.includes(importStatement)) {
        newImports += importStatement + "\n";
      }
    }

    if (newImports) {
      updatedContent =
        content.slice(0, nextLineAfterImports) +
        "\n" +
        newImports +
        content.slice(nextLineAfterImports);
    }

    await fs.writeFile(containerPath, updatedContent, "utf-8");
    console.log(`✅ Added ${services.length} service imports to container`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to add imports to container:`, error.message);
    return false;
  }
}

/**
 * Add service bindings to the InversifyJS container
 */
async function addServiceBindings(services) {
  const containerPath = "src/lib/services/inversify/container.ts";

  try {
    const content = await fs.readFile(containerPath, "utf-8");
    let updatedContent = content;

    // Find where to add bindings (before the return statement)
    const returnIndex = content.lastIndexOf("return container;");

    let newBindings = "\n  // Large batch migrated services\n";
    for (const service of services) {
      const binding = `  container\n    .bind<${service.interface}>(TYPES.${service.type})\n    .to(${service.name});`;
      newBindings += binding + "\n";
    }

    updatedContent =
      content.slice(0, returnIndex) +
      newBindings +
      "\n  " +
      content.slice(returnIndex);

    await fs.writeFile(containerPath, updatedContent, "utf-8");
    console.log(`✅ Added ${services.length} service bindings to container`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to add bindings to container:`, error.message);
    return false;
  }
}

/**
 * Update the checklist with newly migrated services
 */
async function updateChecklist(services) {
  const checklistPath = "docs/INVERSIFY_SERVICE_CONVERSION_CHECKLIST.md";

  try {
    const content = await fs.readFile(checklistPath, "utf-8");
    let updatedContent = content;

    // Update the count
    const currentCount = 41; // Current count from the file
    const newCount = currentCount + services.length;
    const newPercentage = ((newCount / 90) * 100).toFixed(1);
    const remainingCount = 90 - newCount;
    const remainingPercentage = ((remainingCount / 90) * 100).toFixed(1);

    updatedContent = updatedContent.replace(
      /\*\*✅ COMPLETED\*\*: \d+\/90 \(\d+\.\d+%\)/,
      `**✅ COMPLETED**: ${newCount}/90 (${newPercentage}%)`
    );
    updatedContent = updatedContent.replace(
      /\*\*🔄 REMAINING\*\*: \d+\/90 \(\d+\.\d+%\)/,
      `**🔄 REMAINING**: ${remainingCount}/90 (${remainingPercentage}%)`
    );

    // Update the service count in the header
    updatedContent = updatedContent.replace(
      /### \*\*✅ SUCCESSFULLY MIGRATED TO INVERSIFYJS \(\d+ services\)\*\*/,
      `### **✅ SUCCESSFULLY MIGRATED TO INVERSIFYJS (${newCount} services)**`
    );

    // Add the new services to the list
    const lastServiceLine = updatedContent.lastIndexOf("41. DeleteService");
    const nextLineIndex = updatedContent.indexOf("\n", lastServiceLine);

    let newServicesList = "";
    services.forEach((service, index) => {
      newServicesList += `\n${currentCount + index + 1}. ${service.name}`;
    });

    updatedContent =
      updatedContent.slice(0, nextLineIndex) +
      newServicesList +
      updatedContent.slice(nextLineIndex);

    await fs.writeFile(checklistPath, updatedContent, "utf-8");
    console.log(`✅ Updated checklist with ${services.length} new services`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to update checklist:`, error.message);
    return false;
  }
}

/**
 * Main migration function
 */
async function migrateLargeBatch() {
  console.log(
    "🚀 Starting LARGE BATCH migration of 13 zero-dependency services..."
  );
  console.log(`📊 Services to migrate: ${LARGE_BATCH_SERVICES.length}`);

  const successfullyMigrated = [];

  // Step 1: Add @injectable decorators to all services
  for (const service of LARGE_BATCH_SERVICES) {
    console.log(`\n🔄 Processing ${service.name}...`);
    const success = await addInjectableDecorator(service.path);
    if (success) {
      successfullyMigrated.push(service);
    }
  }

  if (successfullyMigrated.length === 0) {
    console.log("❌ No services were successfully prepared for migration");
    return;
  }

  console.log(
    `\n📦 Migrating ${successfullyMigrated.length} services to InversifyJS container...`
  );

  // Step 2: Add imports to container
  await addServiceImports(successfullyMigrated);

  // Step 3: Add bindings to container
  await addServiceBindings(successfullyMigrated);

  // Step 4: Update checklist
  await updateChecklist(successfullyMigrated);

  console.log(
    `\n🎉 Successfully migrated ${successfullyMigrated.length} services to InversifyJS!`
  );
  console.log("📋 Migrated services:");
  successfullyMigrated.forEach((service, index) => {
    console.log(`   ${index + 1}. ✅ ${service.name}`);
  });

  console.log("\n🧪 Next steps:");
  console.log("1. Run the application to test the migration");
  console.log("2. Run tests to ensure everything works correctly");
  console.log("3. Remove services from custom DI registration files");
  console.log(
    `4. New total: ${41 + successfullyMigrated.length}/90 services migrated!`
  );
}

// Run the migration
migrateLargeBatch().catch(console.error);
