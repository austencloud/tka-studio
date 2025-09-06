<!-- src/lib/components/SettingsDialog/ImageExportTab/ImageExportToggleButton.svelte -->
<script lang="ts">
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import type { ImageExportSettings } from '$lib/state/image-export-settings.svelte';
	import { saveImageExportSettings } from '$lib/state/image-export-settings.svelte';

	// Props
	const {
		label,
		settingKey,
		isActive = false,
		onToggle,
		tooltip = ''
	} = $props<{
		label: string;
		settingKey: keyof ImageExportSettings;
		isActive: boolean;
		onToggle: (key: keyof ImageExportSettings) => void;
		tooltip?: string;
	}>();

	// Handle button click
	function handleClick() {
		// Provide haptic feedback
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		// Log toggle action for debugging
		console.log(`Toggle button clicked for ${settingKey}:`, {
			currentValue: isActive,
			newValue: !isActive
		});

		// Call the toggle handler
		onToggle(settingKey);

		// Force save after toggle
		setTimeout(() => {
			saveImageExportSettings();
		}, 50);
	}
</script>

<button
	class="toggle-button"
	class:active={isActive}
	onclick={handleClick}
	aria-pressed={isActive}
	aria-label={`Toggle ${label}`}
	title={tooltip}
>
	<span class="button-text">{label}</span>
	<span class="status-icon">{isActive ? '✓' : '✕'}</span>
</button>

<style>
	.toggle-button {
		position: relative;
		width: 100%;
		text-align: left;
		padding: 0.75rem 1rem;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		font-size: 0.95rem;
		margin: 0;
		transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		overflow: hidden;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
		border: none;
	}

	.button-text {
		position: relative;
		z-index: 1;
	}

	.status-icon {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		font-size: 0.8rem;
		z-index: 1;
	}

	.toggle-button::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		border-radius: 8px;
		opacity: 1;
		z-index: 0;
		transition: all 0.3s ease;
	}

	.toggle-button::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		border-radius: 8px;
		opacity: 0;
		z-index: 0;
		transition: all 0.3s ease;
	}

	/* Inactive state */
	.toggle-button:not(.active) {
		color: rgba(255, 255, 255, 0.9);
		border: 2px solid rgba(255, 255, 255, 0.1);
	}

	.toggle-button:not(.active)::before {
		background: linear-gradient(135deg, #2a2a30, #3a3a43);
		opacity: 1;
	}

	.toggle-button:not(.active) .status-icon {
		color: rgba(255, 255, 255, 0.4);
	}

	.toggle-button:not(.active):hover::before {
		background: linear-gradient(135deg, #32323a, #45454f);
	}

	/* Active state */
	.toggle-button.active {
		color: white;
		border: 2px solid #1271ea;
	}

	.toggle-button.active::before {
		background: linear-gradient(135deg, #167bf4, #329bff);
		opacity: 1;
	}

	.toggle-button.active::after {
		background: radial-gradient(circle at center, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
		opacity: 0.6;
	}

	.toggle-button.active .status-icon {
		color: rgba(255, 255, 255, 0.9);
	}

	/* Hover and focus states */
	.toggle-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
	}

	.toggle-button:active {
		transform: translateY(0);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	.toggle-button:focus-visible {
		outline: none;
		box-shadow: 0 0 0 3px rgba(22, 123, 244, 0.4);
	}

	/* Mobile styles */
	@media (max-width: 480px) {
		.toggle-button {
			padding: 0.5rem 0.75rem;
			font-size: 0.85rem;
		}

		.status-icon {
			top: 0.35rem;
			right: 0.35rem;
			font-size: 0.7rem;
		}
	}
</style>
