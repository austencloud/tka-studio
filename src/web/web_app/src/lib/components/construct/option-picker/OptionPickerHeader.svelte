<!--
OptionPickerHeader.svelte - Main header for option picker

Matches the desktop version's header styling exactly:
- "Choose Your Next Option" title
- Monotype Corsiva font
- Centered layout with proper spacing
-->
<script lang="ts">
	// No props needed - this is a static header like desktop version
</script>

<div class="option-picker-header">
	<div class="title-section">
		<h1 class="unified-title">Choose Your Next Option</h1>
	</div>
</div>

<style>
	.option-picker-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		background: transparent;
		padding: 16px;
		border-bottom: none;
	}

	.title-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		margin: 16px;
	}

	.unified-title {
		font-family: 'Monotype Corsiva', cursive, serif;
		font-size: 24px;
		font-weight: bold;
		text-align: center;
		margin: 0;
		color: var(--foreground, #000000);
		/* Match desktop styling exactly */
		letter-spacing: 0.5px;
	}

	/* Fallback fonts if Monotype Corsiva isn't available */
	@supports not (font-family: 'Monotype Corsiva') {
		.unified-title {
			font-family: 'Brush Script MT', 'Lucida Handwriting', cursive, serif;
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.unified-title {
			font-size: 20px;
		}

		.title-section {
			margin: 12px;
		}

		.option-picker-header {
			padding: 12px;
		}
	}

	@media (max-width: 480px) {
		.unified-title {
			font-size: 18px;
		}

		.title-section {
			margin: 8px;
		}

		.option-picker-header {
			padding: 8px;
		}
	}
</style>
