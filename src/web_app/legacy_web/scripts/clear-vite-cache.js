#!/usr/bin/env node

/**
 * Script to clear Vite's dependency cache
 * This is useful when you're having issues with dependencies not being properly optimized
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

// Get current file directory (ESM equivalent of __dirname)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

// Colors for console output
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  dim: "\x1b[2m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  cyan: "\x1b[36m",
};

// Directories to clean
const directoriesToClean = [
  path.join(rootDir, "node_modules", ".vite"),
  path.join(rootDir, ".svelte-kit"),
  path.join(rootDir, "node_modules", ".cache"),
];

// Files to clean
const filesToClean = [path.join(rootDir, "vite.config.ts.timestamp-*.mjs")];

console.log(
  `${colors.bright}${colors.cyan}Clearing Vite cache...${colors.reset}\n`,
);

// Clear directories
directoriesToClean.forEach((dir) => {
  if (fs.existsSync(dir)) {
    try {
      console.log(`${colors.yellow}Removing directory:${colors.reset} ${dir}`);
      fs.rmSync(dir, { recursive: true, force: true });
      console.log(`${colors.green}✓ Successfully removed${colors.reset}`);
    } catch (error) {
      console.error(
        `${colors.red}Error removing ${dir}:${colors.reset}`,
        error,
      );
    }
  } else {
    console.log(
      `${colors.dim}Directory does not exist, skipping:${colors.reset} ${dir}`,
    );
  }
});

// Clear files using glob patterns
filesToClean.forEach((filePattern) => {
  const basePath = path.dirname(filePattern);
  const fileName = path.basename(filePattern);

  if (fs.existsSync(basePath)) {
    try {
      const files = fs.readdirSync(basePath);
      const matchingFiles = files.filter((file) => {
        // Convert glob pattern to regex
        const regexPattern = fileName
          .replace(/\./g, "\\.")
          .replace(/\*/g, ".*");
        return new RegExp(`^${regexPattern}$`).test(file);
      });

      matchingFiles.forEach((file) => {
        const fullPath = path.join(basePath, file);
        console.log(
          `${colors.yellow}Removing file:${colors.reset} ${fullPath}`,
        );
        fs.unlinkSync(fullPath);
        console.log(`${colors.green}✓ Successfully removed${colors.reset}`);
      });
    } catch (error) {
      console.error(
        `${colors.red}Error processing ${filePattern}:${colors.reset}`,
        error,
      );
    }
  } else {
    console.log(
      `${colors.dim}Directory does not exist, skipping:${colors.reset} ${basePath}`,
    );
  }
});

// Clear npm cache for html2canvas
try {
  console.log(
    `${colors.yellow}Clearing npm cache for html2canvas...${colors.reset}`,
  );
  execSync("npm cache clean --force html2canvas", { stdio: "inherit" });
  console.log(`${colors.green}✓ Successfully cleared npm cache${colors.reset}`);
} catch (error) {
  console.error(`${colors.red}Error clearing npm cache:${colors.reset}`, error);
}

console.log(
  `\n${colors.bright}${colors.green}Vite cache cleared successfully!${colors.reset}`,
);
console.log(
  `${colors.cyan}You can now restart your development server with:${colors.reset}`,
);
console.log(`${colors.bright}npm run dev:clean${colors.reset}`);
