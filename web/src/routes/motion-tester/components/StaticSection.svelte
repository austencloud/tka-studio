<!--
StaticSection.svelte - Static pictograph with motion controls

Combines static pictograph display (no card wrapper) with motion designer controls
(blue/red prop panels) below. Grid toggle positioned as overlay on pictograph.
This is the left 2/3 section of the new layout.
-->
<script lang="ts">
	import type { MotionTesterState } from '../state/motion-tester-state.svelte';
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
	import PropPanel from './PropPanel.svelte';
	import SimpleGridToggle from './SimpleGridToggle.svelte';
	import { createPictographData, createGridData } from '$lib/domain';
	import { GridMode, MotionType, Location, Orientation, RotationDirection } from '$lib/domain/enums';

	interface Props {
		motionState: MotionTesterState;
	}

	let { motionState }: Props = $props();

	// Fixed size for consistent layout
	const PICTOGRAPH_SIZE = 320;

	// Create pictograph data for static display (always at progress = 0)
	function createStaticPictographData() {
		try {
			const gridMode = motionState.gridType === 'diamond' ? GridMode.DIAMOND : GridMode.BOX;
			
			const gridData = createGridData({
				grid_mode: gridMode
			});

			const pictographData = createPictographData({
				id: 'motion-tester-static-pictograph',
				grid_data: gridData,
				arrows: {},
				props: {},
				motions: {
					blue: {
						motion_type: motionState.blueMotionParams.motionType as MotionType,
						start_loc: motionState.blueMotionParams.startLoc as Location,
						end_loc: motionState.blueMotionParams.endLoc as Location,
						start_ori: motionState.blueMotionParams.startOri as Orientation,
						end_ori: motionState.blueMotionParams.endOri as Orientation,
						prop_rot_dir: motionState.blueMotionParams.propRotDir as RotationDirection,
						turns: motionState.blueMotionParams.turns,
						is_visible: true
					},
					red: {
						motion_type: motionState.redMotionParams.motionType as MotionType,
						start_loc: motionState.redMotionParams.startLoc as Location,
						end_loc: motionState.redMotionParams.endLoc as Location,
						start_ori: motionState.redMotionParams.startOri as Orientation,
						end_ori: motionState.redMotionParams.endOri as Orientation,
						prop_rot_dir: motionState.redMotionParams.propRotDir as RotationDirection,
						turns: motionState.redMotionParams.turns,
						is_visible: true
					}
				},
				letter: 'T', // T for "Tester"
				beat: 1,
				is_blank: false,
				is_mirrored: false,
				metadata: {
					source: 'motion_tester_static',
					grid_type: motionState.gridType,
					progress: 0 // Always show initial state
				}
			});

			return pictographData;
		} catch (error) {
			console.error('Error creating static pictograph data:', error);
			return null;
		}
	}

	let pictographData = $derived(createStaticPictographData());


</script>

<div class="static-section-with-controls">
	<!-- Static Pictograph with Grid Toggle Overlay -->
	<div class="pictograph-area">
		<div class="grid-toggle-overlay">
			<SimpleGridToggle state={motionState} />
		</div>
		
		<div class="pictograph-container">
			{#if pictographData}
				<Pictograph
					pictographData={pictographData}
					width={PICTOGRAPH_SIZE}
					height={PICTOGRAPH_SIZE}
					debug={false}
					beatNumber={null}
				/>
			{:else}
				<div class="error-state">
					<span class="error-icon">⚠️</span>
					<p>Unable to display pictograph</p>
				</div>
			{/if}
		</div>
	</div>

	<!-- Motion Designer Controls -->
	<div class="motion-controls">
		<!-- Blue Prop Section -->
		<div class="prop-section">
			<PropPanel
				propName="Blue"
				propColor="#60a5fa"
				startLocation={motionState.blueMotionParams.startLoc}
				endLocation={motionState.blueMotionParams.endLoc}
				startOrientation={motionState.blueMotionParams.startOri as Orientation}
				endOrientation={motionState.blueMotionParams.endOri as Orientation}
				turns={motionState.blueMotionParams.turns}
				motionType={motionState.blueMotionParams.motionType as MotionType}
				onStartLocationChange={(location) => motionState.updateBlueMotionParam('startLoc', location)}
				onEndLocationChange={(location) => motionState.updateBlueMotionParam('endLoc', location)}
				onStartOrientationChange={(orientation) => motionState.updateBlueMotionParam('startOri', orientation)}
				onEndOrientationChange={(orientation) => motionState.updateBlueMotionParam('endOri', orientation)}
				onTurnsChange={(turns) => motionState.updateBlueMotionParam('turns', turns)}
				onMotionTypeChange={(motionType) => motionState.updateBlueMotionParam('motionType', motionType)}
			/>
		</div>

		<!-- Red Prop Section -->
		<div class="prop-section">
			<PropPanel
				propName="Red"
				propColor="#f87171"
				startLocation={motionState.redMotionParams.startLoc}
				endLocation={motionState.redMotionParams.endLoc}
				startOrientation={motionState.redMotionParams.startOri as Orientation}
				endOrientation={motionState.redMotionParams.endOri as Orientation}
				turns={motionState.redMotionParams.turns}
				motionType={motionState.redMotionParams.motionType as MotionType}
				onStartLocationChange={(location) => motionState.updateRedMotionParam('startLoc', location)}
				onEndLocationChange={(location) => motionState.updateRedMotionParam('endLoc', location)}
				onStartOrientationChange={(orientation) => motionState.updateRedMotionParam('startOri', orientation)}
				onEndOrientationChange={(orientation) => motionState.updateRedMotionParam('endOri', orientation)}
				onTurnsChange={(turns) => motionState.updateRedMotionParam('turns', turns)}
				onMotionTypeChange={(motionType) => motionState.updateRedMotionParam('motionType', motionType)}
			/>
		</div>
	</div>
</div>

<style>
	.static-section-with-controls {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: linear-gradient(135deg, rgba(16, 185, 129, 0.03), rgba(59, 130, 246, 0.03));
		border-radius: 8px;
		overflow: hidden;
		container-type: size;
	}

	.pictograph-area {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 20px;
		background: rgba(255, 255, 255, 0.02);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		flex-shrink: 0;
	}

	.grid-toggle-overlay {
		position: absolute;
		top: 16px;
		right: 16px;
		z-index: 10;
	}

	.pictograph-container {
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px;
		background: rgba(255, 255, 255, 0.01);
		padding: 10px;
	}

	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: #f87171;
		text-align: center;
		padding: 40px;
	}

	.error-icon {
		font-size: 32px;
		margin-bottom: 12px;
	}

	.error-state p {
		margin: 0;
		font-size: 16px;
		color: #fca5a5;
	}

	.motion-controls {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1cqw;
		padding: 1.5cqw;
		min-height: 0;
		overflow: auto;
		container-type: size;
	}

	.prop-section {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	/* Container-based responsive layout */
	@container (max-width: 600px) {
		.motion-controls {
			grid-template-columns: 1fr;
			gap: 1.5cqw;
			padding: 2cqw;
		}
	}

	@container (max-width: 400px) {
		.motion-controls {
			gap: 2cqw;
			padding: 2.5cqw;
		}
	}

	/* Fallback media queries for older browsers */
	@media (max-width: 768px) {
		.pictograph-area {
			padding: 1.5vw;
		}

		.motion-controls {
			grid-template-columns: 1fr;
			padding: 2vw;
			gap: 1.5vw;
		}

		.grid-toggle-overlay {
			top: 1vw;
			right: 1vw;
		}
	}
</style>
