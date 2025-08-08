<script lang="ts">
	import type { DebugSession, BeatDebugInfo } from '../../types/debug.js';

	// Props
	let {
		currentSession = null,
		debugHistory = [],
		onExport = () => {}
	}: {
		currentSession?: DebugSession | null;
		debugHistory?: BeatDebugInfo[];
		onExport?: () => void;
	} = $props();

	// State
	let exportFormat = $state<'json' | 'csv' | 'report'>('json');
	let includeRawData = $state(true);
	let includeValidation = $state(true);
	let includeConfiguration = $state(true);
	let includeMetadata = $state(true);
	let filterLevel = $state<'all' | 'issues-only' | 'errors-only'>('all');

	// Computed values
	let exportSummary = $derived(() => {
		if (!currentSession) return null;

		const filteredHistory = getFilteredHistory();

		return {
			sessionId: currentSession.id ?? 'unknown',
			sequenceWord: currentSession.sequenceWord ?? 'unknown',
			totalBeats: debugHistory?.length ?? 0,
			filteredBeats: filteredHistory.length,
			validationSummary: currentSession.validationSummary,
			sessionDuration: currentSession.endTime
				? currentSession.endTime - currentSession.startTime
				: Date.now() - (currentSession.startTime ?? Date.now()),
			exportSize: estimateExportSize(filteredHistory)
		};
	});

	function getFilteredHistory(): BeatDebugInfo[] {
		switch (filterLevel) {
			case 'issues-only':
				return debugHistory.filter(
					(beat) =>
						beat.blueProps.validation.warnings.length > 0 ||
						beat.blueProps.validation.errors.length > 0 ||
						beat.redProps.validation.warnings.length > 0 ||
						beat.redProps.validation.errors.length > 0
				);
			case 'errors-only':
				return debugHistory.filter(
					(beat) =>
						beat.blueProps.validation.errors.length > 0 ||
						beat.redProps.validation.errors.length > 0
				);
			default:
				return debugHistory;
		}
	}

	function estimateExportSize(data: BeatDebugInfo[]): string {
		const jsonString = JSON.stringify(data);
		const sizeInBytes = new Blob([jsonString]).size;

		if (sizeInBytes < 1024) {
			return `${sizeInBytes} B`;
		} else if (sizeInBytes < 1024 * 1024) {
			return `${(sizeInBytes / 1024).toFixed(1)} KB`;
		} else {
			return `${(sizeInBytes / (1024 * 1024)).toFixed(1)} MB`;
		}
	}

	function handleExport(): void {
		if (!currentSession) return;

		const filteredHistory = getFilteredHistory();

		switch (exportFormat) {
			case 'json':
				exportAsJSON(filteredHistory);
				break;
			case 'csv':
				exportAsCSV(filteredHistory);
				break;
			case 'report':
				exportAsReport(filteredHistory);
				break;
		}

		onExport();
	}

	function exportAsJSON(data: BeatDebugInfo[]): void {
		const exportData = {
			...(includeMetadata && {
				metadata: {
					exportTime: Date.now(),
					exportFormat: 'json',
					version: '1.0.0',
					sessionId: currentSession?.id,
					sequenceWord: currentSession?.sequenceWord
				}
			}),
			...(includeConfiguration &&
				currentSession && {
					configuration: currentSession.configuration
				}),
			...(includeValidation &&
				currentSession && {
					validationSummary: currentSession.validationSummary
				}),
			...(includeRawData && {
				debugData: data
			})
		};

		downloadFile(
			JSON.stringify(exportData, null, 2),
			`sequence-debug-${currentSession?.sequenceWord}-${Date.now()}.json`,
			'application/json'
		);
	}

	function exportAsCSV(data: BeatDebugInfo[]): void {
		const headers = [
			'Beat',
			'Blue Motion Type',
			'Blue Turns',
			'Blue Start Ori',
			'Blue End Ori',
			'Blue Valid',
			'Blue Warnings',
			'Blue Errors',
			'Red Motion Type',
			'Red Turns',
			'Red Start Ori',
			'Red End Ori',
			'Red Valid',
			'Red Warnings',
			'Red Errors'
		];

		const rows = data.map((beat) => [
			beat.beatNumber,
			beat.blueProps.attributes.motion_type,
			beat.blueProps.attributes.turns || '',
			beat.blueProps.attributes.start_ori || '',
			beat.blueProps.attributes.end_ori || '',
			beat.blueProps.validation.isValid,
			beat.blueProps.validation.warnings.length,
			beat.blueProps.validation.errors.length,
			beat.redProps.attributes.motion_type,
			beat.redProps.attributes.turns || '',
			beat.redProps.attributes.start_ori || '',
			beat.redProps.attributes.end_ori || '',
			beat.redProps.validation.isValid,
			beat.redProps.validation.warnings.length,
			beat.redProps.validation.errors.length
		]);

		const csvContent = [headers, ...rows]
			.map((row) => row.map((cell) => `"${cell}"`).join(','))
			.join('\n');

		downloadFile(
			csvContent,
			`sequence-debug-${currentSession?.sequenceWord}-${Date.now()}.csv`,
			'text/csv'
		);
	}

	function exportAsReport(data: BeatDebugInfo[]): void {
		const report = generateTextReport(data);

		downloadFile(
			report,
			`sequence-debug-report-${currentSession?.sequenceWord}-${Date.now()}.txt`,
			'text/plain'
		);
	}

	function generateTextReport(data: BeatDebugInfo[]): string {
		const lines: string[] = [];

		lines.push('SEQUENCE INTERPRETATION DEBUG REPORT');
		lines.push('='.repeat(50));
		lines.push('');

		if (currentSession) {
			lines.push(`Sequence: ${currentSession.sequenceWord}`);
			lines.push(`Session ID: ${currentSession.id}`);
			lines.push(`Analysis Date: ${new Date(currentSession.startTime).toLocaleString()}`);
			lines.push('');
		}

		// Summary
		if (includeValidation && currentSession?.validationSummary) {
			const summary = currentSession.validationSummary;
			lines.push('VALIDATION SUMMARY');
			lines.push('-'.repeat(20));
			lines.push(`Total Beats: ${summary.totalBeats}`);
			lines.push(`Valid Beats: ${summary.validBeats}`);
			lines.push(`Warnings: ${summary.warningCount}`);
			lines.push(`Errors: ${summary.errorCount}`);
			lines.push(`Orientation Issues: ${summary.orientationIssues}`);
			lines.push(`Turn Count Issues: ${summary.turnCountIssues}`);
			lines.push('');
		}

		// Beat-by-beat analysis
		lines.push('BEAT-BY-BEAT ANALYSIS');
		lines.push('-'.repeat(25));
		lines.push('');

		data.forEach((beat) => {
			lines.push(`Beat ${beat.beatNumber}:`);

			// Blue prop
			lines.push(`  Blue Prop:`);
			lines.push(`    Motion: ${beat.blueProps.attributes.motion_type}`);
			lines.push(`    Turns: ${beat.blueProps.attributes.turns || 'N/A'}`);
			lines.push(
				`    Orientation: ${beat.blueProps.attributes.start_ori || 'N/A'} → ${beat.blueProps.attributes.end_ori || 'N/A'}`
			);
			lines.push(`    Valid: ${beat.blueProps.validation.isValid ? 'Yes' : 'No'}`);

			if (beat.blueProps.validation.warnings.length > 0) {
				lines.push(`    Warnings: ${beat.blueProps.validation.warnings.join(', ')}`);
			}

			if (beat.blueProps.validation.errors.length > 0) {
				lines.push(`    Errors: ${beat.blueProps.validation.errors.join(', ')}`);
			}

			// Red prop
			lines.push(`  Red Prop:`);
			lines.push(`    Motion: ${beat.redProps.attributes.motion_type}`);
			lines.push(`    Turns: ${beat.redProps.attributes.turns || 'N/A'}`);
			lines.push(
				`    Orientation: ${beat.redProps.attributes.start_ori || 'N/A'} → ${beat.redProps.attributes.end_ori || 'N/A'}`
			);
			lines.push(`    Valid: ${beat.redProps.validation.isValid ? 'Yes' : 'No'}`);

			if (beat.redProps.validation.warnings.length > 0) {
				lines.push(`    Warnings: ${beat.redProps.validation.warnings.join(', ')}`);
			}

			if (beat.redProps.validation.errors.length > 0) {
				lines.push(`    Errors: ${beat.redProps.validation.errors.join(', ')}`);
			}

			lines.push('');
		});

		return lines.join('\n');
	}

	function downloadFile(content: string, filename: string, mimeType: string): void {
		const blob = new Blob([content], { type: mimeType });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

	function formatDuration(ms: number): string {
		const seconds = Math.floor(ms / 1000);
		const minutes = Math.floor(seconds / 60);
		const hours = Math.floor(minutes / 60);

		if (hours > 0) {
			return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
		} else if (minutes > 0) {
			return `${minutes}m ${seconds % 60}s`;
		} else {
			return `${seconds}s`;
		}
	}
</script>

<div class="export-panel">
	<div class="panel-header">
		<h3>💾 Export Debug Data</h3>
		<p class="panel-description">
			Export your debugging session data for analysis, sharing, or archival purposes.
		</p>
	</div>

	{#if currentSession && exportSummary}
		<!-- Export Summary -->
		<div class="export-summary">
			<h4>📊 Export Summary</h4>
			<div class="summary-grid">
				<div class="summary-item">
					<span class="summary-label">Session:</span>
					<span class="summary-value">{exportSummary?.sessionId?.slice(-8) ?? 'N/A'}</span>
				</div>
				<div class="summary-item">
					<span class="summary-label">Sequence:</span>
					<span class="summary-value">{exportSummary?.sequenceWord ?? 'N/A'}</span>
				</div>
				<div class="summary-item">
					<span class="summary-label">Total Beats:</span>
					<span class="summary-value">{exportSummary?.totalBeats ?? 0}</span>
				</div>
				<div class="summary-item">
					<span class="summary-label">Duration:</span>
					<span class="summary-value">{formatDuration(exportSummary?.sessionDuration ?? 0)}</span>
				</div>
				<div class="summary-item">
					<span class="summary-label">Filtered Beats:</span>
					<span class="summary-value">{exportSummary?.filteredBeats ?? 0}</span>
				</div>
				<div class="summary-item">
					<span class="summary-label">Estimated Size:</span>
					<span class="summary-value">{exportSummary?.exportSize ?? 'N/A'}</span>
				</div>
			</div>
		</div>

		<!-- Export Options -->
		<div class="export-options">
			<h4>⚙️ Export Options</h4>

			<div class="options-grid">
				<!-- Format Selection -->
				<div class="option-group">
					<label class="option-label">Export Format:</label>
					<div class="format-options">
						<label class="format-option">
							<input type="radio" bind:group={exportFormat} value="json" />
							<span class="format-info">
								<strong>JSON</strong>
								<small>Complete data with full structure</small>
							</span>
						</label>
						<label class="format-option">
							<input type="radio" bind:group={exportFormat} value="csv" />
							<span class="format-info">
								<strong>CSV</strong>
								<small>Spreadsheet-compatible format</small>
							</span>
						</label>
						<label class="format-option">
							<input type="radio" bind:group={exportFormat} value="report" />
							<span class="format-info">
								<strong>Report</strong>
								<small>Human-readable text report</small>
							</span>
						</label>
					</div>
				</div>

				<!-- Data Filter -->
				<div class="option-group">
					<label class="option-label">Data Filter:</label>
					<select bind:value={filterLevel}>
						<option value="all">All Beats</option>
						<option value="issues-only">Issues Only</option>
						<option value="errors-only">Errors Only</option>
					</select>
				</div>

				<!-- Include Options -->
				<div class="option-group">
					<label class="option-label">Include:</label>
					<div class="include-options">
						<label class="include-option">
							<input type="checkbox" bind:checked={includeRawData} />
							Raw Debug Data
						</label>
						<label class="include-option">
							<input type="checkbox" bind:checked={includeValidation} />
							Validation Results
						</label>
						<label class="include-option">
							<input type="checkbox" bind:checked={includeConfiguration} />
							Configuration Settings
						</label>
						<label class="include-option">
							<input type="checkbox" bind:checked={includeMetadata} />
							Export Metadata
						</label>
					</div>
				</div>
			</div>
		</div>

		<!-- Validation Summary -->
		{#if currentSession.validationSummary}
			<div class="validation-summary">
				<h4>✅ Validation Summary</h4>
				<div class="validation-grid">
					<div class="validation-stat valid">
						<span class="stat-value">{currentSession.validationSummary.validBeats}</span>
						<span class="stat-label">Valid Beats</span>
					</div>
					<div class="validation-stat warning">
						<span class="stat-value">{currentSession.validationSummary.warningCount}</span>
						<span class="stat-label">Warnings</span>
					</div>
					<div class="validation-stat error">
						<span class="stat-value">{currentSession.validationSummary.errorCount}</span>
						<span class="stat-label">Errors</span>
					</div>
					<div class="validation-stat">
						<span class="stat-value">{currentSession.validationSummary.orientationIssues}</span>
						<span class="stat-label">Orientation Issues</span>
					</div>
				</div>
			</div>
		{/if}

		<!-- Export Button -->
		<div class="export-actions">
			<button class="export-button" on:click={handleExport}> 📥 Export Data </button>
			<p class="export-note">The file will be downloaded to your default downloads folder.</p>
		</div>
	{:else}
		<div class="no-session">
			<p>No debugging session available for export</p>
		</div>
	{/if}
</div>

<style>
	.export-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: 1rem;
		gap: 1rem;
		overflow-y: auto;
	}

	.panel-header h3 {
		margin: 0 0 0.5rem 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.panel-description {
		margin: 0;
		color: var(--color-text-secondary);
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.export-summary,
	.export-options,
	.validation-summary {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.export-summary h4,
	.export-options h4,
	.validation-summary h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 0.75rem;
	}

	.summary-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		background: var(--color-surface);
		border-radius: 4px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.summary-label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.summary-value {
		color: var(--color-text);
		font-weight: 600;
		font-family: monospace;
	}

	.options-grid {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.option-group {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.option-label {
		font-weight: 600;
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.format-options {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.format-option {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.format-option:hover {
		background: var(--color-surface-hover);
	}

	.format-option input[type='radio'] {
		margin: 0;
	}

	.format-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.format-info strong {
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.format-info small {
		color: var(--color-text-secondary);
		font-size: 0.75rem;
	}

	.option-group select {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		padding: 0.5rem;
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.include-options {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.include-option {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		color: var(--color-text);
		cursor: pointer;
	}

	.include-option input[type='checkbox'] {
		margin: 0;
	}

	.validation-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		gap: 0.75rem;
	}

	.validation-stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0.75rem;
		background: var(--color-surface);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		text-align: center;
	}

	.validation-stat.valid {
		border-color: #10b981;
		background: rgba(16, 185, 129, 0.1);
	}

	.validation-stat.warning {
		border-color: #f59e0b;
		background: rgba(245, 158, 11, 0.1);
	}

	.validation-stat.error {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.1);
	}

	.stat-value {
		font-size: 1.25rem;
		font-weight: 700;
		color: var(--color-text);
		margin-bottom: 0.25rem;
	}

	.stat-label {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.export-actions {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.export-button {
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 6px;
		padding: 0.75rem 2rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.export-button:hover {
		background: var(--color-primary-hover);
		transform: translateY(-1px);
	}

	.export-note {
		margin: 0;
		color: var(--color-text-secondary);
		font-size: 0.75rem;
		text-align: center;
	}

	.no-session {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--color-text-secondary);
		font-style: italic;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.export-panel {
			padding: 0.5rem;
		}

		.summary-grid,
		.validation-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.format-options {
			gap: 0.25rem;
		}

		.format-option {
			padding: 0.5rem;
		}
	}
</style>
