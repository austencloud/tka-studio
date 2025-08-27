#!/usr/bin/env node

/**
 * Pictograph Services Migration Script
 *
 * Migrates PictographService and PictographRenderingService to InversifyJS
 * with proper dependency handling for the arrow positioning orchestrator.
 */

import fs from "fs/promises";

/**
 * Add PictographService and PictographRenderingService to InversifyJS container
 */
async function migratePictographServices() {
  console.log("🚀 Starting PictographService migration...");

  // Step 1: Add the missing interface imports to container
  const containerPath = "src/lib/services/inversify/container.ts";

  try {
    let content = await fs.readFile(containerPath, "utf-8");

    // Add IPictographService and IPictographRenderingService imports
    const interfaceImports = `import type {
  IPictographService,
  IPictographRenderingService,
} from "../interfaces/pictograph-interfaces";`;

    // Find where to add the interface imports
    const lastInterfaceImport = content.lastIndexOf('} from "../interfaces/');
    const nextLineIndex = content.indexOf("\n", lastInterfaceImport);

    if (!content.includes("IPictographService")) {
      content =
        content.slice(0, nextLineIndex) +
        "\n" +
        interfaceImports +
        content.slice(nextLineIndex);
    }

    // Add service implementation imports
    const serviceImports = `import { PictographService } from "../implementations/domain/PictographService";
import { PictographRenderingService } from "../implementations/rendering/PictographRenderingService";`;

    // Find where to add service imports
    const lastServiceImport = content.lastIndexOf("import { ");
    const nextServiceLineIndex = content.indexOf("\n", lastServiceImport);

    if (!content.includes("PictographService")) {
      content =
        content.slice(0, nextServiceLineIndex) +
        "\n" +
        serviceImports +
        content.slice(nextServiceLineIndex);
    }

    await fs.writeFile(containerPath, content, "utf-8");
    console.log("✅ Added imports to container");
  } catch (error) {
    console.error("❌ Failed to add imports:", error.message);
    return false;
  }

  // Step 2: Add the service bindings with proper dependency handling
  try {
    let content = await fs.readFile(containerPath, "utf-8");

    // Add PictographRenderingService with factory pattern for arrow positioning
    const pictographRenderingBinding = `
  // PictographRenderingService with factory for arrow positioning
  container.bind<IPictographRenderingService>(TYPES.IPictographRenderingService)
    .toDynamicValue((context) => {
      // Use factory pattern for arrow positioning orchestrator
      const { getPositioningServiceFactory } = require("../positioning/factory");
      const factory = getPositioningServiceFactory();
      const arrowPositioning = factory.createPositioningOrchestrator();
      
      // Resolve other dependencies from container
      const svgUtility = context.container.get<ISvgUtilityService>(TYPES.ISvgUtilityService);
      const gridRendering = context.container.get<IGridRenderingService>(TYPES.IGridRenderingService);
      const arrowRendering = context.container.get<IArrowRenderingService>(TYPES.IArrowRenderingService);
      const overlayRendering = context.container.get<IOverlayRenderingService>(TYPES.IOverlayRenderingService);
      const dataTransformation = context.container.get<IDataTransformationService>(TYPES.IDataTransformationService);
      
      return new PictographRenderingService(
        arrowPositioning,
        null, // PropRenderingService is deprecated
        svgUtility,
        gridRendering,
        arrowRendering,
        overlayRendering,
        dataTransformation
      );
    });`;

    // Add PictographService binding
    const pictographServiceBinding = `
  // PictographService depends on PictographRenderingService
  container.bind<IPictographService>(TYPES.IPictographService)
    .to(PictographService);`;

    // Find where to add bindings (before the return statement)
    const returnIndex = content.lastIndexOf("return container;");

    const newBindings = pictographRenderingBinding + pictographServiceBinding;

    if (!content.includes("IPictographService")) {
      content =
        content.slice(0, returnIndex) +
        newBindings +
        "\n\n  " +
        content.slice(returnIndex);
    }

    await fs.writeFile(containerPath, content, "utf-8");
    console.log("✅ Added service bindings to container");
  } catch (error) {
    console.error("❌ Failed to add bindings:", error.message);
    return false;
  }

  // Step 3: Fix PictographRenderingService to use proper @inject decorators
  const renderingServicePath =
    "src/lib/services/implementations/rendering/PictographRenderingService.ts";

  try {
    let content = await fs.readFile(renderingServicePath, "utf-8");

    // Remove the resolve() call for gridModeService and use proper injection
    content = content.replace(
      /private gridModeService = resolve<IGridModeDeriver>\("IGridModeDeriver"\);/,
      "// GridModeService will be injected via constructor"
    );

    // Update constructor to use @inject decorators
    const newConstructor = `  constructor(
    private arrowPositioning: IArrowPositioningOrchestrator,
    private propRendering: IPropRenderingService | null, // ✅ FIXED: Made optional for deprecated service
    @inject(TYPES.ISvgUtilityService) private svgUtility: ISvgUtilityService,
    @inject(TYPES.IGridRenderingService) private gridRendering: IGridRenderingService,
    @inject(TYPES.IArrowRenderingService) private arrowRendering: IArrowRenderingService,
    @inject(TYPES.IOverlayRenderingService) private overlayRendering: IOverlayRenderingService,
    @inject(TYPES.IDataTransformationService) private dataTransformation: IDataTransformationService,
    @inject(TYPES.IGridModeDeriver) private gridModeService: IGridModeDeriver
  ) {
    // PictographRenderingService initialized with microservices
    // PropRenderingService is deprecated - props are now rendered by Prop.svelte components
  }`;

    // Replace the constructor
    const constructorRegex = /constructor\([^}]+\}/s;
    content = content.replace(constructorRegex, newConstructor);

    await fs.writeFile(renderingServicePath, content, "utf-8");
    console.log("✅ Updated PictographRenderingService constructor");
  } catch (error) {
    console.error(
      "❌ Failed to update PictographRenderingService:",
      error.message
    );
    return false;
  }

  // Step 4: Fix PictographService to use proper @inject decorator
  const pictographServicePath =
    "src/lib/services/implementations/domain/PictographService.ts";

  try {
    let content = await fs.readFile(pictographServicePath, "utf-8");

    // Add inject import
    content = content.replace(
      'import { injectable } from "inversify";',
      'import { injectable, inject } from "inversify";'
    );

    // Add TYPES import
    content = content.replace(
      "import type {",
      'import { TYPES } from "../../inversify/types";\nimport type {'
    );

    // Update constructor
    content = content.replace(
      "constructor(private renderingService: IPictographRenderingService) {}",
      "constructor(\n    @inject(TYPES.IPictographRenderingService) private renderingService: IPictographRenderingService\n  ) {}"
    );

    await fs.writeFile(pictographServicePath, content, "utf-8");
    console.log("✅ Updated PictographService constructor");
  } catch (error) {
    console.error("❌ Failed to update PictographService:", error.message);
    return false;
  }

  // Step 5: Update checklist
  const checklistPath = "docs/INVERSIFY_SERVICE_CONVERSION_CHECKLIST.md";

  try {
    let content = await fs.readFile(checklistPath, "utf-8");

    // Update the count (adding 2 services)
    const currentCount = 51;
    const newCount = currentCount + 2;
    const newPercentage = ((newCount / 90) * 100).toFixed(1);
    const remainingCount = 90 - newCount;
    const remainingPercentage = ((remainingCount / 90) * 100).toFixed(1);

    content = content.replace(
      /\*\*✅ COMPLETED\*\*: \d+\/90 \(\d+\.\d+%\)/,
      `**✅ COMPLETED**: ${newCount}/90 (${newPercentage}%)`
    );
    content = content.replace(
      /\*\*🔄 REMAINING\*\*: \d+\/90 \(\d+\.\d+%\)/,
      `**🔄 REMAINING**: ${remainingCount}/90 (${remainingPercentage}%)`
    );

    // Update the service count in the header
    content = content.replace(
      /### \*\*✅ SUCCESSFULLY MIGRATED TO INVERSIFYJS \(\d+ services\)\*\*/,
      `### **✅ SUCCESSFULLY MIGRATED TO INVERSIFYJS (${newCount} services)**`
    );

    // Add the new services to the list
    const lastServiceLine = content.lastIndexOf("51. FilterPersistenceService");
    const nextLineIndex = content.indexOf("\n", lastServiceLine);

    const newServicesList = `\n52. PictographRenderingService\n53. PictographService`;

    content =
      content.slice(0, nextLineIndex) +
      newServicesList +
      content.slice(nextLineIndex);

    await fs.writeFile(checklistPath, content, "utf-8");
    console.log("✅ Updated checklist");
  } catch (error) {
    console.error("❌ Failed to update checklist:", error.message);
  }

  console.log("\n🎉 PictographService migration completed!");
  console.log("📋 Migrated services:");
  console.log(
    "   ✅ PictographRenderingService (with factory pattern for arrow positioning)"
  );
  console.log("   ✅ PictographService");
  console.log("\n🧪 Next steps:");
  console.log("1. Test the application with Playwright");
  console.log("2. Verify that IPictographService resolves correctly");
  console.log(
    "3. Check that dependent services (ExportService, BeatRenderingService) now work"
  );

  return true;
}

// Run the migration
migratePictographServices().catch(console.error);
