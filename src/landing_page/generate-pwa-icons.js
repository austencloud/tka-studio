import fs from "fs";
import path from "path";
import { execSync } from "child_process";

// This script assumes you have ImageMagick installed
// If not, you can manually resize the images or use another tool

const SOURCE_ICON = path.resolve("./static/favicon.png");
const PWA_DIR = path.resolve("./static/pwa");
const SIZES = [72, 96, 128, 144, 152, 192, 384, 512];

// Ensure PWA directory exists
if (!fs.existsSync(PWA_DIR)) {
  fs.mkdirSync(PWA_DIR, { recursive: true });
  console.log("Created PWA icons directory");
}

// Generate icons of different sizes
SIZES.forEach((size) => {
  try {
    const outputFile = path.join(PWA_DIR, `icon-${size}x${size}.png`);
    execSync(`convert ${SOURCE_ICON} -resize ${size}x${size} ${outputFile}`);
    console.log(`Generated ${size}x${size} icon`);
  } catch (error) {
    console.error(`Error generating ${size}x${size} icon:`, error.message);
    console.log(
      "Make sure ImageMagick is installed or create the icon manually.",
    );
  }
});

// Generate maskable icon (with padding for safe area)
try {
  const outputFile = path.join(PWA_DIR, "maskable-icon-512x512.png");
  execSync(
    `convert ${SOURCE_ICON} -resize 384x384 -background none -gravity center -extent 512x512 ${outputFile}`,
  );
  console.log("Generated maskable icon");
} catch (error) {
  console.error("Error generating maskable icon:", error.message);
}

console.log("PWA icon generation complete");
