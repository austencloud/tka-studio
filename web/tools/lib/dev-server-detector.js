/**
 * Shared dev server port auto-detection utility
 * Usage: import { findDevServerPort } from "./lib/dev-server-detector.js"
 */

export async function findDevServerPort() {
  const commonPorts = [5173, 5174, 5175, 5176, 5177];

  console.log("🔍 Checking for running dev server...");

  for (const port of commonPorts) {
    try {
      console.log(`   Trying port ${port}...`);
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      const response = await fetch(`http://localhost:${port}`, {
        method: "HEAD",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        console.log(`✅ Found dev server running on port ${port}`);
        return `http://localhost:${port}`;
      }
    } catch (error) {
      // Port not available, continue checking
      console.log(`   ❌ Port ${port}: ${error.message.substring(0, 50)}...`);
    }
  }

  // Check if we can at least see the process is running
  console.log("\n🔍 Manual verification steps:");
  console.log("1. Check if dev server is running: npm run dev");
  console.log(
    "2. If running, try opening http://localhost:5173 in your browser"
  );
  console.log("3. This might be a Windows/WSL networking issue");

  throw new Error(
    `❌ No dev server found on common ports: ${commonPorts.join(", ")}`
  );
}
