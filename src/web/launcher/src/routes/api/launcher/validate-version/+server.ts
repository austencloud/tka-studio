import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { existsSync } from "fs";
import { resolve } from "path";

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { path } = await request.json();

    if (!path || typeof path !== "string") {
      return json({ valid: false, error: "Invalid path" }, { status: 400 });
    }

    // Resolve path relative to the project root
    const projectRoot = resolve(process.cwd(), "..");
    const versionPath = resolve(projectRoot, path);

    // Check if package.json and src directory exist
    const packageJsonPath = resolve(versionPath, "package.json");
    const srcPath = resolve(versionPath, "src");

    const packageJsonExists = existsSync(packageJsonPath);
    const srcExists = existsSync(srcPath);

    const valid = packageJsonExists && srcExists;

    return json({
      valid,
      details: {
        packageJson: packageJsonExists,
        src: srcExists,
        path: versionPath,
      },
    });
  } catch (error) {
    console.error("Version validation error:", error);
    return json(
      {
        valid: false,
        error: "Failed to validate version",
      },
      { status: 500 },
    );
  }
};
