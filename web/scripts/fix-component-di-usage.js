#!/usr/bin/env node

/**
 * Fix Component DI Usage Script
 *
 * Updates Svelte components to use InversifyJS container instead of old DI system
 */

import fs from "fs/promises";

// Components that need to be updated
const COMPONENTS_TO_FIX = [
  {
    path: "src/lib/components/tabs/build-tab/construct/ConstructTabContent.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport: 'import { resolve } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("ISequenceStateService")',
    newResolve: "resolve(TYPES.ISequenceStateService)",
    needsTypesImport: true,
  },
  {
    path: "src/lib/components/tabs/build-tab/BuildTab.svelte",
    oldImport: 'import { resolve } from "$services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("ISequenceService")',
    newResolve: "resolve(TYPES.ISequenceService)",
    needsTypesImport: false,
  },
  {
    path: "src/lib/components/tabs/build-tab/workbench/Workbench.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("ISequenceStateService")',
    newResolve: "resolve(TYPES.ISequenceStateService)",
    needsTypesImport: false,
  },
  {
    path: "src/lib/components/tabs/build-tab/workbench/BeatFrame.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("IBeatFrameService")',
    newResolve: "resolve(TYPES.IBeatFrameService)",
    needsTypesImport: false,
  },
  {
    path: "src/lib/components/tabs/build-tab/workbench/BeatView.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("IBeatFrameService")',
    newResolve: "resolve(TYPES.IBeatFrameService)",
    needsTypesImport: false,
  },
  {
    path: "src/lib/components/tabs/browse-tab/BrowseTab.svelte",
    oldImport: 'import { resolve } from "$lib/services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    // This one has multiple resolve calls - we'll handle it specially
    needsTypesImport: false,
  },
  {
    path: "src/lib/components/tabs/build-tab/generate/GeneratePanel.svelte",
    oldImport: 'import { resolve } from "$services/bootstrap";',
    newImport:
      'import { resolve, TYPES } from "$lib/services/inversify/container";',
    oldResolve: 'resolve("IDeviceDetectionService")',
    newResolve: "resolve(TYPES.IDeviceDetectionService)",
    needsTypesImport: false,
  },
];

/**
 * Update a single component file
 */
async function updateComponent(component) {
  try {
    console.log(`🔄 Updating ${component.path}...`);

    let content = await fs.readFile(component.path, "utf-8");

    // Update import statement
    if (content.includes(component.oldImport)) {
      content = content.replace(component.oldImport, component.newImport);
      console.log(`  ✅ Updated import statement`);
    }

    // Add TYPES import if needed and not already included
    if (component.needsTypesImport && !content.includes("import { TYPES }")) {
      const importIndex = content.indexOf(component.newImport);
      if (importIndex !== -1) {
        const lineEnd = content.indexOf("\n", importIndex);
        content =
          content.slice(0, lineEnd) +
          '\n  import { TYPES } from "$lib/services/inversify/types";' +
          content.slice(lineEnd);
        console.log(`  ✅ Added TYPES import`);
      }
    }

    // Update resolve calls
    if (component.oldResolve && component.newResolve) {
      if (content.includes(component.oldResolve)) {
        content = content.replace(
          new RegExp(
            component.oldResolve.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
            "g"
          ),
          component.newResolve
        );
        console.log(`  ✅ Updated resolve call`);
      }
    }

    // Special handling for BrowseTab.svelte which has multiple resolve calls
    if (component.path.includes("BrowseTab.svelte")) {
      // Update all string-based resolve calls to use TYPES
      content = content.replace(
        /resolve\("([^"]+)"\)/g,
        (match, serviceName) => {
          return `resolve(TYPES.${serviceName})`;
        }
      );
      console.log(`  ✅ Updated multiple resolve calls`);
    }

    await fs.writeFile(component.path, content, "utf-8");
    console.log(`✅ Successfully updated ${component.path}`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to update ${component.path}:`, error.message);
    return false;
  }
}

/**
 * Main function to update all components
 */
async function fixComponentDIUsage() {
  console.log("🚀 Starting component DI usage fixes...");
  console.log(`📊 Components to update: ${COMPONENTS_TO_FIX.length}`);

  let successCount = 0;

  for (const component of COMPONENTS_TO_FIX) {
    const success = await updateComponent(component);
    if (success) {
      successCount++;
    }
  }

  console.log(`\n🎉 Component DI usage fix completed!`);
  console.log(
    `📊 Results: ${successCount}/${COMPONENTS_TO_FIX.length} components updated successfully`
  );

  if (successCount === COMPONENTS_TO_FIX.length) {
    console.log("\n🧪 Next steps:");
    console.log("1. Test the application with Playwright");
    console.log("2. Verify that ISequenceStateService resolves correctly");
    console.log("3. Check that the app loads past 85%");
    console.log("4. Continue migrating remaining services");
  } else {
    console.log(
      "\n⚠️ Some components failed to update - check the errors above"
    );
  }

  return successCount === COMPONENTS_TO_FIX.length;
}

// Run the fix
fixComponentDIUsage().catch(console.error);
