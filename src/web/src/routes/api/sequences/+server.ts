/**
 * API endpoint to list available sequence PNG files
 */
import { json } from "@sveltejs/kit";
import { readdir } from "fs/promises";
import { join } from "path";
import { fileURLToPath } from "url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));

export async function GET() {
  try {
    const staticDir = join(__dirname, "../../../../static");
    const dictionaryDir = join(staticDir, "dictionary");

    // Read all directories in the dictionary
    const sequenceDirectories = await readdir(dictionaryDir, {
      withFileTypes: true,
    });

    const sequences: Array<{
      name: string;
      path: string;
      word: string;
    }> = [];

    // Check each directory for PNG files
    for (const dirent of sequenceDirectories) {
      if (dirent.isDirectory()) {
        const sequenceName = dirent.name;

        // Skip test sequences and invalid entries
        if (
          sequenceName === "A_A" ||
          sequenceName.length < 2 ||
          sequenceName.includes("test")
        ) {
          continue;
        }

        const sequenceDir = join(dictionaryDir, sequenceName);

        try {
          const files = await readdir(sequenceDir);
          const pngFile = files.find((file) => file.endsWith("_ver1.png"));

          if (pngFile) {
            sequences.push({
              name: pngFile,
              path: `/dictionary/${sequenceName}/${pngFile}`,
              word: sequenceName,
            });
          }
        } catch (error) {
          // Skip directories we can't read
          console.warn(`Could not read directory ${sequenceName}:`, error);
        }
      }
    }

    // Also check the thumbnails directory
    try {
      const thumbnailsDir = join(staticDir, "thumbnails");
      const thumbnailFiles = await readdir(thumbnailsDir);

      for (const file of thumbnailFiles) {
        if (file.endsWith(".png")) {
          const word = file.replace(/(_ver\d+)?\.png$/, "");

          // Skip test sequences and invalid entries
          if (word === "A_A" || word.length < 2 || word.includes("test")) {
            continue;
          }

          sequences.push({
            name: file,
            path: `/thumbnails/${file}`,
            word: word,
          });
        }
      }
    } catch (error) {
      // Thumbnails directory might not exist
      console.warn("Could not read thumbnails directory:", error);
    }

    // Sort by word name
    sequences.sort((a, b) => a.word.localeCompare(b.word));

    return json({
      success: true,
      sequences,
      count: sequences.length,
    });
  } catch (error) {
    console.error("Error listing sequences:", error);
    return json(
      {
        success: false,
        error: "Failed to list sequences",
        sequences: [],
        count: 0,
      },
      { status: 500 },
    );
  }
}
