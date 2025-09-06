<script lang="ts">
	import { fade } from 'svelte/transition';

	export let animationDuration = 300;
</script>

<g transition:fade={{ duration: animationDuration }}>
	<circle cx="475" cy="475" r="40" fill="none" stroke="#ccc" stroke-width="8" />
	<path
		d="M475 435 A40 40 0 0 1 515 475"
		fill="none"
		stroke="#4299e1"
		stroke-width="8"
		stroke-linecap="round"
	>
		<animate
			attributeName="stroke-dasharray"
			from="0 1000"
			to="1000 1000"
			dur="1s"
			repeatCount="indefinite"
		/>
	</path>
</g>
