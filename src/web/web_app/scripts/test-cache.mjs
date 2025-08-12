import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CACHE_METADATA_PATH = path.join(__dirname, '../static/browse_thumbnails/cache_metadata.json');

console.log('🔍 Testing cache metadata reading...');
console.log('📁 Cache metadata path:', CACHE_METADATA_PATH);

try {
	console.log('📖 Reading cache metadata...');
	const data = await fs.readFile(CACHE_METADATA_PATH, 'utf8');
	const cacheMetadata = JSON.parse(data);

	console.log('✅ Successfully read cache metadata');
	console.log('📊 Number of entries:', Object.keys(cacheMetadata).length);

	// Show first few entries
	const entries = Object.entries(cacheMetadata).slice(0, 3);
	console.log('🔍 First few entries:');
	entries.forEach(([hash, metadata]) => {
		console.log(`   ${hash}: ${metadata.image_path}`);
	});
} catch (error) {
	console.error('❌ Error:', error);
}
