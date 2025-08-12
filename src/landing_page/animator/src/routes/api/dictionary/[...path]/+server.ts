import { error } from "@sveltejs/kit";
import { readFile } from "fs/promises";
import { join } from "path";
import type { RequestHandler } from "./$types.js";

export const GET: RequestHandler = async ({ params }) => {
  try {
    const path = params.path;
    if (!path) {
      throw error(400, "Path is required");
    }

    // Construct the file path
    const filePath = join(
      process.cwd(),
      "src",
      "lib",
      "animator",
      "dictionary",
      path,
    );

    // Security check - ensure the path is within the dictionary directory
    if (!filePath.includes("dictionary")) {
      throw error(403, "Access denied");
    }

    // Read the file
    const fileBuffer = await readFile(filePath);

    // Determine content type based on file extension
    const contentType = path.endsWith(".png")
      ? "image/png"
      : "application/octet-stream";

    return new Response(fileBuffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600", // Cache for 1 hour
      },
    });
  } catch {
    // Error serving dictionary file
    throw error(404, "File not found");
  }
};
