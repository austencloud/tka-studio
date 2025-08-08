<script lang="ts">
	import type {
		BeatDebugInfo
		// DebugSession,
		// DebugModalState,
		// PropDebugInfo
	} from '../../types/debug.js';

	// Props
	let {
		debugHistory = [],
		// currentSession = null, // Not used in this component
		// modalState, // Not used in this component
		onBeatSelect = () => {}
		// onPropSelect = () => {} // Not used in this component
	}: {
		debugHistory?: BeatDebugInfo[];
		// currentSession?: DebugSession | null; // Not used in this component
		// modalState: DebugModalState; // Not used in this component
		onBeatSelect?: (_beatNumber: number) => void;
		// onPropSelect?: (_prop: 'blue' | 'red') => void; // Not used in this component
	} = $props();

	// State
	let viewMode = $state<'table' | 'graph' | 'timeline'>('table');
	let filterLevel = $state<'all' | 'errors' | 'warnings'>('all');
	let sortBy = $state<'beat' | 'issues' | 'turns'>('beat');
	let selectedBeat = $state<number | null>(null);

	// Computed values
	let filteredHistory = $derived.by(() => {
		// Add null safety check for debugHistory
		const safeDebugHistory = debugHistory ?? [];
		let filtered = [...safeDebugHistory];

		// Apply filter
		if (filterLevel === 'errors') {
			filtered = filtered.filter(
				(beat) =>
					(beat?.blueProps?.validation?.errors?.length ?? 0) > 0 ||
					(beat?.redProps?.validation?.errors?.length ?? 0) > 0
			);
		} else if (filterLevel === 'warnings') {
			filtered = filtered.filter(
				(beat) =>
					(beat?.blueProps?.validation?.warnings?.length ?? 0) > 0 ||
					(beat?.redProps?.validation?.warnings?.length ?? 0) > 0
			);
		}

		// Apply sort
		filtered.sort((a, b) => {
			switch (sortBy) {
				case 'beat':
					return (a?.beatNumber ?? 0) - (b?.beatNumber ?? 0);
				case 'issues': {
					const aIssues = getTotalIssues(a);
					const bIssues = getTotalIssues(b);
					return bIssues - aIssues;
				}
				case 'turns': {
					const aTurns =
						(a?.blueProps?.attributes?.turns ?? 0) + (a?.redProps?.attributes?.turns ?? 0);
					const bTurns =
						(b?.blueProps?.attributes?.turns ?? 0) + (b?.redProps?.attributes?.turns ?? 0);
					return bTurns - aTurns;
				}
				default:
					return 0;
			}
		});

		return filtered;
	});

	let summaryStats = $derived.by(() => {
		const stats = {
			totalBeats: debugHistory?.length ?? 0,
			validBeats: 0,
			totalWarnings: 0,
			totalErrors: 0,
			orientationIssues: 0,
			turnCountIssues: 0,
			motionTypeBreakdown: {} as Record<string, number>
		};

		// Add null safety check for debugHistory
		const safeDebugHistory = debugHistory ?? [];

		safeDebugHistory.forEach((beat) => {
			// Add null safety checks for beat structure
			if (!beat?.blueProps?.validation || !beat?.redProps?.validation) {
				return;
			}

			const blueValid = beat.blueProps.validation.isValid;
			const redValid = beat.redProps.validation.isValid;

			if (blueValid && redValid) {
				stats.validBeats++;
			}

			stats.totalWarnings +=
				(beat.blueProps.validation.warnings?.length ?? 0) +
				(beat.redProps.validation.warnings?.length ?? 0);
			stats.totalErrors +=
				(beat.blueProps.validation.errors?.length ?? 0) +
				(beat.redProps.validation.errors?.length ?? 0);

			if (
				!beat.blueProps.validation.orientationContinuity?.isValid ||
				!beat.redProps.validation.orientationContinuity?.isValid
			) {
				stats.orientationIssues++;
			}

			if (
				!beat.blueProps.validation.turnCountAccuracy?.isValid ||
				!beat.redProps.validation.turnCountAccuracy?.isValid
			) {
				stats.turnCountIssues++;
			}

			// Motion type breakdown with null safety
			const blueMotion = beat.blueProps.attributes?.motion_type;
			const redMotion = beat.redProps.attributes?.motion_type;

			if (blueMotion) {
				stats.motionTypeBreakdown[blueMotion] = (stats.motionTypeBreakdown[blueMotion] || 0) + 1;
			}
			if (redMotion) {
				stats.motionTypeBreakdown[redMotion] = (stats.motionTypeBreakdown[redMotion] || 0) + 1;
			}
		});

		return stats;
	});

	function getTotalIssues(beat: BeatDebugInfo): number {
		return (
			(beat?.blueProps?.validation?.warnings?.length ?? 0) +
			(beat?.blueProps?.validation?.errors?.length ?? 0) +
			(beat?.redProps?.validation?.warnings?.length ?? 0) +
			(beat?.redProps?.validation?.errors?.length ?? 0)
		);
	}

	function getIssueIcon(beat: BeatDebugInfo): string {
		const hasErrors =
			(beat?.blueProps?.validation?.errors?.length ?? 0) > 0 ||
			(beat?.redProps?.validation?.errors?.length ?? 0) > 0;
		const hasWarnings =
			(beat?.blueProps?.validation?.warnings?.length ?? 0) > 0 ||
			(beat?.redProps?.validation?.warnings?.length ?? 0) > 0;

		if (hasErrors) return '❌';
		if (hasWarnings) return '⚠️';
		return '✅';
	}

	function getIssueClass(beat: BeatDebugInfo): string {
		const hasErrors =
			(beat?.blueProps?.validation?.errors?.length ?? 0) > 0 ||
			(beat?.redProps?.validation?.errors?.length ?? 0) > 0;
		const hasWarnings =
			(beat?.blueProps?.validation?.warnings?.length ?? 0) > 0 ||
			(beat?.redProps?.validation?.warnings?.length ?? 0) > 0;

		if (hasErrors) return 'error';
		if (hasWarnings) return 'warning';
		return 'valid';
	}

	function handleBeatClick(beatNumber: number): void {
		selectedBeat = beatNumber;
		onBeatSelect(beatNumber);
	}

	// function handlePropClick(prop: 'blue' | 'red'): void {
	// 	onPropSelect(prop);
	// }

	// function formatAngle(angle: number): string {
	// 	return `${((angle * 180) / Math.PI).toFixed(1)}°`;
	// }

	function formatTurns(turns: number | undefined): string {
		return turns !== undefined ? turns.toString() : 'N/A';
	}

	function getMotionTypeColor(motionType: string): string {
		const colors: Record<string, string> = {
			pro: '#3b82f6',
			anti: '#ef4444',
			static: '#10b981',
			dash: '#f59e0b',
			none: '#6b7280'
		};
		return colors[motionType] || '#6b7280';
	}
</script>

<div class="debug-overview">
	<!-- Summary Statistics -->
	<div class="summary-section">
		<h3>📊 Analysis Summary</h3>
		<div class="summary-grid">
			<div class="summary-card">
				<div class="summary-value">{summaryStats.totalBeats}</div>
				<div class="summary-label">Total Beats</div>
			</div>

			<div class="summary-card valid">
				<div class="summary-value">{summaryStats.validBeats}</div>
				<div class="summary-label">Valid Beats</div>
			</div>

			<div class="summary-card warning">
				<div class="summary-value">{summaryStats.totalWarnings}</div>
				<div class="summary-label">Warnings</div>
			</div>

			<div class="summary-card error">
				<div class="summary-value">{summaryStats.totalErrors}</div>
				<div class="summary-label">Errors</div>
			</div>

			<div class="summary-card">
				<div class="summary-value">{summaryStats.orientationIssues}</div>
				<div class="summary-label">Orientation Issues</div>
			</div>

			<div class="summary-card">
				<div class="summary-value">{summaryStats.turnCountIssues}</div>
				<div class="summary-label">Turn Count Issues</div>
			</div>
		</div>

		<!-- Motion Type Breakdown -->
		<div class="motion-breakdown">
			<h4>Motion Type Distribution</h4>
			<div class="motion-chart">
				{#each Object.entries(summaryStats.motionTypeBreakdown ?? {}) as [motionType, count]}
					<div class="motion-item">
						<div
							class="motion-color"
							style:background-color="{getMotionTypeColor(motionType)}"
						></div>
						<span class="motion-label">{motionType}</span>
						<span class="motion-count">{count}</span>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Controls -->
	<div class="controls-section">
		<div class="control-group">
			<label>View Mode:</label>
			<select bind:value={viewMode}>
				<option value="table">Table</option>
				<option value="graph">Graph</option>
				<option value="timeline">Timeline</option>
			</select>
		</div>

		<div class="control-group">
			<label>Filter:</label>
			<select bind:value={filterLevel}>
				<option value="all">All Beats</option>
				<option value="warnings">Warnings Only</option>
				<option value="errors">Errors Only</option>
			</select>
		</div>

		<div class="control-group">
			<label>Sort By:</label>
			<select bind:value={sortBy}>
				<option value="beat">Beat Number</option>
				<option value="issues">Issue Count</option>
				<option value="turns">Turn Count</option>
			</select>
		</div>
	</div>

	<!-- Beat Analysis Table -->
	{#if viewMode === 'table'}
		<div class="table-section">
			<div class="table-container">
				<table class="debug-table">
					<thead>
						<tr>
							<th>Beat</th>
							<th>Status</th>
							<th>Blue Motion</th>
							<th>Blue Turns</th>
							<th>Blue Orientation</th>
							<th>Red Motion</th>
							<th>Red Turns</th>
							<th>Red Orientation</th>
							<th>Issues</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each filteredHistory as beat (beat.beatNumber)}
							<tr
								class="beat-row {getIssueClass(beat)}"
								class:selected={selectedBeat === beat.beatNumber}
								on:click={() => handleBeatClick(beat.beatNumber)}
							>
								<td class="beat-number">{beat.beatNumber}</td>
								<td class="status-cell">
									<span class="status-icon">{getIssueIcon(beat)}</span>
								</td>

								<!-- Blue Prop -->
								<td class="motion-type">
									<span
										class="motion-badge"
										style:background-color="{getMotionTypeColor(
											beat.blueProps.attributes.motion_type
										)}"
									>
										{beat.blueProps.attributes.motion_type}
									</span>
								</td>
								<td class="turns">{formatTurns(beat.blueProps.attributes.turns)}</td>
								<td class="orientation">
									<div class="orientation-info">
										<span class="ori-start">{beat.blueProps.attributes.start_ori || 'N/A'}</span>
										<span class="ori-arrow">→</span>
										<span class="ori-end">{beat.blueProps.attributes.end_ori || 'N/A'}</span>
									</div>
								</td>

								<!-- Red Prop -->
								<td class="motion-type">
									<span
										class="motion-badge"
										style:background-color="{getMotionTypeColor(
											beat.redProps.attributes.motion_type
										)}"
									>
										{beat.redProps.attributes.motion_type}
									</span>
								</td>
								<td class="turns">{formatTurns(beat.redProps.attributes.turns)}</td>
								<td class="orientation">
									<div class="orientation-info">
										<span class="ori-start">{beat.redProps.attributes.start_ori || 'N/A'}</span>
										<span class="ori-arrow">→</span>
										<span class="ori-end">{beat.redProps.attributes.end_ori || 'N/A'}</span>
									</div>
								</td>

								<td class="issues">
									<span class="issue-count">{getTotalIssues(beat)}</span>
								</td>

								<td class="actions">
									<button
										class="action-button edit"
										on:click|stopPropagation={() => handleBeatClick(beat.beatNumber)}
										title="Edit Beat"
									>
										✏️
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{:else if viewMode === 'graph'}
		<div class="graph-section">
			<p class="coming-soon">📈 Graph view coming soon...</p>
		</div>
	{:else if viewMode === 'timeline'}
		<div class="timeline-section">
			<p class="coming-soon">📅 Timeline view coming soon...</p>
		</div>
	{/if}
</div>

<style>
	.debug-overview {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: 1rem;
		gap: 1rem;
		overflow: hidden;
	}

	.summary-section {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.summary-section h3 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.summary-card {
		background: var(--color-surface);
		border-radius: 6px;
		padding: 0.75rem;
		text-align: center;
		border: 1px solid var(--color-border);
	}

	.summary-card.valid {
		border-color: #10b981;
		background: rgba(16, 185, 129, 0.1);
	}

	.summary-card.warning {
		border-color: #f59e0b;
		background: rgba(245, 158, 11, 0.1);
	}

	.summary-card.error {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.1);
	}

	.summary-value {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-text);
		margin-bottom: 0.25rem;
	}

	.summary-label {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.motion-breakdown h4 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.motion-chart {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.motion-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
	}

	.motion-color {
		width: 12px;
		height: 12px;
		border-radius: 2px;
	}

	.motion-label {
		color: var(--color-text);
		font-weight: 500;
	}

	.motion-count {
		color: var(--color-text-secondary);
		font-weight: 600;
	}

	.controls-section {
		display: flex;
		gap: 1rem;
		align-items: center;
		padding: 0.75rem 1rem;
		background: var(--color-surface-elevated);
		border-radius: 6px;
		border: 1px solid var(--color-border);
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
	}

	.control-group label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.control-group select {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		padding: 0.25rem 0.5rem;
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.table-section {
		flex: 1;
		overflow: hidden;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.table-container {
		height: 100%;
		overflow: auto;
	}

	.debug-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	.debug-table th {
		background: var(--color-surface);
		color: var(--color-text-secondary);
		font-weight: 600;
		padding: 0.75rem 0.5rem;
		text-align: left;
		border-bottom: 1px solid var(--color-border);
		position: sticky;
		top: 0;
		z-index: 1;
	}

	.debug-table td {
		padding: 0.5rem;
		border-bottom: 1px solid var(--color-border);
		vertical-align: middle;
		color: var(--color-text);
	}

	.beat-row {
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.beat-row:hover {
		background: var(--color-surface-hover);
	}

	.beat-row.selected {
		background: rgba(59, 130, 246, 0.1);
		border-left: 3px solid var(--color-primary);
	}

	.beat-row.error {
		background: rgba(239, 68, 68, 0.05);
	}

	.beat-row.warning {
		background: rgba(245, 158, 11, 0.05);
	}

	.beat-number {
		font-weight: 600;
		color: var(--color-text);
	}

	.status-icon {
		font-size: 1rem;
	}

	.motion-badge {
		display: inline-block;
		padding: 0.25rem 0.5rem;
		border-radius: 12px;
		color: white;
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
	}

	.orientation-info {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		font-size: 0.75rem;
	}

	.ori-arrow {
		color: var(--color-text-secondary);
	}

	.issue-count {
		display: inline-block;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 12px;
		padding: 0.25rem 0.5rem;
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.action-button {
		background: none;
		border: none;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: background-color 0.2s ease;
	}

	.action-button:hover {
		background: var(--color-surface-hover);
	}

	.graph-section,
	.timeline-section {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.coming-soon {
		color: var(--color-text-secondary);
		font-style: italic;
		margin: 0;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.debug-overview {
			padding: 0.5rem;
		}

		.summary-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.controls-section {
			flex-direction: column;
			align-items: stretch;
			gap: 0.5rem;
		}

		.debug-table {
			font-size: 0.75rem;
		}

		.debug-table th,
		.debug-table td {
			padding: 0.5rem 0.25rem;
		}
	}
</style>
