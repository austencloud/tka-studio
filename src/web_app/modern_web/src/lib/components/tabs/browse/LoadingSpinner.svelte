<script lang="ts">
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let color: string = 'var(--primary-color)';
</script>

<div
	class="loading-spinner"
	class:small={size === 'small'}
	class:medium={size === 'medium'}
	class:large={size === 'large'}
	style="--spinner-color: {color}"
>
	<div class="spinner-ring">
		<div></div>
		<div></div>
		<div></div>
		<div></div>
	</div>
</div>

<style>
	.loading-spinner {
		display: inline-block;
		position: relative;
	}

	.spinner-ring {
		display: inline-block;
		position: relative;
	}

	.spinner-ring div {
		box-sizing: border-box;
		display: block;
		position: absolute;
		border-radius: 50%;
		animation: spinner-ring-animation 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
		border-color: var(--spinner-color) transparent transparent transparent;
	}

	.spinner-ring div:nth-child(1) {
		animation-delay: -0.45s;
	}

	.spinner-ring div:nth-child(2) {
		animation-delay: -0.3s;
	}

	.spinner-ring div:nth-child(3) {
		animation-delay: -0.15s;
	}

	/* Size variants */
	.small .spinner-ring {
		width: 24px;
		height: 24px;
	}

	.small .spinner-ring div {
		width: 20px;
		height: 20px;
		margin: 2px;
		border-width: 2px;
	}

	.medium .spinner-ring {
		width: 40px;
		height: 40px;
	}

	.medium .spinner-ring div {
		width: 32px;
		height: 32px;
		margin: 4px;
		border-width: 3px;
	}

	.large .spinner-ring {
		width: 64px;
		height: 64px;
	}

	.large .spinner-ring div {
		width: 52px;
		height: 52px;
		margin: 6px;
		border-width: 4px;
	}

	@keyframes spinner-ring-animation {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
