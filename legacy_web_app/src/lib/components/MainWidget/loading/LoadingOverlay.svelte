<script lang="ts">
	import LoadingSpinner from "./LoadingSpinner.svelte";

	// Remove loadingStore import
	// import { loadingState } from '$lib/stores/ui/loadingStore';

	// --- Props ---
	export let onRetry: () => void;
	export let showInitializationError: boolean = false;
	export let progress: number = 0; // Get progress from parent (MainWidget)
	export let message: string = 'Loading...'; // Get message from parent
	export let errorMessage: string | null = null; // Get error message from parent
</script>

<div class="loading-overlay">
	<div class="loading-container">
		<LoadingSpinner />
		<div class="loading-progress-container">
			<div class="loading-progress-bar">
				<div class="loading-progress-fill" style="width: {progress}%"></div>
			</div>
			<p class="loading-text">{message}</p>

			{#if showInitializationError}
				<p class="error-text">
					{errorMessage ?? 'An error occurred during initialization.'}
					<button class="retry-button" on:click={onRetry}> Retry </button>
				</p>
			{/if}
		</div>
	</div>
</div>

<style>
	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 999;
		background: rgba(11, 29, 42, 0.4);
		backdrop-filter: blur(2px);
	}
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
		padding: 30px;
		border-radius: 12px;
		background: rgba(30, 40, 60, 0.85);
		backdrop-filter: blur(5px);
		max-width: 400px;
		width: 100%;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		animation: fadeIn 0.5s ease-out;
	}
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.loading-progress-container {
		width: 100%;
		text-align: center;
	}
	.loading-progress-bar {
		width: 100%;
		height: 10px;
		background-color: rgba(255, 255, 255, 0.2);
		border-radius: 5px;
		overflow: hidden;
		margin-bottom: 10px;
	}
	.loading-progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #6c9ce9, #1e3c72);
		border-radius: 5px;
		transition: width 0.3s ease;
	}
	.loading-text {
		font-size: 16px;
		color: #fff;
		margin: 0;
	}
	.error-text {
		color: #ff6b6b;
		margin-top: 10px;
	}
	.retry-button {
		margin-left: 10px;
		padding: 5px 15px;
		background: #3a7bd5;
		color: #fff;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 14px;
		transition: background 0.2s;
	}
	.retry-button:hover {
		background: #2a5298;
	}
</style>
