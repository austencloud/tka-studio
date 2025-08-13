<script lang="ts">
	import { MOTION_TYPES, type MotionType } from '../utils/motion-helpers.js';

	interface Props {
		motionType: MotionType;
		propColor: string;
		onMotionTypeChange: (motionType: MotionType) => void;
	}

	let { motionType, propColor, onMotionTypeChange }: Props = $props();
</script>

<div class="motion-type-selector">
	<div class="prop-row">
		<div class="prop-label" style="color: {propColor}">
			Motion
		</div>
		<select 
			value={motionType}
			onchange={(e) => onMotionTypeChange((e.target as HTMLSelectElement).value as MotionType)}
		>
			{#each MOTION_TYPES as type}
				<option value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.motion-type-selector {
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
