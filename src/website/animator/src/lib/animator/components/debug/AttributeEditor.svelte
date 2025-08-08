<script lang="ts">
	import type { MotionType, PropRotDir, Orientation } from '../../types/core.js';

	// Props
	let {
		editMode = 'view',
		attributes = {},
		onAttributeChange = () => {}
	}: {
		editMode?: 'view' | 'edit' | 'compare';
		attributes?: any;
		onAttributeChange?: (_key: string, _value: any) => void;
	} = $props();

	// Available options
	const motionTypes: MotionType[] = ['pro', 'anti', 'static', 'dash', 'none'];
	const rotationDirections: PropRotDir[] = ['cw', 'ccw', 'no_rot'];
	const orientations: Orientation[] = ['in', 'out', 'n', 'e', 's', 'w'];
	const positions = ['n', 'e', 's', 'w', 'n_hand', 'e_hand', 's_hand', 'w_hand'];
	const turnOptions = [0, 0.5, 1, 1.5, 2, 2.5, 3];

	function handleChange(key: string, event: Event): void {
		const target = event.target as HTMLSelectElement;
		let value: any = target.value;

		// Handle special cases for undefined values
		if (value === 'undefined') {
			value = undefined;
		} else if (key === 'turns' && value !== undefined) {
			value = parseFloat(value);
		}

		onAttributeChange(key, value);
	}
</script>

<div class="attribute-editor">
	<div class="editor-grid">
		<!-- Motion Type -->
		<div class="attribute-group">
			<label for="motion-type-select">Motion Type:</label>
			{#if editMode === 'edit'}
				<select
					id="motion-type-select"
					value={attributes.motion_type}
					onchange={(e) => handleChange('motion_type', e)}
				>
					{#each motionTypes as motionType}
						<option value={motionType}>{motionType}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value motion-type {attributes.motion_type}">
					{attributes.motion_type}
				</span>
			{/if}
		</div>

		<!-- Start Location -->
		<div class="attribute-group">
			<label for="start-loc-select">Start Location:</label>
			{#if editMode === 'edit'}
				<select
					id="start-loc-select"
					value={attributes.start_loc}
					onchange={(e) => handleChange('start_loc', e)}
				>
					{#each positions as position}
						<option value={position}>{position}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.start_loc}</span>
			{/if}
		</div>

		<!-- End Location -->
		<div class="attribute-group">
			<label for="end-loc-select">End Location:</label>
			{#if editMode === 'edit'}
				<select
					id="end-loc-select"
					value={attributes.end_loc}
					onchange={(e) => handleChange('end_loc', e)}
				>
					{#each positions as position}
						<option value={position}>{position}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.end_loc}</span>
			{/if}
		</div>

		<!-- Start Orientation -->
		<div class="attribute-group">
			<label for="start-ori-select">Start Orientation:</label>
			{#if editMode === 'edit'}
				<select
					id="start-ori-select"
					value={attributes.start_ori}
					onchange={(e) => handleChange('start_ori', e)}
				>
					<option value="undefined">None</option>
					{#each orientations as orientation}
						<option value={orientation}>{orientation}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.start_ori || 'None'}</span>
			{/if}
		</div>

		<!-- End Orientation -->
		<div class="attribute-group">
			<label for="end-ori-select">End Orientation:</label>
			{#if editMode === 'edit'}
				<select
					id="end-ori-select"
					value={attributes.end_ori}
					onchange={(e) => handleChange('end_ori', e)}
				>
					<option value="undefined">None</option>
					{#each orientations as orientation}
						<option value={orientation}>{orientation}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.end_ori || 'None'}</span>
			{/if}
		</div>

		<!-- Rotation Direction -->
		<div class="attribute-group">
			<label for="rot-dir-select">Rotation Direction:</label>
			{#if editMode === 'edit'}
				<select
					id="rot-dir-select"
					value={attributes.prop_rot_dir}
					onchange={(e) => handleChange('prop_rot_dir', e)}
				>
					<option value="undefined">None</option>
					{#each rotationDirections as direction}
						<option value={direction}>{direction}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.prop_rot_dir || 'None'}</span>
			{/if}
		</div>

		<!-- Turns -->
		<div class="attribute-group">
			<label for="turns-select">Turns:</label>
			{#if editMode === 'edit'}
				<select
					id="turns-select"
					value={attributes.turns}
					onchange={(e) => handleChange('turns', e)}
				>
					<option value="undefined">None</option>
					{#each turnOptions as turns}
						<option value={turns}>{turns}</option>
					{/each}
				</select>
			{:else}
				<span class="attribute-value">{attributes.turns ?? 'None'}</span>
			{/if}
		</div>
	</div>
</div>

<style>
	.attribute-editor {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.editor-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1rem;
	}

	.attribute-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.attribute-group label {
		font-weight: 600;
		color: var(--color-text);
		font-size: 0.875rem;
	}

	.attribute-group select {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		padding: 0.5rem;
		color: var(--color-text);
	}

	.attribute-value {
		padding: 0.5rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		color: var(--color-text);
		font-family: monospace;
	}

	.attribute-value.motion-type {
		font-weight: 600;
		text-transform: uppercase;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.editor-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
