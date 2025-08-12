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
		padding: clamp(12px, 1.5vw, 24px);
		container-type: inline-size;
	}

	.toggle-setting {
		display: flex;
		align-items: center;
		gap: clamp(8px, 1vw, 16px);
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
		width: clamp(38px, 5vw, 50px);
		height: clamp(20px, 2.5vw, 26px);
		background: rgba(255, 255, 255, 0.2);
		border-radius: calc(clamp(20px, 2.5vw, 26px) / 2);
		transition: background-color var(--transition-fast);
		flex-shrink: 0;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.toggle-slider::before {
		content: '';
		position: absolute;
		top: 1px;
		left: 1px;
		width: calc(clamp(20px, 2.5vw, 26px) - 4px);
		height: calc(clamp(20px, 2.5vw, 26px) - 4px);
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
		transform: translateX(calc(clamp(38px, 5vw, 50px) - clamp(20px, 2.5vw, 26px) + 2px));
	}

	.setting-label {
		font-weight: 500;
		color: #ffffff;
		font-size: clamp(12px, 1.2vw, 16px);
	}

	.help-tooltip {
		font-size: clamp(10px, 1vw, 14px);
		color: rgba(255, 255, 255, 0.6);
		margin-top: clamp(6px, 0.8vw, 12px);
		line-height: 1.3;
		margin-left: clamp(46px, 6vw, 58px);
	}
</style>
