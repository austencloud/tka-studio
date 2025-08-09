<!-- SelectInput.svelte - Improved contrast select dropdown -->
<script lang="ts">
	interface Option {
		value: string;
		label: string;
	}

	interface Props {
		label: string;
		value: string;
		options: Option[] | string[];
		helpText?: string;
		disabled?: boolean;
		required?: boolean;
		onchange?: (value: string) => void;
	}

	let {
		label,
		value = '',
		options = [],
		helpText,
		disabled = false,
		required = false,
		onchange,
	}: Props = $props();

	// Convert string array to option objects if needed
	const normalizedOptions = $derived(() => {
		return options.map((option) =>
			typeof option === 'string' ? { value: option, label: option } : option
		);
	});

	// Get the actual options array
	let optionsArray = $derived(normalizedOptions());

	function handleChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		onchange?.(target.value);
	}
</script>

<div class="setting-card">
	<label for={label} class="setting-label">
		{label}
		{#if required}<span class="required">*</span>{/if}
	</label>
	<select id={label} {value} {disabled} {required} class="modern-select" onchange={handleChange}>
		{#each optionsArray as option}
			<option value={option.value}>{option.label}</option>
		{/each}
	</select>
	{#if helpText}
		<div class="help-tooltip">{helpText}</div>
	{/if}
</div>

<style>
	.setting-card {
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 6px;
		padding: var(--spacing-md);
	}

	.setting-label {
		display: block;
		font-weight: 500;
		color: #ffffff;
		margin-bottom: var(--spacing-sm);
		font-size: var(--font-size-sm);
	}

	.required {
		color: #ef4444;
		margin-left: 2px;
	}

	.modern-select {
		width: 100%;
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.25);
		border-radius: 4px;
		color: #ffffff;
		font-size: var(--font-size-sm);
		transition: border-color var(--transition-fast);
		cursor: pointer;
	}

	.modern-select:focus {
		outline: none;
		border-color: #6366f1;
		box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
	}

	.modern-select:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.modern-select option {
		background: #2d3748;
		color: #ffffff;
	}

	.help-tooltip {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
		margin-top: var(--spacing-xs);
		line-height: 1.3;
	}
</style>
