<!-- ExportSettingsCard.svelte - Consolidated export settings matching desktop app -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	interface Props {
		exportSettings: {
			include_start_position: boolean;
			add_beat_numbers: boolean;
			add_reversal_symbols: boolean;
			add_user_info: boolean;
			add_word: boolean;
			use_last_save_directory: boolean;
			export_format: string;
			export_quality: string;
			user_name: string;
			custom_note: string;
		};
	}

	let { exportSettings }: Props = $props();
	const dispatch = createEventDispatcher();

	// Format options matching desktop app
	const formatOptions = [
		{ value: 'PNG', label: 'PNG' },
		{ value: 'JPG', label: 'JPG' },
		{ value: 'SVG', label: 'SVG' },
		{ value: 'PDF', label: 'PDF' },
	];

	// Quality options matching desktop app
	const qualityOptions = [
		{ value: '72 DPI', label: '72 DPI (Web)' },
		{ value: '150 DPI', label: '150 DPI (Standard)' },
		{ value: '300 DPI', label: '300 DPI (Print)' },
		{ value: '600 DPI', label: '600 DPI (High Quality)' },
	];

	// User name options (can be extended)
	const userOptions = [
		{ value: 'Default User', label: 'Default User' },
		{ value: 'Custom', label: 'Custom...' },
	];

	// Handle checkbox changes
	function handleCheckboxChange(setting: string, checked: boolean) {
		dispatch('settingChanged', { setting, value: checked });
	}

	// Handle select changes
	function handleSelectChange(setting: string, value: string) {
		dispatch('settingChanged', { setting, value });
	}

	// Handle text input changes
	function handleTextChange(setting: string, value: string) {
		dispatch('settingChanged', { setting, value });
	}
</script>

<div class="export-settings-card">
	<h3 class="card-title">Export Settings</h3>

	<!-- Export Options Section -->
	<div class="settings-section">
		<h4 class="section-title">Export Options</h4>
		<div class="options-grid">
			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.include_start_position}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('include_start_position', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Include Start Position</span>
			</label>

			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.add_beat_numbers}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('add_beat_numbers', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Add Beat Numbers</span>
			</label>

			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.add_reversal_symbols}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('add_reversal_symbols', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Add Reversal Symbols</span>
			</label>

			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.add_user_info}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('add_user_info', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Add User Info</span>
			</label>

			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.add_word}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('add_word', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Add Word</span>
			</label>

			<label class="checkbox-option">
				<input
					type="checkbox"
					checked={exportSettings.use_last_save_directory}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLInputElement) {
							handleCheckboxChange('use_last_save_directory', target.checked);
						}
					}}
				/>
				<span class="checkmark"></span>
				<span class="option-label">Use Last Save Directory</span>
			</label>
		</div>
	</div>

	<!-- Format Settings Section -->
	<div class="settings-section">
		<h4 class="section-title">Format Settings</h4>
		<div class="format-controls">
			<div class="control-group">
				<label class="control-label" for="export-format">Export Format</label>
				<select
					id="export-format"
					class="modern-select"
					value={exportSettings.export_format}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLSelectElement) {
							handleSelectChange('export_format', target.value);
						}
					}}
				>
					{#each formatOptions as option}
						<option value={option.value}>{option.label}</option>
					{/each}
				</select>
			</div>

			<div class="control-group">
				<label class="control-label" for="export-quality">Quality</label>
				<select
					id="export-quality"
					class="modern-select"
					value={exportSettings.export_quality}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLSelectElement) {
							handleSelectChange('export_quality', target.value);
						}
					}}
				>
					{#each qualityOptions as option}
						<option value={option.value}>{option.label}</option>
					{/each}
				</select>
			</div>
		</div>
	</div>

	<!-- User Settings Section -->
	<div class="settings-section">
		<h4 class="section-title">User Settings</h4>
		<div class="user-controls">
			<div class="control-group">
				<label class="control-label" for="user-name">User Name</label>
				<select
					id="user-name"
					class="modern-select"
					value={exportSettings.user_name}
					onchange={(e) => {
						const target = e.target;
						if (target instanceof HTMLSelectElement) {
							handleSelectChange('user_name', target.value);
						}
					}}
				>
					{#each userOptions as option}
						<option value={option.value}>{option.label}</option>
					{/each}
				</select>
			</div>

			<div class="control-group">
				<label class="control-label" for="custom-note">Custom Note</label>
				<textarea
					id="custom-note"
					class="modern-textarea"
					value={exportSettings.custom_note}
					placeholder="Add a custom note to your export..."
					rows="3"
					oninput={(e) => {
						const target = e.target;
						if (target instanceof HTMLTextAreaElement) {
							handleTextChange('custom_note', target.value);
						}
					}}
				></textarea>
			</div>
		</div>
	</div>
</div>

<style>
	.export-settings-card {
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 8px;
		padding: var(--spacing-sm);
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
	}

	.card-title {
		margin: 0;
		font-size: var(--font-size-md);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
	}

	.settings-section {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
	}

	.section-title {
		margin: 0;
		font-size: var(--font-size-sm);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		padding-bottom: 2px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.options-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2px;
	}

	.checkbox-option {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		cursor: pointer;
		padding: 2px var(--spacing-xs);
		border-radius: 3px;
		transition: background-color var(--transition-fast);
	}

	.checkbox-option:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.checkbox-option input[type='checkbox'] {
		display: none;
	}

	.checkmark {
		width: 14px;
		height: 14px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 2px;
		position: relative;
		transition: all var(--transition-fast);
		flex-shrink: 0;
	}

	.checkbox-option input:checked + .checkmark {
		background: #6366f1;
		border-color: #6366f1;
	}

	.checkbox-option input:checked + .checkmark::after {
		content: '✓';
		position: absolute;
		top: -2px;
		left: 2px;
		color: white;
		font-size: 12px;
		font-weight: bold;
	}

	.option-label {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.9);
		line-height: 1.1;
	}

	.format-controls,
	.user-controls {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
	}

	.control-group {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.control-label {
		font-size: var(--font-size-xs);
		font-weight: 500;
		color: rgba(255, 255, 255, 0.9);
	}

	.modern-select,
	.modern-textarea {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.25);
		border-radius: 3px;
		color: #ffffff;
		font-size: var(--font-size-xs);
		transition: border-color var(--transition-fast);
	}

	.modern-select:focus,
	.modern-textarea:focus {
		outline: none;
		border-color: #6366f1;
		box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
	}

	.modern-select option {
		background: #2d3748;
		color: #ffffff;
	}

	.modern-textarea {
		resize: vertical;
		min-height: 40px;
		font-family: inherit;
	}

	.modern-textarea::placeholder {
		color: rgba(255, 255, 255, 0.5);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.options-grid {
			grid-template-columns: 1fr;
		}

		.export-settings-card {
			padding: var(--spacing-md);
		}
	}
</style>
