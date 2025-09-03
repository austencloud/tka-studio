<script lang="ts">
	export let type: 'empty' | 'initial' = 'empty';
	export let message: string = 'No options available';
</script>

<div class="message-container {type}">
	<div class="message-content">
		{#if type === 'empty'}
			<div class="icon">📋</div>
		{:else if type === 'initial'}
			<div class="icon">👆</div>
		{/if}
		<div class="text">{message}</div>
	</div>
</div>

<style>
	.message-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 2rem;
		text-align: center;
		color: #6b7280;
		box-sizing: border-box;
		font-size: 1.1rem;
	}

	.message-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		max-width: 80%;
	}

	.icon {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
		opacity: 0.8;
	}

	.text {
		font-size: 1.1rem;
		line-height: 1.5;
	}

	.message-container.empty {
		color: #6b7280;
	}

	.message-container.initial {
		color: #9ca3af;
	}

	/* Responsive styles */
	@media (max-width: 640px) {
		.message-container {
			padding: 1rem;
		}

		.icon {
			font-size: 2rem;
		}

		.text {
			font-size: 1rem;
		}
	}
</style>
