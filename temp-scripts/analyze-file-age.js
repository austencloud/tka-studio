#!/usr/bin/env node

/**
 * File Age Analysis Tool
 * Cross-references ts-prune results with git history to find old unused files
 */

import fs from "fs";
import { execSync } from "child_process";

// Read the JSON report from dead code analysis
const jsonReport = JSON.parse(
  fs.readFileSync("dead-code-analysis.json", "utf-8")
);

console.log("=".repeat(80));
console.log("FILE AGE ANALYSIS FOR POTENTIALLY DEAD CODE");
console.log("=".repeat(80));
console.log("");

// Get the top files with most unused exports
const topFiles = jsonReport.topFiles.slice(0, 30);

console.log("Analyzing git history for files with most unused exports...");
console.log("");

const results = [];

topFiles.forEach(({ file, count }) => {
  try {
    // Get last modification date
    const lastModified = execSync(`git log -1 --format="%ai" -- "${file}"`, {
      encoding: "utf-8",
    }).trim();

    // Get total number of commits
    const commitCount = execSync(`git log --oneline -- "${file}" | wc -l`, {
      encoding: "utf-8",
    }).trim();

    // Get the author of last modification
    const lastAuthor = execSync(`git log -1 --format="%an" -- "${file}"`, {
      encoding: "utf-8",
    }).trim();

    results.push({
      file,
      unusedExports: count,
      lastModified,
      commitCount: parseInt(commitCount),
      lastAuthor,
    });
  } catch (error) {
    // File might be new or untracked
    results.push({
      file,
      unusedExports: count,
      lastModified: "Never committed",
      commitCount: 0,
      lastAuthor: "N/A",
    });
  }
});

// Sort by last modified date (oldest first)
results.sort((a, b) => {
  if (a.lastModified === "Never committed") return 1;
  if (b.lastModified === "Never committed") return -1;
  return new Date(a.lastModified) - new Date(b.lastModified);
});

console.log("TOP CANDIDATES FOR ARCHIVING");
console.log("(Old files with many unused exports)");
console.log("-".repeat(80));
console.log("");

results.forEach((result, index) => {
  const date =
    result.lastModified === "Never committed"
      ? "Never committed"
      : new Date(result.lastModified).toLocaleDateString();

  console.log(`${index + 1}. ${result.file}`);
  console.log(`   Unused exports: ${result.unusedExports}`);
  console.log(`   Last modified: ${date}`);
  console.log(`   Commits: ${result.commitCount}`);
  console.log(`   Last author: ${result.lastAuthor}`);
  console.log("");
});

// Find files not modified in the last 6 months
const sixMonthsAgo = new Date();
sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

const oldFiles = results.filter((r) => {
  if (r.lastModified === "Never committed") return false;
  return new Date(r.lastModified) < sixMonthsAgo;
});

console.log("=".repeat(80));
console.log(`FILES NOT MODIFIED IN LAST 6 MONTHS (${oldFiles.length} files)`);
console.log("-".repeat(80));
console.log("");

oldFiles.forEach((result, index) => {
  const date = new Date(result.lastModified).toLocaleDateString();
  console.log(`${index + 1}. ${result.file}`);
  console.log(
    `   Unused: ${result.unusedExports} | Last: ${date} | Commits: ${result.commitCount}`
  );
  console.log("");
});

// Save detailed results
fs.writeFileSync("file-age-analysis.json", JSON.stringify(results, null, 2));
console.log("Detailed results saved to: file-age-analysis.json");
