import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const WEB_APP_STATIC = path.resolve(__dirname, '../static');
const BROWSE_THUMBNAILS_DIR = path.join(WEB_APP_STATIC, 'browse_thumbnails');
const CACHE_METADATA_PATH = path.join(BROWSE_THUMBNAILS_DIR, 'cache_metadata.json');
const SEQUENCE_INDEX_PATH = path.join(WEB_APP_STATIC, 'sequence-index.json');

// Authors for realistic metadata
const AUTHORS = ['TKA Dictionary', 'Expert User', 'Advanced Practitioner', 'Master Creator'];

// Difficulty estimation based on word complexity
function estimateDifficulty(word) {
	if (word.length <= 3) return 'beginner';
	if (word.length <= 5) return 'intermediate';
	return 'advanced';
}

// Sequence length estimation based on word complexity and special characters
function estimateSequenceLength(word) {
	let baseLength = word.length;

	// Count special characters that indicate complexity
	const specialChars = (word.match(/[Ψ-Ω Α-Δ Θ-Λ Σ-Φ α-ω]/g) || []).length;
	const complexity = specialChars * 0.5;

	return Math.max(3, Math.min(16, Math.round(baseLength + complexity)));
}

// Extract word from image path
function extractWordFromPath(imagePath) {
	// Extract from path like "F:\CODE\TKA\src\data\dictionary\WΩ-Z-θ\WΩ-Z-θ_ver1.png"
	const match = imagePath.match(/dictionary[\\/]([^\\/]+)[\\/]/);
	return match ? match[1] : null;
}

// Generate realistic metadata
function generateSequenceMetadata(word, thumbnailHash, index) {
	const now = new Date();
	const daysAgo = Math.floor(Math.random() * 365);
	const dateAdded = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);

	return {
		id: word.toLowerCase().replace(/[^a-z0-9]/g, '_'),
		name: `${word} Sequence`,
		word: word,
		thumbnails: [`/browse_thumbnails/${thumbnailHash}.png`],
		sequenceLength: estimateSequenceLength(word),
		author: AUTHORS[index % AUTHORS.length],
		difficultyLevel: estimateDifficulty(word),
		level: Math.floor(Math.random() * 4) + 1,
		dateAdded: dateAdded.toISOString(),
		isFavorite: Math.random() > 0.85, // 15% chance of being favorite
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

// Main migration function
async function migrateSequenceData() {
	console.log('🚀 Starting TKA sequence data migration using browse thumbnails cache...');

	try {
		// Read the cache metadata
		console.log('📖 Reading browse thumbnails cache metadata...');
		const cacheMetadata = JSON.parse(await fs.readFile(CACHE_METADATA_PATH, 'utf8'));

		console.log(`📊 Found ${Object.keys(cacheMetadata).length} cached thumbnails`);

		// Group thumbnails by sequence (same image path, different sizes)
		const sequenceMap = new Map();

		for (const [hash, metadata] of Object.entries(cacheMetadata)) {
			const imagePath = metadata.image_path;
			const word = extractWordFromPath(imagePath);

			if (!word) {
				console.warn(`⚠️  Could not extract word from path: ${imagePath}`);
				continue;
			}

			// Use the largest available thumbnail (highest resolution)
			if (
				!sequenceMap.has(word) ||
				parseInt(metadata.target_size.split('x')[0]) >
					parseInt(sequenceMap.get(word).target_size.split('x')[0])
			) {
				sequenceMap.set(word, {
					hash,
					metadata,
					word,
				});
			}
		}

		console.log(`🎯 Found ${sequenceMap.size} unique sequences with thumbnails`);

		// Generate sequence metadata for each sequence
		const sequences = [];
		let index = 0;

		for (const [word, thumbnailInfo] of sequenceMap.entries()) {
			const sequenceMetadata = generateSequenceMetadata(word, thumbnailInfo.hash, index++);
			sequences.push(sequenceMetadata);

			if (index % 100 === 0) {
				console.log(`📝 Generated metadata for ${index} sequences...`);
			}
		}

		// Sort sequences alphabetically
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
		console.log(`📊 Statistics:`);
		console.log(`   • Total sequences: ${sequences.length}`);
		console.log(`   • Browse thumbnails used: ${sequenceMap.size}`);
		console.log(`   • Sequence index: ${SEQUENCE_INDEX_PATH}`);

		// Show some examples
		console.log('\n🔍 Sample sequences:');
		sequences.slice(0, 5).forEach((seq) => {
			console.log(
				`   • ${seq.word} (${seq.sequenceLength} beats, ${seq.difficultyLevel}) - ${seq.thumbnails[0]}`
			);
		});
	} catch (error) {
		console.error('❌ Migration failed:', error);
		process.exit(1);
	}
}

// Run the migration
if (import.meta.url === `file://${process.argv[1]}`) {
	migrateSequenceData();
}

export default migrateSequenceData;
