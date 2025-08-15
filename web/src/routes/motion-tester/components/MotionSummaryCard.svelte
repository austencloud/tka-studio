<!--
MotionSummaryCard.svelte - Motion description summary

Displays concise motion descriptions for both props with clear formatting
and accessibility features. Shows motion types, locations, and parameters.
-->
<script lang="ts">
	import type { MotionTesterState } from '../state/motion-tester-state.svelte';

	interface Props {
		state: MotionTesterState;
	}

	let { state: motionState }: Props = $props();

	// Local state for display options
	let showFullDetails = $state(false);
	let showMotionTypes = $state(true);
	let compactView = $state(false);

	// Helper functions for motion description formatting
	function formatMotionType(motionType: string): string {
		switch (motionType) {
			case 'static': return 'Static';
			case 'shift': return 'Shift';
			case 'dash': return 'Dash';
			case 'linear': return 'Linear';
			case 'circular': return 'Circular';
			default: return motionType.charAt(0).toUpperCase() + motionType.slice(1);
		}
	}

	function formatLocation(location: string): string {
		return location.toUpperCase();
	}

	function formatOrientation(orientation: string | undefined): string {
		if (!orientation) return '';
		return orientation.toUpperCase();
	}

	function formatPropRotDir(propRotDir: string): string {
		switch (propRotDir) {
			case 'no_rot': return 'No Rotation';
			case 'cw': return 'Clockwise';
			case 'ccw': return 'Counter-CW';
			default: return propRotDir;
		}
	}

	function formatTurns(turns: number | "fl"): string {
		if (turns === "fl") return 'Float';
		if (turns === 0) return 'No Turns';
		if (turns === 1) return '1 Turn';
		return `${turns} Turns`;
	}

	// Generate readable motion description
	function generateMotionDescription(params: any): string {
		const { motionType, startLoc, endLoc, startOri, endOri, propRotDir, turns } = params;
		
		let description = formatMotionType(motionType);
		
		if (startLoc !== endLoc) {
			description += ` from ${formatLocation(startLoc)} to ${formatLocation(endLoc)}`;
		} else {
			description += ` at ${formatLocation(startLoc)}`;
		}

		if (startOri && (startOri !== endOri || showFullDetails)) {
			if (endOri && startOri !== endOri) {
				description += `, ${formatOrientation(startOri)} → ${formatOrientation(endOri)}`;
			} else if (showFullDetails) {
				description += `, ${formatOrientation(startOri)}`;
			}
		}

		if (propRotDir !== 'no_rot' || showFullDetails) {
			description += `, ${formatPropRotDir(propRotDir)}`;
		}

		if (turns > 0 || showFullDetails) {
			description += `, ${formatTurns(turns)}`;
		}

		return description;
	}

	// Generate motion complexity indicator
	function getMotionComplexity(params: any): 'simple' | 'moderate' | 'complex' {
		const { motionType, startLoc, endLoc, propRotDir, turns } = params;
		
		let complexity = 0;
		
		// Base complexity for motion type
		if (motionType === 'static') complexity += 0;
		else if (motionType === 'shift') complexity += 1;
		else if (motionType === 'dash') complexity += 2;
		else complexity += 3;
		
		// Location change adds complexity
		if (startLoc !== endLoc) complexity += 1;
		
		// Prop rotation adds complexity
		if (propRotDir !== 'no_rot') complexity += 1;
		
		// Turns add complexity
		complexity += Math.min(turns, 3);
		
		if (complexity <= 2) return 'simple';
		if (complexity <= 5) return 'moderate';
		return 'complex';
	}

	// Toggle functions
	function toggleFullDetails() {
		showFullDetails = !showFullDetails;
	}

	function toggleMotionTypes() {
		showMotionTypes = !showMotionTypes;
	}

	function toggleCompactView() {
		compactView = !compactView;
	}

	// Keyboard shortcuts
	function handleKeyDown(event: KeyboardEvent) {
		switch (event.key) {
			case 'f':
			case 'F':
				event.preventDefault();
				toggleFullDetails();
				break;
			case 't':
			case 'T':
				event.preventDefault();
				toggleMotionTypes();
				break;
			case 'c':
			case 'C':
				event.preventDefault();
				toggleCompactView();
				break;
		}
	}
</script>

<div 
	class="motion-summary-card"
	class:compact={compactView}
	role="region"
	aria-label="Motion summary"
	tabindex="-1"
	onkeydown={handleKeyDown}
>
	<div class="summary-header">
		<h3>📝 Motion Summary</h3>
		
		<div class="view-toggles">
			<button
				class="toggle-btn {showFullDetails ? 'active' : ''}"
				onclick={toggleFullDetails}
				aria-pressed={showFullDetails}
				aria-label="Toggle full details"
				title="Show full motion details (F)"
			>
				📋
			</button>
			
			<button
				class="toggle-btn {showMotionTypes ? 'active' : ''}"
				onclick={toggleMotionTypes}
				aria-pressed={showMotionTypes}
				aria-label="Toggle motion type indicators"
				title="Show motion type indicators (T)"
			>
				🏷️
			</button>
			
			<button
				class="toggle-btn {compactView ? 'active' : ''}"
				onclick={toggleCompactView}
				aria-pressed={compactView}
				aria-label="Toggle compact view"
				title="Toggle compact view (C)"
			>
				📏
			</button>
		</div>
	</div>

	<div class="motion-summaries">
		<!-- Blue Motion Summary -->
		<div class="motion-summary blue-motion">
			<div class="motion-header">
				<span class="prop-icon" aria-hidden="true">🔵</span>
				<h4>Blue Prop Motion</h4>
				{#if showMotionTypes}
					<span class="complexity-badge {getMotionComplexity(motionState.blueMotionParams)}">
						{getMotionComplexity(motionState.blueMotionParams)}
					</span>
				{/if}
			</div>

			<div class="motion-description">
				<p class="description-text">
					{generateMotionDescription(motionState.blueMotionParams)}
				</p>
				
				{#if !compactView}
					<div class="motion-details">
						{#if showFullDetails}
							<div class="detail-grid">
								<div class="detail-item">
									<span class="detail-label">Type:</span>
									<span class="detail-value">{formatMotionType(motionState.blueMotionParams.motionType)}</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Path:</span>
									<span class="detail-value">
										{formatLocation(motionState.blueMotionParams.startLoc)} → {formatLocation(motionState.blueMotionParams.endLoc)}
									</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Rotation:</span>
									<span class="detail-value">{formatPropRotDir(motionState.blueMotionParams.propRotDir)}</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Turns:</span>
									<span class="detail-value">{formatTurns(motionState.blueMotionParams.turns)}</span>
								</div>
							</div>
						{:else}
							<div class="quick-stats">
								<span class="stat-chip motion-type">
									{formatMotionType(motionState.blueMotionParams.motionType)}
								</span>
								<span class="stat-chip location-path">
									{formatLocation(motionState.blueMotionParams.startLoc)} → {formatLocation(motionState.blueMotionParams.endLoc)}
								</span>
								{#if typeof motionState.blueMotionParams.turns === 'number' && motionState.blueMotionParams.turns > 0}
									<span class="stat-chip turns">
										{motionState.blueMotionParams.turns}T
									</span>
								{:else if motionState.blueMotionParams.turns === 'fl'}
									<span class="stat-chip turns">
										FL
									</span>
								{/if}
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</div>

		<!-- Red Motion Summary -->
		<div class="motion-summary red-motion">
			<div class="motion-header">
				<span class="prop-icon" aria-hidden="true">🔴</span>
				<h4>Red Prop Motion</h4>
				{#if showMotionTypes}
					<span class="complexity-badge {getMotionComplexity(motionState.redMotionParams)}">
						{getMotionComplexity(motionState.redMotionParams)}
					</span>
				{/if}
			</div>

			<div class="motion-description">
				<p class="description-text">
					{generateMotionDescription(motionState.redMotionParams)}
				</p>
				
				{#if !compactView}
					<div class="motion-details">
						{#if showFullDetails}
							<div class="detail-grid">
								<div class="detail-item">
									<span class="detail-label">Type:</span>
									<span class="detail-value">{formatMotionType(motionState.redMotionParams.motionType)}</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Path:</span>
									<span class="detail-value">
										{formatLocation(motionState.redMotionParams.startLoc)} → {formatLocation(motionState.redMotionParams.endLoc)}
									</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Rotation:</span>
									<span class="detail-value">{formatPropRotDir(motionState.redMotionParams.propRotDir)}</span>
								</div>
								<div class="detail-item">
									<span class="detail-label">Turns:</span>
									<span class="detail-value">{formatTurns(motionState.redMotionParams.turns)}</span>
								</div>
							</div>
						{:else}
							<div class="quick-stats">
								<span class="stat-chip motion-type">
									{formatMotionType(motionState.redMotionParams.motionType)}
								</span>
								<span class="stat-chip location-path">
									{formatLocation(motionState.redMotionParams.startLoc)} → {formatLocation(motionState.redMotionParams.endLoc)}
								</span>
								{#if typeof motionState.redMotionParams.turns === 'number' && motionState.redMotionParams.turns > 0}
									<span class="stat-chip turns">
										{motionState.redMotionParams.turns}T
									</span>
								{:else if motionState.redMotionParams.turns === 'fl'}
									<span class="stat-chip turns">
										FL
									</span>
								{/if}
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- Overall Sequence Info -->
	{#if !compactView}
		<div class="sequence-info">
			<div class="info-item">
				<span class="info-label">Grid Type:</span>
				<span class="info-value">{motionState.gridType === 'diamond' ? 'Diamond' : 'Box'}</span>
			</div>
			<div class="info-item">
				<span class="info-label">Sync Status:</span>
				<span class="info-value {motionState.animationState.isPlaying ? 'active' : 'paused'}">
					{motionState.animationState.isPlaying ? 'Active' : 'Paused'}
				</span>
			</div>
			<div class="info-item">
				<span class="info-label">Progress:</span>
				<span class="info-value">
					{Math.round(motionState.animationState.progress * 100)}%
				</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.motion-summary-card {
		background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(251, 191, 36, 0.05));
		border: 1px solid rgba(245, 158, 11, 0.2);
		border-radius: 12px;
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 16px;
		min-height: fit-content;
	}

	.motion-summary-card.compact {
		padding: 12px;
		gap: 12px;
	}

	.motion-summary-card:focus-within {
		border-color: rgba(245, 158, 11, 0.4);
		box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.1);
	}

	.summary-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.summary-header h3 {
		margin: 0;
		color: #e0e7ff;
		font-size: 1rem;
		font-weight: 600;
	}

	.view-toggles {
		display: flex;
		gap: 4px;
	}

	.toggle-btn {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: #c7d2fe;
		padding: 4px 8px;
		cursor: pointer;
		font-size: 12px;
		transition: all 0.2s ease;
		min-width: 32px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.toggle-btn:hover {
		background: rgba(245, 158, 11, 0.2);
		border-color: rgba(245, 158, 11, 0.4);
	}

	.toggle-btn:focus {
		outline: none;
		box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.5);
	}

	.toggle-btn.active {
		background: rgba(245, 158, 11, 0.3);
		border-color: rgba(245, 158, 11, 0.5);
		color: white;
	}

	/* Motion Summaries */
	.motion-summaries {
		display: flex;
		flex-direction: column;
		gap: 14px;
	}

	.motion-summary {
		background: rgba(0, 0, 0, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 10px;
		padding: 14px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.motion-header {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.prop-icon {
		font-size: 14px;
		line-height: 1;
	}

	.motion-header h4 {
		margin: 0;
		color: #e0e7ff;
		font-size: 13px;
		font-weight: 600;
		flex: 1;
	}

	.complexity-badge {
		font-size: 10px;
		padding: 2px 6px;
		border-radius: 12px;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.complexity-badge.simple {
		background: rgba(34, 197, 94, 0.2);
		color: #86efac;
		border: 1px solid rgba(34, 197, 94, 0.3);
	}

	.complexity-badge.moderate {
		background: rgba(245, 158, 11, 0.2);
		color: #fbbf24;
		border: 1px solid rgba(245, 158, 11, 0.3);
	}

	.complexity-badge.complex {
		background: rgba(239, 68, 68, 0.2);
		color: #f87171;
		border: 1px solid rgba(239, 68, 68, 0.3);
	}

	/* Motion Description */
	.description-text {
		margin: 0;
		color: #e0e7ff;
		font-size: 13px;
		line-height: 1.4;
		background: rgba(0, 0, 0, 0.2);
		padding: 8px 12px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	/* Motion Details */
	.motion-details {
		margin-top: 8px;
	}

	.detail-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 6px;
	}

	.detail-item {
		display: flex;
		justify-content: space-between;
		font-size: 11px;
		padding: 4px 8px;
		background: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
	}

	.detail-label {
		color: #a5b4fc;
		font-weight: 500;
	}

	.detail-value {
		color: #e0e7ff;
		font-family: 'Courier New', monospace;
		font-weight: 600;
	}

	/* Quick Stats */
	.quick-stats {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
	}

	.stat-chip {
		font-size: 10px;
		padding: 3px 6px;
		border-radius: 6px;
		font-weight: 600;
		border: 1px solid transparent;
	}

	.stat-chip.motion-type {
		background: rgba(99, 102, 241, 0.2);
		color: #c7d2fe;
		border-color: rgba(99, 102, 241, 0.3);
	}

	.stat-chip.location-path {
		background: rgba(16, 185, 129, 0.2);
		color: #6ee7b7;
		border-color: rgba(16, 185, 129, 0.3);
	}

	.stat-chip.turns {
		background: rgba(245, 158, 11, 0.2);
		color: #fbbf24;
		border-color: rgba(245, 158, 11, 0.3);
	}

	/* Sequence Info */
	.sequence-info {
		display: flex;
		justify-content: space-between;
		padding-top: 12px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		font-size: 12px;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 4px;
	}

	.info-label {
		color: #a5b4fc;
		font-size: 10px;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.info-value {
		color: #e0e7ff;
		font-weight: 600;
		font-variant-numeric: tabular-nums;
	}

	.info-value.active {
		color: #10b981;
	}

	.info-value.paused {
		color: #f59e0b;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.motion-summary-card {
			padding: 12px;
			gap: 12px;
		}

		.view-toggles {
			gap: 2px;
		}

		.toggle-btn {
			min-width: 28px;
			height: 24px;
			font-size: 11px;
		}

		.motion-summaries {
			gap: 10px;
		}

		.detail-grid {
			grid-template-columns: 1fr;
		}

		.sequence-info {
			font-size: 11px;
		}

		.summary-header h3 {
			font-size: 0.9rem;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.motion-summary-card {
			border: 2px solid white;
			background: rgba(0, 0, 0, 0.8);
		}

		.motion-summary {
			border: 2px solid white;
		}

		.toggle-btn {
			border: 2px solid white;
		}

		.description-text {
			border: 2px solid white;
		}
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.toggle-btn {
			transition: none;
		}
	}
</style>
