<script lang="ts">
	import type { SequenceData, SequenceStep } from '../../types/core.js';

	// Props
	let {
		sequenceData = null
	}: {
		sequenceData?: SequenceData | null;
	} = $props();

	// State
	let analysisResults = $state<any>(null);
	let isAnalyzing = $state(false);

	function analyzeSequence(): void {
		if (!sequenceData) return;

		isAnalyzing = true;

		try {
			const metadata = sequenceData[0] || {};
			const startPosition = sequenceData[1] || {};
			const steps = sequenceData.slice(2) as SequenceStep[];

			const analysis = {
				metadata: {
					word: (metadata as any).word || 'Unknown',
					id: (metadata as any).id || 'Unknown',
					totalSteps: steps.length
				},
				startPosition: {
					blue: startPosition.blue_attributes || {},
					red: startPosition.red_attributes || {}
				},
				steps: steps.map((step, index) => ({
					stepNumber: index + 1,
					blue: {
						motionType: step.blue_attributes?.motion_type || 'none',
						startLoc: step.blue_attributes?.start_loc || 'unknown',
						endLoc: step.blue_attributes?.end_loc || 'unknown',
						startOri: step.blue_attributes?.start_ori || 'unknown',
						endOri: step.blue_attributes?.end_ori || 'unknown',
						turns: step.blue_attributes?.turns || 0,
						propRotDir: step.blue_attributes?.prop_rot_dir || 'no_rot'
					},
					red: {
						motionType: step.red_attributes?.motion_type || 'none',
						startLoc: step.red_attributes?.start_loc || 'unknown',
						endLoc: step.red_attributes?.end_loc || 'unknown',
						startOri: step.red_attributes?.start_ori || 'unknown',
						endOri: step.red_attributes?.end_ori || 'unknown',
						turns: step.red_attributes?.turns || 0,
						propRotDir: step.red_attributes?.prop_rot_dir || 'no_rot'
					}
				})),
				validation: validateSequence(steps)
			};

			analysisResults = analysis;
		} catch (error) {
			console.error('Analysis failed:', error);
			analysisResults = { error: 'Analysis failed: ' + String(error) };
		} finally {
			isAnalyzing = false;
		}
	}

	function validateSequence(steps: SequenceStep[]) {
		const issues: string[] = [];
		const warnings: string[] = [];

		steps.forEach((step, index) => {
			// Check for missing attributes
			if (!step.blue_attributes?.motion_type) {
				issues.push(`Step ${index + 1}: Blue prop missing motion type`);
			}
			if (!step.red_attributes?.motion_type) {
				issues.push(`Step ${index + 1}: Red prop missing motion type`);
			}

			// Check for undefined turns
			if (
				step.blue_attributes?.turns === undefined &&
				step.blue_attributes?.motion_type !== 'static'
			) {
				warnings.push(`Step ${index + 1}: Blue prop turns undefined`);
			}
			if (
				step.red_attributes?.turns === undefined &&
				step.red_attributes?.motion_type !== 'static'
			) {
				warnings.push(`Step ${index + 1}: Red prop turns undefined`);
			}

			// Check orientation continuity (basic check)
			if (index > 0) {
				const prevStep = steps[index - 1];
				if (prevStep.blue_attributes?.end_ori !== step.blue_attributes?.start_ori) {
					warnings.push(`Step ${index + 1}: Blue prop orientation discontinuity`);
				}
				if (prevStep.red_attributes?.end_ori !== step.red_attributes?.start_ori) {
					warnings.push(`Step ${index + 1}: Red prop orientation discontinuity`);
				}
			}
		});

		return {
			totalIssues: issues.length + warnings.length,
			errors: issues,
			warnings: warnings,
			isValid: issues.length === 0
		};
	}

	function exportAnalysis(): void {
		if (!analysisResults) return;

		const exportData = {
			timestamp: new Date().toISOString(),
			sequenceWord: analysisResults.metadata.word,
			analysis: analysisResults
		};

		const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `sequence-analysis-${analysisResults.metadata.word}-${Date.now()}.json`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}
</script>

<div class="debug-analyzer">
	<div class="analyzer-header">
		<h3>🔍 Sequence Analysis</h3>
		<div class="analyzer-actions">
			<button class="analyze-btn" onclick={analyzeSequence} disabled={!sequenceData || isAnalyzing}>
				{isAnalyzing ? '⏳ Analyzing...' : '🔍 Analyze'}
			</button>

			{#if analysisResults}
				<button class="export-btn" onclick={exportAnalysis}> 💾 Export </button>
			{/if}
		</div>
	</div>

	{#if analysisResults}
		<div class="analysis-results">
			{#if analysisResults.error}
				<div class="error-section">
					<h4>❌ Analysis Error</h4>
					<p>{analysisResults.error}</p>
				</div>
			{:else}
				<!-- Metadata Section -->
				<div class="metadata-section">
					<h4>📋 Sequence Metadata</h4>
					<div class="metadata-grid">
						<div class="metadata-item">
							<span class="label">Word:</span>
							<span class="value">{analysisResults.metadata.word}</span>
						</div>
						<div class="metadata-item">
							<span class="label">ID:</span>
							<span class="value">{analysisResults.metadata.id}</span>
						</div>
						<div class="metadata-item">
							<span class="label">Steps:</span>
							<span class="value">{analysisResults.metadata.totalSteps}</span>
						</div>
					</div>
				</div>

				<!-- Validation Section -->
				<div class="validation-section">
					<h4>✅ Validation Results</h4>
					<div class="validation-summary">
						<div class="validation-item {analysisResults.validation.isValid ? 'valid' : 'invalid'}">
							<span class="validation-icon">{analysisResults.validation.isValid ? '✅' : '❌'}</span
							>
							<span class="validation-text">
								{analysisResults.validation.isValid ? 'Sequence Valid' : 'Issues Found'}
							</span>
							<span class="validation-count">
								{analysisResults.validation.totalIssues} issues
							</span>
						</div>
					</div>

					{#if analysisResults.validation.errors.length > 0}
						<div class="issues-section errors">
							<h5>❌ Errors ({analysisResults.validation.errors.length})</h5>
							<ul>
								{#each analysisResults.validation.errors as error}
									<li>{error}</li>
								{/each}
							</ul>
						</div>
					{/if}

					{#if analysisResults.validation.warnings.length > 0}
						<div class="issues-section warnings">
							<h5>⚠️ Warnings ({analysisResults.validation.warnings.length})</h5>
							<ul>
								{#each analysisResults.validation.warnings as warning}
									<li>{warning}</li>
								{/each}
							</ul>
						</div>
					{/if}
				</div>

				<!-- Steps Section -->
				<div class="steps-section">
					<h4>🎯 Animation Steps</h4>
					<div class="steps-table">
						<div class="table-header">
							<div class="col-step">Step</div>
							<div class="col-prop">Blue Prop</div>
							<div class="col-prop">Red Prop</div>
						</div>
						{#each analysisResults.steps as step}
							<div class="table-row">
								<div class="col-step">
									<span class="step-number">{step.stepNumber}</span>
								</div>
								<div class="col-prop blue">
									<div class="prop-info">
										<div class="motion-type">{step.blue.motionType}</div>
										<div class="locations">{step.blue.startLoc} → {step.blue.endLoc}</div>
										<div class="orientations">{step.blue.startOri} → {step.blue.endOri}</div>
										<div class="turns">Turns: {step.blue.turns} ({step.blue.propRotDir})</div>
									</div>
								</div>
								<div class="col-prop red">
									<div class="prop-info">
										<div class="motion-type">{step.red.motionType}</div>
										<div class="locations">{step.red.startLoc} → {step.red.endLoc}</div>
										<div class="orientations">{step.red.startOri} → {step.red.endOri}</div>
										<div class="turns">Turns: {step.red.turns} ({step.red.propRotDir})</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.debug-analyzer {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
		margin: 1rem 0;
	}

	.analyzer-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid var(--color-border);
	}

	.analyzer-header h3 {
		margin: 0;
		color: var(--color-text);
		font-size: 1.125rem;
	}

	.analyzer-actions {
		display: flex;
		gap: 0.5rem;
	}

	.analyze-btn,
	.export-btn {
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 6px;
		padding: 0.5rem 1rem;
		cursor: pointer;
		font-weight: 600;
		font-size: 0.875rem;
		transition: all 0.2s ease;
	}

	.analyze-btn:hover:not(:disabled),
	.export-btn:hover {
		background: var(--color-primary-hover);
		transform: translateY(-1px);
	}

	.analyze-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
	}

	.export-btn {
		background: #10b981;
	}

	.export-btn:hover {
		background: #059669;
	}

	.analysis-results {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.metadata-section,
	.validation-section,
	.steps-section {
		background: var(--color-surface);
		border-radius: 6px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.metadata-section h4,
	.validation-section h4,
	.steps-section h4 {
		margin: 0 0 1rem 0;
		color: var(--color-text);
		font-size: 1rem;
	}

	.metadata-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 0.75rem;
	}

	.metadata-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		background: var(--color-surface-elevated);
		border-radius: 4px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.metadata-item .label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.metadata-item .value {
		color: var(--color-text);
		font-weight: 600;
		font-family: monospace;
	}

	.validation-summary {
		margin-bottom: 1rem;
	}

	.validation-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem;
		border-radius: 6px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.validation-item.valid {
		background: rgba(16, 185, 129, 0.1);
		border-color: #10b981;
	}

	.validation-item.invalid {
		background: rgba(239, 68, 68, 0.1);
		border-color: #ef4444;
	}

	.validation-icon {
		font-size: 1rem;
	}

	.validation-text {
		flex: 1;
		font-weight: 600;
		color: var(--color-text);
	}

	.validation-count {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.issues-section {
		margin-top: 1rem;
		padding: 1rem;
		border-radius: 6px;
		border: 1px solid var(--color-border);
	}

	.issues-section.errors {
		background: rgba(239, 68, 68, 0.05);
		border-color: #ef4444;
	}

	.issues-section.warnings {
		background: rgba(245, 158, 11, 0.05);
		border-color: #f59e0b;
	}

	.issues-section h5 {
		margin: 0 0 0.75rem 0;
		font-size: 0.875rem;
		color: var(--color-text);
	}

	.issues-section ul {
		margin: 0;
		padding-left: 1.5rem;
		color: var(--color-text);
	}

	.issues-section li {
		margin: 0.25rem 0;
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.steps-table {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.table-header {
		display: grid;
		grid-template-columns: 60px 1fr 1fr;
		gap: 1rem;
		padding: 0.75rem;
		background: var(--color-surface-elevated);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		font-weight: 600;
		color: var(--color-text-secondary);
		font-size: 0.875rem;
	}

	.table-row {
		display: grid;
		grid-template-columns: 60px 1fr 1fr;
		gap: 1rem;
		padding: 0.75rem;
		background: var(--color-surface-elevated);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.col-step {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.step-number {
		background: var(--color-primary);
		color: white;
		border-radius: 50%;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.75rem;
		font-weight: 600;
	}

	.col-prop {
		display: flex;
		flex-direction: column;
	}

	.col-prop.blue {
		border-left: 3px solid #3b82f6;
		padding-left: 0.75rem;
	}

	.col-prop.red {
		border-left: 3px solid #ef4444;
		padding-left: 0.75rem;
	}

	.prop-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.motion-type {
		font-weight: 600;
		color: var(--color-text);
		text-transform: uppercase;
		font-size: 0.75rem;
	}

	.locations,
	.orientations,
	.turns {
		color: var(--color-text-secondary);
		font-size: 0.75rem;
		font-family: monospace;
	}

	.error-section {
		background: rgba(239, 68, 68, 0.1);
		border: 1px solid #ef4444;
		border-radius: 6px;
		padding: 1rem;
		text-align: center;
	}

	.error-section h4 {
		margin: 0 0 0.5rem 0;
		color: #ef4444;
	}

	.error-section p {
		margin: 0;
		color: var(--color-text);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.analyzer-header {
			flex-direction: column;
			gap: 1rem;
			align-items: stretch;
		}

		.metadata-grid {
			grid-template-columns: 1fr;
		}

		.table-header,
		.table-row {
			grid-template-columns: 1fr;
			gap: 0.5rem;
		}

		.col-step {
			justify-content: flex-start;
		}
	}
</style>
