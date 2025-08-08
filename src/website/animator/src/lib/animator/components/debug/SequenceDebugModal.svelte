<script lang="ts">
	import type { SequenceData } from '../../types/core.js';
	import type { DebugSession, BeatDebugInfo, DebugModalState } from '../../types/debug.js';

	import { SequenceDebugger } from '../../core/debug/sequence-debugger.js';
	import DebugOverview from './DebugOverview.svelte';
	import BeatEditor from './BeatEditor.svelte';
	import ValidationPanel from './ValidationPanel.svelte';
	import ExportPanel from './ExportPanel.svelte';

	// Props
	let {
		isOpen = false,
		sequenceData = null,
		onClose = () => {},
		onApplyOverrides = () => {}
	}: {
		isOpen?: boolean;
		sequenceData?: SequenceData | null;
		onClose?: () => void;
		onApplyOverrides?: (_overrides: any) => void;
	} = $props();

	// State
	let sequenceDebugger = $state<SequenceDebugger | null>(null);
	let currentSession = $state<DebugSession | null>(null);
	let debugHistory = $state<BeatDebugInfo[]>([]);
	let isAnalyzing = $state(false);
	let analysisProgress = $state(0);

	let modalState = $state<DebugModalState>({
		isOpen: false,
		activeTab: 'overview', // Use existing type for now
		selectedBeat: null,
		selectedProp: null,
		viewMode: 'table'
	});

	// UI state for collapsible sections
	let expandedSections = $state({
		summary: true,
		beatAnalysis: true,
		validation: false,
		configuration: false,
		export: false
	});

	// Initialize debugger when sequence data changes
	$effect(() => {
		if (sequenceData && isOpen && !sequenceDebugger) {
			initializeDebugger();
		}
	});

	// Update modal state when isOpen changes
	$effect(() => {
		if (modalState.isOpen !== isOpen) {
			modalState.isOpen = isOpen;
			if (!isOpen) {
				cleanup();
			}
		}
	});

	async function initializeDebugger(): Promise<void> {
		if (!sequenceData) return;

		try {
			sequenceDebugger = new SequenceDebugger({
				enabled: true,
				captureMode: 'manual',
				validationLevel: 'comprehensive',
				visualizationMode: 'modal',
				autoValidate: true,
				recordHistory: true,
				maxHistorySize: 1000
			});

			// Set up event listeners
			sequenceDebugger.addEventListener('beat_calculated', handleBeatCalculated);
			sequenceDebugger.addEventListener('validation_completed', handleValidationCompleted);
			sequenceDebugger.addEventListener('session_started', handleSessionStarted);
			sequenceDebugger.addEventListener('session_ended', handleSessionEnded);

			// Start debugging session
			currentSession = sequenceDebugger.startSession(sequenceData);

			// Analyze all beats
			await analyzeAllBeats();
		} catch (error) {
			console.error('Failed to initialize debugger:', error);
		}
	}

	async function analyzeAllBeats(): Promise<void> {
		if (!sequenceDebugger || !sequenceData) return;

		isAnalyzing = true;
		analysisProgress = 0;

		const totalBeats = sequenceData.length - 2; // Exclude metadata and start position

		try {
			for (let beat = 0; beat <= totalBeats; beat++) {
				const debugInfo = sequenceDebugger.analyzeBeat(beat);
				if (debugInfo) {
					debugHistory = [...debugHistory, debugInfo];
				}

				analysisProgress = ((beat + 1) / (totalBeats + 1)) * 100;

				// Allow UI to update
				await new Promise((resolve) => setTimeout(resolve, 1));
			}
		} catch (error) {
			console.error('Error during beat analysis:', error);
		} finally {
			isAnalyzing = false;
			analysisProgress = 100;
		}
	}

	function handleBeatCalculated(_event: any): void {
		// Update UI with new debug info if needed
	}

	function handleValidationCompleted(_event: any): void {
		// Update validation display if needed
	}

	function handleSessionStarted(event: any): void {
		const { session } = event;
		currentSession = session;
	}

	function handleSessionEnded(_event: any): void {
		// Handle session end if needed
	}

	function handleBeatSelect(beatNumber: number): void {
		modalState.selectedBeat = beatNumber;
		// Expand configuration section when beat is selected
		expandedSections.configuration = true;
		// Scroll to configuration section
		setTimeout(() => {
			const configSection = document.querySelector('.configuration-section');
			configSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
		}, 100);
	}

	function handlePropSelect(prop: 'blue' | 'red'): void {
		modalState.selectedProp = prop;
	}

	function toggleSection(section: keyof typeof expandedSections): void {
		expandedSections[section] = !expandedSections[section];
	}

	function handleOverrideApply(overrides: any): void {
		if (sequenceDebugger) {
			sequenceDebugger.setOverrides(overrides);
			onApplyOverrides(overrides);

			// Re-analyze affected beats
			reanalyzeBeats();
		}
	}

	async function reanalyzeBeats(): Promise<void> {
		if (!sequenceDebugger) return;

		// Clear current history
		debugHistory = [];

		// Re-analyze all beats with new overrides
		await analyzeAllBeats();
	}

	function handleExport(): void {
		if (!currentSession || !sequenceDebugger) return;

		const session = sequenceDebugger.endSession();
		if (session) {
			const exportData = {
				session,
				rawData: debugHistory,
				configuration: sequenceDebugger.getConfiguration(),
				validationResults: session.validationSummary,
				exportTime: Date.now(),
				version: '1.0.0'
			};

			// Create download
			const blob = new Blob([JSON.stringify(exportData, null, 2)], {
				type: 'application/json'
			});
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.download = `sequence-debug-${session.sequenceWord}-${Date.now()}.json`;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		}
	}

	function cleanup(): void {
		if (sequenceDebugger) {
			sequenceDebugger.endSession();
			sequenceDebugger = null;
		}
		currentSession = null;
		debugHistory = [];
		modalState.selectedBeat = null;
		modalState.selectedProp = null;
		modalState.activeTab = 'configuration';
	}

	function handleClose(): void {
		cleanup();
		onClose();
	}

	// Keyboard shortcuts
	function handleKeydown(event: KeyboardEvent): void {
		if (!isOpen) return;

		switch (event.key) {
			case 'Escape':
				handleClose();
				break;
			case '1':
				if (event.ctrlKey || event.metaKey) {
					event.preventDefault();
					toggleSection('summary');
				}
				break;
			case '2':
				if (event.ctrlKey || event.metaKey) {
					event.preventDefault();
					toggleSection('beatAnalysis');
				}
				break;
			case '3':
				if (event.ctrlKey || event.metaKey) {
					event.preventDefault();
					toggleSection('validation');
				}
				break;
			case '4':
				if (event.ctrlKey || event.metaKey) {
					event.preventDefault();
					toggleSection('configuration');
				}
				break;
			case '5':
				if (event.ctrlKey || event.metaKey) {
					event.preventDefault();
					toggleSection('export');
				}
				break;
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
	<div
		class="debug-modal-overlay"
		onclick={handleClose}
		role="button"
		tabindex="0"
		onkeydown={(e) => e.key === 'Enter' && handleClose()}
	>
		<div
			class="debug-modal"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.stopPropagation()}
			role="dialog"
			aria-modal="true"
			tabindex="-1"
		>
			<!-- Modal Header -->
			<div class="debug-modal-header">
				<div class="header-content">
					<h2>🔍 Sequence Interpretation Debugger</h2>
					{#if currentSession}
						<div class="session-info">
							<span class="sequence-word">{currentSession.sequenceWord}</span>
							<span class="session-id">Session: {currentSession.id.slice(-8)}</span>
						</div>
					{/if}
				</div>

				<div class="header-actions">
					{#if isAnalyzing}
						<div class="analysis-progress">
							<div class="progress-bar">
								<div class="progress-fill" style:width="{analysisProgress}%"></div>
							</div>
							<span class="progress-text">Analyzing... {analysisProgress.toFixed(0)}%</span>
						</div>
					{/if}

					<button class="close-button" onclick={handleClose} title="Close (Esc)"> ✕ </button>
				</div>
			</div>

			<!-- Debug Console Header -->
			<div class="debug-console-header">
				<h3>🔧 Debug Console</h3>
				<div class="section-toggles">
					<button
						class="toggle-button"
						class:active={expandedSections.summary}
						onclick={() => toggleSection('summary')}
						title="Toggle Summary (Ctrl+1)"
					>
						📊 Summary
					</button>
					<button
						class="toggle-button"
						class:active={expandedSections.beatAnalysis}
						onclick={() => toggleSection('beatAnalysis')}
						title="Toggle Beat Analysis (Ctrl+2)"
					>
						📋 Analysis
					</button>
					<button
						class="toggle-button"
						class:active={expandedSections.validation}
						onclick={() => toggleSection('validation')}
						title="Toggle Validation (Ctrl+3)"
					>
						✅ Validation
					</button>
					<button
						class="toggle-button"
						class:active={expandedSections.configuration}
						onclick={() => toggleSection('configuration')}
						title="Toggle Configuration (Ctrl+4)"
					>
						⚙️ Config
					</button>
					<button
						class="toggle-button"
						class:active={expandedSections.export}
						onclick={() => toggleSection('export')}
						title="Toggle Export (Ctrl+5)"
					>
						💾 Export
					</button>
				</div>
			</div>

			<!-- Consolidated Debug Console Content -->
			<div class="debug-content">
				<div class="debug-console">
					<!-- Summary Section -->
					{#if expandedSections.summary}
						<div class="debug-section summary-section">
							<div class="section-header">
								<h4>📊 Analysis Summary</h4>
								<button
									class="collapse-button"
									onclick={() => toggleSection('summary')}
									title="Collapse Summary"
								>
									−
								</button>
							</div>
							<div class="section-content">
								{#if debugHistory.length > 0}
									<DebugOverview
										{debugHistory}
										{currentSession}
										{modalState}
										onBeatSelect={handleBeatSelect}
										onPropSelect={handlePropSelect}
									/>
								{:else}
									<div class="loading-state">
										<p>Loading debug data...</p>
										{#if isAnalyzing}
											<div class="progress-bar">
												<div class="progress-fill" style:width="{analysisProgress}%"></div>
											</div>
										{/if}
									</div>
								{/if}
							</div>
						</div>
					{/if}

					<!-- Beat Analysis Section -->
					{#if expandedSections.beatAnalysis}
						<div class="debug-section beat-analysis-section">
							<div class="section-header">
								<h4>📋 Beat Analysis</h4>
								<button
									class="collapse-button"
									onclick={() => toggleSection('beatAnalysis')}
									title="Collapse Beat Analysis"
								>
									−
								</button>
							</div>
							<div class="section-content">
								<!-- Simplified beat analysis table from DebugOverview -->
								<div class="beat-analysis-compact">
									{#if debugHistory.length > 0}
										<div class="analysis-table-container">
											<table class="analysis-table">
												<thead>
													<tr>
														<th>Beat</th>
														<th>Blue Motion</th>
														<th>Red Motion</th>
														<th>Issues</th>
														<th>Actions</th>
													</tr>
												</thead>
												<tbody>
													{#each debugHistory.slice(0, 10) as beat}
														<tr
															class="beat-row"
															class:selected={modalState.selectedBeat === beat.beatNumber}
														>
															<td class="beat-number">{beat.beatNumber}</td>
															<td class="motion-type">
																{beat.blueProps?.attributes?.motion_type ?? 'N/A'}
															</td>
															<td class="motion-type">
																{beat.redProps?.attributes?.motion_type ?? 'N/A'}
															</td>
															<td class="issues">
																{(beat.blueProps?.validation?.errors?.length ?? 0) +
																	(beat.redProps?.validation?.errors?.length ?? 0) +
																	(beat.blueProps?.validation?.warnings?.length ?? 0) +
																	(beat.redProps?.validation?.warnings?.length ?? 0)}
															</td>
															<td class="actions">
																<button
																	class="action-button"
																	onclick={() => handleBeatSelect(beat.beatNumber)}
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
										{#if debugHistory.length > 10}
											<div class="table-footer">
												<span class="table-info">
													Showing first 10 of {debugHistory.length} beats
												</span>
											</div>
										{/if}
									{:else}
										<div class="empty-state">
											<p>No beat analysis data available</p>
										</div>
									{/if}
								</div>
							</div>
						</div>
					{/if}

					<!-- Validation Section -->
					{#if expandedSections.validation}
						<div class="debug-section validation-section">
							<div class="section-header">
								<h4>✅ Validation Results</h4>
								<button
									class="collapse-button"
									onclick={() => toggleSection('validation')}
									title="Collapse Validation"
								>
									−
								</button>
							</div>
							<div class="section-content">
								<ValidationPanel {debugHistory} {currentSession} {modalState} />
							</div>
						</div>
					{/if}

					<!-- Configuration Section -->
					{#if expandedSections.configuration}
						<div class="debug-section configuration-section">
							<div class="section-header">
								<h4>⚙️ Beat Configuration</h4>
								<button
									class="collapse-button"
									onclick={() => toggleSection('configuration')}
									title="Collapse Configuration"
								>
									−
								</button>
							</div>
							<div class="section-content">
								{#if modalState.selectedBeat !== null}
									<BeatEditor
										{debugHistory}
										{modalState}
										{sequenceDebugger}
										onOverrideApply={handleOverrideApply}
									/>
								{:else}
									<div class="empty-state">
										<p>Select a beat from the analysis table to configure parameters</p>
									</div>
								{/if}
							</div>
						</div>
					{/if}

					<!-- Export Section -->
					{#if expandedSections.export}
						<div class="debug-section export-section">
							<div class="section-header">
								<h4>💾 Export Debug Data</h4>
								<button
									class="collapse-button"
									onclick={() => toggleSection('export')}
									title="Collapse Export"
								>
									−
								</button>
							</div>
							<div class="section-content">
								<ExportPanel {currentSession} {debugHistory} onExport={handleExport} />
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.debug-modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.8);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		backdrop-filter: blur(4px);
	}

	.debug-modal {
		background: var(--color-surface);
		border-radius: 12px;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
		width: 95vw;
		height: 95vh;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		border: 1px solid var(--color-border);
	}

	.debug-modal-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	.header-content h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.session-info {
		display: flex;
		gap: 1rem;
		margin-top: 0.25rem;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.sequence-word {
		font-weight: 600;
		color: var(--color-primary);
	}

	.header-actions {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.analysis-progress {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.progress-bar {
		width: 120px;
		height: 4px;
		background: var(--color-border);
		border-radius: 2px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: var(--color-primary);
		transition: width 0.3s ease;
	}

	.progress-text {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		white-space: nowrap;
	}

	.close-button {
		background: none;
		border: none;
		font-size: 1.25rem;
		color: var(--color-text-secondary);
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.close-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text);
	}

	.debug-console-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	.debug-console-header h3 {
		margin: 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.section-toggles {
		display: flex;
		gap: 0.5rem;
	}

	.toggle-button {
		background: none;
		border: 1px solid var(--color-border);
		padding: 0.5rem 0.75rem;
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		cursor: pointer;
		border-radius: 6px;
		transition: all 0.2s ease;
		white-space: nowrap;
	}

	.toggle-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text);
		border-color: var(--color-border-hover);
	}

	.toggle-button.active {
		color: var(--color-primary);
		border-color: var(--color-primary);
		background: var(--color-primary-subtle);
	}

	.debug-content {
		flex: 1;
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.debug-console {
		flex: 1;
		overflow-y: auto;
		padding: 0;
	}

	.debug-section {
		border-bottom: 1px solid var(--color-border);
	}

	.section-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.5rem;
		background: var(--color-surface);
		border-bottom: 1px solid var(--color-border);
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.section-header h4 {
		margin: 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.collapse-button {
		background: none;
		border: none;
		font-size: 1rem;
		color: var(--color-text-secondary);
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.collapse-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text);
	}

	.section-content {
		padding: 0;
	}

	/* Beat Analysis Compact Table */
	.beat-analysis-compact {
		padding: 1rem;
	}

	.analysis-table-container {
		overflow-x: auto;
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.analysis-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	.analysis-table th {
		background: var(--color-surface-elevated);
		padding: 0.75rem;
		text-align: left;
		font-weight: 600;
		color: var(--color-text);
		border-bottom: 1px solid var(--color-border);
	}

	.analysis-table td {
		padding: 0.75rem;
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text);
	}

	.analysis-table .beat-row:hover {
		background: var(--color-surface-hover);
	}

	.analysis-table .beat-row.selected {
		background: var(--color-primary-subtle);
	}

	.analysis-table .beat-number {
		font-weight: 600;
		color: var(--color-primary);
	}

	.analysis-table .motion-type {
		font-family: monospace;
		font-size: 0.8rem;
	}

	.analysis-table .issues {
		text-align: center;
		font-weight: 600;
	}

	.analysis-table .action-button {
		background: none;
		border: none;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.analysis-table .action-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text);
	}

	.table-footer {
		padding: 0.75rem;
		text-align: center;
		background: var(--color-surface);
		border-top: 1px solid var(--color-border);
	}

	.table-info {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
	}

	.empty-state {
		padding: 2rem;
		text-align: center;
		color: var(--color-text-secondary);
	}

	.empty-state p {
		margin: 0;
		font-style: italic;
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 2rem;
		gap: 1rem;
		color: var(--color-text-secondary);
	}

	.loading-state p {
		margin: 0;
		font-style: italic;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.debug-modal {
			width: 100vw;
			height: 100vh;
			max-width: none;
			max-height: none;
			border-radius: 0;
		}

		.debug-modal-header {
			padding: 1rem;
		}

		.header-content h2 {
			font-size: 1.125rem;
		}

		.session-info {
			flex-direction: column;
			gap: 0.25rem;
		}

		.debug-console-header {
			padding: 0.75rem 1rem;
		}

		.section-toggles {
			flex-wrap: wrap;
			gap: 0.25rem;
		}

		.toggle-button {
			padding: 0.375rem 0.5rem;
			font-size: 0.7rem;
		}

		.section-header {
			padding: 0.75rem 1rem;
		}

		.beat-analysis-compact {
			padding: 0.75rem;
		}

		.analysis-table {
			font-size: 0.8rem;
		}

		.analysis-table th,
		.analysis-table td {
			padding: 0.5rem;
		}
	}
</style>
