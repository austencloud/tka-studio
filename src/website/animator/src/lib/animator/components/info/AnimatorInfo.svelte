<script lang="ts">
	// Import sub-components
	import SequenceHeader from './SequenceHeader.svelte';
	import TechnicalDetails from './TechnicalDetails.svelte';

	// Modern Svelte 5 props
	let {
		currentBeat = 0,
		totalBeats = 0,
		sequenceWord = '',
		sequenceAuthor = '',
		showAdvanced = false
	}: {
		currentBeat?: number;
		totalBeats?: number;
		sequenceWord?: string;
		sequenceAuthor?: string;
		showAdvanced?: boolean;
	} = $props();
</script>

<div class="animator-info">
	<!-- Primary Information - Always Visible -->
	<div class="primary-info">
		<SequenceHeader {sequenceWord} {sequenceAuthor} />
	</div>

	<!-- Advanced Information - Collapsible -->
	<TechnicalDetails {currentBeat} {totalBeats} {showAdvanced} />
</div>

<style>
	.animator-info {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		padding: 1.5rem;
		background: var(--color-surface);
		border-radius: 12px;
		border: 1px solid var(--color-border);
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		transition: all 0.3s ease;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}

	/* Primary Information Section */
	.primary-info {
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.animator-info {
			padding: 1rem;
			gap: 1rem;
		}
	}

	@media (max-width: 480px) {
		.animator-info {
			padding: 0.75rem;
			gap: 0.75rem;
		}
	}
</style>
