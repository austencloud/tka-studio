<script lang="ts">
	import type { ArrowDebugState } from './state/arrow-debug-state.svelte';

	interface Props {
		state: ArrowDebugState;
	}

	let { state }: Props = $props();

	function formatCoordinate(value: number | undefined): string {
		if (value === undefined || value === null) return 'N/A';
		return value.toFixed(2);
	}

	function formatPoint(point: any): string {
		if (!point) return 'N/A';
		if (typeof point.x === 'function' && typeof point.y === 'function') {
			return `(${formatCoordinate(point.x())}, ${formatCoordinate(point.y())})`;
		}
		return `(${formatCoordinate(point.x)}, ${formatCoordinate(point.y)})`;
	}

	function formatTimestamp(timestamp: number): string {
		return new Date(timestamp).toLocaleTimeString();
	}

	function getStepStatus(stepIndex: number): 'completed' | 'current' | 'pending' {
		if (stepIndex < state.currentStep) return 'completed';
		if (stepIndex === state.currentStep) return 'current';
		return 'pending';
	}

	function isStepVisible(stepIndex: number): boolean {
		if (!state.stepByStepMode) return true;
		return stepIndex <= state.currentStep;
	}
</script>

<div class="debug-info-panel">
	<h2>🔍 Debug Information</h2>

	<!-- Calculation Status -->
	<section class="debug-section">
		<div 
			class="section-header" 
			onclick={() => state.toggleSection('calculation_status')}
			onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('calculation_status') : null}
			role="button"
			tabindex="0"
			aria-expanded={state.expandedSections.has('calculation_status')}
		>
			<h3>⚙️ Calculation Status</h3>
			<span class="toggle-icon {state.expandedSections.has('calculation_status') ? 'expanded' : ''}">▼</span>
		</div>
		
		{#if state.expandedSections.has('calculation_status')}
			<div class="section-content">
				<div class="status-item">
					<span class="label">Status:</span>
					<span class="value {state.isCalculating ? 'calculating' : 'idle'}">
						{state.isCalculating ? '⏳ Calculating...' : '✅ Ready'}
					</span>
				</div>
				
				{#if state.currentDebugData.timing}
					<div class="status-item">
						<span class="label">Total Time:</span>
						<span class="value">{state.currentDebugData.timing.totalDuration.toFixed(2)}ms</span>
					</div>
				{/if}
				
				{#if state.currentDebugData.errors.length > 0}
					<div class="error-list">
						<h4>❌ Errors:</h4>
						{#each state.currentDebugData.errors as error}
							<div class="error-item">
								<span class="error-step">{error.step}:</span>
								<span class="error-message">{error.error}</span>
								<span class="error-time">{formatTimestamp(error.timestamp)}</span>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</section>

	<!-- Step 1: Location Calculation -->
	{#if isStepVisible(1)}
		<section class="debug-section step-section" data-status={getStepStatus(1)}>
			<div 
				class="section-header" 
				onclick={() => state.toggleSection('location_calc')}
				onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('location_calc') : null}
				role="button"
				tabindex="0"
				aria-expanded={state.expandedSections.has('location_calc')}
			>
				<h3>📍 Step 1: Location Calculation</h3>
				<span class="step-status">{getStepStatus(1)}</span>
				<span class="toggle-icon {state.expandedSections.has('location_calc') ? 'expanded' : ''}">▼</span>
			</div>
			
			{#if state.expandedSections.has('location_calc')}
				<div class="section-content">
					{#if state.currentDebugData.locationDebugInfo}
						<div class="debug-grid">
							<div class="debug-item">
								<span class="label">Motion Type:</span>
								<span class="value">{state.currentDebugData.locationDebugInfo.motionType}</span>
							</div>
							<div class="debug-item">
								<span class="label">Start Orientation:</span>
								<span class="value">{state.currentDebugData.locationDebugInfo.startOri}</span>
							</div>
							<div class="debug-item">
								<span class="label">End Orientation:</span>
								<span class="value">{state.currentDebugData.locationDebugInfo.endOri}</span>
							</div>
							<div class="debug-item">
								<span class="label">Calculation Method:</span>
								<span class="value">{state.currentDebugData.locationDebugInfo.calculationMethod}</span>
							</div>
						</div>
					{/if}
					
					<div class="result-box">
						<span class="result-label">Calculated Location:</span>
						<span class="result-value location">
							{state.currentDebugData.calculatedLocation || 'Not calculated'}
						</span>
					</div>
					
					{#if state.currentDebugData.timing?.stepDurations.location}
						<div class="timing-info">
							Time: {state.currentDebugData.timing.stepDurations.location.toFixed(2)}ms
						</div>
					{/if}
				</div>
			{/if}
		</section>
	{/if}

	<!-- Step 2: Initial Position -->
	{#if isStepVisible(2)}
		<section class="debug-section step-section" data-status={getStepStatus(2)}>
			<div 
				class="section-header" 
				onclick={() => state.toggleSection('initial_pos')}
				onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('initial_pos') : null}
				role="button"
				tabindex="0"
				aria-expanded={state.expandedSections.has('initial_pos')}
			>
				<h3>🎯 Step 2: Initial Position</h3>
				<span class="step-status">{getStepStatus(2)}</span>
				<span class="toggle-icon {state.expandedSections.has('initial_pos') ? 'expanded' : ''}">▼</span>
			</div>
			
			{#if state.expandedSections.has('initial_pos')}
				<div class="section-content">
					{#if state.currentDebugData.coordinateSystemDebugInfo}
						<div class="coordinate-system-info">
							<h4>🗺️ Coordinate System Info</h4>
							<div class="debug-grid">
								<div class="debug-item">
									<span class="label">Scene Center:</span>
									<span class="value">{formatPoint(state.currentDebugData.coordinateSystemDebugInfo.sceneCenter)}</span>
								</div>
								<div class="debug-item">
									<span class="label">Scene Size:</span>
									<span class="value">{state.currentDebugData.coordinateSystemDebugInfo.sceneDimensions[0]}×{state.currentDebugData.coordinateSystemDebugInfo.sceneDimensions[1]}</span>
								</div>
								<div class="debug-item">
									<span class="label">Used Coordinate Set:</span>
									<span class="value coordinate-set">{state.currentDebugData.coordinateSystemDebugInfo.usedCoordinateSet}</span>
								</div>
								<div class="debug-item">
									<span class="label">Coordinate System Type:</span>
									<span class="value">{state.currentDebugData.coordinateSystemDebugInfo.coordinateSystemType}</span>
								</div>
							</div>
						</div>
					{/if}
					
					<div class="result-box">
						<span class="result-label">Initial Position:</span>
						<span class="result-value position">
							{formatPoint(state.currentDebugData.initialPosition)}
						</span>
					</div>
					
					{#if state.currentDebugData.timing?.stepDurations.initial_position}
						<div class="timing-info">
							Time: {state.currentDebugData.timing.stepDurations.initial_position.toFixed(2)}ms
						</div>
					{/if}
				</div>
			{/if}
		</section>
	{/if}

	<!-- Step 3: Default Adjustment -->
	{#if isStepVisible(3)}
		<section class="debug-section step-section" data-status={getStepStatus(3)}>
			<div 
				class="section-header" 
				onclick={() => state.toggleSection('default_adj')}
				onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('default_adj') : null}
				role="button"
				tabindex="0"
				aria-expanded={state.expandedSections.has('default_adj')}
			>
				<h3>⚙️ Step 3: Default Adjustment</h3>
				<span class="step-status">{getStepStatus(3)}</span>
				<span class="toggle-icon {state.expandedSections.has('default_adj') ? 'expanded' : ''}">▼</span>
			</div>
			
			{#if state.expandedSections.has('default_adj')}
				<div class="section-content">
					{#if state.currentDebugData.defaultAdjustmentDebugInfo}
						<div class="debug-grid">
							<div class="debug-item">
								<span class="label">Placement Key:</span>
								<span class="value">{state.currentDebugData.defaultAdjustmentDebugInfo.placementKey}</span>
							</div>
							<div class="debug-item">
								<span class="label">Turns:</span>
								<span class="value">{state.currentDebugData.defaultAdjustmentDebugInfo.turns}</span>
							</div>
							<div class="debug-item">
								<span class="label">Motion Type:</span>
								<span class="value">{state.currentDebugData.defaultAdjustmentDebugInfo.motionType}</span>
							</div>
							<div class="debug-item">
								<span class="label">Grid Mode:</span>
								<span class="value">{state.currentDebugData.defaultAdjustmentDebugInfo.gridMode}</span>
							</div>
							<div class="debug-item">
								<span class="label">Adjustment Source:</span>
								<span class="value source-{state.currentDebugData.defaultAdjustmentDebugInfo.adjustmentSource}">
									{state.currentDebugData.defaultAdjustmentDebugInfo.adjustmentSource}
								</span>
							</div>
						</div>
					{/if}
					
					<div class="result-box">
						<span class="result-label">Default Adjustment:</span>
						<span class="result-value adjustment">
							{formatPoint(state.currentDebugData.defaultAdjustment)}
						</span>
					</div>
				</div>
			{/if}
		</section>
	{/if}

	<!-- Step 4: Special Adjustment -->
	{#if isStepVisible(4)}
		<section class="debug-section step-section" data-status={getStepStatus(4)}>
			<div 
				class="section-header" 
				onclick={() => state.toggleSection('special_adj')}
				onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('special_adj') : null}
				role="button"
				tabindex="0"
				aria-expanded={state.expandedSections.has('special_adj')}
			>
				<h3>✨ Step 4: Special Adjustment</h3>
				<span class="step-status">{getStepStatus(4)}</span>
				<span class="toggle-icon {state.expandedSections.has('special_adj') ? 'expanded' : ''}">▼</span>
			</div>
			
			{#if state.expandedSections.has('special_adj')}
				<div class="section-content">
					{#if state.currentDebugData.specialAdjustmentDebugInfo}
						<div class="debug-grid">
							<div class="debug-item">
								<span class="label">Letter:</span>
								<span class="value">{state.currentDebugData.specialAdjustmentDebugInfo.letter}</span>
							</div>
							<div class="debug-item">
								<span class="label">Orientation Key:</span>
								<span class="value">{state.currentDebugData.specialAdjustmentDebugInfo.oriKey}</span>
							</div>
							<div class="debug-item">
								<span class="label">Turns Tuple:</span>
								<span class="value">{state.currentDebugData.specialAdjustmentDebugInfo.turnsTuple}</span>
							</div>
							<div class="debug-item">
								<span class="label">Arrow Color:</span>
								<span class="value color-{state.currentDebugData.specialAdjustmentDebugInfo.arrowColor}">
									{state.currentDebugData.specialAdjustmentDebugInfo.arrowColor}
								</span>
							</div>
							<div class="debug-item">
								<span class="label">Special Placement Found:</span>
								<span class="value {state.currentDebugData.specialAdjustmentDebugInfo.specialPlacementFound ? 'found' : 'not-found'}">
									{state.currentDebugData.specialAdjustmentDebugInfo.specialPlacementFound ? '✅ Yes' : '❌ No'}
								</span>
							</div>
							<div class="debug-item">
								<span class="label">Adjustment Source:</span>
								<span class="value source-{state.currentDebugData.specialAdjustmentDebugInfo.adjustmentSource}">
									{state.currentDebugData.specialAdjustmentDebugInfo.adjustmentSource}
								</span>
							</div>
						</div>
					{/if}
					
					<div class="result-box">
						<span class="result-label">Special Adjustment:</span>
						<span class="result-value adjustment">
							{formatPoint(state.currentDebugData.specialAdjustment)}
						</span>
					</div>
				</div>
			{/if}
		</section>
	{/if}

	<!-- Step 5: Final Result -->
	{#if isStepVisible(5)}
		<section class="debug-section step-section" data-status={getStepStatus(5)}>
			<div 
				class="section-header" 
				onclick={() => state.toggleSection('final_result')}
				onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? state.toggleSection('final_result') : null}
				role="button"
				tabindex="0"
				aria-expanded={state.expandedSections.has('final_result')}
			>
				<h3>🎯 Step 5: Final Result</h3>
				<span class="step-status">{getStepStatus(5)}</span>
				<span class="toggle-icon {state.expandedSections.has('final_result') ? 'expanded' : ''}">▼</span>
			</div>
			
			{#if state.expandedSections.has('final_result')}
				<div class="section-content">
					{#if state.currentDebugData.tupleProcessingDebugInfo}
						<div class="tuple-processing-info">
							<h4>🔄 Directional Tuple Processing</h4>
							<div class="debug-grid">
								<div class="debug-item">
									<span class="label">Base Adjustment:</span>
									<span class="value">{formatPoint(state.currentDebugData.tupleProcessingDebugInfo.baseAdjustment)}</span>
								</div>
								<div class="debug-item">
									<span class="label">Quadrant Index:</span>
									<span class="value">{state.currentDebugData.tupleProcessingDebugInfo.quadrantIndex}</span>
								</div>
								<div class="debug-item">
									<span class="label">Selected Tuple:</span>
									<span class="value">({state.currentDebugData.tupleProcessingDebugInfo.selectedTuple[0]}, {state.currentDebugData.tupleProcessingDebugInfo.selectedTuple[1]})</span>
								</div>
								<div class="debug-item">
									<span class="label">Transformation Method:</span>
									<span class="value">{state.currentDebugData.tupleProcessingDebugInfo.transformationMethod}</span>
								</div>
							</div>
						</div>
					{/if}
					
					<div class="final-results">
						<div class="result-box major">
							<span class="result-label">Final Position:</span>
							<span class="result-value position final">
								{formatPoint(state.currentDebugData.finalPosition)}
							</span>
						</div>
						
						<div class="result-box">
							<span class="result-label">Final Rotation:</span>
							<span class="result-value rotation">
								{formatCoordinate(state.currentDebugData.finalRotation)}°
							</span>
						</div>
					</div>
					
					<!-- Breakdown calculation -->
					{#if state.currentDebugData.initialPosition && state.currentDebugData.tupleProcessedAdjustment}
						<div class="calculation-breakdown">
							<h4>📊 Position Calculation Breakdown</h4>
							<div class="breakdown-step">
								<span class="breakdown-label">Initial Position:</span>
								<span class="breakdown-value">{formatPoint(state.currentDebugData.initialPosition)}</span>
							</div>
							<div class="breakdown-step">
								<span class="breakdown-label">+ Total Adjustment:</span>
								<span class="breakdown-value">{formatPoint(state.currentDebugData.tupleProcessedAdjustment)}</span>
							</div>
							<div class="breakdown-step final-calc">
								<span class="breakdown-label">= Final Position:</span>
								<span class="breakdown-value">{formatPoint(state.currentDebugData.finalPosition)}</span>
							</div>
						</div>
					{/if}
				</div>
			{/if}
		</section>
	{/if}
</div>

<style>
	.debug-info-panel {
		display: flex;
		flex-direction: column;
		gap: 15px;
		height: 100%;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #fbbf24;
		font-size: 1.3rem;
		border-bottom: 2px solid rgba(251, 191, 36, 0.3);
		padding-bottom: 10px;
		text-align: center;
	}

	.debug-section {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		overflow: hidden;
	}

	.step-section[data-status="completed"] {
		border-color: rgba(34, 197, 94, 0.3);
		background: rgba(34, 197, 94, 0.05);
	}

	.step-section[data-status="current"] {
		border-color: rgba(251, 191, 36, 0.5);
		background: rgba(251, 191, 36, 0.1);
		box-shadow: 0 0 12px rgba(251, 191, 36, 0.2);
	}

	.step-section[data-status="pending"] {
		border-color: rgba(156, 163, 175, 0.3);
		background: rgba(156, 163, 175, 0.05);
		opacity: 0.7;
	}

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 15px;
		background: rgba(0, 0, 0, 0.3);
		cursor: pointer;
		transition: background 0.2s ease;
	}

	.section-header:hover {
		background: rgba(255, 255, 255, 0.1);
	}

	.section-header h3 {
		margin: 0;
		font-size: 0.95rem;
		color: #fde047;
		flex: 1;
	}

	.step-status {
		font-size: 0.8rem;
		padding: 2px 8px;
		border-radius: 4px;
		text-transform: uppercase;
		font-weight: 600;
		margin-right: 10px;
	}

	.step-section[data-status="completed"] .step-status {
		background: rgba(34, 197, 94, 0.2);
		color: #22c55e;
	}

	.step-section[data-status="current"] .step-status {
		background: rgba(251, 191, 36, 0.2);
		color: #fbbf24;
	}

	.step-section[data-status="pending"] .step-status {
		background: rgba(156, 163, 175, 0.2);
		color: #9ca3af;
	}

	.toggle-icon {
		font-size: 0.8rem;
		color: #a3a3a3;
		transition: transform 0.2s ease;
	}

	.toggle-icon.expanded {
		transform: rotate(180deg);
	}

	.section-content {
		padding: 15px;
	}

	.status-item, .debug-item {
		display: flex;
		justify-content: space-between;
		margin-bottom: 8px;
		font-size: 0.85rem;
	}

	.label {
		color: #a3a3a3;
		font-weight: 500;
	}

	.value {
		color: #e5e7eb;
		font-family: 'Courier New', monospace;
	}

	.value.calculating {
		color: #fbbf24;
	}

	.value.idle {
		color: #22c55e;
	}

	.value.location {
		color: #60a5fa;
		font-weight: 600;
	}

	.value.coordinate-set {
		color: #f59e0b;
		font-weight: 600;
	}

	.value.color-blue {
		color: #60a5fa;
	}

	.value.color-red {
		color: #f87171;
	}

	.value.found {
		color: #22c55e;
	}

	.value.not-found {
		color: #f87171;
	}

	.value.source-default_placement {
		color: #a78bfa;
	}

	.value.source-special_placement {
		color: #34d399;
	}

	.value.source-none {
		color: #9ca3af;
	}

	.debug-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 6px;
		margin-bottom: 12px;
	}

	.result-box {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		padding: 10px;
		margin-bottom: 10px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.result-box.major {
		border-color: #fbbf24;
		background: rgba(251, 191, 36, 0.1);
	}

	.result-label {
		color: #c7d2fe;
		font-size: 0.9rem;
		font-weight: 600;
	}

	.result-value {
		font-family: 'Courier New', monospace;
		font-weight: 600;
		font-size: 0.95rem;
	}

	.result-value.position {
		color: #60a5fa;
	}

	.result-value.adjustment {
		color: #34d399;
	}

	.result-value.rotation {
		color: #f472b6;
	}

	.result-value.final {
		color: #fbbf24;
		font-size: 1.1rem;
	}

	.timing-info {
		font-size: 0.8rem;
		color: #9ca3af;
		text-align: right;
		margin-top: 8px;
	}

	.error-list {
		margin-top: 12px;
	}

	.error-list h4 {
		margin: 0 0 8px 0;
		color: #f87171;
		font-size: 0.9rem;
	}

	.error-item {
		background: rgba(248, 113, 113, 0.1);
		border: 1px solid rgba(248, 113, 113, 0.3);
		border-radius: 4px;
		padding: 8px;
		margin-bottom: 6px;
		font-size: 0.8rem;
	}

	.error-step {
		color: #fbbf24;
		font-weight: 600;
	}

	.error-message {
		color: #f87171;
		margin-left: 8px;
	}

	.error-time {
		color: #9ca3af;
		font-size: 0.7rem;
		display: block;
		margin-top: 4px;
	}

	.coordinate-system-info h4,
	.tuple-processing-info h4,
	.calculation-breakdown h4 {
		margin: 0 0 10px 0;
		color: #a78bfa;
		font-size: 0.9rem;
		border-bottom: 1px solid rgba(167, 139, 250, 0.2);
		padding-bottom: 6px;
	}

	.final-results {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.calculation-breakdown {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 6px;
		padding: 12px;
		margin-top: 12px;
	}

	.breakdown-step {
		display: flex;
		justify-content: space-between;
		margin-bottom: 6px;
		font-size: 0.85rem;
	}

	.breakdown-step.final-calc {
		border-top: 1px solid rgba(251, 191, 36, 0.3);
		padding-top: 6px;
		margin-top: 8px;
		font-weight: 600;
	}

	.breakdown-label {
		color: #c7d2fe;
	}

	.breakdown-value {
		color: #60a5fa;
		font-family: 'Courier New', monospace;
	}

	.breakdown-step.final-calc .breakdown-value {
		color: #fbbf24;
	}
</style>
