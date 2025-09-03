<!-- src/lib/components/GenerateTab/controls/ParametersSection.svelte -->
<script lang="ts">
	import LengthSelector from '../components/LengthSelector.svelte';
	import TurnIntensity from '../components/TurnIntensity.svelte';
	import PropContinuity from '../components/PropContinuity.svelte';
	import LevelSelector from '../components/LevelSelector.svelte';
</script>

<section class="control-section parameters-section">
	<div class="panel-header compact">
		<h3>Sequence Parameters</h3>
	</div>

	<div class="controls-container compact">
		<div class="control-card" data-tooltip="Set the number of beats">
			<LengthSelector />
		</div>

		<div class="control-card" data-tooltip="Control turn intensity">
			<TurnIntensity />
		</div>

		<div class="control-card" data-tooltip="Set prop movement style">
			<PropContinuity />
		</div>

		<div class="control-card" data-tooltip="Set complexity level">
			<LevelSelector />
		</div>
	</div>
</section>

<style>
	.control-section {
		margin-bottom: 1rem;
		background: var(--color-surface-700, rgba(30, 40, 60, 0.5));
		border-radius: 0.5rem;
		overflow: visible; /* Changed from hidden to allow tooltips to show */
		border: 1px solid rgba(255, 255, 255, 0.05);
		position: relative; /* Ensure proper stacking context */
		animation: fadeIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		opacity: 0;
	}

	.parameters-section {
		margin-bottom: 1rem;
		animation-delay: 0.4s;
	}

	.panel-header {
		padding: 1rem 1rem 0.75rem 1rem;
		position: relative;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	.panel-header.compact {
		padding: 0.75rem 1rem;
	}

	.panel-header::after {
		content: '';
		position: absolute;
		bottom: -1px;
		left: 1rem;
		width: 2rem;
		height: 2px;
		background: linear-gradient(to right, var(--color-accent, #3a7bd5), transparent);
		border-radius: 2px;
	}

	.panel-header h3 {
		margin: 0;
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		letter-spacing: -0.01em;
	}

	.controls-container {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		padding: 0.75rem 1rem 1rem;
		overflow-y: auto;
	}

	.controls-container.compact {
		padding: 0.5rem 0.75rem 0.75rem;
	}

	.control-card {
		background: var(--color-surface-600, rgba(40, 50, 70, 0.7));
		border-radius: 0.5rem;
		padding: 0.75rem;
		transition: all 0.2s ease;
		border: 1px solid rgba(255, 255, 255, 0.08);
		position: relative;
		overflow: visible; /* Changed from hidden to allow buttons to be clickable */
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		z-index: 0; /* Ensure proper stacking */
		animation: slideIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		opacity: 0;
	}

	.control-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent);
		opacity: 0;
		transition: opacity 0.2s ease;
		z-index: -1; /* Place behind content */
		pointer-events: none; /* Ensure clicks pass through */
	}

	.control-card:hover {
		background: var(--color-surface-500, rgba(50, 60, 80, 0.7));
		transform: translateY(-1px);
		box-shadow:
			0 4px 8px rgba(0, 0, 0, 0.15),
			0 0 0 1px rgba(58, 123, 213, 0.3);
		border-color: rgba(58, 123, 213, 0.3);
		z-index: 2; /* Bring to front when hovered */
	}

	.control-card:hover::before {
		opacity: 1;
	}

	/* Make sure all interactive elements inside control cards are clickable */
	.control-card :global(button),
	.control-card :global(input),
	.control-card :global(select),
	.control-card :global(.intensity-button) {
		position: relative;
		z-index: 3; /* Higher than the card's z-index */
		pointer-events: auto; /* Ensure clicks register */
	}

	/* Tooltips */
	.control-card {
		position: relative;
	}

	.control-card::after {
		content: attr(data-tooltip);
		position: absolute;
		bottom: 100%;
		left: 50%;
		transform: translateX(-50%) translateY(-8px) scale(0.95);
		padding: 0.5rem 0.75rem;
		background: var(--color-surface-900, rgba(15, 25, 40, 0.95));
		color: white;
		border-radius: 0.375rem;
		font-size: 0.75rem;
		white-space: nowrap;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
		opacity: 0;
		pointer-events: none;
		transition: all 0.2s ease;
		z-index: 10;
	}

	.control-card:hover::after {
		opacity: 1;
		transform: translateX(-50%) translateY(-4px) scale(1);
	}

	/* Focus states for accessibility */
	.control-card:focus-within {
		outline: none;
		box-shadow:
			0 0 0 2px var(--color-accent, #3a7bd5),
			0 4px 8px rgba(0, 0, 0, 0.2);
	}

	/* Animation for panel transitions */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
			filter: blur(5px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
			filter: blur(0);
		}
	}

	@keyframes slideIn {
		from {
			transform: translateX(20px);
			opacity: 0;
		}
		to {
			transform: translateX(0);
			opacity: 1;
		}
	}

	.control-card:nth-child(1) {
		animation-delay: 0.5s;
	}
	.control-card:nth-child(2) {
		animation-delay: 0.6s;
	}
	.control-card:nth-child(3) {
		animation-delay: 0.7s;
	}
	.control-card:nth-child(4) {
		animation-delay: 0.8s;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.controls-container {
			padding: 1rem;
		}

		.panel-header {
			padding: 1rem 1rem 0.5rem 1rem;
		}

		.control-section {
			margin-bottom: 1rem;
		}

		.control-card {
			padding: 0.75rem;
		}

		.control-card::after {
			white-space: normal;
			width: 200px;
			text-align: center;
		}
	}

	/* Touch device optimizations */
	@media (hover: none) {
		.control-card:active {
			background: var(--color-surface-600, rgba(40, 50, 70, 0.7));
		}

		.control-card::after {
			display: none;
		}
	}
</style>
