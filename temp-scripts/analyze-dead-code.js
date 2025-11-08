#!/usr/bin/env node

/**
 * Dead Code Analysis Tool
 * Analyzes ts-prune output to identify potentially unused code
 */

import fs from "fs";
import path from "path";

// Read the ts-prune report
const reportPath = "ts-prune-full-report.txt";
const reportContent = fs.readFileSync(reportPath, "utf-8");
const lines = reportContent.split("\n").filter((line) => line.trim());

// Categories for analysis
const categories = {
  modules: [],
  shared: [],
  routes: [],
  config: [],
  tests: [],
  generated: [],
  other: [],
};

const moduleBreakdown = {};
const sharedBreakdown = {};

// Parse each line
lines.forEach((line) => {
  const match = line.match(/^\\src\\(.+?):(\d+) - (.+)$/);
  if (!match) return;

  const [, filePath, lineNum, exportName] = match;
  const fullPath = `src\\${filePath}`;

  const entry = {
    file: fullPath,
    line: parseInt(lineNum),
    export: exportName,
    isUsedInModule: line.includes("(used in module)"),
  };

  // Categorize
  if (filePath.startsWith("lib\\modules\\")) {
    categories.modules.push(entry);

    // Extract module name
    const moduleMatch = filePath.match(/lib\\modules\\([^\\]+)/);
    if (moduleMatch) {
      const moduleName = moduleMatch[1];
      if (!moduleBreakdown[moduleName]) {
        moduleBreakdown[moduleName] = [];
      }
      moduleBreakdown[moduleName].push(entry);
    }
  } else if (filePath.startsWith("lib\\shared\\")) {
    categories.shared.push(entry);

    // Extract shared category
    const sharedMatch = filePath.match(/lib\\shared\\([^\\]+)/);
    if (sharedMatch) {
      const sharedCategory = sharedMatch[1];
      if (!sharedBreakdown[sharedCategory]) {
        sharedBreakdown[sharedCategory] = [];
      }
      sharedBreakdown[sharedCategory].push(entry);
    }
  } else if (filePath.startsWith("routes\\")) {
    categories.routes.push(entry);
  } else if (filePath.startsWith("config\\")) {
    categories.config.push(entry);
  } else if (filePath.startsWith("lib\\")) {
    categories.other.push(entry);
  }
});

// Also parse test files
const testLines = reportContent
  .split("\n")
  .filter((line) => line.includes("\\tests\\"));
testLines.forEach((line) => {
  const match = line.match(/^\\tests\\(.+?):(\d+) - (.+)$/);
  if (!match) return;

  const [, filePath, lineNum, exportName] = match;
  categories.tests.push({
    file: `tests\\${filePath}`,
    line: parseInt(lineNum),
    export: exportName,
    isUsedInModule: line.includes("(used in module)"),
  });
});

// Also parse .svelte-kit generated files
const generatedLines = reportContent
  .split("\n")
  .filter((line) => line.includes("\\.svelte-kit\\"));
generatedLines.forEach((line) => {
  const match = line.match(/^\\(.+?):(\d+) - (.+)$/);
  if (!match) return;

  const [, filePath, lineNum, exportName] = match;
  categories.generated.push({
    file: filePath,
    line: parseInt(lineNum),
    export: exportName,
    isUsedInModule: line.includes("(used in module)"),
  });
});

// Generate report
console.log("=".repeat(80));
console.log("DEAD CODE ANALYSIS REPORT");
console.log("=".repeat(80));
console.log("");

console.log("SUMMARY");
console.log("-".repeat(80));
console.log(`Total unused exports found: ${lines.length}`);
console.log(`  Modules:    ${categories.modules.length}`);
console.log(`  Shared:     ${categories.shared.length}`);
console.log(`  Routes:     ${categories.routes.length}`);
console.log(`  Config:     ${categories.config.length}`);
console.log(`  Tests:      ${categories.tests.length}`);
console.log(`  Generated:  ${categories.generated.length}`);
console.log(`  Other:      ${categories.other.length}`);
console.log("");

// Module breakdown
console.log("MODULES BREAKDOWN (by module)");
console.log("-".repeat(80));
const sortedModules = Object.entries(moduleBreakdown).sort(
  (a, b) => b[1].length - a[1].length
);

sortedModules.forEach(([moduleName, items]) => {
  console.log(`  ${moduleName}: ${items.length} unused exports`);
});
console.log("");

// Shared breakdown
console.log("SHARED BREAKDOWN (by category)");
console.log("-".repeat(80));
const sortedShared = Object.entries(sharedBreakdown).sort(
  (a, b) => b[1].length - a[1].length
);

sortedShared.forEach(([category, items]) => {
  console.log(`  ${category}: ${items.length} unused exports`);
});
console.log("");

// Top offenders - files with most unused exports
console.log("TOP FILES WITH MOST UNUSED EXPORTS");
console.log("-".repeat(80));

const fileGroups = {};
[...categories.modules, ...categories.shared, ...categories.other].forEach(
  (entry) => {
    if (!fileGroups[entry.file]) {
      fileGroups[entry.file] = [];
    }
    fileGroups[entry.file].push(entry);
  }
);

const sortedFiles = Object.entries(fileGroups)
  .sort((a, b) => b[1].length - a[1].length)
  .slice(0, 20);

sortedFiles.forEach(([file, items]) => {
  console.log(`  ${file}: ${items.length} exports`);
});
console.log("");

// Detailed module reports
console.log("DETAILED MODULE REPORTS");
console.log("=".repeat(80));
console.log("");

sortedModules.forEach(([moduleName, items]) => {
  console.log(
    `MODULE: ${moduleName.toUpperCase()} (${items.length} unused exports)`
  );
  console.log("-".repeat(80));

  // Group by file
  const moduleFileGroups = {};
  items.forEach((item) => {
    if (!moduleFileGroups[item.file]) {
      moduleFileGroups[item.file] = [];
    }
    moduleFileGroups[item.file].push(item);
  });

  Object.entries(moduleFileGroups)
    .sort((a, b) => b[1].length - a[1].length)
    .forEach(([file, fileItems]) => {
      console.log(`  ${file} (${fileItems.length}):`);
      fileItems.slice(0, 10).forEach((item) => {
        const marker = item.isUsedInModule ? "(internal)" : "(UNUSED)";
        console.log(`    - ${item.export} ${marker}`);
      });
      if (fileItems.length > 10) {
        console.log(`    ... and ${fileItems.length - 10} more`);
      }
    });
  console.log("");
});

// Generate JSON report for further analysis
const jsonReport = {
  summary: {
    total: lines.length,
    byCategory: {
      modules: categories.modules.length,
      shared: categories.shared.length,
      routes: categories.routes.length,
      config: categories.config.length,
      tests: categories.tests.length,
      generated: categories.generated.length,
      other: categories.other.length,
    },
  },
  moduleBreakdown: Object.fromEntries(
    Object.entries(moduleBreakdown).map(([name, items]) => [
      name,
      {
        count: items.length,
        files: Object.keys(
          items.reduce((acc, item) => {
            acc[item.file] = true;
            return acc;
          }, {})
        ),
      },
    ])
  ),
  sharedBreakdown: Object.fromEntries(
    Object.entries(sharedBreakdown).map(([name, items]) => [
      name,
      {
        count: items.length,
        files: Object.keys(
          items.reduce((acc, item) => {
            acc[item.file] = true;
            return acc;
          }, {})
        ),
      },
    ])
  ),
  topFiles: sortedFiles.map(([file, items]) => ({
    file,
    count: items.length,
    exports: items.map((i) => i.export),
  })),
};

fs.writeFileSync(
  "dead-code-analysis.json",
  JSON.stringify(jsonReport, null, 2)
);
console.log("JSON report saved to: dead-code-analysis.json");
console.log("");

// Recommendations
console.log("RECOMMENDATIONS");
console.log("=".repeat(80));
console.log("");
console.log("1. IGNORE THESE (not actually dead code):");
console.log("   - Routes (exported for SvelteKit)");
console.log("   - Tests (test helpers may not be fully used yet)");
console.log("   - Generated files (.svelte-kit)");
console.log("   - Config files (may be used at build time)");
console.log('   - Exports marked "(used in module)" (internal use only)');
console.log("");
console.log("2. INVESTIGATE THESE (likely candidates for archiving):");
console.log("");

// Find modules with high unused export counts
const highUnusedModules = sortedModules.filter(([, items]) => {
  const trulyUnused = items.filter((item) => !item.isUsedInModule);
  return trulyUnused.length > 20;
});

if (highUnusedModules.length > 0) {
  console.log("   High-priority modules (>20 truly unused exports):");
  highUnusedModules.forEach(([moduleName, items]) => {
    const trulyUnused = items.filter((item) => !item.isUsedInModule);
    console.log(
      `   - src/lib/modules/${moduleName}: ${trulyUnused.length} unused exports`
    );
  });
  console.log("");
}

// Find files that are entirely unused
console.log("   Files that might be entirely unused:");
const potentiallyDeadFiles = Object.entries(fileGroups)
  .filter(([, items]) => {
    const trulyUnused = items.filter((item) => !item.isUsedInModule);
    return trulyUnused.length === items.length && items.length >= 3;
  })
  .slice(0, 15);

potentiallyDeadFiles.forEach(([file, items]) => {
  console.log(`   - ${file} (${items.length} exports, all unused)`);
});

console.log("");
console.log("3. NEXT STEPS:");
console.log("   a) Review high-priority modules listed above");
console.log("   b) Check git history to see when files were last modified");
console.log(
  "   c) Search for dynamic imports or runtime usage not detected by ts-prune"
);
console.log("   d) Move confirmed dead code to archive/");
console.log("");
