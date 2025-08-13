<script lang="ts">
	import { ORIENTATIONS, type Orientation } from '../utils/motion-helpers.js';

	interface Props {
		orientation: Orientation;
		propColor: string;
		label: string;
		onOrientationChange: (orientation: Orientation) => void;
	}

	let { orientation, propColor, label, onOrientationChange }: Props = $props();
</script>

<div class="orientation-selector">
	<div class="prop-row">
		<div class="prop-label" style="color: {propColor}">
			{label}
		</div>
		<select 
			value={orientation}
			onchange={(e) => onOrientationChange((e.target as HTMLSelectElement).value as Orientation)}
		>
			{#each ORIENTATIONS as ori}
				<option value={ori}>{ori.charAt(0).toUpperCase() + ori.slice(1)}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.orientation-selector {
		width: 100%;
	}

	.prop-row {
		display: grid;
		grid-template-columns: 60px 1fr;
		gap: 10px;
		align-items: center;
	}

	.prop-label {
		font-weight: 600;
		font-size: 0.9rem;
	}

	select {
		padding: 6px 8px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		font-size: 13px;
	}

	select option {
		background: #312e81;
		color: white;
	}

	select:focus {
		outline: none;
		border-color: rgba(99, 102, 241, 0.5);
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
	}
</style>
