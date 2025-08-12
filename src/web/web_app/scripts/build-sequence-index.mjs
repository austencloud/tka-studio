import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const WEB_APP_STATIC = path.resolve(__dirname, '../static');
const CACHE_METADATA_PATH = path.join(WEB_APP_STATIC, 'browse_thumbnails/cache_metadata.json');
const SEQUENCE_INDEX_PATH = path.join(WEB_APP_STATIC, 'sequence-index.json');

// Authors for realistic metadata
const AUTHORS = ['TKA Dictionary', 'Expert User', 'Advanced Practitioner', 'Master Creator'];

// Extract word from image path
function extractWordFromPath(imagePath) {
	const match = imagePath.match(/dictionary[\\/]([^\\/]+)[\\/]/);
	return match ? match[1] : null;
}

// Generate realistic metadata
function generateSequenceMetadata(word, thumbnailHash, index) {
	const now = new Date();
	const daysAgo = Math.floor(Math.random() * 365);
	const dateAdded = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);

	// Estimate difficulty and length
	const difficultyLevel =
		word.length <= 3 ? 'beginner' : word.length <= 5 ? 'intermediate' : 'advanced';
	const sequenceLength = Math.max(
		3,
		Math.min(
			16,
			Math.round(word.length + (word.match(/[Ψ-Ω Α-Δ Θ-Λ Σ-Φ α-ω]/g) || []).length * 0.5)
		)
	);

	return {
		id: word.toLowerCase().replace(/[^a-z0-9]/g, '_'),
		name: `${word} Sequence`,
		word: word,
		thumbnails: [`/browse_thumbnails/${thumbnailHash}.png`],
		sequenceLength,
		author: AUTHORS[index % AUTHORS.length],
		difficultyLevel,
		level: Math.floor(Math.random() * 4) + 1,
		dateAdded: dateAdded.toISOString(),
		isFavorite: Math.random() > 0.85,
		isCircular: false,
		tags: ['flow', 'practice'],
		propType: 'fans',
		startingPosition: 'center',
		gridMode: Math.random() > 0.5 ? 'diamond' : 'box',
		metadata: {
			source: 'tka_dictionary',
			migrated: true,
			originalPath: `dictionary/${word}`,
			thumbnailHash: thumbnailHash,
		},
	};
}

console.log('🚀 Building sequence index from browse thumbnails...');

try {
	// Read the cache metadata
	console.log('📖 Reading cache metadata...');
	const cacheMetadata = JSON.parse(await fs.readFile(CACHE_METADATA_PATH, 'utf8'));
	console.log(`📊 Found ${Object.keys(cacheMetadata).length} cached thumbnails`);

	// Group thumbnails by sequence
	const sequenceMap = new Map();

	for (const [hash, metadata] of Object.entries(cacheMetadata)) {
		const word = extractWordFromPath(metadata.image_path);
		if (!word) continue;

		// Use the largest available thumbnail (default to 0 if no target_size)
		const currentSize = metadata.target_size ? parseInt(metadata.target_size.split('x')[0]) : 0;
		const existingSize =
			sequenceMap.has(word) && sequenceMap.get(word).metadata.target_size
				? parseInt(sequenceMap.get(word).metadata.target_size.split('x')[0])
				: 0;

		if (!sequenceMap.has(word) || currentSize > existingSize) {
			sequenceMap.set(word, { hash, metadata, word });
		}
	}

	console.log(`🎯 Found ${sequenceMap.size} unique sequences`);

	// Generate sequence metadata
	const sequences = Array.from(sequenceMap.values()).map((thumbnailInfo, index) =>
		generateSequenceMetadata(thumbnailInfo.word, thumbnailInfo.hash, index)
	);

	// Sort alphabetically
	sequences.sort((a, b) => a.word.localeCompare(b.word));

	// Create the sequence index
	const sequenceIndex = {
		version: '2.0.0',
		generatedAt: new Date().toISOString(),
		totalSequences: sequences.length,
		source: 'browse_thumbnails_cache',
		description: 'Generated from browse thumbnails cache with hash-based thumbnail mapping',
		sequences: sequences,
	};

	// Write the sequence index
	console.log('💾 Writing sequence index...');
	await fs.writeFile(SEQUENCE_INDEX_PATH, JSON.stringify(sequenceIndex, null, 2), 'utf8');

	console.log('✅ Migration completed successfully!');
	console.log(`📊 Total sequences: ${sequences.length}`);
	console.log(`📁 Sequence index: sequence-index.json`);

	// Show examples
	console.log('\n🔍 Sample sequences:');
	sequences.slice(0, 5).forEach((seq) => {
		console.log(`   • ${seq.word} (${seq.sequenceLength} beats, ${seq.difficultyLevel})`);
	});
} catch (error) {
	console.error('❌ Error:', error);
}
