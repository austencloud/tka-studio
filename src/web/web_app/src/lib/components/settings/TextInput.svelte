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
		onchange?: (value: string) => void;
	}

	const dispatch = createEventDispatcher<{ change: string }>();

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
		onchange,
	}: Props = $props();

	function handleInput(event: Event) {
		const target = event.target;
		if (target instanceof HTMLInputElement) {
			onchange?.(target.value);
			dispatch('change', target.value);
		}
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
		padding: clamp(12px, 1.5vw, 24px);
		container-type: inline-size;
	}

	.setting-label {
		display: block;
		font-weight: 500;
		color: #ffffff;
		margin-bottom: clamp(8px, 1vw, 16px);
		font-size: clamp(12px, 1.2vw, 16px);
	}

	.required {
		color: #ef4444;
		margin-left: 2px;
	}

	.modern-input {
		width: 100%;
		padding: clamp(8px, 1vw, 12px) clamp(12px, 1.5vw, 20px);
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.25);
		border-radius: 4px;
		color: #ffffff;
		font-size: clamp(12px, 1.2vw, 16px);
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
		font-size: clamp(10px, 1vw, 14px);
		color: rgba(255, 255, 255, 0.6);
		margin-top: clamp(6px, 0.8vw, 12px);
		line-height: 1.3;
	}
</style>
