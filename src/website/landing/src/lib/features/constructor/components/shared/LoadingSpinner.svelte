<!--
  LoadingSpinner Component

  A reusable loading spinner component.
-->
<script lang="ts">
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let color = '#4299e1';

	$: spinnerSize = {
		small: '24px',
		medium: '40px',
		large: '60px'
	}[size];
</script>

<div class="loading-spinner" style="width: {spinnerSize}; height: {spinnerSize};">
	<svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
		<circle
			cx="25"
			cy="25"
			r="20"
			fill="none"
			stroke="#e2e8f0"
			stroke-width="4"
		/>
		<circle
			cx="25"
			cy="25"
			r="20"
			fill="none"
			stroke={color}
			stroke-width="4"
			stroke-linecap="round"
			stroke-dasharray="31.416"
			stroke-dashoffset="31.416"
		>
			<animate
				attributeName="stroke-dasharray"
				dur="2s"
				values="0 31.416;15.708 15.708;0 31.416"
				repeatCount="indefinite"
			/>
			<animate
				attributeName="stroke-dashoffset"
				dur="2s"
				values="0;-15.708;-31.416"
				repeatCount="indefinite"
			/>
		</circle>
	</svg>
</div>

<style>
	.loading-spinner {
		display: inline-block;
		animation: rotate 2s linear infinite;
	}

	.loading-spinner svg {
		width: 100%;
		height: 100%;
	}

	@keyframes rotate {
		100% {
			transform: rotate(360deg);
		}
	}
</style>
