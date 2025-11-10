import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Extract WebP EXIF metadata
 */
function extractWebPMetadata(buffer) {
  try {
    let offset = 12; // Skip RIFF + WEBP headers

    while (offset < buffer.length - 8) {
      const chunkType = buffer.slice(offset, offset + 4).toString('ascii');
      offset += 4;

      const chunkSize = buffer.readUInt32LE(offset);
      offset += 4;

      if (chunkType === 'EXIF') {
        const exifData = buffer.slice(offset, offset + chunkSize);
        const jsonStart = exifData.indexOf(Buffer.from('{'));
        const jsonEnd = exifData.lastIndexOf(Buffer.from('}'));

        if (jsonStart !== -1 && jsonEnd !== -1) {
          const jsonStr = exifData.slice(jsonStart, jsonEnd + 1).toString('utf8');
          return JSON.parse(jsonStr);
        }
      }

      offset += chunkSize;
      if (chunkSize % 2 === 1) offset++;
    }
    return null;
  } catch (error) {
    return null;
  }
}

/**
 * Transform motion attributes from old to new format
 */
function transformAttributes(attrs) {
  if (!attrs) return null;

  return {
    motion_type: attrs.motion_type,
    start_loc: attrs.start_loc,
    end_loc: attrs.end_loc,
    start_ori: attrs.start_ori,
    end_ori: attrs.end_ori,
    prop_rot_dir: attrs.prop_rot_dir === 'no_rot' ? 'no_rotation' : attrs.prop_rot_dir,
    turns: attrs.turns
  };
}

/**
 * Migrate image metadata from old to new format
 */
function migrateImageMetadata(oldMetadata) {
  if (!oldMetadata || !oldMetadata.sequence || oldMetadata.sequence.length === 0) {
    return null;
  }

  // First element contains sequence-level metadata
  const metaObj = oldMetadata.sequence[0];

  // Remaining elements are the actual beats
  const beats = oldMetadata.sequence.slice(1);

  // Transform to new format
  return {
    word: metaObj.word,
    author: metaObj.author || 'TKA',
    level: metaObj.level || 1,
    prop_type: metaObj.prop_type === 'unknown' ? 'staff' : (metaObj.prop_type || 'staff'),
    grid_mode: metaObj.grid_mode || 'diamond',
    is_circular: metaObj.is_circular || false,
    date_added: oldMetadata.date_added || new Date().toISOString(),
    sequence: beats.map(beat => {
      const transformed = {
        beat: beat.beat,
        letter: beat.letter,
        blue_attributes: transformAttributes(beat.blue_attributes),
        red_attributes: transformAttributes(beat.red_attributes)
      };

      // Include sequence_start_position if present (beat 0)
      if (beat.sequence_start_position) {
        transformed.sequence_start_position = beat.sequence_start_position;
      }

      return transformed;
    })
  };
}

/**
 * Process a directory recursively
 */
async function processDirectory(dirPath, dryRun = true) {
  const results = {
    processed: 0,
    succeeded: 0,
    failed: 0,
    skipped: 0,
    errors: []
  };

  const items = fs.readdirSync(dirPath);

  for (const item of items) {
    const itemPath = path.join(dirPath, item);
    const stat = fs.statSync(itemPath);

    if (stat.isDirectory()) {
      const subResults = await processDirectory(itemPath, dryRun);
      results.processed += subResults.processed;
      results.succeeded += subResults.succeeded;
      results.failed += subResults.failed;
      results.skipped += subResults.skipped;
      results.errors.push(...subResults.errors);
    } else if (item.endsWith('.webp')) {
      results.processed++;

      try {
        const sidecarPath = itemPath.replace('.webp', '.meta.json');

        // Skip if sidecar already exists
        if (fs.existsSync(sidecarPath)) {
          console.log('SKIP: ' + itemPath + ' (sidecar exists)');
          results.skipped++;
          continue;
        }

        // Read and extract metadata
        const buffer = fs.readFileSync(itemPath);
        const oldMetadata = extractWebPMetadata(buffer);

        if (!oldMetadata) {
          console.log('WARN: ' + itemPath + ' (no EXIF metadata)');
          results.skipped++;
          continue;
        }

        // Transform metadata
        const newMetadata = migrateImageMetadata(oldMetadata);

        if (!newMetadata) {
          console.log('FAIL: ' + itemPath + ' (invalid metadata structure)');
          results.failed++;
          results.errors.push({ file: itemPath, error: 'Invalid metadata structure' });
          continue;
        }

        // Write sidecar file
        if (dryRun) {
          console.log('DRY-RUN: ' + itemPath + ' -> ' + path.basename(sidecarPath));
        } else {
          fs.writeFileSync(sidecarPath, JSON.stringify({ metadata: newMetadata }, null, 2));
          console.log('SUCCESS: ' + itemPath + ' -> ' + path.basename(sidecarPath));
        }

        results.succeeded++;
      } catch (error) {
        console.log('ERROR: ' + itemPath + ' - ' + error.message);
        results.failed++;
        results.errors.push({ file: itemPath, error: error.message });
      }
    }
  }

  return results;
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--execute');
  const galleryPath = path.join(__dirname, 'static', 'gallery');

  console.log('================================================================================');
  console.log('METADATA MIGRATION SCRIPT');
  console.log('================================================================================');
  console.log('Mode: ' + (dryRun ? 'DRY RUN (use --execute to write files)' : 'EXECUTE'));
  console.log('Gallery Path: ' + galleryPath);
  console.log('--------------------------------------------------------------------------------\n');

  if (!fs.existsSync(galleryPath)) {
    console.error('ERROR: Gallery directory not found: ' + galleryPath);
    process.exit(1);
  }

  const results = await processDirectory(galleryPath, dryRun);

  console.log('\n================================================================================');
  console.log('MIGRATION SUMMARY');
  console.log('================================================================================');
  console.log('Total Processed: ' + results.processed);
  console.log('Succeeded: ' + results.succeeded);
  console.log('Skipped: ' + results.skipped);
  console.log('Failed: ' + results.failed);

  if (results.errors.length > 0) {
    console.log('\nERRORS:');
    results.errors.forEach(err => {
      console.log('  - ' + err.file + ': ' + err.error);
    });
  }

  console.log('================================================================================');

  if (dryRun) {
    console.log('\nThis was a DRY RUN. No files were written.');
    console.log('Run with --execute to write the .meta.json files.');
  }
}

main().catch(console.error);
