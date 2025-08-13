<script lang="ts">
	/**
	 * Arrow Debug Header Component
	 * Simple header with title and description
	 */
</script>

<header class="debug-header">
	<h1>🎯 Arrow Debug</h1>
	<p>Step-by-step analysis of arrow positioning with visual debugging</p>
</header>

<style>
	.debug-header {
		text-align: center;
		margin-bottom: 20px;
		padding-bottom: 15px;
		border-bottom: 2px solid rgba(251, 191, 36, 0.3);
		flex-shrink: 0;
	}

	.debug-header h1 {
		font-size: 1.8rem;
		margin-bottom: 8px;
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
	}

	.debug-header p {
		color: #c7d2fe;
		font-size: 1rem;
	}

	/* Responsive design */
	@media (max-width: 1000px) {
		.debug-header h1 {
			font-size: 1.5rem;
		}
	}

	@media (max-width: 768px) {
		.debug-header {
			margin-bottom: 15px;
			padding-bottom: 10px;
		}

		.debug-header h1 {
			font-size: 1.3rem;
		}

		.debug-header p {
			font-size: 0.9rem;
		}
	}
</style>
