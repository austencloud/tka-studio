#!/usr/bin/env node

/**
 * Eliminate ALL Legacy DI Usage Script
 *
 * Finds and eliminates every single remaining usage of legacyResolve and string-based resolution
 */

import fs from "fs/promises";

// All files that still use legacy DI
const LEGACY_FILES = [
  {
    path: "src/lib/state/motion-tester/motion-tester-state.svelte.ts",
    fixes: [
      {
        old: 'resolve(\n    "ISequenceAnimationEngine"\n  ) as ISequenceAnimationEngine;',
        new: "resolve(TYPES.ISequenceAnimationEngine);",
      },
    ],
  },
  {
    path: "src/lib/services/implementations/construct/OptionsService.ts",
    fixes: [
      {
        old: 'import { legacyResolve } from "$lib/services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'legacyResolve("IPositionMapper")',
        new: "resolve(TYPES.IPositionMapper)",
      },
    ],
  },
  {
    path: "src/lib/components/tabs/browse-tab/sequence-browser/SequenceBrowserPanel.svelte",
    fixes: [
      {
        old: 'import { legacyResolve } from "$lib/services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'legacyResolve("IThumbnailService")',
        new: "resolve(TYPES.IThumbnailService)",
      },
    ],
  },
  {
    path: "src/lib/state/construct/option-picker/focused/option-data-state.svelte.ts",
    fixes: [
      {
        old: 'import { legacyResolve } from "$services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'const positionService = legacyResolve("IPositionMapper") as IPositionMapper;',
        new: "const positionService = resolve(TYPES.IPositionMapper);",
      },
      {
        old: "const letterQueryService = legacyResolve(\n            ILetterQueryServiceInterface\n          );",
        new: "const letterQueryService = resolve(TYPES.ILetterQueryService);",
      },
    ],
  },
  {
    path: "src/lib/state/generate/generate-actions.svelte.ts",
    fixes: [
      {
        old: 'import { legacyResolve } from "$lib/services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'legacyResolve("ISequenceGenerationService")',
        new: "resolve(TYPES.ISequenceGenerationService)",
      },
    ],
  },
  {
    path: "src/lib/services/implementations/construct/ConstructTabEventService.ts",
    fixes: [
      {
        old: 'import { legacyResolve } from "$lib/services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'this.constructCoordinator = legacyResolve(\n        "IConstructTabCoordinationService"\n      );',
        new: "this.constructCoordinator = resolve(TYPES.IConstructTabCoordinationService);",
      },
    ],
  },
  {
    path: "src/lib/components/tabs/build-tab/edit/DetailedInfoPanel.svelte",
    fixes: [
      {
        old: 'import { legacyResolve } from "$lib/services/bootstrap";',
        new: 'import { resolve, TYPES } from "$lib/services/inversify/container";',
      },
      {
        old: 'legacyResolve("IGridModeDeriver")',
        new: "resolve(TYPES.IGridModeDeriver)",
      },
    ],
  },
  {
    path: "src/lib/utils/error-handling.svelte.ts",
    fixes: [
      {
        old: 'const { legacyResolve: resolve } = await import("$lib/services/bootstrap");',
        new: 'const { resolve, TYPES } = await import("$lib/services/inversify/container");',
      },
    ],
  },
];

/**
 * Apply fixes to a single file
 */
async function fixFile(fileConfig) {
  try {
    console.log(`🔄 Eliminating legacy DI from ${fileConfig.path}...`);

    let content = await fs.readFile(fileConfig.path, "utf-8");
    let updated = false;

    for (const fix of fileConfig.fixes) {
      if (content.includes(fix.old)) {
        content = content.replace(fix.old, fix.new);
        console.log(`  ✅ Fixed: ${fix.old.substring(0, 50)}...`);
        updated = true;
      }
    }

    if (updated) {
      await fs.writeFile(fileConfig.path, content, "utf-8");
      console.log(
        `✅ Successfully eliminated legacy DI from ${fileConfig.path}`
      );
    } else {
      console.log(`ℹ️ No legacy DI found in ${fileConfig.path}`);
    }

    return true;
  } catch (error) {
    console.error(`❌ Failed to fix ${fileConfig.path}:`, error.message);
    return false;
  }
}

/**
 * Main function to eliminate all legacy DI usage
 */
async function eliminateAllLegacyDI() {
  console.log("🚀 ELIMINATING ALL LEGACY DI USAGE...");
  console.log(`📊 Files to fix: ${LEGACY_FILES.length}`);

  let successCount = 0;

  for (const fileConfig of LEGACY_FILES) {
    const success = await fixFile(fileConfig);
    if (success) {
      successCount++;
    }
  }

  console.log(`\n🎉 Legacy DI elimination completed!`);
  console.log(
    `📊 Results: ${successCount}/${LEGACY_FILES.length} files processed successfully`
  );

  if (successCount === LEGACY_FILES.length) {
    console.log("\n🧪 Next steps:");
    console.log("1. Test the application with Playwright");
    console.log("2. ALL components should now use InversifyJS only!");
    console.log("3. The old DI system should be completely abandoned");
    console.log("4. ISequenceStateService error should be GONE!");
  } else {
    console.log("\n⚠️ Some files failed to update - check the errors above");
  }

  return successCount === LEGACY_FILES.length;
}

// Run the elimination
eliminateAllLegacyDI().catch(console.error);
