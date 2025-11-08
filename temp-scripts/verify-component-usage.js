#!/usr/bin/env node

/**
 * Component Usage Verification Tool
 * Verifies which Svelte components and TypeScript modules are actually used
 * by searching for imports and usage patterns
 */

import fs from "fs";
import { execSync } from "child_process";
import path from "path";

console.log("=".repeat(80));
console.log("COMPONENT USAGE VERIFICATION");
console.log("=".repeat(80));
console.log("");

// Helper to search for component usage
function searchForUsage(componentName, modulePath) {
  const results = {
    component: componentName,
    file: modulePath,
    usages: [],
  };

  try {
    // Search for direct .svelte file imports
    const svelteImportPattern = `${componentName}\\.svelte`;
    const svelteImports = execSync(
      `git grep -n "${svelteImportPattern}" -- "*.ts" "*.svelte" "*.js" || true`,
      { encoding: "utf-8" }
    ).trim();

    if (svelteImports) {
      results.usages.push({
        type: "svelte-import",
        matches: svelteImports.split("\n").filter(
          (line) => !line.includes(`${modulePath}/${componentName}.svelte:`) // Exclude self-reference
        ),
      });
    }

    // Search for component usage in templates
    const componentUsagePattern = `<${componentName}`;
    const componentUsages = execSync(
      `git grep -n "${componentUsagePattern}" -- "*.svelte" || true`,
      { encoding: "utf-8" }
    ).trim();

    if (componentUsages) {
      results.usages.push({
        type: "template-usage",
        matches: componentUsages.split("\n"),
      });
    }

    // Search for barrel imports (from index.ts)
    const barrelPattern = `{[^}]*${componentName}[^}]*}.*from.*${modulePath.split("/").slice(-2).join("/")}`;
    const barrelImports = execSync(
      `git grep -E "${barrelPattern}" -- "*.ts" "*.svelte" "*.js" || true`,
      { encoding: "utf-8" }
    ).trim();

    if (barrelImports) {
      results.usages.push({
        type: "barrel-import",
        matches: barrelImports.split("\n"),
      });
    }
  } catch (error) {
    // grep failed (no matches)
  }

  results.isUsed =
    results.usages.length > 0 &&
    results.usages.some((u) => u.matches.length > 0);
  results.totalMatches = results.usages.reduce(
    (acc, u) => acc + (Array.isArray(u.matches) ? u.matches.length : 0),
    0
  );

  return results;
}

// Modules to check
const modulesToCheck = [
  {
    name: "About",
    path: "src/lib/modules/about/components",
    components: [
      "AboutTab",
      "AboutTheSystem",
      "CallToAction",
      "Contact",
      "ContactSection",
      "Features",
      "GettingStarted",
      "HeroSection",
      "Home",
      "LandingNavBar",
      "Links",
      "ProjectOverview",
      "QuickAccess",
      "ResourcesHistorian",
      "SettingsModal",
    ],
  },
  {
    name: "Word Card",
    path: "src/lib/modules/word-card/components",
    components: ["Navigation", "PageDisplay", "WordCard", "WordCardTab"],
  },
  {
    name: "Write",
    path: "src/lib/modules/write/components",
    components: [
      "WriteTab",
      "ActBrowser",
      "ActHeader",
      "ActSheet",
      "ActThumbnail",
      "MusicPlayer",
      "WriteSequenceGrid",
      "WriteSequenceThumbnail",
      "WriteToolbar",
    ],
  },
  {
    name: "Library",
    path: "src/lib/modules/library",
    components: ["LibraryTab", "SequencesView"],
  },
];

const allResults = [];

modulesToCheck.forEach((module) => {
  console.log(`\n${"=".repeat(80)}`);
  console.log(`MODULE: ${module.name.toUpperCase()}`);
  console.log(`Path: ${module.path}`);
  console.log("=".repeat(80));
  console.log("");

  const moduleResults = {
    module: module.name,
    path: module.path,
    components: [],
    summary: {
      total: module.components.length,
      used: 0,
      unused: 0,
    },
  };

  module.components.forEach((component) => {
    const result = searchForUsage(component, module.path);
    moduleResults.components.push(result);

    if (result.isUsed) {
      moduleResults.summary.used++;
      console.log(`✅ ${component} (${result.totalMatches} usages)`);

      // Show first few usage examples
      result.usages.forEach((usage) => {
        if (usage.matches && usage.matches.length > 0) {
          const firstMatch = usage.matches[0];
          if (firstMatch) {
            const preview =
              firstMatch.length > 100
                ? firstMatch.substring(0, 100) + "..."
                : firstMatch;
            console.log(`   ${usage.type}: ${preview}`);
          }
        }
      });
    } else {
      moduleResults.summary.unused++;
      console.log(`❌ ${component} (NO USAGES FOUND)`);
    }
  });

  console.log("");
  console.log(
    `Summary: ${moduleResults.summary.used} used / ${moduleResults.summary.unused} unused`
  );

  allResults.push(moduleResults);
});

// Overall summary
console.log("\n" + "=".repeat(80));
console.log("OVERALL SUMMARY");
console.log("=".repeat(80));
console.log("");

allResults.forEach((module) => {
  const percentage = (
    (module.summary.used / module.summary.total) *
    100
  ).toFixed(1);
  console.log(`${module.module}:`);
  console.log(
    `  ${module.summary.used}/${module.summary.total} components used (${percentage}%)`
  );

  if (module.summary.unused > 0) {
    console.log(`  Unused components:`);
    module.components
      .filter((c) => !c.isUsed)
      .forEach((c) => console.log(`    - ${c.component}`));
  }
  console.log("");
});

// Save results
fs.writeFileSync(
  "component-usage-verification.json",
  JSON.stringify(allResults, null, 2)
);
console.log("\nDetailed results saved to: component-usage-verification.json");

// Recommendations
console.log("\n" + "=".repeat(80));
console.log("RECOMMENDATIONS");
console.log("=".repeat(80));
console.log("");

const totalUnused = allResults.reduce((acc, m) => acc + m.summary.unused, 0);
const totalComponents = allResults.reduce((acc, m) => acc + m.summary.total, 0);

if (totalUnused === 0) {
  console.log("✅ All components are being used! No dead components found.");
  console.log("");
  console.log('The "unused exports" from ts-prune are likely just:');
  console.log("  - Barrel index.ts files (safe to delete)");
  console.log("  - Service contracts (used by Inversify)");
  console.log("  - Type definitions (used at compile time)");
} else {
  console.log(
    `⚠️  Found ${totalUnused}/${totalComponents} components with no direct usages.`
  );
  console.log("");
  console.log("Before archiving, verify:");
  console.log("  1. Component might be used dynamically");
  console.log("  2. Component might be loaded lazily");
  console.log("  3. Component might be a future feature");
  console.log("");
  console.log("Components to investigate:");
  allResults.forEach((module) => {
    module.components
      .filter((c) => !c.isUsed)
      .forEach((c) => console.log(`  - ${module.module}/${c.component}`));
  });
}

console.log("");
