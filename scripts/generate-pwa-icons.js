/**
 * Generate PWA icons at correct sizes from source image
 * Uses sharp library for high-quality image resizing
 */

import { existsSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import sharp from "sharp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Icon sizes needed for PWA
const ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512];

// Paths
const SOURCE_IMAGE = join(__dirname, "../static/Artboard 9@16x.png");
const OUTPUT_DIR = join(__dirname, "../static/pwa");

async function generateIcons() {
  console.log("🎨 Generating PWA icons from source image...\n");

  // Ensure output directory exists
  if (!existsSync(OUTPUT_DIR)) {
    mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  // Check if source image exists
  if (!existsSync(SOURCE_IMAGE)) {
    console.error("❌ Source image not found:", SOURCE_IMAGE);
    process.exit(1);
  }

  // Get source image info
  const sourceInfo = await sharp(SOURCE_IMAGE).metadata();
  console.log(`📐 Source image: ${sourceInfo.width}x${sourceInfo.height}\n`);

  // Generate each icon size
  for (const size of ICON_SIZES) {
    const outputPath = join(OUTPUT_DIR, `icon-${size}x${size}.png`);

    try {
      await sharp(SOURCE_IMAGE)
        .resize(size, size, {
          fit: "contain",
          background: { r: 11, g: 29, b: 42, alpha: 1 }, // Match theme_color from manifest
        })
        .png({ quality: 100, compressionLevel: 9 })
        .toFile(outputPath);

      console.log(`✅ Generated: icon-${size}x${size}.png`);
    } catch (error) {
      console.error(
        `❌ Failed to generate icon-${size}x${size}.png:`,
        error.message
      );
    }
  }

  // Generate maskable icon (512x512 with safe zone)
  const maskableSize = 512;
  const maskablePath = join(OUTPUT_DIR, "maskable-icon-512x512.png");

  try {
    // Maskable icons need 40% safe zone, so scale down the content
    // Calculate exact padding to ensure final size is exactly 512x512
    const contentSize = 307; // 60% of 512 = 307.2, rounded down
    const totalPadding = maskableSize - contentSize; // 205
    const paddingTop = Math.floor(totalPadding / 2); // 102
    const paddingBottom = totalPadding - paddingTop; // 103

    await sharp(SOURCE_IMAGE)
      .resize(contentSize, contentSize, {
        fit: "contain",
        background: { r: 11, g: 29, b: 42, alpha: 1 },
      })
      .extend({
        top: paddingTop,
        bottom: paddingBottom,
        left: paddingTop,
        right: paddingBottom,
        background: { r: 11, g: 29, b: 42, alpha: 1 },
      })
      .png({ quality: 100, compressionLevel: 9 })
      .toFile(maskablePath);

    console.log(`✅ Generated: maskable-icon-512x512.png (with safe zone)`);
  } catch (error) {
    console.error("❌ Failed to generate maskable icon:", error.message);
  }

  console.log("\n🎉 All PWA icons generated successfully!");
  console.log("📁 Output directory:", OUTPUT_DIR);
}

// Run the generator
generateIcons().catch((error) => {
  console.error("❌ Icon generation failed:", error);
  process.exit(1);
});
