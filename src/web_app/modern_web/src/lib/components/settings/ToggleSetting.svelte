<!-- ToggleSetting.svelte - Improved contrast toggle component -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	interface Props {
		label: string;
		checked: boolean;
		helpText?: string;
		disabled?: boolean;
	}

	let { label, checked = false, helpText, disabled = false }: Props = $props();

	const dispatch = createEventDispatcher();

	function handleToggle() {
		if (disabled) return;
		dispatch('change', !checked);
	}
</script>

<div class="setting-card">
	<label class="toggle-setting" class:disabled>
		<input type="checkbox" {checked} {disabled} onchange={handleToggle} />
		<span class="toggle-slider"></span>
		<span class="setting-label">{label}</span>
	</label>
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

	.toggle-setting {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
		cursor: pointer;
		margin: 0;
	}

	.toggle-setting.disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	.toggle-setting input[type='checkbox'] {
		display: none;
	}

	.toggle-slider {
		position: relative;
		width: 42px;
		height: 22px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 11px;
		transition: background-color var(--transition-fast);
		flex-shrink: 0;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.toggle-slider::before {
		content: '';
		position: absolute;
		top: 1px;
		left: 1px;
		width: 18px;
		height: 18px;
		background: #ffffff;
		border-radius: 50%;
		transition: transform var(--transition-fast);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.toggle-setting input:checked + .toggle-slider {
		background: #6366f1;
		border-color: #6366f1;
	}

	.toggle-setting input:checked + .toggle-slider::before {
		transform: translateX(20px);
	}

	.setting-label {
		font-weight: 500;
		color: #ffffff;
		font-size: var(--font-size-sm);
	}

	.help-tooltip {
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.6);
		margin-top: var(--spacing-xs);
		line-height: 1.3;
		margin-left: 50px;
	}
</style>
