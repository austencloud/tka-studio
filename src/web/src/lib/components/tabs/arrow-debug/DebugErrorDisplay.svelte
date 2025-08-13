<script lang="ts">
	/**
	 * Debug Error Display Component
	 * Shows initialization errors with retry functionality
	 */

	interface Props {
		error: string;
		onRetry?: () => void;
	}

	let { error, onRetry }: Props = $props();

	function handleRetry() {
		if (onRetry) {
			onRetry();
		} else {
			window.location.reload();
		}
	}
</script>

<div class="error-container">
	<div class="error-box">
		<h2>❌ Initialization Error</h2>
		<p>Failed to initialize the arrow debug system:</p>
		<code>{error}</code>
		<p>Please check the console for more details.</p>
		<button onclick={handleRetry} class="retry-btn">
			🔄 Retry
		</button>
	</div>
</div>

<style>
	.error-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
		padding: 40px;
	}

	.error-box {
		background: rgba(248, 113, 113, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(248, 113, 113, 0.5);
		border-radius: 16px;
		padding: 40px;
		text-align: center;
		max-width: 500px;
		width: 100%;
	}

	.error-box h2 {
		margin: 20px 0 15px 0;
		color: #f87171;
		font-size: 1.5rem;
	}

	.error-box p {
		color: #c7d2fe;
		margin-bottom: 10px;
		line-height: 1.5;
	}

	.error-box code {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		padding: 8px 12px;
		font-family: 'Courier New', monospace;
		color: #f87171;
		display: block;
		margin: 15px 0;
		word-break: break-all;
	}

	.retry-btn {
		background: linear-gradient(135deg, #f87171, #ef4444);
		border: none;
		border-radius: 8px;
		padding: 10px 16px;
		color: white;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		margin-top: 15px;
	}

	.retry-btn:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
	}
</style>
