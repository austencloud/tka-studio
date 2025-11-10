/**
 * Responsive Image Generator
 *
 * Generates multiple sizes of gallery images for responsive loading:
 * - Small: 200px width (mobile thumbnail grid)
 * - Medium: 600px width (tablet, desktop grid)
 * - Large: 1900px width (full resolution, existing files)
 *
 * This dramatically improves mobile performance by serving appropriately sized images.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const SIZES = {
  small: 200,   // Mobile (200px grid cells)
  medium: 600,  // Tablet/Desktop grid
  // large: 1900   // Keep original (already exists)
};

const QUALITY = 85; // WebP quality (0-100)

/**
 * Generate responsive versions of a single image
 */
async function generateResponsiveVersions(imagePath) {
  try {
    const dir = path.dirname(imagePath);
    const ext = path.extname(imagePath);
    const basename = path.basename(imagePath, ext);

    // Read original image
    const image = sharp(imagePath);
    const metadata = await image.metadata();

    console.log(`Processing: ${basename} (${metadata.width}x${metadata.height})`);

    // Generate each size
    for (const [sizeName, targetWidth] of Object.entries(SIZES)) {
      const outputPath = path.join(dir, `${basename}_${sizeName}.webp`);

      // Skip if already exists
      if (fs.existsSync(outputPath)) {
        console.log(`  ⏭️  ${sizeName}: exists`);
        continue;
      }

      // Calculate height maintaining aspect ratio
      const aspectRatio = metadata.height / metadata.width;
      const targetHeight = Math.round(targetWidth * aspectRatio);

      // Generate resized image
      await sharp(imagePath)
        .resize(targetWidth, targetHeight, {
          fit: 'inside',
          withoutEnlargement: true,
        })
        .webp({ quality: QUALITY })
        .toFile(outputPath);

      const stats = fs.statSync(outputPath);
      const sizeMB = (stats.size / 1024).toFixed(1);
      console.log(`  ✓ ${sizeName}: ${targetWidth}x${targetHeight} (${sizeMB}KB)`);
    }

    return true;
  } catch (error) {
    console.error(`  ❌ ERROR: ${error.message}`);
    return false;
  }
}

/**
 * Process all images in gallery directory
 */
async function processGallery(dryRun = true) {
  const galleryPath = path.join(__dirname, 'static', 'gallery');

  console.log('================================================================================');
  console.log('RESPONSIVE IMAGE GENERATOR');
  console.log('================================================================================');
  console.log(`Mode: ${dryRun ? 'DRY RUN (use --execute to generate)' : 'EXECUTE'}`);
  console.log(`Gallery Path: ${galleryPath}`);
  console.log(`Sizes: ${Object.entries(SIZES).map(([name, width]) => `${name}=${width}px`).join(', ')}`);
  console.log('--------------------------------------------------------------------------------\n');

  if (!fs.existsSync(galleryPath)) {
    console.error(`ERROR: Gallery directory not found: ${galleryPath}`);
    process.exit(1);
  }

  const results = {
    processed: 0,
    succeeded: 0,
    failed: 0,
    skipped: 0,
  };

  // Recursively find all WebP files
  function findWebPFiles(dir) {
    const files = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
      const itemPath = path.join(dir, item);
      const stat = fs.statSync(itemPath);

      if (stat.isDirectory()) {
        files.push(...findWebPFiles(itemPath));
      } else if (item.endsWith('.webp') && !item.includes('_small') && !item.includes('_medium')) {
        // Only process original files (not already generated responsive versions)
        files.push(itemPath);
      }
    }

    return files;
  }

  const imageFiles = findWebPFiles(galleryPath);
  console.log(`Found ${imageFiles.length} original images\n`);

  if (dryRun) {
    console.log('DRY RUN - No files will be generated\n');
    // Just show what would be done
    for (const file of imageFiles.slice(0, 5)) {
      const basename = path.basename(file, '.webp');
      console.log(`Would process: ${basename}`);
      for (const sizeName of Object.keys(SIZES)) {
        console.log(`  → ${basename}_${sizeName}.webp`);
      }
    }
    console.log(`\n... and ${imageFiles.length - 5} more files\n`);
  } else {
    // Process all images
    for (const file of imageFiles) {
      results.processed++;
      const success = await generateResponsiveVersions(file);

      if (success) {
        results.succeeded++;
      } else {
        results.failed++;
      }
    }
  }

  console.log('\n================================================================================');
  console.log('SUMMARY');
  console.log('================================================================================');
  console.log(`Total Images: ${imageFiles.length}`);
  console.log(`Processed: ${results.processed}`);
  console.log(`Succeeded: ${results.succeeded}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Skipped: ${results.skipped}`);
  console.log('================================================================================');

  if (dryRun) {
    console.log('\nThis was a DRY RUN. No files were generated.');
    console.log('Run with --execute to generate responsive images.');
  } else {
    console.log('\n✅ Responsive images generated successfully!');
    console.log('\nNext steps:');
    console.log('1. Update gallery-manifest.json with srcset URLs');
    console.log('2. Update ExploreThumbnailImage.svelte to use srcset');
    console.log('3. Test on mobile device');
  }
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--execute');

  // Check if sharp is installed
  try {
    await import('sharp');
  } catch (error) {
    console.error('ERROR: sharp package not found');
    console.error('Install it with: npm install sharp');
    process.exit(1);
  }

  await processGallery(dryRun);
}

main().catch(console.error);
