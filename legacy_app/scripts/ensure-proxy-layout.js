#!/usr/bin/env node

/**
 * This script ensures that the proxy+layout.server.ts file exists
 * This file is needed by SvelteKit when using certain features like authentication
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

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

// Path to the proxy layout file
const proxyLayoutPath = path.join(
  rootDir,
  "src",
  "routes",
  "proxy+layout.server.ts",
);

// Content for the proxy layout file
const proxyLayoutContent = `// This is a placeholder proxy layout server file
// It's needed because SvelteKit is looking for this file due to the auth route structure

import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async () => {
  // This is an empty load function that doesn't do anything
  // But it satisfies SvelteKit's requirement for this file
  return {};
};
`;

// Check if the proxy layout file exists
if (!fs.existsSync(proxyLayoutPath)) {
  console.log(`${colors.yellow}Creating proxy layout file...${colors.reset}`);

  try {
    // Create the file
    fs.writeFileSync(proxyLayoutPath, proxyLayoutContent);
    console.log(
      `${colors.green}✓ Successfully created proxy layout file${colors.reset}`,
    );
  } catch (error) {
    console.error(
      `${colors.red}Error creating proxy layout file:${colors.reset}`,
      error,
    );
    process.exit(1);
  }
} else {
  console.log(
    `${colors.dim}Proxy layout file already exists, skipping...${colors.reset}`,
  );
}

// Run svelte-kit sync to regenerate types
console.log(`${colors.yellow}Running svelte-kit sync...${colors.reset}`);

// We're using ESM, so we can't use child_process.execSync directly
// Instead, we'll use a dynamic import
try {
  const { execSync } = await import("child_process");
  execSync("npx svelte-kit sync", { stdio: "inherit" });
  console.log(
    `${colors.green}✓ Successfully synced SvelteKit types${colors.reset}`,
  );
} catch (error) {
  console.error(
    `${colors.red}Error syncing SvelteKit types:${colors.reset}`,
    error,
  );
  process.exit(1);
}

console.log(
  `${colors.bright}${colors.green}Proxy layout setup complete!${colors.reset}`,
);
