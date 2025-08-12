import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CACHE_METADATA_PATH = path.join(__dirname, '../static/browse_thumbnails/cache_metadata.json');

// Extract word from image path
function extractWordFromPath(imagePath) {
	// Extract from path like "F:\CODE\TKA\src\data\dictionary\WΩ-Z-θ\WΩ-Z-θ_ver1.png"
	const match = imagePath.match(/dictionary[\\/]([^\\/]+)[\\/]/);
	return match ? match[1] : null;
}

try {
	console.log('🔍 Testing word extraction...');
	const data = await fs.readFile(CACHE_METADATA_PATH, 'utf8');
	const cacheMetadata = JSON.parse(data);

	console.log('📊 Processing entries...');

	const sequenceMap = new Map();
	let processedCount = 0;
	let extractedCount = 0;

	for (const [hash, metadata] of Object.entries(cacheMetadata)) {
		processedCount++;
		const imagePath = metadata.image_path;
		const word = extractWordFromPath(imagePath);

		if (word) {
			extractedCount++;
			if (!sequenceMap.has(word)) {
				sequenceMap.set(word, hash);
				console.log(`✅ ${word}: ${hash}`);

				// Show first 10 words extracted
				if (sequenceMap.size <= 10) {
					console.log(`   Path: ${imagePath}`);
				}
			}
		} else {
			console.log(`❌ Could not extract word from: ${imagePath}`);
		}

		// Stop after 50 entries for testing
		if (processedCount >= 50) break;
	}

	console.log(`📊 Results:`);
	console.log(`   Processed: ${processedCount} entries`);
	console.log(`   Extracted: ${extractedCount} words`);
	console.log(`   Unique sequences: ${sequenceMap.size}`);
} catch (error) {
	console.error('❌ Error:', error);
}
