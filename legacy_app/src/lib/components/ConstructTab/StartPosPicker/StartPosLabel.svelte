<script lang="ts">
	export let customStyles: string = ''; // Optional additional styles
</script>

<div class="label" style={customStyles}>Choose your start position</div>

<style>
	.label {
		margin-bottom: 10%;
		font-size: 1.5rem;
		font-family: var(
			--font-sans,
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif
		);
		font-weight: 500;
		color: var(--color-text-primary, rgba(0, 0, 0, 0.8));
		background-color: transparent;
		padding: 10px 20px;
		text-align: center;
		line-height: 1.4;
	}

	@media (orientation: portrait) {
		.label {
			margin-bottom: 5%;
			margin-top: 5%;
			font-size: 1.25rem;
		}
	}

	@media (max-width: 768px) {
		.label {
			font-size: 1.25rem;
		}
	}
</style>
