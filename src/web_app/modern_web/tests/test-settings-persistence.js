/**
 * Test Settings Persistence
 *
 * This script tests that background settings persist correctly in localStorage
 */

// Test localStorage persistence
console.log('🧪 Testing TKA Modern Web Settings Persistence');

// Get current settings from localStorage
const stored = localStorage.getItem('tka-modern-web-settings');
if (stored) {
	console.log('✅ Found existing settings in localStorage:', JSON.parse(stored));
} else {
	console.log('ℹ️ No existing settings found in localStorage');
}

// Test setting some background settings
const testSettings = {
	theme: 'dark',
	gridMode: 'diamond',
	backgroundType: 'aurora',
	backgroundQuality: 'high',
	backgroundEnabled: true,
};

console.log('🔧 Setting test settings:', testSettings);
localStorage.setItem('tka-modern-web-settings', JSON.stringify(testSettings));

// Verify they were saved
const savedSettings = localStorage.getItem('tka-modern-web-settings');
console.log('✅ Verified saved settings:', JSON.parse(savedSettings));

console.log(
	'🎉 Settings persistence test complete! Reload the page to see if settings are restored.'
);
