#!/usr/bin/env node

/**
 * Fix Remaining DI Usage Script
 *
 * Updates all remaining components that are still using the old DI system
 * to use the InversifyJS container instead.
 */

import fs from "fs/promises";

// All remaining components that need to be updated
const REMAINING_COMPONENTS = [
  {
    path: "src/lib/state/background-state.svelte.ts",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("IBackgroundService")'],
    typeResolves: ["resolve(TYPES.IBackgroundService)"],
  },
  {
    path: "src/lib/components/tabs/build-tab/export/ExportPanel.svelte",
    oldImport: 'import { resolve } from "$services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("ITKAImageExportService")'],
    typeResolves: ["resolve(TYPES.ITKAImageExportService)"],
  },
  {
    path: "src/lib/state/pictograph-generation.svelte.ts",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("IPictographGenerator")'],
    typeResolves: ["resolve(TYPES.IPictographGenerator)"],
  },
  {
    path: "src/lib/state/construct/option-picker/focused/option-persistence-state.svelte.ts",
    oldImport: 'import { resolve } from "$services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("IPositionMapper")'],
    typeResolves: ["resolve(TYPES.IPositionMapper)"],
  },
  {
    path: "src/lib/components/core/pictograph/PictographSvg.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("IGridModeDeriver")'],
    typeResolves: ["resolve(TYPES.IGridModeDeriver)"],
  },
  {
    path: "src/lib/state/motion-tester/motion-tester-state.svelte.ts",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("ISequenceAnimationEngine")'],
    typeResolves: ["resolve(TYPES.ISequenceAnimationEngine)"],
  },
  {
    path: "src/lib/components/core/pictograph/components/PropSvg.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ["resolve(IPropCoordinatorServiceInterface)"],
    typeResolves: ["resolve(TYPES.IPropCoordinatorService)"],
  },
  {
    path: "src/lib/services/implementations/construct/StartPositionServiceResolver.ts",
    oldImport: 'import { resolve } from "$services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    stringResolves: ['resolve("IStartPositionService")'],
    typeResolves: ["resolve(TYPES.IStartPositionService)"],
  },
  {
    path: "src/lib/utils/error-handling.svelte.ts",
    oldImport: 'const { resolve } = await import("$lib/services/bootstrap");',
    newImport:
      'const { resolve, TYPES } = await import("$lib/services/inversify/container");',
    // This one is more complex - it uses dynamic imports
    stringResolves: [],
    typeResolves: [],
  },
];

/**
 * Update a single component file
 */
async function updateComponent(component) {
  try {
    console.log(`🔄 Updating ${component.path}...`);

    let content = await fs.readFile(component.path, "utf-8");
    let updated = false;

    // Update import statement
    if (content.includes(component.oldImport)) {
      content = content.replace(component.oldImport, component.newImport);
      console.log(`  ✅ Updated import statement`);
      updated = true;
    }

    // Update resolve calls from strings to TYPES
    for (let i = 0; i < component.stringResolves.length; i++) {
      const oldResolve = component.stringResolves[i];
      const newResolve = component.typeResolves[i];

      if (content.includes(oldResolve)) {
        content = content.replace(
          new RegExp(oldResolve.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g"),
          newResolve
        );
        console.log(`  ✅ Updated resolve call: ${oldResolve} → ${newResolve}`);
        updated = true;
      }
    }

    // Special handling for PropSvg.svelte - it uses interface directly
    if (component.path.includes("PropSvg.svelte")) {
      if (content.includes("resolve(IPropCoordinatorServiceInterface)")) {
        content = content.replace(
          "resolve(IPropCoordinatorServiceInterface)",
          "resolve(TYPES.IPropCoordinatorService)"
        );
        console.log(`  ✅ Updated interface-based resolve call`);
        updated = true;
      }
    }

    // Special handling for error-handling.svelte.ts - it needs different approach
    if (component.path.includes("error-handling.svelte.ts")) {
      // This file uses dynamic imports and string-based resolution
      // For now, we'll leave it as is since it's a utility function
      console.log(
        `  ⚠️ Skipping error-handling.svelte.ts - needs manual review`
      );
      return true;
    }

    if (updated) {
      await fs.writeFile(component.path, content, "utf-8");
      console.log(`✅ Successfully updated ${component.path}`);
    } else {
      console.log(`ℹ️ No changes needed for ${component.path}`);
    }

    return true;
  } catch (error) {
    console.error(`❌ Failed to update ${component.path}:`, error.message);
    return false;
  }
}

/**
 * Main function to update all remaining components
 */
async function fixRemainingDIUsage() {
  console.log("🚀 Starting comprehensive DI usage fixes...");
  console.log(`📊 Components to update: ${REMAINING_COMPONENTS.length}`);

  let successCount = 0;

  for (const component of REMAINING_COMPONENTS) {
    const success = await updateComponent(component);
    if (success) {
      successCount++;
    }
  }

  console.log(`\n🎉 Comprehensive DI usage fix completed!`);
  console.log(
    `📊 Results: ${successCount}/${REMAINING_COMPONENTS.length} components processed successfully`
  );

  if (successCount === REMAINING_COMPONENTS.length) {
    console.log("\n🧪 Next steps:");
    console.log("1. Test the application with Playwright");
    console.log("2. Verify that all services resolve correctly");
    console.log("3. Check that the app loads past 85%");
    console.log("4. All components should now use InversifyJS!");
  } else {
    console.log(
      "\n⚠️ Some components failed to update - check the errors above"
    );
  }

  return successCount === REMAINING_COMPONENTS.length;
}

// Run the fix
fixRemainingDIUsage().catch(console.error);
