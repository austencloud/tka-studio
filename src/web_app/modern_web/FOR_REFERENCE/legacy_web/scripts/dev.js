#!/usr/bin/env node

/**
 * Custom development server script
 * Runs Vite with minimal logging but shows the localhost URL
 */

import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

// Get current file directory (ESM equivalent of __dirname)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create scripts directory if it doesn't exist
const scriptsDir = path.join(process.cwd(), "scripts");
if (!fs.existsSync(scriptsDir)) {
  fs.mkdirSync(scriptsDir, { recursive: true });
}

// Colors for console output
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
};

// Find an available port starting from 5175
async function findAvailablePort(startPort) {
  const net = await import("net");

  function isPortAvailable(port) {
    return new Promise((resolve) => {
      const server = net.default.createServer();

      server.once("error", () => {
        resolve(false);
      });

      server.once("listening", () => {
        server.close();
        resolve(true);
      });

      server.listen(port);
    });
  }

  let port = startPort;
  while (!(await isPortAvailable(port))) {
    port++;
  }

  return port;
}

// Main function
async function main() {
  // Clear console
  console.clear();

  // Show startup message
  console.log(
    `${colors.bright}${colors.cyan}Starting development server...${colors.reset}\n`,
  );

  // Find available port
  const port = await findAvailablePort(5175);

  // Prepare Vite command
  const args = ["dev", "--logLevel=error"];

  // Add any command line arguments passed to this script
  process.argv.slice(2).forEach((arg) => {
    if (arg !== "--logLevel=error") {
      args.push(arg);
    }
  });

  // Start Vite
  const vite = spawn("vite", args, {
    stdio: ["inherit", "pipe", "pipe"],
    shell: true,
  });

  // Handle Vite output
  let serverStarted = false;

  vite.stdout.on("data", (data) => {
    const output = data.toString();

    // Only show the URL when the server is ready
    if (output.includes("VITE") && output.includes("ready")) {
      serverStarted = true;

      // Show the localhost URL
      console.log(
        `\n${colors.bright}${colors.green}Server running at:${colors.reset}`,
      );
      console.log(
        `${colors.bright}${colors.yellow}➜ Local:   ${colors.cyan}http://localhost:${port}/${colors.reset}`,
      );
      console.log(
        `\n${colors.bright}${colors.green}Ready for development!${colors.reset}`,
      );
    }

    // Show any error messages
    if (output.includes("ERROR")) {
      console.error(output);
    }
  });

  vite.stderr.on("data", (data) => {
    console.error(data.toString());
  });

  // Handle process exit
  vite.on("close", (code) => {
    if (code !== 0) {
      console.log(
        `\n${colors.bright}Vite process exited with code ${code}${colors.reset}`,
      );
    }
  });

  // Handle termination signals
  ["SIGINT", "SIGTERM"].forEach((signal) => {
    process.on(signal, () => {
      vite.kill(signal);
      process.exit();
    });
  });

  // Show URL after a timeout if it hasn't been shown yet
  setTimeout(() => {
    if (!serverStarted) {
      console.log(
        `\n${colors.bright}${colors.green}Server should be running at:${colors.reset}`,
      );
      console.log(
        `${colors.bright}${colors.yellow}➜ Local:   ${colors.cyan}http://localhost:${port}/${colors.reset}`,
      );
    }
  }, 3000);
}

main().catch((err) => {
  console.error("Error starting development server:", err);
  process.exit(1);
});
