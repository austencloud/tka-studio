<script lang="ts">
	import PropPanel from './components/PropPanel.svelte';
	import { getMotionDescription } from './utils/motion-helpers.js';
	import type { MotionTesterState } from './state/motion-tester-state.svelte.ts';
	import type { Orientation, MotionType } from './utils/motion-helpers.js';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	// Quick test functions
	function setQuickTest(testName: string) {
		switch (testName) {
			case 'pro':
				state.updateBlueMotionParam('startLoc', 'n');
				state.updateBlueMotionParam('endLoc', 'e');
				state.updateBlueMotionParam('motionType', 'pro');
				state.updateBlueMotionParam('turns', 1);
				break;
			case 'dash':
				state.updateBlueMotionParam('startLoc', 'e');
				state.updateBlueMotionParam('endLoc', 'w');
				state.updateBlueMotionParam('motionType', 'dash');
				state.updateBlueMotionParam('turns', 0);
				break;
			case 'anti':
				state.updateBlueMotionParam('startLoc', 's');
				state.updateBlueMotionParam('endLoc', 'w');
				state.updateBlueMotionParam('motionType', 'anti');
				state.updateBlueMotionParam('turns', 1);
				break;
			case 'float':
				state.updateBlueMotionParam('startLoc', 'n');
				state.updateBlueMotionParam('endLoc', 's');
				state.updateBlueMotionParam('motionType', 'float');
				state.updateBlueMotionParam('turns', 0);
				break;
		}
	}
</script>

<div class="motion-params-panel">
	<h2>🎯 Motion Designer</h2>

	<div class="panels-container">
		<!-- Blue Prop Panel -->
		<div class="prop-section">
			<div class="motion-summary blue-summary">
				{getMotionDescription(
					state.blueMotionParams.startLoc,
					state.blueMotionParams.endLoc,
					state.blueMotionParams.motionType,
					state.blueMotionParams.turns
				)}
			</div>
			
			<PropPanel
				propName="Blue"
				propColor="#60a5fa"
				startLocation={state.blueMotionParams.startLoc}
				endLocation={state.blueMotionParams.endLoc}
				startOrientation={state.blueMotionParams.startOri as Orientation}
				endOrientation={state.blueMotionParams.endOri as Orientation}
				turns={state.blueMotionParams.turns}
				motionType={state.blueMotionParams.motionType as MotionType}
				onStartLocationChange={(location) => state.updateBlueMotionParam('startLoc', location)}
				onEndLocationChange={(location) => state.updateBlueMotionParam('endLoc', location)}
				onStartOrientationChange={(orientation) => state.updateBlueMotionParam('startOri', orientation)}
				onEndOrientationChange={(orientation) => state.updateBlueMotionParam('endOri', orientation)}
				onTurnsChange={(turns) => state.updateBlueMotionParam('turns', turns)}
				onMotionTypeChange={(motionType) => state.updateBlueMotionParam('motionType', motionType)}
			/>
		</div>

		<!-- Red Prop Panel -->
		<div class="prop-section">
			<div class="motion-summary red-summary">
				{getMotionDescription(
					state.redMotionParams.startLoc,
					state.redMotionParams.endLoc,
					state.redMotionParams.motionType,
					state.redMotionParams.turns
				)}
			</div>
			
			<PropPanel
				propName="Red"
				propColor="#f87171"
				startLocation={state.redMotionParams.startLoc}
				endLocation={state.redMotionParams.endLoc}
				startOrientation={state.redMotionParams.startOri as Orientation}
				endOrientation={state.redMotionParams.endOri as Orientation}
				turns={state.redMotionParams.turns}
				motionType={state.redMotionParams.motionType as MotionType}
				onStartLocationChange={(location) => state.updateRedMotionParam('startLoc', location)}
				onEndLocationChange={(location) => state.updateRedMotionParam('endLoc', location)}
				onStartOrientationChange={(orientation) => state.updateRedMotionParam('startOri', orientation)}
				onEndOrientationChange={(orientation) => state.updateRedMotionParam('endOri', orientation)}
				onTurnsChange={(turns) => state.updateRedMotionParam('turns', turns)}
				onMotionTypeChange={(motionType) => state.updateRedMotionParam('motionType', motionType)}
			/>
		</div>
	</div>

	<!-- Quick Test Section -->
	<div class="quick-tests-section">
		<h3>⚡ Quick Tests</h3>
		<div class="quick-tests">
			<button class="quick-test-btn" onclick={() => setQuickTest('pro')}>N→E PRO</button>
			<button class="quick-test-btn" onclick={() => setQuickTest('dash')}>E→W DASH</button>
			<button class="quick-test-btn" onclick={() => setQuickTest('anti')}>S→W ANTI</button>
			<button class="quick-test-btn" onclick={() => setQuickTest('float')}>N→S FLOAT</button>
		</div>
	</div>
</div>

<style>
	.motion-params-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 20px;
		padding: 20px;
		box-sizing: border-box;
		overflow-y: auto;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #e0e7ff;
		font-size: 1.3rem;
		font-weight: 700;
		text-align: center;
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.panels-container {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.prop-section {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.motion-summary {
		background: rgba(99, 102, 241, 0.2);
		border: 1px solid rgba(99, 102, 241, 0.3);
		border-radius: 8px;
		padding: 8px 16px;
		color: #c7d2fe;
		font-size: 13px;
		font-weight: 600;
		font-family: 'Courier New', monospace;
		text-align: center;
	}

	.blue-summary {
		border-color: rgba(96, 165, 250, 0.3);
		background: rgba(96, 165, 250, 0.1);
	}

	.red-summary {
		border-color: rgba(248, 113, 113, 0.3);
		background: rgba(248, 113, 113, 0.1);
	}

	/* Quick Tests */
	.quick-tests-section {
		background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
		border: 1px solid rgba(34, 197, 94, 0.2);
		border-radius: 12px;
		padding: 20px;
		margin-top: 10px;
	}

	.quick-tests-section h3 {
		margin: 0 0 15px 0;
		color: #bbf7d0;
		font-size: 1rem;
		font-weight: 600;
	}

	.quick-tests {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 10px;
	}

	.quick-test-btn {
		background: rgba(34, 197, 94, 0.2);
		border: 1px solid rgba(34, 197, 94, 0.3);
		border-radius: 6px;
		color: #bbf7d0;
		padding: 12px 16px;
		cursor: pointer;
		font-size: 13px;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.quick-test-btn:hover {
		background: rgba(34, 197, 94, 0.3);
		border-color: rgba(34, 197, 94, 0.5);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
	}
</style>
