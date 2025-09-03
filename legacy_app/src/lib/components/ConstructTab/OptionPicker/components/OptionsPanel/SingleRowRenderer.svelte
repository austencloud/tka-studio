<script lang="ts">
	import type { PictographData } from '$lib/types/PictographData';
	import SectionHeader from '../SectionHeader.svelte';
	import OptionGroupGrid from '../OptionGroupGrid.svelte';

	// Props
	export let groups: Array<{ key: string; options: PictographData[] }>;
	export let transitionKey: string | number;
	export let rowIndex: number;
</script>

{#each groups as group (transitionKey + '-group-' + group.key)}
	<SectionHeader groupKey={group.key} isFirstHeader={rowIndex === 0} />
	<OptionGroupGrid options={group.options} key={transitionKey + '-optgroup-' + group.key} />
{/each}

