<script lang="ts">
	import type { MotionTesterState } from './motion-tester-state.svelte.ts';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	function radToDeg(rad: number): string {
		return (rad * 180 / Math.PI).toFixed(1);
	}

	function formatAngle(rad: number | undefined): string {
		if (rad === undefined || rad === null || isNaN(rad)) {
			return '0.000';
		}
		return rad.toFixed(3);
	}
</script>

<div class="debug-panel">
	<h2>🔧 Debug Information</h2>

	{#if state.isEngineInitialized}
		<!-- Current Prop States -->
		<div class="debug-section current-state">
			<h3>Current Prop States</h3>
			<div class="prop-debug">
				<div class="prop-info">
					<h4>Blue Prop</h4>
					<div class="debug-item">
						<span class="label">Center Angle:</span>
						<span class="value">{formatAngle(state.currentPropStates.blue?.centerPathAngle)} rad</span>
					</div>
					<div class="debug-item">
						<span class="label">Staff Angle:</span>
						<span class="value">{formatAngle(state.currentPropStates.blue?.staffRotationAngle)} rad</span>
					</div>
					<div class="debug-item">
						<span class="label">X Position:</span>
						<span class="value">{state.currentPropStates.blue?.x?.toFixed(1) || '0.0'} px</span>
					</div>
					<div class="debug-item">
						<span class="label">Y Position:</span>
						<span class="value">{state.currentPropStates.blue?.y?.toFixed(1) || '0.0'} px</span>
					</div>
				</div>
				<div class="prop-info">
					<h4>Red Prop</h4>
					<div class="debug-item">
						<span class="label">Center Angle:</span>
						<span class="value">{formatAngle(state.currentPropStates.red?.centerPathAngle)} rad</span>
					</div>
					<div class="debug-item">
						<span class="label">Staff Angle:</span>
						<span class="value">{formatAngle(state.currentPropStates.red?.staffRotationAngle)} rad</span>
					</div>
					<div class="debug-item">
						<span class="label">X Position:</span>
						<span class="value">{state.currentPropStates.red?.x?.toFixed(1) || '0.0'} px</span>
					</div>
					<div class="debug-item">
						<span class="label">Y Position:</span>
						<span class="value">{state.currentPropStates.red?.y?.toFixed(1) || '0.0'} px</span>
					</div>
				</div>
			</div>
		</div>

		{#if state.debugInfo}
			<!-- Start Endpoints -->
			<div class="debug-section">
				<h3>Start Endpoints</h3>
				<div class="debug-item">
					<span class="label">Center Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.startCenterAngle) : 'N/A'} rad</span>
				</div>
				<div class="debug-item">
					<span class="label">Staff Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.startStaffAngle) : 'N/A'} rad</span>
				</div>
			</div>

			<!-- Target Endpoints -->
			<div class="debug-section">
				<h3>Target Endpoints</h3>
				<div class="debug-item">
					<span class="label">Center Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.targetCenterAngle) : 'N/A'} rad</span>
				</div>
				<div class="debug-item">
					<span class="label">Staff Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.targetStaffAngle) : 'N/A'} rad</span>
				</div>
			</div>

			<!-- Motion Calculation -->
			<div class="debug-section">
				<h3>Motion Calculation</h3>
				<div class="debug-item">
					<span class="label">Motion Type:</span>
					<span class="value">{state.blueMotionParams.motionType}</span>
				</div>
				<div class="debug-item">
					<span class="label">Delta Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.deltaAngle) : 'N/A'} rad</span>
				</div>
				<div class="debug-item">
					<span class="label">Turn Angle:</span>
					<span class="value">{state.debugInfo ? formatAngle(state.debugInfo.blue.turnAngle) : 'N/A'} rad</span>
				</div>
				<div class="debug-item">
					<span class="label">Interpolation (t):</span>
					<span class="value">{state.debugInfo?.interpolationT?.toFixed(3) || '0.000'}</span>
				</div>
				<div class="debug-item">
					<span class="label">Current Beat:</span>
					<span class="value">{state.debugInfo?.currentBeat?.toFixed(3) || '0.000'}</span>
				</div>
			</div>

			<!-- Grid Positions -->
			<div class="debug-section">
				<h3>Grid Positions</h3>
				<div class="debug-item">
					<span class="label">Start Location:</span>
					<span class="value">{state.blueMotionParams.startLoc}</span>
				</div>
				<div class="debug-item">
					<span class="label">End Location:</span>
					<span class="value">{state.blueMotionParams.endLoc}</span>
				</div>
				<div class="debug-item">
					<span class="label">Distance:</span>
					<span class="value">{state.debugInfo ? state.debugInfo.blue.distance.toFixed(1) : 'N/A'}°</span>
				</div>
			</div>

			<!-- Angle Conversions -->
			<div class="debug-section">
				<h3>Angle Conversions (Blue Prop)</h3>
				<div class="debug-item">
					<span class="label">Center (degrees):</span>
					<span class="value">{radToDeg(state.currentPropStates?.blue?.centerPathAngle || 0)}°</span>
				</div>
				<div class="debug-item">
					<span class="label">Staff (degrees):</span>
					<span class="value">{radToDeg(state.currentPropStates?.blue?.staffRotationAngle || 0)}°</span>
				</div>
			</div>
		{/if}

		<!-- Engine Status -->
		<div class="debug-section summary">
			<h3>Engine Status</h3>
			<div class="debug-item">
				<span class="label">Engine Initialized:</span>
				<span class="value engine-status" class:initialized={state.isEngineInitialized}>
					{state.isEngineInitialized ? 'Yes' : 'No'}
				</span>
			</div>
			<div class="debug-item">
				<span class="label">Total Beats:</span>
				<span class="value">{state.totalBeats || 'N/A'}</span>
			</div>
			<div class="debug-item">
				<span class="label">Progress:</span>
				<span class="value">{(state.animationState?.progress * 100)?.toFixed(1) || '0.0'}%</span>
			</div>
			<div class="debug-item">
				<span class="label">Speed:</span>
				<span class="value">{(state.animationState?.speed * 1000)?.toFixed(0) || '0'}%</span>
			</div>
			<div class="debug-item">
				<span class="label">Playing:</span>
				<span class="value" class:playing={state.animationState.isPlaying}>
					{state.animationState.isPlaying ? 'Yes' : 'No'}
				</span>
			</div>
		</div>
	{:else}
		<!-- Engine not initialized -->
		<div class="debug-section error">
			<h3>Engine Status</h3>
			<p>Animation engine not initialized. Check motion parameters.</p>
		</div>
	{/if}

	<!-- Motion Parameters Summary -->
	<div class="debug-section motion-summary">
		<h3>Motion Summary</h3>
		<div class="debug-item">
			<span class="label">Description:</span>
			<span class="value motion-desc">{state.blueMotionDescription}</span>
		</div>
	</div>

	<!-- Quick Test Buttons -->
	<div class="debug-section">
		<h3>Quick Tests</h3>
		<div class="quick-test-grid">
			<button
				class="quick-test-btn"
				onclick={() => {
					state.setBlueStartLocation('n');
					state.setBlueEndLocation('e');
					state.updateBlueMotionParam('motionType', 'pro');
					state.updateBlueMotionParam('turns', 0);
				}}
			>
				N→E Pro (Shift)
			</button>
			<button
				class="quick-test-btn"
				onclick={() => {
					state.setBlueStartLocation('n');
					state.setBlueEndLocation('e');
					state.updateBlueMotionParam('motionType', 'anti');
					state.updateBlueMotionParam('turns', 1);
				}}
			>
				N→E Anti 1T (Shift)
			</button>
			<button
				class="quick-test-btn"
				onclick={() => {
					state.setBlueStartLocation('n');
					state.setBlueEndLocation('s');
					state.updateBlueMotionParam('motionType', 'dash');
					state.updateBlueMotionParam('turns', 0);
				}}
			>
				N→S Dash (Opposite)
			</button>
			<button
				class="quick-test-btn"
				onclick={() => {
					state.setBlueStartLocation('n');
					state.setBlueEndLocation('n');
					state.updateBlueMotionParam('motionType', 'static');
					state.updateBlueMotionParam('turns', 1);
				}}
			>
				N→N Static 1T
			</button>
			<button
				class="quick-test-btn"
				onclick={() => {
					state.setBlueStartLocation('w');
					state.setBlueEndLocation('n');
					state.updateBlueMotionParam('motionType', 'float');
					state.updateBlueMotionParam('turns', 0);
				}}
			>
				W→N Float
			</button>
		</div>
	</div>
</div>

<style>
	.debug-panel {
		display: flex;
		flex-direction: column;
		gap: 15px;
		max-height: calc(100vh - 200px);
		overflow-y: auto;
	}

	h2 {
		margin: 0 0 15px 0;
		color: #e0e7ff;
		font-size: 1.25rem;
		border-bottom: 2px solid rgba(99, 102, 241, 0.3);
		padding-bottom: 10px;
	}

	.debug-section {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 12px;
	}

	.debug-section.current-state {
		background: rgba(34, 197, 94, 0.1);
		border-color: rgba(34, 197, 94, 0.3);
	}

	.debug-section.summary {
		background: rgba(99, 102, 241, 0.1);
		border-color: rgba(99, 102, 241, 0.3);
	}

	.debug-section.motion-summary {
		background: rgba(168, 85, 247, 0.1);
		border-color: rgba(168, 85, 247, 0.3);
	}

	.debug-section.error {
		background: rgba(239, 68, 68, 0.1);
		border-color: rgba(239, 68, 68, 0.3);
	}

	.debug-section h3 {
		margin: 0 0 10px 0;
		color: #fbbf24;
		font-size: 0.95rem;
		font-weight: 600;
	}

	.current-state h3 {
		color: #4ade80;
	}

	.summary h3 {
		color: #a5b4fc;
	}

	.motion-summary h3 {
		color: #c084fc;
	}

	.error h3 {
		color: #f87171;
	}

	.prop-debug {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.prop-info h4 {
		margin: 0 0 8px 0;
		font-size: 0.85rem;
		text-align: center;
		padding: 4px 8px;
		border-radius: 4px;
	}

	.prop-info:first-child h4 {
		color: #60a5fa;
		background: rgba(96, 165, 250, 0.1);
	}

	.prop-info:last-child h4 {
		color: #f87171;
		background: rgba(248, 113, 113, 0.1);
	}

	.debug-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 6px;
		font-size: 0.8rem;
		gap: 10px;
	}

	.debug-item:last-child {
		margin-bottom: 0;
	}

	.debug-item .label {
		color: #c7d2fe;
		flex: 1;
		min-width: 0;
	}

	.debug-item .value {
		color: #34d399;
		font-family: 'Courier New', monospace;
		font-weight: 500;
		flex-shrink: 0;
		text-align: right;
	}

	.debug-item .value.motion-desc {
		font-size: 0.75rem;
		color: #c084fc;
		word-break: break-all;
	}

	.debug-item .value.engine-status.initialized {
		color: #10b981;
		font-weight: 600;
	}

	.debug-item .value.playing {
		color: #10b981;
		font-weight: 600;
	}

	.quick-test-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px;
		margin-top: 5px;
	}

	.quick-test-btn {
		padding: 8px 10px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.05);
		color: #c7d2fe;
		cursor: pointer;
		font-size: 0.75rem;
		font-weight: 500;
		transition: all 0.2s ease;
	}

	.quick-test-btn:hover {
		background: rgba(99, 102, 241, 0.2);
		border-color: rgba(99, 102, 241, 0.4);
		color: white;
	}

	/* Scrollbar styling for webkit browsers */
	.debug-panel::-webkit-scrollbar {
		width: 6px;
	}

	.debug-panel::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}

	.debug-panel::-webkit-scrollbar-thumb {
		background: rgba(99, 102, 241, 0.5);
		border-radius: 3px;
	}

	.debug-panel::-webkit-scrollbar-thumb:hover {
		background: rgba(99, 102, 241, 0.7);
	}

	@media (max-width: 768px) {
		.debug-item {
			font-size: 0.75rem;
		}

		.prop-debug {
			grid-template-columns: 1fr;
		}

		.quick-test-grid {
			grid-template-columns: 1fr;
		}

		.quick-test-btn {
			font-size: 0.7rem;
		}
	}
</style>
