const sharp = require("sharp");
const path = require("path");

async function checkMetadata() {
  const testFiles = [
    { file: "BΦ-_ver1.webp", dir: "BΦ-" },
    { file: "A_ver1.webp", dir: "A" },
    { file: "TEST_ver1.webp", dir: "A" },
  ];

  for (const { file, dir } of testFiles) {
    const fullPath = path.join("..", "static", "Explore", dir, file);
    try {
      const metadata = await sharp(fullPath).metadata();
      console.log(`\n=== ${file} ===`);
      console.log("Has EXIF:", !!metadata.exif);
      console.log(
        "EXIF size:",
        metadata.exif ? metadata.exif.length : 0,
        "bytes"
      );

      if (metadata.exif) {
        const exifHex = metadata.exif.toString("hex");
        const exifString = metadata.exif.toString("ascii");

        console.log(
          "EXIF hex preview (first 200 chars):",
          exifHex.substring(0, 200)
        );
        console.log(
          "EXIF string preview (first 200 chars):",
          exifString.substring(0, 200).replace(/[^\x20-\x7E]/g, ".")
        );

        // Look for UserComment tag (0x9286) in hex
        const userCommentTag = "8692"; // 0x9286 in little-endian hex
        const userCommentPos = exifHex.indexOf(userCommentTag);
        console.log(
          "UserComment tag (0x9286) found at position:",
          userCommentPos
        );

        // Look for JSON patterns
        const hasJson =
          exifString.includes("sequence") || exifString.includes("{");
        console.log("Contains JSON-like content:", hasJson);

        if (hasJson) {
          const jsonStart = exifString.indexOf("{");
          if (jsonStart !== -1) {
            console.log("JSON starts at position:", jsonStart);
            console.log(
              "JSON preview:",
              exifString.substring(jsonStart, jsonStart + 100)
            );
          }
        }
      }
    } catch (error) {
      console.error(`Error reading ${file}:`, error.message);
    }
  }
}

checkMetadata().catch(console.error);

checkMetadata().catch(console.error);
