#!/usr/bin/env node

/**
 * Dependency Usage Analysis Script
 *
 * Analyzes which dependencies in package.json are actually used in the codebase
 */

import fs from "fs/promises";
import path from "path";

// Dependencies to analyze
const DEPENDENCIES_TO_CHECK = [
  "@tauri-apps/plugin-store",
  "@xstate/svelte",
  "fabric",
  "file-saver",
  "html2canvas",
  "inversify",
  "lodash",
  "lodash-es",
  "lucide-svelte",
  "lz-string",
  "reflect-metadata",
  "xstate",
  "zod",
];

// Common import patterns for each dependency
const IMPORT_PATTERNS = {
  "@tauri-apps/plugin-store": [
    /import.*from.*["']@tauri-apps\/plugin-store["']/,
    /require\(["']@tauri-apps\/plugin-store["']\)/,
  ],
  "@xstate/svelte": [
    /import.*from.*["']@xstate\/svelte["']/,
    /require\(["']@xstate\/svelte["']\)/,
  ],
  fabric: [
    /import.*from.*["']fabric["']/,
    /require\(["']fabric["']\)/,
    /import.*{.*}.*from.*["']fabric["']/,
  ],
  "file-saver": [
    /import.*from.*["']file-saver["']/,
    /require\(["']file-saver["']\)/,
    /import.*saveAs/,
  ],
  html2canvas: [
    /import.*from.*["']html2canvas["']/,
    /require\(["']html2canvas["']\)/,
    /import.*html2canvas/,
    /loadHtml2Canvas/,
    /html2canvas\(/,
  ],
  inversify: [
    /import.*from.*["']inversify["']/,
    /require\(["']inversify["']\)/,
    /@injectable/,
    /@inject/,
    /Container/,
  ],
  lodash: [
    /import.*from.*["']lodash["']/,
    /require\(["']lodash["']\)/,
    /import.*_.*from.*["']lodash["']/,
  ],
  "lodash-es": [
    /import.*from.*["']lodash-es["']/,
    /require\(["']lodash-es["']\)/,
  ],
  "lucide-svelte": [
    /import.*from.*["']lucide-svelte["']/,
    /require\(["']lucide-svelte["']\)/,
  ],
  "lz-string": [
    /import.*from.*["']lz-string["']/,
    /require\(["']lz-string["']\)/,
    /LZString/,
    /LZ\.compress/,
    /LZ\.decompress/,
  ],
  "reflect-metadata": [
    /import.*["']reflect-metadata["']/,
    /require\(["']reflect-metadata["']\)/,
  ],
  xstate: [
    /import.*from.*["']xstate["']/,
    /require\(["']xstate["']\)/,
    /createMachine/,
    /assign/,
    /interpret/,
  ],
  zod: [
    /import.*from.*["']zod["']/,
    /require\(["']zod["']\)/,
    /import.*{.*z.*}.*from.*["']zod["']/,
    /\.parse\(/,
    /\.parseStrict\(/,
  ],
};

async function getAllSourceFiles() {
  const files = [];

  async function scanDirectory(dir) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
          // Skip certain directories
          if (
            !["node_modules", "build", ".svelte-kit", "dist", ".git"].includes(
              entry.name
            )
          ) {
            await scanDirectory(fullPath);
          }
        } else if (entry.isFile()) {
          // Include relevant file types
          if (/\.(js|ts|jsx|tsx|svelte)$/.test(entry.name)) {
            files.push(fullPath);
          }
        }
      }
    } catch (error) {
      console.warn(
        `Warning: Could not scan directory ${dir}: ${error.message}`
      );
    }
  }

  await scanDirectory(".");
  return files;
}

async function analyzeFile(filePath, dependency, patterns) {
  try {
    const content = await fs.readFile(filePath, "utf-8");
    const matches = [];

    for (const pattern of patterns) {
      const regexMatches = [...content.matchAll(new RegExp(pattern, "gm"))];
      if (regexMatches.length > 0) {
        matches.push(
          ...regexMatches.map((match) => ({
            pattern: pattern.toString(),
            match: match[0],
            line: content.substring(0, match.index).split("\n").length,
          }))
        );
      }
    }

    return matches;
  } catch (error) {
    console.warn(`Warning: Could not read ${filePath}: ${error.message}`);
    return [];
  }
}

async function analyzeAllDependencies() {
  console.log("🔍 Analyzing dependency usage...\n");

  const sourceFiles = await getAllSourceFiles();
  console.log(`📁 Found ${sourceFiles.length} source files to analyze\n`);

  const results = {};

  for (const dependency of DEPENDENCIES_TO_CHECK) {
    console.log(`📦 Checking ${dependency}...`);
    const patterns = IMPORT_PATTERNS[dependency] || [];
    const usages = [];

    for (const file of sourceFiles) {
      const matches = await analyzeFile(file, dependency, patterns);
      if (matches.length > 0) {
        usages.push({ file, matches });
      }
    }

    results[dependency] = usages;

    if (usages.length > 0) {
      console.log(`  ✅ Found ${usages.length} file(s) using ${dependency}`);
    } else {
      console.log(`  ❌ No usage found for ${dependency}`);
    }
  }

  return results;
}

function generateReport(results) {
  console.log("\n" + "=".repeat(60));
  console.log("📊 DEPENDENCY USAGE ANALYSIS REPORT");
  console.log("=".repeat(60));

  const used = [];
  const unused = [];

  for (const [dependency, usages] of Object.entries(results)) {
    if (usages.length > 0) {
      used.push({ dependency, usages });
    } else {
      unused.push(dependency);
    }
  }

  console.log("\n✅ DEPENDENCIES IN USE:");
  console.log("-".repeat(30));
  if (used.length === 0) {
    console.log("None found");
  } else {
    used.forEach(({ dependency, usages }) => {
      console.log(`\n📦 ${dependency}`);
      usages.forEach(({ file, matches }) => {
        console.log(`  📄 ${file} (${matches.length} usage(s))`);
        matches.slice(0, 3).forEach((match) => {
          console.log(`    Line ${match.line}: ${match.match.trim()}`);
        });
        if (matches.length > 3) {
          console.log(`    ... and ${matches.length - 3} more`);
        }
      });
    });
  }

  console.log("\n❌ UNUSED DEPENDENCIES (safe to remove):");
  console.log("-".repeat(30));
  if (unused.length === 0) {
    console.log("All dependencies are in use! 🎉");
  } else {
    unused.forEach((dep) => {
      console.log(`🗑️  ${dep}`);
    });

    console.log(
      `\n💡 You can remove these ${unused.length} unused dependencies to reduce bundle size:`
    );
    console.log("\nnpm uninstall " + unused.join(" "));
  }

  console.log("\n" + "=".repeat(60));
  console.log(`📈 Summary: ${used.length} used, ${unused.length} unused`);
  console.log("=".repeat(60));
}

async function main() {
  try {
    const results = await analyzeAllDependencies();
    generateReport(results);
  } catch (error) {
    console.error("❌ Analysis failed:", error);
    process.exit(1);
  }
}

main();
