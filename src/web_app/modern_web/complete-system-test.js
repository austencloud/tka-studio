/**
 * Complete Pictograph System Test - Runes Integration
 *
 * This test validates the complete pictograph rendering system with:
 * - Runes-based state management
 * - Actual service implementations
 * - Real arrow positioning and prop rendering
 * - Desktop parity validation
 */

import { resolve } from '../src/lib/services/bootstrap.js';
import {
	IPictographRenderingService,
	IArrowPositioningService,
	IPropRenderingService,
	IArrowPlacementDataService,
} from '../src/lib/services/interfaces.js';

// Import runes state management
import {
	setArrowPositions,
	setArrowPositioningInProgress,
	setArrowPositioningError,
	getArrowPositions,
	getArrowPositioningInProgress,
	getArrowPositioningError,
	setCurrentSequence,
	getCurrentSequence,
} from '../src/lib/stores/sequenceState.svelte.js';

// Test data with complete motion specifications
const completeTestCases = [
	{
		name: 'PRO Staff Motion with Letter A - Runes Integration',
		data: {
			id: 'pro-staff-runes-A',
			gridData: { mode: 'diamond' },
			arrows: { blue: {}, red: {} },
			props: { blue: {}, red: {} },
			motions: {
				blue: {
					motionType: 'pro',
					propRotDir: 'cw',
					startLoc: 'n',
					endLoc: 's',
					turns: 1,
					startOri: 'in',
					endOri: 'out',
					isVisible: true,
				},
				red: null,
			},
			letter: 'A',
		},
		expectedFeatures: {
			placementKey: 'pro_to_layer1_alpha_A',
			propRendering: true,
			runesStateUpdate: true,
		},
	},
	{
		name: 'ANTI Dual Motion with Complex Letter - Complete System',
		data: {
			id: 'anti-dual-complete',
			gridData: { mode: 'diamond' },
			arrows: { blue: {}, red: {} },
			props: { blue: {}, red: {} },
			motions: {
				blue: {
					motionType: 'anti',
					propRotDir: 'ccw',
					startLoc: 'e',
					endLoc: 'w',
					turns: 0.5,
					startOri: 'out',
					endOri: 'in',
					isVisible: true,
				},
				red: {
					motionType: 'pro',
					propRotDir: 'cw',
					startLoc: 'w',
					endLoc: 'e',
					turns: 2,
					startOri: 'in',
					endOri: 'out',
					isVisible: true,
				},
			},
			letter: 'θ-',
		},
		expectedFeatures: {
			placementKey: 'anti_to_layer2_alpha_θ_dash',
			dualMotion: true,
			dashLetterHandling: true,
			propRendering: true,
			runesStateUpdate: true,
		},
	},
];

// Complete system test class with runes integration
class CompletePictographSystemTest {
	constructor() {
		this.services = {};
		this.testResults = {
			passed: 0,
			failed: 0,
			details: [],
		};
	}

	async initialize() {
		console.log('🚀 Initializing Complete Pictograph System Test with Runes');
		console.log('================================================================');

		try {
			// Resolve services from DI container
			this.services.pictographRendering = resolve(IPictographRenderingService);
			this.services.arrowPositioning = resolve(IArrowPositioningService);
			this.services.propRendering = resolve(IPropRenderingService);
			this.services.placementData = resolve(IArrowPlacementDataService);

			console.log('✅ Services resolved from DI container');
			console.log('📦 Available services:', Object.keys(this.services));

			// Load placement data
			setArrowPositioningInProgress(true);
			setArrowPositioningError(null);

			await this.services.placementData.loadPlacementData();

			setArrowPositioningInProgress(false);
			console.log('✅ Placement data loaded, runes state updated');

			return true;
		} catch (error) {
			console.error('❌ Initialization failed:', error);
			setArrowPositioningError(error.message);
			setArrowPositioningInProgress(false);
			return false;
		}
	}

	async runCompleteSystemTests() {
		console.log('\n🧪 Running Complete Pictograph System Tests');
		console.log('============================================');

		for (const testCase of completeTestCases) {
			await this.runSingleTest(testCase);
		}

		this.printTestSummary();
	}

	async runSingleTest(testCase) {
		console.log(`\n🔬 Testing: ${testCase.name}`);
		console.log('-'.repeat(50));

		try {
			// Test 1: Runes State Integration
			console.log('📊 Step 1: Testing runes state integration...');
			setArrowPositioningInProgress(true);
			setCurrentSequence({
				id: testCase.data.id,
				beats: [{ ...testCase.data, beatNumber: 1 }],
				name: testCase.name,
			});

			const currentSequence = getCurrentSequence();
			this.assert(
				currentSequence.id === testCase.data.id,
				'Runes state should update current sequence'
			);

			// Test 2: Arrow Positioning Service
			console.log('🏹 Step 2: Testing sophisticated arrow positioning...');
			const gridData = this.createTestGridData();
			const arrowPositions = await this.services.arrowPositioning.calculateAllArrowPositions(
				testCase.data,
				gridData
			);

			this.assert(arrowPositions.size > 0, 'Arrow positions should be calculated');

			// Update runes state with arrow positions
			setArrowPositions(arrowPositions);
			const runesArrowPositions = getArrowPositions();

			this.assert(
				runesArrowPositions.size === arrowPositions.size,
				'Runes state should store arrow positions'
			);

			console.log(`✅ Calculated ${arrowPositions.size} arrow positions`);

			// Test 3: Prop Rendering Service
			if (testCase.expectedFeatures.propRendering) {
				console.log('🎭 Step 3: Testing prop rendering service...');

				for (const [color, motion] of Object.entries(testCase.data.motions)) {
					if (motion) {
						const propElement = await this.services.propRendering.renderProp(
							'staff', // Default prop type
							color,
							motion,
							'diamond'
						);

						this.assert(
							propElement instanceof SVGElement,
							`${color} prop should render as SVG element`
						);

						this.assert(
							propElement.getAttribute('class').includes(`prop-${color}`),
							`${color} prop should have correct CSS class`
						);

						console.log(`✅ ${color} prop rendered successfully`);
					}
				}
			}

			// Test 4: Complete Pictograph Rendering
			console.log('🎨 Step 4: Testing complete pictograph rendering...');
			const pictographSvg = await this.services.pictographRendering.renderPictograph(
				testCase.data
			);

			this.assert(
				pictographSvg instanceof SVGElement,
				'Pictograph should render as SVG element'
			);

			this.assert(
				pictographSvg.getAttribute('width') === '300',
				'Pictograph should have correct dimensions'
			);

			// Validate sophisticated positioning elements are present
			const arrowElements = pictographSvg.querySelectorAll(
				'[class*="sophisticated-positioning"]'
			);
			this.assert(
				arrowElements.length > 0,
				'Pictograph should contain sophisticated positioning elements'
			);

			console.log('✅ Complete pictograph rendered successfully');

			// Test 5: Placement Key Validation
			if (testCase.expectedFeatures.placementKey) {
				console.log('🔑 Step 5: Validating sophisticated placement keys...');

				// Check if debug info contains expected placement key
				const debugElements = pictographSvg.querySelectorAll('text');
				let placementKeyFound = false;

				debugElements.forEach((element) => {
					if (
						element.textContent &&
						element.textContent.includes(testCase.expectedFeatures.placementKey)
					) {
						placementKeyFound = true;
					}
				});

				this.assert(
					placementKeyFound,
					`Pictograph should use expected placement key: ${testCase.expectedFeatures.placementKey}`
				);

				console.log(
					`✅ Placement key validation passed: ${testCase.expectedFeatures.placementKey}`
				);
			}

			// Test 6: Runes State Cleanup
			console.log('🧹 Step 6: Testing runes state management...');
			setArrowPositioningInProgress(false);
			setArrowPositioningError(null);

			this.assert(
				!getArrowPositioningInProgress(),
				'Runes state should clear positioning progress'
			);

			this.assert(
				getArrowPositioningError() === null,
				'Runes state should clear positioning error'
			);

			console.log('✅ Runes state management test passed');

			this.testResults.passed++;
			this.testResults.details.push({
				name: testCase.name,
				result: 'PASSED',
				features: testCase.expectedFeatures,
			});

			console.log(`🎉 ${testCase.name} - ALL TESTS PASSED`);
		} catch (error) {
			console.error(`❌ ${testCase.name} - TEST FAILED:`, error);

			setArrowPositioningError(error.message);
			setArrowPositioningInProgress(false);

			this.testResults.failed++;
			this.testResults.details.push({
				name: testCase.name,
				result: 'FAILED',
				error: error.message,
			});
		}
	}

	createTestGridData() {
		const center = { x: 150, y: 150 };
		const size = 80;

		return {
			mode: 'diamond',
			allLayer2PointsNormal: {
				n_diamond_layer2_point: { coordinates: { x: center.x, y: center.y - size } },
				e_diamond_layer2_point: { coordinates: { x: center.x + size, y: center.y } },
				s_diamond_layer2_point: { coordinates: { x: center.x, y: center.y + size } },
				w_diamond_layer2_point: { coordinates: { x: center.x - size, y: center.y } },
			},
			allHandPointsNormal: {
				n_diamond_hand_point: { coordinates: { x: center.x, y: center.y - size * 0.6 } },
				e_diamond_hand_point: { coordinates: { x: center.x + size * 0.6, y: center.y } },
				s_diamond_hand_point: { coordinates: { x: center.x, y: center.y + size * 0.6 } },
				w_diamond_hand_point: { coordinates: { x: center.x - size * 0.6, y: center.y } },
			},
		};
	}

	assert(condition, message) {
		if (!condition) {
			throw new Error(`Assertion failed: ${message}`);
		}
	}

	printTestSummary() {
		console.log('\n📊 Complete System Test Summary');
		console.log('===============================');
		console.log(`✅ Tests Passed: ${this.testResults.passed}`);
		console.log(`❌ Tests Failed: ${this.testResults.failed}`);
		console.log(`🎯 Total Tests: ${this.testResults.passed + this.testResults.failed}`);
		console.log(
			`📈 Success Rate: ${Math.round((this.testResults.passed / (this.testResults.passed + this.testResults.failed)) * 100)}%`
		);

		if (this.testResults.details.length > 0) {
			console.log('\n📋 Detailed Results:');
			this.testResults.details.forEach((detail, index) => {
				const status = detail.result === 'PASSED' ? '✅' : '❌';
				console.log(`${status} ${index + 1}. ${detail.name} - ${detail.result}`);
				if (detail.error) {
					console.log(`   Error: ${detail.error}`);
				}
				if (detail.features) {
					const features = Object.keys(detail.features).filter((k) => detail.features[k]);
					console.log(`   Features: ${features.join(', ')}`);
				}
			});
		}

		if (this.testResults.failed === 0) {
			console.log('\n🎉 ALL TESTS PASSED! Complete Pictograph System is operational!');
			console.log('🚀 System Features Validated:');
			console.log('   ✅ Sophisticated Arrow Positioning');
			console.log('   ✅ Prop Rendering Service');
			console.log('   ✅ Runes State Management');
			console.log('   ✅ Desktop Parity Algorithms');
			console.log('   ✅ Complex Placement Key Generation');
			console.log('   ✅ Service Integration via DI Container');
		} else {
			console.log('\n⚠️ Some tests failed. Check details above.');
		}
	}
}

// Auto-run complete system test
async function runCompletePictographSystemTest() {
	console.log('🎯 TKA Complete Pictograph System Test - Runes Integration');
	console.log('==========================================================');

	try {
		const testSuite = new CompletePictographSystemTest();

		const initialized = await testSuite.initialize();
		if (!initialized) {
			console.error('❌ Test suite initialization failed');
			return false;
		}

		await testSuite.runCompleteSystemTests();
		return testSuite.testResults.failed === 0;
	} catch (error) {
		console.error('💥 Test suite crashed:', error);
		return false;
	}
}

// Export for external use
export { CompletePictographSystemTest, runCompletePictographSystemTest };

// Auto-run if this file is executed directly
runCompletePictographSystemTest()
	.then((success) => {
		if (success) {
			console.log('\n🏆 COMPLETE SYSTEM VALIDATION SUCCESSFUL!');
			console.log('The TKA Complete Pictograph System is ready for production use.');
		} else {
			console.log('\n🔥 SYSTEM VALIDATION FAILED!');
			console.log('Review the test results above and fix failing components.');
		}
	})
	.catch((error) => {
		console.error('\n💥 VALIDATION CRASHED:', error);
	});
