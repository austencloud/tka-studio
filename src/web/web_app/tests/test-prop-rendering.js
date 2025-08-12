// @ts-nocheck
/**
 * Test Script for Prop Rendering Service
 *
 * This script tests the PropRenderingService implementation to ensure
 * props are loaded, positioned, and rendered correctly.
 */

// Mock DOM environment for testing
if (typeof document === 'undefined') {
	global.document = {
		createElementNS: () => ({
			setAttribute: () => {},
			appendChild: () => {},
			firstChild: null,
		}),
	};

	global.DOMParser = class {
		parseFromString() {
			return {
				documentElement: {
					firstChild: null,
				},
			};
		}
	};

	global.fetch = async () => ({
		ok: true,
		status: 200,
		text: async () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
			<rect x="10" y="10" width="80" height="80" fill="#000000"/>
		</svg>`,
	});
}

// Import the service (this would normally be done through the DI container)
import { PropRenderingService } from '../src/lib/services/implementations/PropRenderingService.js';

async function testPropRendering() {
	console.log('🧪 Testing PropRenderingService...');

	const propService = new PropRenderingService();

	// Test 1: Check supported prop types
	console.log('\n📋 Test 1: Supported prop types');
	const supportedTypes = propService.getSupportedPropTypes();
	console.log('Supported props:', supportedTypes);

	// Test 2: Load prop SVG
	console.log('\n📦 Test 2: Loading prop SVG');
	try {
		const staffSvg = await propService.loadPropSVG('staff', 'blue');
		console.log('✅ Staff SVG loaded successfully');
		console.log('SVG length:', staffSvg.length);
	} catch (error) {
		console.error('❌ Failed to load staff SVG:', error);
	}

	// Test 3: Calculate prop position
	console.log('\n📍 Test 3: Calculating prop position');
	const testMotion = {
		motionType: 'pro',
		startLoc: 's',
		endLoc: 'n',
		startOri: 'in',
		endOri: 'out',
		turns: 1,
	};

	try {
		const position = await propService.calculatePropPosition(testMotion, 'blue', 'diamond');
		console.log('✅ Position calculated:', position);
	} catch (error) {
		console.error('❌ Failed to calculate position:', error);
	}

	// Test 4: Render complete prop
	console.log('\n🎭 Test 4: Rendering complete prop');
	try {
		const propElement = await propService.renderProp('staff', 'red', testMotion, 'diamond');
		console.log('✅ Prop rendered successfully');
		console.log('Element type:', propElement.constructor.name);
	} catch (error) {
		console.error('❌ Failed to render prop:', error);
	}

	// Test 5: Test different colors
	console.log('\n🎨 Test 5: Testing color transformations');
	try {
		const blueStaff = await propService.loadPropSVG('staff', 'blue');
		const redStaff = await propService.loadPropSVG('staff', 'red');

		console.log('✅ Blue staff loaded, contains blue color:', blueStaff.includes('#2E3192'));
		console.log('✅ Red staff loaded, contains red color:', redStaff.includes('#ED1C24'));
	} catch (error) {
		console.error('❌ Failed to test color transformations:', error);
	}

	console.log('\n🎉 PropRenderingService testing complete!');
}

// Run the test
testPropRendering().catch(console.error);
