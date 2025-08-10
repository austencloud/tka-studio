<!--
IOSToggle.svelte - Clean iOS-style toggle component
A beautiful toggle switch that follows iOS design patterns with proper interaction model.
-->
<script lang="ts">
	interface Props {
		/** The currently selected option */
		value: string;
		/** Array of exactly 2 options with value and label */
		options: Array<{ value: string; label: string; icon?: string }>;
		/** Optional label for the control */
		label?: string;
		/** Whether the control is disabled */
		disabled?: boolean;
		/** Size variant */
		size?: 'small' | 'medium' | 'large';
		/** Color variant */
		variant?: 'primary' | 'secondary';
		/** Callback when value changes */
		onchange?: (value: string) => void;
	}

	let {
		value,
		options,
		label,
		disabled = false,
		size = 'medium',
		variant = 'primary',
		onchange,
	}: Props = $props();

	// Ensure we have exactly 2 options
	$effect(() => {
		if (options.length !== 2) {
			console.warn('IOSToggle expects exactly 2 options');
		}
	});

	// Derived state
	let isSecondOption = $derived(value === options[1]?.value);
	let firstOption = $derived(options[0]);
	let secondOption = $derived(options[1]);

	function handleToggleClick() {
		if (disabled) return;

		const newValue = isSecondOption ? firstOption?.value : secondOption?.value;
		if (newValue !== undefined) {
			onchange?.(newValue);
		}
	}
</script>

<div class="ios-toggle-container">
	{#if label}
		<div class="control-label">{label}</div>
	{/if}

	<div class="toggle-layout">
		<!-- Left label (not clickable) -->
		<div class="option-label" class:active={!isSecondOption}>
			{#if firstOption?.icon}
				<span class="label-icon">{firstOption.icon}</span>
			{/if}
			<span class="label-text">{firstOption?.label}</span>
		</div>

		<!-- iOS-style toggle switch (only clickable element) -->
		<button
			type="button"
			class="ios-toggle"
			class:checked={isSecondOption}
			class:disabled
			{disabled}
			onclick={handleToggleClick}
			data-size={size}
			data-variant={variant}
			role="switch"
			aria-checked={isSecondOption}
			aria-label={`Toggle between ${firstOption?.label} and ${secondOption?.label}`}
		>
			<div class="toggle-track">
				<div class="toggle-thumb"></div>
			</div>
		</button>

		<!-- Right label (not clickable) -->
		<div class="option-label" class:active={isSecondOption}>
			{#if secondOption?.icon}
				<span class="label-icon">{secondOption.icon}</span>
			{/if}
			<span class="label-text">{secondOption?.label}</span>
		</div>
	</div>
</div>

<style>
	.ios-toggle-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
	}

	.control-label {
		color: rgba(255, 255, 255, 0.9);
		font-size: 14px;
		font-weight: 500;
		text-align: center;
	}

	.toggle-layout {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.option-label {
		display: flex;
		align-items: center;
		gap: 6px;
		color: rgba(255, 255, 255, 0.6);
		font-size: 14px;
		font-weight: 500;
		transition: all 0.2s ease;
		user-select: none;
		min-width: 80px;
		justify-content: center;
	}

	.option-label.active {
		color: rgba(255, 255, 255, 0.95);
		font-weight: 600;
	}

	.label-icon {
		font-size: 0.9em;
	}

	.label-text {
		white-space: nowrap;
	}

	.ios-toggle {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		outline: none;
		transition: all 0.2s ease;
	}

	.ios-toggle:disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	.toggle-track {
		width: 60px;
		height: 32px;
		background: rgba(255, 255, 255, 0.15);
		border-radius: 16px;
		position: relative;
		transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		border: 1px solid rgba(255, 255, 255, 0.2);
		backdrop-filter: blur(10px);
		box-shadow:
			inset 0 2px 4px rgba(0, 0, 0, 0.1),
			0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.ios-toggle.checked .toggle-track {
		background: rgba(70, 130, 255, 0.8);
		border-color: rgba(70, 130, 255, 0.9);
		box-shadow:
			inset 0 2px 4px rgba(0, 0, 0, 0.1),
			0 2px 8px rgba(70, 130, 255, 0.3);
	}

	.toggle-thumb {
		width: 28px;
		height: 28px;
		background: #ffffff;
		border-radius: 50%;
		position: absolute;
		top: 1px;
		left: 1px;
		transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		box-shadow:
			0 2px 4px rgba(0, 0, 0, 0.2),
			0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.ios-toggle.checked .toggle-thumb {
		transform: translateX(28px);
	}

	.ios-toggle:hover:not(:disabled) .toggle-track {
		border-color: rgba(255, 255, 255, 0.3);
		box-shadow:
			inset 0 2px 4px rgba(0, 0, 0, 0.1),
			0 2px 8px rgba(0, 0, 0, 0.15);
	}

	.ios-toggle.checked:hover:not(:disabled) .toggle-track {
		background: rgba(80, 140, 255, 0.9);
		border-color: rgba(80, 140, 255, 1);
		box-shadow:
			inset 0 2px 4px rgba(0, 0, 0, 0.1),
			0 3px 12px rgba(70, 130, 255, 0.4);
	}

	.ios-toggle:focus-visible {
		outline: 2px solid rgba(70, 130, 255, 0.6);
		outline-offset: 3px;
	}

	/* Size variants */
	.ios-toggle[data-size='small'] .toggle-track {
		width: 48px;
		height: 26px;
		border-radius: 13px;
	}

	.ios-toggle[data-size='small'] .toggle-thumb {
		width: 22px;
		height: 22px;
	}

	.ios-toggle[data-size='small'].checked .toggle-thumb {
		transform: translateX(20px);
	}

	.ios-toggle[data-size='large'] .toggle-track {
		width: 72px;
		height: 38px;
		border-radius: 19px;
	}

	.ios-toggle[data-size='large'] .toggle-thumb {
		width: 34px;
		height: 34px;
	}

	.ios-toggle[data-size='large'].checked .toggle-thumb {
		transform: translateX(32px);
	}

	/* Color variants */
	.ios-toggle[data-variant='secondary'].checked .toggle-track {
		background: rgba(156, 163, 175, 0.8);
		border-color: rgba(156, 163, 175, 0.9);
		box-shadow:
			inset 0 2px 4px rgba(0, 0, 0, 0.1),
			0 2px 8px rgba(156, 163, 175, 0.3);
	}

	.ios-toggle[data-variant='secondary']:focus-visible {
		outline-color: rgba(156, 163, 175, 0.6);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.toggle-layout {
			gap: 12px;
		}

		.option-label {
			min-width: 70px;
			font-size: 13px;
		}
	}

	/* High contrast mode support */
	@media (prefers-contrast: high) {
		.toggle-track {
			border-width: 2px;
		}

		.ios-toggle.checked .toggle-track {
			background: #0066cc;
			border-color: #ffffff;
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.toggle-track,
		.toggle-thumb,
		.option-label {
			transition: none;
		}
	}
</style>
