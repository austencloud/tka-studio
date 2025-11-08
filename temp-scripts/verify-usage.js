#!/usr/bin/env node

/**
 * Usage Verification Tool
 * Verifies if supposedly "unused" exports are actually used through dynamic imports,
 * Svelte components, or other patterns that ts-prune might miss
 */

import fs from "fs";
import { execSync } from "child_process";

console.log("=".repeat(80));
console.log("USAGE VERIFICATION TOOL");
console.log("=".repeat(80));
console.log("");

// Read the dead code analysis
const jsonReport = JSON.parse(
  fs.readFileSync("dead-code-analysis.json", "utf-8")
);

// Focus on the "entirely unused" files
const suspiciousFiles = [
  "src/lib/modules/about/components/index.ts",
  "src/lib/modules/about/services/index.ts",
  "src/lib/modules/about/state/index.ts",
  "src/lib/modules/word-card/components/index.ts",
  "src/lib/modules/word-card/domain/index.ts",
  "src/lib/modules/word-card/state/index.ts",
  "src/lib/modules/write/components/index.ts",
  "src/lib/modules/write/services/index.ts",
  "src/lib/modules/library/index.ts",
];

console.log("Checking for dynamic imports and Svelte usage patterns...");
console.log("");

const results = [];

suspiciousFiles.forEach((file) => {
  const fileName = file.split("/").pop().replace(".ts", "");
  const modulePath = file.replace("src/", "").replace(/\\/g, "/");

  // Search for various import patterns
  const searches = [
    // Direct imports from this file
    `import.*from.*['"\`].*${modulePath.replace("/index.ts", "")}`,
    // Dynamic imports
    `import\\(['"\`].*${modulePath.replace("/index.ts", "")}`,
    // Barrel re-exports
    `export.*from.*['"\`].*${modulePath.replace("/index.ts", "")}`,
  ];

  let totalMatches = 0;
  const matchDetails = [];

  searches.forEach((pattern) => {
    try {
      const result = execSync(
        `git grep -E "${pattern}" -- "*.ts" "*.svelte" "*.js" | grep -v "${file}" | wc -l`,
        { encoding: "utf-8" }
      ).trim();

      const count = parseInt(result);
      if (count > 0) {
        totalMatches += count;

        // Get actual matches
        try {
          const matches = execSync(
            `git grep -E "${pattern}" -- "*.ts" "*.svelte" "*.js" | grep -v "${file}" | head -5`,
            { encoding: "utf-8" }
          ).trim();
          if (matches) {
            matchDetails.push(matches);
          }
        } catch (e) {
          // No matches
        }
      }
    } catch (error) {
      // grep returned no results (exit code 1)
    }
  });

  results.push({
    file,
    totalMatches,
    matchDetails,
    verdict: totalMatches === 0 ? "LIKELY DEAD" : "POSSIBLY USED",
  });
});

// Print results
console.log("VERIFICATION RESULTS");
console.log("-".repeat(80));
console.log("");

results.forEach((result) => {
  console.log(`${result.verdict}: ${result.file}`);
  console.log(`  Potential usage references found: ${result.totalMatches}`);

  if (result.matchDetails.length > 0) {
    console.log("  Sample usages:");
    result.matchDetails.slice(0, 3).forEach((detail) => {
      const lines = detail.split("\n").slice(0, 2);
      lines.forEach((line) => console.log(`    ${line}`));
    });
  }
  console.log("");
});

// Summary
const likelyDead = results.filter((r) => r.verdict === "LIKELY DEAD");
const possiblyUsed = results.filter((r) => r.verdict === "POSSIBLY USED");

console.log("=".repeat(80));
console.log("SUMMARY");
console.log("-".repeat(80));
console.log(`Likely dead files: ${likelyDead.length}`);
console.log(`Possibly used files: ${possiblyUsed.length}`);
console.log("");

if (likelyDead.length > 0) {
  console.log("Files that are LIKELY DEAD and can be archived:");
  likelyDead.forEach((r) => console.log(`  - ${r.file}`));
  console.log("");
}

if (possiblyUsed.length > 0) {
  console.log("Files that might be used (manual verification needed):");
  possiblyUsed.forEach((r) =>
    console.log(`  - ${r.file} (${r.totalMatches} references)`)
  );
  console.log("");
}

// Save results
fs.writeFileSync("usage-verification.json", JSON.stringify(results, null, 2));
console.log("Detailed results saved to: usage-verification.json");
