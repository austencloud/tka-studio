<script lang="ts">
	// Create a function to manually show the first-time setup dialog
	// This will be exported and used by the FirstTimeSetupDialog component
	export let showDialog: () => void;
</script>

<button
	class="debug-button"
	on:click={showDialog}
	title="Show First-Time Setup Dialog (Debug)"
	aria-label="Show First-Time Setup Dialog (Debug)"
>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		width="16"
		height="16"
		viewBox="0 0 24 24"
		fill="none"
		stroke="currentColor"
		stroke-width="2"
		stroke-linecap="round"
		stroke-linejoin="round"
	>
		<path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
		<path d="M12 16v-4"></path>
		<path d="M12 8h.01"></path>
	</svg>
</button>

<style>
	.debug-button {
		background: #1e293b;
		color: white;
		border: 1px solid #334155;
		border-radius: 50%;
		width: 36px;
		height: 36px;
		cursor: pointer;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		display: flex;
		align-items: center;
		justify-content: center;
		opacity: 0.7;
		transition: all 0.2s ease;
		position: fixed;
		bottom: 10px;
		left: 10px;
		z-index: 9999;
	}

	.debug-button:hover {
		opacity: 1;
		background: #334155;
		box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
		transform: scale(1.05);
	}

	/* Adjust position on larger screens */
	@media (min-width: 768px) {
		.debug-button {
			bottom: 15px;
			left: 15px;
		}
	}
</style>
