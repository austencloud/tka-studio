<!--
PyToggle Component - Svelte Version
A custom toggle switch with smooth animations.
-->
<script lang="ts">
	interface Props {
		checked?: boolean;
		width?: number;
		bgColor?: string;
		activeColor?: string;
		circleColor?: string;
		disabled?: boolean;
		onstateChanged?: (event: CustomEvent) => void;
	}

	let {
		checked = false,
		width = 50,
		bgColor = 'rgba(255, 255, 255, 0.1)',
		activeColor = 'var(--gradient-primary)',
		circleColor = '#FFFFFF',
		disabled = false,
		onstateChanged,
	}: Props = $props();

	// State
	let isChecked = $state(checked);

	// Handle click
	function handleToggle() {
		if (!disabled) {
			isChecked = !isChecked;
			// Dispatch custom event
			const event = new CustomEvent('stateChanged', {
				detail: { checked: isChecked },
			});
			document.dispatchEvent(event);

			// Call the callback if provided
			if (onstateChanged) {
				onstateChanged(event);
			}
		}
	}

	// Export method for parent to control
	export function setChecked(value: boolean) {
		isChecked = value;
	}

	export function getChecked() {
		return isChecked;
	}

	// Computed styles
	let toggleWidth = $derived(`${width}px`);
	let toggleHeight = $derived(`${width * 0.6}px`);
	let circleSize = $derived(`${width * 0.45}px`);
	let circleOffset = $derived(isChecked ? `${width * 0.5}px` : '4px');
</script>

<button
	class="py-toggle"
	class:checked={isChecked}
	class:disabled
	{disabled}
	onclick={handleToggle}
	style="
		width: {toggleWidth};
		height: {toggleHeight};
		background-color: {isChecked ? activeColor : bgColor};
	"
	type="button"
	role="switch"
	aria-checked={isChecked}
	aria-label="Toggle switch"
>
	<div
		class="toggle-circle"
		style="
			width: {circleSize};
			height: {circleSize};
			background-color: {circleColor};
			transform: translateX({circleOffset});
		"
	></div>
</button>

<style>
	.py-toggle {
		position: relative;
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 25px;
		cursor: pointer;
		padding: 0;
		transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		outline: none;
		overflow: hidden;
		backdrop-filter: blur(10px);
		box-shadow:
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.py-toggle:hover:not(:disabled) {
		border-color: rgba(255, 255, 255, 0.3);
		box-shadow:
			0 6px 20px rgba(0, 0, 0, 0.15),
			inset 0 1px 0 rgba(255, 255, 255, 0.15);
		transform: translateY(-1px);
	}

	.py-toggle.checked {
		background: linear-gradient(
			135deg,
			var(--primary-color, #6366f1),
			var(--accent-color, #06b6d4)
		) !important;
		border-color: rgba(255, 255, 255, 0.4);
		box-shadow:
			0 8px 25px rgba(99, 102, 241, 0.3),
			inset 0 1px 0 rgba(255, 255, 255, 0.2);
	}

	.py-toggle:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.py-toggle:focus-visible {
		box-shadow:
			0 0 0 2px rgba(99, 102, 241, 0.5),
			0 4px 16px rgba(0, 0, 0, 0.1);
	}

	.toggle-circle {
		border-radius: 50%;
		transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		position: absolute;
		top: 50%;
		transform-origin: center;
		margin-top: calc(-1 * var(--circle-size) / 2);
		box-shadow:
			0 2px 8px rgba(0, 0, 0, 0.2),
			0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
	}
</style>
