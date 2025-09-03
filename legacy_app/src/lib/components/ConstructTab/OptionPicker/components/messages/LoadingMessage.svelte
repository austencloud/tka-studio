<script lang="ts">
	import LoadingSpinner from '$lib/components/MainWidget/loading/LoadingSpinner.svelte';
</script>

<div class="message-container loading">
	<div class="pulse-container">
		<LoadingSpinner />
	</div>
	<p>Loading options...</p>
</div>

<style>
	.message-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 2rem;
		text-align: center;
		color: #6b7280;
		box-sizing: border-box;
		font-size: 1.1rem;
	}

	.message-container.loading p {
		margin-top: 1rem;
	}

	/* Pulse animation container */
	.pulse-container {
		animation: pulse 1.5s ease-in-out infinite;
	}

	@keyframes pulse {
		0% {
			opacity: 0.6;
			transform: scale(0.95);
		}
		50% {
			opacity: 1;
			transform: scale(1.05);
		}
		100% {
			opacity: 0.6;
			transform: scale(0.95);
		}
	}
</style>