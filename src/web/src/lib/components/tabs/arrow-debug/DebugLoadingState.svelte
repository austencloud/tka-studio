<script lang="ts">
	/**
	 * Debug Loading State Component
	 * Shows loading spinner and initialization message
	 */

	interface Props {
		message?: string;
	}

	let { message = "Setting up positioning services and debug tools..." }: Props = $props();
</script>

<div class="loading-container">
	<div class="loading-box">
		<div class="spinner"></div>
		<h2>🔧 Initializing Arrow Debug</h2>
		<p>{message}</p>
	</div>
</div>

<style>
	.loading-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
		padding: 40px;
	}

	.loading-box {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 40px;
		text-align: center;
		max-width: 500px;
		width: 100%;
	}

	.loading-box h2 {
		margin: 20px 0 15px 0;
		color: #fbbf24;
		font-size: 1.5rem;
	}

	.loading-box p {
		color: #c7d2fe;
		margin-bottom: 10px;
		line-height: 1.5;
	}

	.spinner {
		width: 50px;
		height: 50px;
		border: 4px solid rgba(251, 191, 36, 0.3);
		border-top: 4px solid #fbbf24;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
