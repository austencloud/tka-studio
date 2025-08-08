<script lang="ts">
	import type { BeatDebugInfo /* DebugSession, DebugModalState */ } from '../../types/debug.js';

	// Props
	let {
		debugHistory = []
		// currentSession = null, // Not used in this component
		// modalState // Not used in this component
	}: {
		debugHistory?: BeatDebugInfo[];
		// currentSession?: DebugSession | null; // Not used in this component
		// modalState: DebugModalState; // Not used in this component
	} = $props();

	// State
	let filterLevel = $state<'all' | 'errors' | 'warnings'>('all');
	let sortBy = $state<'beat' | 'severity' | 'type'>('beat');
	let expandedItems = $state<Set<string>>(new Set());
	let showDetails = $state(true);

	// Computed values
	let validationIssues = $derived.by(() => {
		const issues: Array<{
			id: string;
			beatNumber: number;
			prop: 'blue' | 'red';
			type: 'error' | 'warning';
			category: string;
			message: string;
			details: any;
		}> = [];

		// Add null safety check for debugHistory
		const safeDebugHistory = debugHistory ?? [];

		safeDebugHistory.forEach((beat) => {
			// Add null safety checks for beat structure
			if (!beat?.blueProps?.validation || !beat?.redProps?.validation) {
				return;
			}

			// Blue prop issues
			const blueErrors = beat.blueProps.validation.errors ?? [];
			const blueWarnings = beat.blueProps.validation.warnings ?? [];

			blueErrors.forEach((error, index) => {
				issues.push({
					id: `${beat.beatNumber}-blue-error-${index}`,
					beatNumber: beat.beatNumber,
					prop: 'blue',
					type: 'error',
					category: 'General',
					message: error,
					details: beat.blueProps.validation
				});
			});

			blueWarnings.forEach((warning, index) => {
				issues.push({
					id: `${beat.beatNumber}-blue-warning-${index}`,
					beatNumber: beat.beatNumber,
					prop: 'blue',
					type: 'warning',
					category: 'General',
					message: warning,
					details: beat.blueProps.validation
				});
			});

			// Red prop issues
			const redErrors = beat.redProps.validation.errors ?? [];
			const redWarnings = beat.redProps.validation.warnings ?? [];

			redErrors.forEach((error, index) => {
				issues.push({
					id: `${beat.beatNumber}-red-error-${index}`,
					beatNumber: beat.beatNumber,
					prop: 'red',
					type: 'error',
					category: 'General',
					message: error,
					details: beat.redProps.validation
				});
			});

			redWarnings.forEach((warning, index) => {
				issues.push({
					id: `${beat.beatNumber}-red-warning-${index}`,
					beatNumber: beat.beatNumber,
					prop: 'red',
					type: 'warning',
					category: 'General',
					message: warning,
					details: beat.redProps.validation
				});
			});
		});

		return issues;
	});

	let filteredIssues = $derived.by(() => {
		// Get the current validation issues array from the derived value
		const issues = validationIssues;
		let filtered = [...issues];

		// Apply filter
		if (filterLevel === 'errors') {
			filtered = filtered.filter((issue) => issue?.type === 'error');
		} else if (filterLevel === 'warnings') {
			filtered = filtered.filter((issue) => issue?.type === 'warning');
		}

		// Apply sort
		filtered.sort((a, b) => {
			switch (sortBy) {
				case 'beat':
					return (a?.beatNumber ?? 0) - (b?.beatNumber ?? 0);
				case 'severity':
					if (a?.type === 'error' && b?.type === 'warning') return -1;
					if (a?.type === 'warning' && b?.type === 'error') return 1;
					return (a?.beatNumber ?? 0) - (b?.beatNumber ?? 0);
				case 'type':
					return (a?.category ?? '').localeCompare(b?.category ?? '');
				default:
					return 0;
			}
		});

		return filtered;
	});

	let validationSummary = $derived.by(() => {
		// Get the current validation issues array from the derived value
		const issues = validationIssues;

		const summary = {
			totalIssues: issues.length,
			errorCount: issues.filter((i) => i?.type === 'error').length,
			warningCount: issues.filter((i) => i?.type === 'warning').length,
			affectedBeats: new Set(issues.map((i) => i?.beatNumber).filter(Boolean)).size,
			categoryBreakdown: {} as Record<string, number>,
			propBreakdown: { blue: 0, red: 0 }
		};

		issues.forEach((issue) => {
			if (issue?.category) {
				summary.categoryBreakdown[issue.category] =
					(summary.categoryBreakdown[issue.category] || 0) + 1;
			}
			if (issue?.prop && (issue.prop === 'blue' || issue.prop === 'red')) {
				summary.propBreakdown[issue.prop]++;
			}
		});

		return summary;
	});

	function toggleExpanded(itemId: string): void {
		if (expandedItems.has(itemId)) {
			expandedItems.delete(itemId);
		} else {
			expandedItems.add(itemId);
		}
		expandedItems = new Set(expandedItems);
	}

	function getIssueIcon(type: 'error' | 'warning'): string {
		return type === 'error' ? '❌' : '⚠️';
	}

	function getIssueClass(type: 'error' | 'warning'): string {
		return type === 'error' ? 'error' : 'warning';
	}

	function getPropColor(prop: 'blue' | 'red'): string {
		return prop === 'blue' ? '#3b82f6' : '#ef4444';
	}

	function formatValidationDetail(_key: string, value: any): string {
		if (typeof value === 'number') {
			return value.toFixed(3);
		}
		if (typeof value === 'boolean') {
			return value ? 'Yes' : 'No';
		}
		return String(value);
	}
</script>

<div class="validation-panel">
	<!-- Summary Section -->
	<div class="summary-section">
		<h3>📋 Validation Summary</h3>
		<div class="summary-grid">
			<div class="summary-card">
				<div class="summary-value">{validationSummary.totalIssues}</div>
				<div class="summary-label">Total Issues</div>
			</div>

			<div class="summary-card error">
				<div class="summary-value">{validationSummary.errorCount}</div>
				<div class="summary-label">Errors</div>
			</div>

			<div class="summary-card warning">
				<div class="summary-value">{validationSummary.warningCount}</div>
				<div class="summary-label">Warnings</div>
			</div>

			<div class="summary-card">
				<div class="summary-value">{validationSummary.affectedBeats}</div>
				<div class="summary-label">Affected Beats</div>
			</div>
		</div>

		<!-- Prop Breakdown -->
		<div class="prop-breakdown">
			<h4>Issues by Prop</h4>
			<div class="prop-chart">
				<div class="prop-item">
					<div class="prop-color" style:background-color="{getPropColor('blue')}"></div>
					<span class="prop-label">Blue Prop</span>
					<span class="prop-count">{validationSummary.propBreakdown.blue}</span>
				</div>
				<div class="prop-item">
					<div class="prop-color" style:background-color="{getPropColor('red')}"></div>
					<span class="prop-label">Red Prop</span>
					<span class="prop-count">{validationSummary.propBreakdown.red}</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Controls -->
	<div class="controls-section">
		<div class="control-group">
			<label>Filter:</label>
			<select bind:value={filterLevel}>
				<option value="all">All Issues</option>
				<option value="errors">Errors Only</option>
				<option value="warnings">Warnings Only</option>
			</select>
		</div>

		<div class="control-group">
			<label>Sort By:</label>
			<select bind:value={sortBy}>
				<option value="beat">Beat Number</option>
				<option value="severity">Severity</option>
				<option value="type">Category</option>
			</select>
		</div>

		<div class="control-group">
			<label>
				<input type="checkbox" bind:checked={showDetails} />
				Show Details
			</label>
		</div>
	</div>

	<!-- Issues List -->
	<div class="issues-section">
		{#if filteredIssues.length === 0}
			<div class="no-issues">
				{#if filterLevel === 'all'}
					<p>🎉 No validation issues found!</p>
				{:else}
					<p>No {filterLevel} found.</p>
				{/if}
			</div>
		{:else}
			<div class="issues-list">
				{#each filteredIssues as issue (issue.id)}
					<div class="issue-item {getIssueClass(issue.type)}">
						<div class="issue-header" on:click={() => toggleExpanded(issue.id)}>
							<div class="issue-info">
								<span class="issue-icon">{getIssueIcon(issue.type)}</span>
								<span class="issue-beat">Beat {issue.beatNumber}</span>
								<span class="issue-prop" style:color="{getPropColor(issue.prop)}">
									{issue.prop.toUpperCase()}
								</span>
								<span class="issue-category">{issue.category}</span>
							</div>

							<div class="issue-actions">
								{#if showDetails}
									<button class="expand-button" class:expanded={expandedItems.has(issue.id)}>
										{expandedItems.has(issue.id) ? '▼' : '▶'}
									</button>
								{/if}
							</div>
						</div>

						<div class="issue-message">
							{issue.message}
						</div>

						{#if showDetails && expandedItems.has(issue.id)}
							<div class="issue-details">
								<h5>Validation Details:</h5>
								<div class="details-grid">
									{#if issue.details.orientationContinuity}
										<div class="detail-section">
											<h6>Orientation Continuity</h6>
											<div class="detail-items">
												<div class="detail-item">
													<span class="detail-label">Valid:</span>
													<span
														class="detail-value {issue.details.orientationContinuity.isValid
															? 'valid'
															: 'invalid'}"
													>
														{formatValidationDetail(
															'isValid',
															issue.details.orientationContinuity.isValid
														)}
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Expected Start:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'expectedStartOri',
															issue.details.orientationContinuity.expectedStartOri
														)}°
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Actual Start:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'actualStartOri',
															issue.details.orientationContinuity.actualStartOri
														)}°
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Difference:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'difference',
															issue.details.orientationContinuity.difference
														)}°
													</span>
												</div>
											</div>
										</div>
									{/if}

									{#if issue.details.turnCountAccuracy}
										<div class="detail-section">
											<h6>Turn Count Accuracy</h6>
											<div class="detail-items">
												<div class="detail-item">
													<span class="detail-label">Valid:</span>
													<span
														class="detail-value {issue.details.turnCountAccuracy.isValid
															? 'valid'
															: 'invalid'}"
													>
														{formatValidationDetail(
															'isValid',
															issue.details.turnCountAccuracy.isValid
														)}
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Expected Turns:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'expectedTurns',
															issue.details.turnCountAccuracy.expectedTurns
														)}
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Calculated Turns:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'calculatedTurns',
															issue.details.turnCountAccuracy.calculatedTurns
														)}
													</span>
												</div>
												<div class="detail-item">
													<span class="detail-label">Difference:</span>
													<span class="detail-value">
														{formatValidationDetail(
															'difference',
															issue.details.turnCountAccuracy.difference
														)}
													</span>
												</div>
											</div>
										</div>
									{/if}
								</div>
							</div>
						{/if}
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.validation-panel {
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

	.summary-card.error {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.1);
	}

	.summary-card.warning {
		border-color: #f59e0b;
		background: rgba(245, 158, 11, 0.1);
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

	.prop-breakdown h4 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.prop-chart {
		display: flex;
		gap: 1rem;
	}

	.prop-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
	}

	.prop-color {
		width: 12px;
		height: 12px;
		border-radius: 2px;
	}

	.prop-label {
		color: var(--color-text);
		font-weight: 500;
	}

	.prop-count {
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

	.issues-section {
		flex: 1;
		overflow: hidden;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.no-issues {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: var(--color-text-secondary);
		font-style: italic;
	}

	.issues-list {
		height: 100%;
		overflow-y: auto;
		padding: 1rem;
	}

	.issue-item {
		background: var(--color-surface);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		margin-bottom: 0.75rem;
		overflow: hidden;
	}

	.issue-item.error {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.05);
	}

	.issue-item.warning {
		border-color: #f59e0b;
		background: rgba(245, 158, 11, 0.05);
	}

	.issue-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.issue-header:hover {
		background: var(--color-surface-hover);
	}

	.issue-info {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		font-size: 0.875rem;
	}

	.issue-icon {
		font-size: 1rem;
	}

	.issue-beat {
		font-weight: 600;
		color: var(--color-text);
	}

	.issue-prop {
		font-weight: 600;
		font-size: 0.75rem;
		text-transform: uppercase;
	}

	.issue-category {
		color: var(--color-text-secondary);
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.expand-button {
		background: none;
		border: none;
		cursor: pointer;
		color: var(--color-text-secondary);
		font-size: 0.75rem;
		padding: 0.25rem;
		border-radius: 2px;
		transition: all 0.2s ease;
	}

	.expand-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text);
	}

	.issue-message {
		padding: 0 1rem 0.75rem 1rem;
		color: var(--color-text);
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.issue-details {
		padding: 0 1rem 1rem 1rem;
		border-top: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	.issue-details h5 {
		margin: 0.75rem 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.details-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1rem;
	}

	.detail-section h6 {
		margin: 0 0 0.5rem 0;
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.detail-items {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.detail-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.75rem;
		padding: 0.25rem 0;
	}

	.detail-label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.detail-value {
		color: var(--color-text);
		font-weight: 600;
		font-family: monospace;
	}

	.detail-value.valid {
		color: #10b981;
	}

	.detail-value.invalid {
		color: #ef4444;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.validation-panel {
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

		.issue-info {
			flex-wrap: wrap;
			gap: 0.5rem;
		}

		.details-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
