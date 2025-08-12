<!-- Debug page for testing actual arrow positioning in the UI -->
<script lang="ts">
	import Arrow from '$lib/components/pictograph/Arrow.svelte';
	import { arrowPositioningService } from '$lib/components/pictograph/services/arrowPositioningService';
	import type { ArrowData, MotionData, PictographData } from '$lib/domain';
	import { ArrowType, GridMode, Location, MotionType, RotationDirection } from '$lib/domain';
	import { getPositioningServiceFactory } from '$lib/services/positioning/PositioningServiceFactory';
	import { onMount } from 'svelte';

	let debugInfo: any[] = [];
	let testResults: any[] = [];

	function addDebugInfo(message: string, data?: any) {
		debugInfo = [...debugInfo, { timestamp: new Date().toISOString(), message, data }];
		console.log(`🔍 ${message}`, data);
	}

	async function runPositioningTests() {
		addDebugInfo('🚀 Starting arrow positioning tests...');

		// Test 1: Direct service test
		addDebugInfo('Test 1: Direct ArrowPositioningService test');

		const testArrowData: ArrowData = {
			id: 'test-blue',
			color: 'blue',
			arrow_type: ArrowType.BLUE,
			location: Location.NORTH,
			motion_type: MotionType.PRO,
			is_visible: true,
			turns: 0,
			is_mirrored: false,
			position_x: 0,
			position_y: 0,
			rotation_angle: 0,
		};

		const testMotionData: MotionData = {
			motion_type: MotionType.PRO,
			prop_rot_dir: RotationDirection.CW,
			start_location: Location.NORTH,
			end_location: Location.SOUTH,
			start_loc: Location.NORTH,
			end_loc: Location.SOUTH,
			start_ori: 'in',
			end_ori: 'in',
			turns: 0,
		};

		const testPictographData: PictographData = {
			id: 'test-pictograph',
			letter: 'A',
			grid_mode: GridMode.DIAMOND,
			arrows: { blue: testArrowData },
			motions: { blue: testMotionData },
			grid_data: {
				grid_mode: GridMode.DIAMOND,
				hand_points: {},
				layer2_points: {},
			},
			props: {
				blue: {
					color: 'blue',
					motion_type: MotionType.STATIC,
					location: Location.NORTH,
				},
				red: {
					color: 'red',
					motion_type: MotionType.STATIC,
					location: Location.SOUTH,
				},
			},
			beat: 1,
			is_draft: false,
			metadata: {},
			sequence: [],
		};

		try {
			// Test the arrowPositioningService directly
			const result = await arrowPositioningService.calculatePosition(
				testArrowData,
				testMotionData,
				testPictographData
			);

			addDebugInfo('✅ ArrowPositioningService result:', result);
			testResults = [...testResults, { test: 'Service Test', result, success: true }];

			// Test the sync version too
			const syncResult = arrowPositioningService.calculatePositionSync(
				testArrowData,
				testMotionData,
				testPictographData
			);

			addDebugInfo('✅ ArrowPositioningService sync result:', syncResult);
			testResults = [
				...testResults,
				{ test: 'Sync Service Test', result: syncResult, success: true },
			];
		} catch (error) {
			addDebugInfo('❌ ArrowPositioningService error:', error);
			testResults = [
				...testResults,
				{ test: 'Service Test', error: error.message, success: false },
			];
		}

		// Test 2: Direct orchestrator test
		addDebugInfo('Test 2: Direct orchestrator test');
		try {
			const factory = getPositioningServiceFactory();
			const orchestrator = factory.createPositioningOrchestrator();

			const orchestratorResult = orchestrator.calculateArrowPosition(
				testArrowData,
				testPictographData,
				testMotionData
			);

			addDebugInfo('✅ Direct orchestrator result:', orchestratorResult);
			testResults = [
				...testResults,
				{ test: 'Orchestrator Test', result: orchestratorResult, success: true },
			];
		} catch (error) {
			addDebugInfo('❌ Direct orchestrator error:', error);
			testResults = [
				...testResults,
				{ test: 'Orchestrator Test', error: error.message, success: false },
			];
		}

		// Test 3: Check if async method exists and works
		addDebugInfo('Test 3: Testing async orchestrator method');
		try {
			const factory = getPositioningServiceFactory();
			const orchestrator = factory.createPositioningOrchestrator() as any;

			if (typeof orchestrator.calculateArrowPositionAsync === 'function') {
				const asyncResult = await orchestrator.calculateArrowPositionAsync(
					testArrowData,
					testPictographData,
					testMotionData
				);

				addDebugInfo('✅ Async orchestrator result:', asyncResult);
				testResults = [
					...testResults,
					{ test: 'Async Orchestrator Test', result: asyncResult, success: true },
				];
			} else {
				addDebugInfo('⚠️ Async method not available on orchestrator');
				testResults = [
					...testResults,
					{
						test: 'Async Orchestrator Test',
						error: 'Method not available',
						success: false,
					},
				];
			}
		} catch (error) {
			addDebugInfo('❌ Async orchestrator error:', error);
			testResults = [
				...testResults,
				{ test: 'Async Orchestrator Test', error: error.message, success: false },
			];
		}

		addDebugInfo('🏁 Positioning tests completed');
	}

	onMount(() => {
		runPositioningTests();
	});

	// Test data for rendering arrows
	const testArrow1: ArrowData = {
		id: 'test-arrow-1',
		color: 'blue',
		arrow_type: ArrowType.BLUE,
		location: Location.NORTH,
		motion_type: MotionType.PRO,
		is_visible: true,
		turns: 0,
		is_mirrored: false,
		position_x: 0, // Let the service calculate this
		position_y: 0, // Let the service calculate this
		rotation_angle: 0,
	};

	const testMotion1: MotionData = {
		motion_type: MotionType.PRO,
		prop_rot_dir: RotationDirection.CW,
		start_location: Location.NORTH,
		end_location: Location.SOUTH,
		start_loc: Location.NORTH,
		end_loc: Location.SOUTH,
		start_ori: 'in',
		end_ori: 'in',
		turns: 0,
	};

	const testArrow2: ArrowData = {
		id: 'test-arrow-2',
		color: 'red',
		arrow_type: ArrowType.RED,
		location: Location.EAST,
		motion_type: MotionType.ANTI,
		is_visible: true,
		turns: 0,
		is_mirrored: false,
		position_x: 0,
		position_y: 0,
		rotation_angle: 0,
	};

	const testMotion2: MotionData = {
		motion_type: MotionType.ANTI,
		prop_rot_dir: RotationDirection.CCW,
		start_location: Location.EAST,
		end_location: Location.WEST,
		start_loc: Location.EAST,
		end_loc: Location.WEST,
		start_ori: 'in',
		end_ori: 'in',
		turns: 0,
	};
</script>

<svelte:head>
	<title>Arrow Positioning Debug</title>
</svelte:head>

<div class="debug-page">
	<h1>Arrow Positioning Debug Page</h1>

	<div class="test-section">
		<h2>Test Results</h2>
		{#each testResults as result}
			<div class="test-result" class:success={result.success} class:error={!result.success}>
				<h3>{result.test}</h3>
				{#if result.success}
					<pre>{JSON.stringify(result.result, null, 2)}</pre>
				{:else}
					<p class="error-msg">❌ {result.error}</p>
				{/if}
			</div>
		{/each}
	</div>

	<div class="visual-test">
		<h2>Visual Arrow Test</h2>
		<div class="pictograph-container">
			<svg width="950" height="950" viewBox="0 0 950 950" class="pictograph-svg">
				<!-- Grid background -->
				<rect width="950" height="950" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1" />

				<!-- Center point -->
				<circle cx="475" cy="475" r="5" fill="#6c757d" />
				<text x="485" y="480" font-size="12" fill="#6c757d">Center (475, 475)</text>

				<!-- Location markers -->
				<circle cx="475" cy="331.9" r="3" fill="#dc3545" />
				<text x="485" y="335" font-size="10" fill="#dc3545">N (475, 331.9)</text>

				<circle cx="618.1" cy="475" r="3" fill="#dc3545" />
				<text x="628" y="480" font-size="10" fill="#dc3545">E (618.1, 475)</text>

				<circle cx="475" cy="618.1" r="3" fill="#dc3545" />
				<text x="485" y="635" font-size="10" fill="#dc3545">S (475, 618.1)</text>

				<circle cx="331.9" cy="475" r="3" fill="#dc3545" />
				<text x="280" y="480" font-size="10" fill="#dc3545">W (331.9, 475)</text>

				<!-- Test arrows -->
				<Arrow arrowData={testArrow1} motionData={testMotion1} />
				<Arrow arrowData={testArrow2} motionData={testMotion2} />
			</svg>
		</div>
	</div>

	<div class="debug-log">
		<h2>Debug Log</h2>
		<div class="log-container">
			{#each debugInfo as log}
				<div class="log-entry">
					<span class="timestamp">{log.timestamp}</span>
					<span class="message">{log.message}</span>
					{#if log.data}
						<pre class="data">{JSON.stringify(log.data, null, 2)}</pre>
					{/if}
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.debug-page {
		padding: 20px;
		max-width: 1200px;
		margin: 0 auto;
		font-family: monospace;
	}

	.test-section {
		margin-bottom: 30px;
	}

	.test-result {
		margin: 15px 0;
		padding: 15px;
		border-radius: 8px;
		border: 2px solid;
	}

	.test-result.success {
		border-color: #28a745;
		background-color: #d4edda;
	}

	.test-result.error {
		border-color: #dc3545;
		background-color: #f8d7da;
	}

	.error-msg {
		color: #721c24;
		font-weight: bold;
	}

	.visual-test {
		margin-bottom: 30px;
	}

	.pictograph-container {
		border: 2px solid #dee2e6;
		border-radius: 8px;
		overflow: hidden;
		display: inline-block;
	}

	.pictograph-svg {
		max-width: 100%;
		height: auto;
	}

	.debug-log {
		margin-top: 30px;
	}

	.log-container {
		max-height: 400px;
		overflow-y: auto;
		border: 1px solid #dee2e6;
		border-radius: 4px;
		padding: 10px;
		background: #f8f9fa;
	}

	.log-entry {
		margin-bottom: 10px;
		padding-bottom: 10px;
		border-bottom: 1px solid #e9ecef;
	}

	.timestamp {
		color: #6c757d;
		font-size: 12px;
	}

	.message {
		margin-left: 10px;
		font-weight: bold;
	}

	.data {
		margin-top: 5px;
		padding: 8px;
		background: white;
		border-radius: 4px;
		font-size: 11px;
		overflow-x: auto;
	}

	h1,
	h2,
	h3 {
		color: #495057;
	}

	pre {
		background: #f8f9fa;
		padding: 10px;
		border-radius: 4px;
		overflow-x: auto;
		font-size: 12px;
	}
</style>
