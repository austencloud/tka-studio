<script lang="ts">
	// Props
	const { size = 'medium', color = '#6c9ce9' } = $props<{
		size?: 'small' | 'medium' | 'large';
		color?: string;
	}>();

	// Determine spinner size based on prop
	const sizeMap = {
		small: { width: '20px', height: '20px', borderWidth: '2px' },
		medium: { width: '40px', height: '40px', borderWidth: '3px' },
		large: { width: '60px', height: '60px', borderWidth: '4px' }
	};

	const spinnerSize = sizeMap[size];
</script>

<div class="spinner-container">
	<div
		class="spinner"
		style:width={spinnerSize.width}
		style:height={spinnerSize.height}
		style:border-width={spinnerSize.borderWidth}
		style:border-top-color={color}
	></div>
</div>

<style>
	.spinner-container {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.spinner {
		border-style: solid;
		border-color: rgba(255, 255, 255, 0.1);
		border-top-style: solid;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
