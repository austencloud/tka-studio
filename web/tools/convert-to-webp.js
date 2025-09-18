#!/usr/bin/env node

/**
 * WebP Conversion Tool for TKA Gallery Optimization
 * 
 * Converts PNG thumbnails to WebP format for 70-80% file size reduction
 * Maintains original PNG files as fallbacks for older browsers
 * 
 * Usage:
 *   npm run optimize:images
 *   node tools/convert-to-webp.js
 */

import { promises as fs } from 'fs';
import path from 'path';
import sharp from 'sharp';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  // Source directory containing PNG files
  sourceDir: path.join(__dirname, '../static/gallery'),
  
  // WebP quality settings (0-100, higher = better quality but larger files)
  webpQuality: 85,
  
  // WebP effort (0-6, higher = better compression but slower)
  webpEffort: 6,
  
  // Whether to preserve original PNG files
  preserveOriginals: true,
  
  // File extensions to convert
  extensions: ['.png', '.PNG'],
  
  // Batch size for processing (to avoid memory issues)
  batchSize: 10
};

// Statistics tracking
const stats = {
  totalFiles: 0,
  convertedFiles: 0,
  skippedFiles: 0,
  totalOriginalSize: 0,
  totalWebpSize: 0,
  errors: []
};

/**
 * Get all PNG files recursively from a directory
 */
async function getAllPngFiles(dir) {
  const files = [];
  
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        // Recursively process subdirectories
        const subFiles = await getAllPngFiles(fullPath);
        files.push(...subFiles);
      } else if (entry.isFile() && CONFIG.extensions.includes(path.extname(entry.name))) {
        files.push(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error.message);
  }
  
  return files;
}

/**
 * Convert a single PNG file to WebP
 */
async function convertToWebP(pngPath) {
  const webpPath = pngPath.replace(/\.png$/i, '.webp');
  
  try {
    // Check if WebP already exists and is newer
    try {
      const [pngStat, webpStat] = await Promise.all([
        fs.stat(pngPath),
        fs.stat(webpPath)
      ]);
      
      if (webpStat.mtime > pngStat.mtime) {
        console.log(`⏭️  Skipping ${path.basename(pngPath)} (WebP is newer)`);
        stats.skippedFiles++;
        return;
      }
    } catch {
      // WebP doesn't exist, continue with conversion
    }
    
    // Get original file size
    const originalStat = await fs.stat(pngPath);
    const originalSize = originalStat.size;
    
    // Convert PNG to WebP
    await sharp(pngPath)
      .webp({
        quality: CONFIG.webpQuality,
        effort: CONFIG.webpEffort,
        lossless: false // Use lossy compression for better file size reduction
      })
      .toFile(webpPath);
    
    // Get WebP file size
    const webpStat = await fs.stat(webpPath);
    const webpSize = webpStat.size;
    
    // Update statistics
    stats.totalOriginalSize += originalSize;
    stats.totalWebpSize += webpSize;
    stats.convertedFiles++;
    
    const reduction = ((originalSize - webpSize) / originalSize * 100).toFixed(1);
    const originalKB = (originalSize / 1024).toFixed(1);
    const webpKB = (webpSize / 1024).toFixed(1);
    
    console.log(`✅ ${path.basename(pngPath)}: ${originalKB}KB → ${webpKB}KB (${reduction}% reduction)`);
    
  } catch (error) {
    console.error(`❌ Error converting ${path.basename(pngPath)}:`, error.message);
    stats.errors.push({ file: pngPath, error: error.message });
  }
}

/**
 * Process files in batches to avoid memory issues
 */
async function processBatch(files, startIndex) {
  const batch = files.slice(startIndex, startIndex + CONFIG.batchSize);
  const promises = batch.map(file => convertToWebP(file));
  await Promise.all(promises);
}

/**
 * Main conversion function
 */
async function convertAllImages() {
  console.log('🚀 Starting WebP conversion for TKA Gallery optimization...\n');
  
  // Check if source directory exists
  try {
    await fs.access(CONFIG.sourceDir);
  } catch {
    console.error(`❌ Source directory not found: ${CONFIG.sourceDir}`);
    process.exit(1);
  }
  
  // Get all PNG files
  console.log('📁 Scanning for PNG files...');
  const pngFiles = await getAllPngFiles(CONFIG.sourceDir);
  stats.totalFiles = pngFiles.length;
  
  if (pngFiles.length === 0) {
    console.log('ℹ️  No PNG files found to convert.');
    return;
  }
  
  console.log(`📊 Found ${pngFiles.length} PNG files to process\n`);
  
  // Process files in batches
  const startTime = Date.now();
  
  for (let i = 0; i < pngFiles.length; i += CONFIG.batchSize) {
    const batchNumber = Math.floor(i / CONFIG.batchSize) + 1;
    const totalBatches = Math.ceil(pngFiles.length / CONFIG.batchSize);
    
    console.log(`🔄 Processing batch ${batchNumber}/${totalBatches}...`);
    await processBatch(pngFiles, i);
  }
  
  const endTime = Date.now();
  const duration = ((endTime - startTime) / 1000).toFixed(1);
  
  // Print final statistics
  console.log('\n🎉 WebP conversion completed!\n');
  console.log('📈 PERFORMANCE STATISTICS:');
  console.log(`   Total files processed: ${stats.totalFiles}`);
  console.log(`   Successfully converted: ${stats.convertedFiles}`);
  console.log(`   Skipped (already up-to-date): ${stats.skippedFiles}`);
  console.log(`   Errors: ${stats.errors.length}`);
  console.log(`   Processing time: ${duration}s\n`);
  
  if (stats.convertedFiles > 0) {
    const totalReduction = ((stats.totalOriginalSize - stats.totalWebpSize) / stats.totalOriginalSize * 100).toFixed(1);
    const originalMB = (stats.totalOriginalSize / (1024 * 1024)).toFixed(1);
    const webpMB = (stats.totalWebpSize / (1024 * 1024)).toFixed(1);
    const savedMB = (originalMB - webpMB).toFixed(1);
    
    console.log('💾 FILE SIZE REDUCTION:');
    console.log(`   Original total: ${originalMB} MB`);
    console.log(`   WebP total: ${webpMB} MB`);
    console.log(`   Space saved: ${savedMB} MB (${totalReduction}% reduction)`);
    console.log(`   Bandwidth savings: ~${totalReduction}% for WebP-capable browsers\n`);
  }
  
  if (stats.errors.length > 0) {
    console.log('⚠️  ERRORS:');
    stats.errors.forEach(({ file, error }) => {
      console.log(`   ${path.basename(file)}: ${error}`);
    });
  }
  
  console.log('🏆 Gallery optimization Phase 2 complete!');
  console.log('   Next: Update thumbnail service to serve WebP with PNG fallback');
}

// Run the conversion
convertAllImages().catch(error => {
  console.error('💥 Fatal error:', error);
  process.exit(1);
});
