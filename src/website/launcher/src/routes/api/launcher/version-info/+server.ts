import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { existsSync, readFileSync } from "fs";
import { resolve } from "path";

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { path } = await request.json();

    if (!path || typeof path !== "string") {
      return json({ error: "Invalid path" }, { status: 400 });
    }

    // Resolve path relative to the project root
    const projectRoot = resolve(process.cwd(), "..");
    const versionPath = resolve(projectRoot, path);
    const packageJsonPath = resolve(versionPath, "package.json");

    if (!existsSync(packageJsonPath)) {
      return json({ error: "package.json not found" }, { status: 404 });
    }

    const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf-8"));

    return json({
      name: packageJson.name || "Unknown",
      description: packageJson.description || "No description available",
      version: packageJson.version || "0.0.0",
      dependencies: Object.keys(packageJson.dependencies || {}),
      devDependencies: Object.keys(packageJson.devDependencies || {}),
      scripts: Object.keys(packageJson.scripts || {}),
    });
  } catch (error) {
    console.error("Version info error:", error);
    return json(
      {
        error: "Failed to get version info",
      },
      { status: 500 },
    );
  }
};
