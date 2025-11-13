/**
 * Sanitize Sequence Metadata
 *
 * Removes old "level" fields from sequence-index.json to prevent cached
 * difficulty values from interfering with the new calculated difficulty system.
 *
 * The system now calculates difficulty dynamically from sequence content:
 * - Level 1 (Beginner): Zero turns, only radial orientations (IN/OUT)
 * - Level 2 (Intermediate): Whole number turns (1,2,3), only radial orientations
 * - Level 3 (Advanced): Non-radial orientations (CLOCK/COUNTER) and/or half-turns/floats
 *
 * This script ensures old stored level values can never override calculated values.
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

const SEQUENCE_INDEX_PATH = resolve(process.cwd(), 'static', 'sequence-index.json');

function sanitizeSequenceMetadata() {
  console.log('🧹 Starting metadata sanitization...\n');

  // Read the current sequence index
  console.log(`📖 Reading: ${SEQUENCE_INDEX_PATH}`);
  const rawData = readFileSync(SEQUENCE_INDEX_PATH, 'utf-8');
  const data = JSON.parse(rawData);

  console.log(`📊 Total sequences: ${data.totalSequences}\n`);

  // Track changes
  let removedCount = 0;
  let processedCount = 0;

  // Remove "level" field from each sequence
  if (data.sequences && Array.isArray(data.sequences)) {
    data.sequences = data.sequences.map(sequence => {
      processedCount++;

      if ('level' in sequence) {
        const oldLevel = sequence.level;
        const { level, ...sanitized } = sequence;
        removedCount++;

        if (processedCount <= 5) {
          console.log(`✂️  Removing level from "${sequence.word}" (was: ${oldLevel})`);
        }

        return sanitized;
      }

      return sequence;
    });
  }

  if (removedCount > 5) {
    console.log(`   ... and ${removedCount - 5} more\n`);
  } else {
    console.log('');
  }

  // Update metadata
  data.generatedAt = new Date().toISOString();
  data.description = "Sanitized - level fields removed, difficulty calculated dynamically";

  // Write back to file
  console.log(`💾 Writing sanitized data back to file...`);
  writeFileSync(
    SEQUENCE_INDEX_PATH,
    JSON.stringify(data, null, 2),
    'utf-8'
  );

  // Summary
  console.log('\n✅ Sanitization complete!\n');
  console.log(`📈 Statistics:`);
  console.log(`   - Sequences processed: ${processedCount}`);
  console.log(`   - Level fields removed: ${removedCount}`);
  console.log(`   - Sequences unchanged: ${processedCount - removedCount}`);
  console.log('\n🎯 All sequences will now use calculated difficulty levels!');
  console.log('   Refresh your browser to see the updated data.\n');
}

// Run the sanitization
try {
  sanitizeSequenceMetadata();
} catch (error) {
  console.error('❌ Error during sanitization:', error);
  process.exit(1);
}
