<script lang="ts">
	/**
	 * Debug Info Panel Component
	 * Shows detailed debug information for each step of the positioning process
	 */

	import type { DebugStepData } from './types';

	interface Props {
		debugData: DebugStepData;
		expandedSections: Set<string>;
		onToggleSection: (section: string) => void;
		isCalculating: boolean;
	}

	let { debugData, expandedSections, onToggleSection, isCalculating }: Props = $props();

	function formatJson(obj: unknown): string {
		return JSON.stringify(obj, null, 2);
	}

	function formatTimestamp(timestamp: number): string {
		return new Date(timestamp).toLocaleTimeString();
	}

	function isExpanded(section: string): boolean {
		return expandedSections.has(section);
	}
</script>

<div class="debug-info">
	<div class="info-header">
		<h3>📋 Debug Information</h3>
		{#if isCalculating}
			<div class="calculating-indicator">
				<div class="spinner-small"></div>
				Calculating...
			</div>
		{/if}
	</div>

	<div class="info-sections">
		<!-- Input Data Section -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('input_data')}
				onclick={() => onToggleSection('input_data')}
			>
				<span class="icon">{isExpanded('input_data') ? '▼' : '▶'}</span>
				Input Data
			</button>
			{#if isExpanded('input_data')}
				<div class="section-content">
					{#if debugData.pictographData}
						<div class="data-item">
							<strong>Pictograph:</strong> {debugData.pictographData.letter || debugData.pictographData.id}
						</div>
					{/if}
					{#if debugData.motionData}
						<div class="data-item">
							<strong>Motion Type:</strong> {debugData.motionData.motion_type}
						</div>
						<div class="data-item">
							<strong>Start Orientation:</strong> {debugData.motionData.start_ori}
						</div>
						<div class="data-item">
							<strong>End Orientation:</strong> {debugData.motionData.end_ori}
						</div>
					{/if}
					{#if debugData.arrowData}
						<div class="data-item">
							<strong>Arrow Color:</strong> {debugData.arrowData.color}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Step 1: Location Calculation -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('location_calculation')}
				onclick={() => onToggleSection('location_calculation')}
			>
				<span class="icon">{isExpanded('location_calculation') ? '▼' : '▶'}</span>
				Step 1: Location Calculation
				{#if debugData.calculatedLocation}
					<span class="result-badge success">{debugData.calculatedLocation}</span>
				{:else}
					<span class="result-badge pending">Pending</span>
				{/if}
			</button>
			{#if isExpanded('location_calculation')}
				<div class="section-content">
					{#if debugData.locationDebugInfo}
						<div class="data-item">
							<strong>Motion Type:</strong> {debugData.locationDebugInfo.motionType}
						</div>
						<div class="data-item">
							<strong>Calculation Method:</strong> {debugData.locationDebugInfo.calculationMethod}
						</div>
						<div class="data-item">
							<strong>Start Orientation:</strong> {debugData.locationDebugInfo.startOri}
						</div>
						<div class="data-item">
							<strong>End Orientation:</strong> {debugData.locationDebugInfo.endOri}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Step 2: Coordinate System -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('coordinate_system')}
				onclick={() => onToggleSection('coordinate_system')}
			>
				<span class="icon">{isExpanded('coordinate_system') ? '▼' : '▶'}</span>
				Step 2: Coordinate System
				{#if debugData.initialPosition}
					<span class="result-badge success">
						({debugData.initialPosition.x.toFixed(1)}, {debugData.initialPosition.y.toFixed(1)})
					</span>
				{:else}
					<span class="result-badge pending">Pending</span>
				{/if}
			</button>
			{#if isExpanded('coordinate_system')}
				<div class="section-content">
					{#if debugData.coordinateSystemDebugInfo}
						<div class="data-item">
							<strong>Scene Center:</strong> 
							({debugData.coordinateSystemDebugInfo.sceneCenter.x}, {debugData.coordinateSystemDebugInfo.sceneCenter.y})
						</div>
						<div class="data-item">
							<strong>Scene Dimensions:</strong> 
							{debugData.coordinateSystemDebugInfo.sceneDimensions[0]} × {debugData.coordinateSystemDebugInfo.sceneDimensions[1]}
						</div>
						<div class="data-item">
							<strong>Coordinate Set Used:</strong> {debugData.coordinateSystemDebugInfo.usedCoordinateSet}
						</div>
						<div class="data-item">
							<strong>System Type:</strong> {debugData.coordinateSystemDebugInfo.coordinateSystemType}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Step 3: Default Adjustment -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('default_adjustment')}
				onclick={() => onToggleSection('default_adjustment')}
			>
				<span class="icon">{isExpanded('default_adjustment') ? '▼' : '▶'}</span>
				Step 3: Default Adjustment
				{#if debugData.defaultAdjustment}
					<span class="result-badge success">
						({debugData.defaultAdjustment.x.toFixed(1)}, {debugData.defaultAdjustment.y.toFixed(1)})
					</span>
				{:else}
					<span class="result-badge pending">Pending</span>
				{/if}
			</button>
			{#if isExpanded('default_adjustment')}
				<div class="section-content">
					{#if debugData.defaultAdjustmentDebugInfo}
						<div class="data-item">
							<strong>Placement Key:</strong> {debugData.defaultAdjustmentDebugInfo.placementKey}
						</div>
						<div class="data-item">
							<strong>Turns:</strong> {debugData.defaultAdjustmentDebugInfo.turns}
						</div>
						<div class="data-item">
							<strong>Grid Mode:</strong> {debugData.defaultAdjustmentDebugInfo.gridMode}
						</div>
						<div class="data-item">
							<strong>Adjustment Source:</strong> {debugData.defaultAdjustmentDebugInfo.adjustmentSource}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Step 4: Special Adjustment -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('special_adjustment')}
				onclick={() => onToggleSection('special_adjustment')}
			>
				<span class="icon">{isExpanded('special_adjustment') ? '▼' : '▶'}</span>
				Step 4: Special Adjustment
				{#if debugData.specialAdjustment}
					<span class="result-badge success">
						({debugData.specialAdjustment.x.toFixed(1)}, {debugData.specialAdjustment.y.toFixed(1)})
					</span>
				{:else}
					<span class="result-badge pending">Pending</span>
				{/if}
			</button>
			{#if isExpanded('special_adjustment')}
				<div class="section-content">
					{#if debugData.specialAdjustmentDebugInfo}
						<div class="data-item">
							<strong>Letter:</strong> {debugData.specialAdjustmentDebugInfo.letter}
						</div>
						<div class="data-item">
							<strong>Orientation Key:</strong> {debugData.specialAdjustmentDebugInfo.oriKey}
						</div>
						<div class="data-item">
							<strong>Turns Tuple:</strong> {debugData.specialAdjustmentDebugInfo.turnsTuple}
						</div>
						<div class="data-item">
							<strong>Special Placement Found:</strong> 
							{debugData.specialAdjustmentDebugInfo.specialPlacementFound ? 'Yes' : 'No'}
						</div>
						<div class="data-item">
							<strong>Adjustment Source:</strong> {debugData.specialAdjustmentDebugInfo.adjustmentSource}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Step 5: Tuple Processing -->
		<div class="section">
			<button 
				class="section-header" 
				class:expanded={isExpanded('tuple_processing')}
				onclick={() => onToggleSection('tuple_processing')}
			>
				<span class="icon">{isExpanded('tuple_processing') ? '▼' : '▶'}</span>
				Step 5: Tuple Processing
				{#if debugData.tupleProcessedAdjustment}
					<span class="result-badge success">
						({debugData.tupleProcessedAdjustment.x.toFixed(1)}, {debugData.tupleProcessedAdjustment.y.toFixed(1)})
					</span>
				{:else}
					<span class="result-badge pending">Pending</span>
				{/if}
			</button>
			{#if isExpanded('tuple_processing')}
				<div class="section-content">
					{#if debugData.tupleProcessingDebugInfo}
						<div class="data-item">
							<strong>Base Adjustment:</strong> 
							({debugData.tupleProcessingDebugInfo.baseAdjustment.x}, {debugData.tupleProcessingDebugInfo.baseAdjustment.y})
						</div>
						<div class="data-item">
							<strong>Quadrant Index:</strong> {debugData.tupleProcessingDebugInfo.quadrantIndex}
						</div>
						<div class="data-item">
							<strong>Selected Tuple:</strong> 
							[{debugData.tupleProcessingDebugInfo.selectedTuple[0]}, {debugData.tupleProcessingDebugInfo.selectedTuple[1]}]
						</div>
						<div class="data-item">
							<strong>Transformation Method:</strong> {debugData.tupleProcessingDebugInfo.transformationMethod}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Errors Section -->
		{#if debugData.errors.length > 0}
			<div class="section error-section">
				<button 
					class="section-header" 
					class:expanded={isExpanded('errors')}
					onclick={() => onToggleSection('errors')}
				>
					<span class="icon">{isExpanded('errors') ? '▼' : '▶'}</span>
					Errors ({debugData.errors.length})
				</button>
				{#if isExpanded('errors')}
					<div class="section-content">
						{#each debugData.errors as error}
							<div class="error-item">
								<div class="error-step">{error.step}</div>
								<div class="error-message">{error.error}</div>
								<div class="error-time">{formatTimestamp(error.timestamp)}</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}

		<!-- Performance Section -->
		{#if debugData.timing}
			<div class="section">
				<button 
					class="section-header" 
					class:expanded={isExpanded('performance')}
					onclick={() => onToggleSection('performance')}
				>
					<span class="icon">{isExpanded('performance') ? '▼' : '▶'}</span>
					Performance
				</button>
				{#if isExpanded('performance')}
					<div class="section-content">
						<div class="data-item">
							<strong>Total Duration:</strong> {debugData.timing.totalDuration.toFixed(2)}ms
						</div>
						{#each Object.entries(debugData.timing.stepDurations) as [step, duration]}
							<div class="data-item">
								<strong>{step}:</strong> {duration.toFixed(2)}ms
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>

<style>
	.debug-info {
		display: flex;
		flex-direction: column;
		height: 100%;
	}

	.info-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16px;
		padding: 0 4px;
	}

	.info-header h3 {
		margin: 0;
		color: #fbbf24;
		font-size: 1.1rem;
	}

	.calculating-indicator {
		display: flex;
		align-items: center;
		gap: 8px;
		color: #fbbf24;
		font-size: 0.9rem;
	}

	.spinner-small {
		width: 16px;
		height: 16px;
		border: 2px solid rgba(251, 191, 36, 0.3);
		border-top: 2px solid #fbbf24;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.info-sections {
		flex: 1;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.section {
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.05);
		overflow: hidden;
	}

	.error-section {
		border-color: rgba(248, 113, 113, 0.3);
		background: rgba(248, 113, 113, 0.05);
	}

	.section-header {
		width: 100%;
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 12px;
		background: none;
		border: none;
		color: #c7d2fe;
		cursor: pointer;
		font-size: 0.95rem;
		text-align: left;
		transition: background-color 0.2s ease;
	}

	.section-header:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.section-header.expanded {
		background: rgba(251, 191, 36, 0.1);
		color: #fbbf24;
	}

	.icon {
		font-size: 0.8rem;
		color: #fbbf24;
		min-width: 12px;
	}

	.result-badge {
		margin-left: auto;
		padding: 2px 8px;
		border-radius: 10px;
		font-size: 0.8rem;
		font-weight: 600;
	}

	.result-badge.success {
		background: rgba(16, 185, 129, 0.2);
		color: #10b981;
		border: 1px solid rgba(16, 185, 129, 0.3);
	}

	.result-badge.pending {
		background: rgba(156, 163, 175, 0.2);
		color: #9ca3af;
		border: 1px solid rgba(156, 163, 175, 0.3);
	}

	.section-content {
		padding: 16px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(0, 0, 0, 0.2);
	}

	.data-item {
		margin-bottom: 8px;
		color: #c7d2fe;
		font-size: 0.9rem;
		line-height: 1.4;
	}

	.data-item:last-child {
		margin-bottom: 0;
	}

	.data-item strong {
		color: #fbbf24;
	}

	.error-item {
		margin-bottom: 12px;
		padding: 8px;
		background: rgba(248, 113, 113, 0.1);
		border: 1px solid rgba(248, 113, 113, 0.2);
		border-radius: 4px;
	}

	.error-item:last-child {
		margin-bottom: 0;
	}

	.error-step {
		font-weight: 600;
		color: #f87171;
		font-size: 0.85rem;
		margin-bottom: 4px;
	}

	.error-message {
		color: #fecaca;
		font-size: 0.9rem;
		margin-bottom: 4px;
	}

	.error-time {
		color: #9ca3af;
		font-size: 0.8rem;
	}
</style>
