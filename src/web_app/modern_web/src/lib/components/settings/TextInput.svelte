<!-- TextInput.svelte - Improved contrast text input -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	interface Props {
		label: string;
		value: string;
		placeholder?: string;
		helpText?: string;
		type?: 'text' | 'email' | 'password' | 'number';
		maxlength?: number;
		min?: number;
		max?: number;
		disabled?: boolean;
		required?: boolean;
	}

	let {
		label,
		value = '',
		placeholder,
		helpText,
		type = 'text',
		maxlength,
		min,
		max,
		disabled = false,
		required = false,
	}: Props = $props();

	const dispatch = createEventDispatcher();

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		dispatch('change', target.value);
	}
</script>

<div class="setting-card">
	<label for={label} class="setting-label">
		{label}
		{#if required}<span class="required">*</span>{/if}
	</label>
	<input
		id={label}
		{type}
		{value}
		{placeholder}
		{maxlength}
		{min}
		{max}
		{disabled}
		{required}
		class="modern-input"
		oninput={handleInput}
	/>
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

	.modern-input {
		width: 100%;
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.25);
		border-radius: 4px;
		color: #ffffff;
		font-size: var(--font-size-sm);
		transition: border-color var(--transition-fast);
	}

	.modern-input:focus {
		outline: none;
		border-color: #6366f1;
		box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
	}

	.modern-input::placeholder {
		color: rgba(255, 255, 255, 0.5);
	}

	.modern-input:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.help-tooltip {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
		margin-top: var(--spacing-xs);
		line-height: 1.3;
	}
</style>
