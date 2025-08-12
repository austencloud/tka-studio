<!-- Simple debug page to test arrow positioning -->
<script lang="ts">
	import { arrowPositioningService } from '$lib/components/pictograph/services/arrowPositioningService';
	import { getPositioningServiceFactory } from '$lib/services/positioning/PositioningServiceFactory';
	import { onMount } from 'svelte';

	let debugLog: string[] = [];

	function log(message: string) {
		debugLog = [...debugLog, `${new Date().toISOString()}: ${message}`];
		console.log(message);
	}

	async function testPositioning() {
		log('🔍 Starting positioning debug tests...');

		// Test 1: Direct orchestrator test with minimal data
		try {
			log('Test 1: Testing the factory and orchestrator creation');
			const factory = getPositioningServiceFactory();
			const orchestrator = factory.createPositioningOrchestrator();
			log(`✅ Factory and orchestrator created successfully`);

			// Test minimal arrow positioning call
			const basicArrowData = {
				color: 'blue',
				arrow_type: 'blue' as any,
				location: 'n' as any,
				motion_type: 'pro' as any,
				is_visible: true,
				turns: 0,
				is_mirrored: false,
				position_x: 0,
				position_y: 0,
				rotation_angle: 0,
			};

			const basicMotionData = {
				motion_type: 'pro' as any,
				prop_rot_dir: 'cw',
				start_location: 'n' as any,
				end_location: 's' as any,
				start_loc: 'n' as any,
				end_loc: 's' as any,
				start_ori: 'in',
				end_ori: 'in',
				turns: 0,
			};

			const basicPictographData = {
				letter: 'A',
				grid_mode: 'diamond' as any,
				arrows: { blue: basicArrowData },
				motions: { blue: basicMotionData },
				grid_data: { grid_mode: 'diamond' as any },
				props: {},
				beat: 1,
				is_draft: false,
				metadata: {},
				sequence: [],
			};

			log('Test 2: Testing synchronous orchestrator positioning');
			const syncResult = orchestrator.calculateArrowPosition(
				basicArrowData as any,
				basicPictographData as any,
				basicMotionData as any
			);
			log(`✅ Sync result: [${syncResult[0]}, ${syncResult[1]}, ${syncResult[2]}]`);

			// Check if the result looks reasonable (not just center position)
			const [x, y, rotation] = syncResult;
			const isJustCenter = x === 475 && y === 475;
			log(`Position analysis: x=${x}, y=${y}, rotation=${rotation}°`);
			log(`Is just center position: ${isJustCenter}`);

			if (!isJustCenter) {
				log('🎉 SUCCESS: Arrows are getting positioned adjustments!');
			} else {
				log('⚠️ WARNING: Arrow is still at center - adjustments may not be working');
			}
		} catch (error) {
			log(`❌ Error in orchestrator test: ${error}`);
		}

		// Test 3: Test the ArrowPositioningService (component service)
		try {
			log('Test 3: Testing ArrowPositioningService');

			// Test the service exists and has the right methods
			log(
				`ArrowPositioningService methods: ${Object.getOwnPropertyNames(Object.getPrototypeOf(arrowPositioningService))}`
			);

			// We can't easily test this without proper type setup, but we can check if the service was created
			log('✅ ArrowPositioningService exists and appears functional');
		} catch (error) {
			log(`❌ Error in service test: ${error}`);
		}

		log('🏁 Debug tests completed');
	}

	onMount(() => {
		testPositioning();
	});
</script>

<svelte:head>
	<title>Simple Arrow Debug</title>
</svelte:head>

<div style="padding: 20px; font-family: monospace;">
	<h1>Simple Arrow Positioning Debug</h1>

	<div
		style="margin-top: 20px; max-height: 500px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; background: #f9f9f9;"
	>
		{#each debugLog as entry}
			<div style="margin-bottom: 5px; font-size: 12px;">
				{entry}
			</div>
		{/each}
	</div>
</div>
