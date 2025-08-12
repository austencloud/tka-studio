<script lang="ts">
	interface Props {
		currentBeat: number;
		totalBeats: number;
	}

	let { currentBeat, totalBeats }: Props = $props();

	// Calculate display values
	const clampedBeat = $derived(Math.max(0, Math.min(currentBeat, totalBeats)));
	const currentAnimationStepIndex = $derived(Math.floor(
		clampedBeat === totalBeats ? totalBeats - 1 : clampedBeat
	));
	const displayBeatNum = $derived(clampedBeat === totalBeats ? 'End' : currentAnimationStepIndex + 1);
	const t = $derived(clampedBeat === totalBeats ? 1.0 : clampedBeat - currentAnimationStepIndex);
</script>

<div class="info">
	Elapsed Time: <span>{clampedBeat.toFixed(2)}</span> | 
	Current Beat: <span>{displayBeatNum}</span> | 
	Progress (t): <span>{t.toFixed(3)}</span>
</div>

<style>
	.info {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 1rem;
		padding: 1rem;
		width: 100%;
		max-width: 600px;
		font-size: 0.875rem;
		text-align: center;
		color: rgba(255, 255, 255, 0.9);
	}

	.info span {
		font-weight: 600;
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		color: rgba(255, 255, 255, 1);
		margin: 0 0.25rem;
	}
</style>
