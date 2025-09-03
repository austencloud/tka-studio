<script lang="ts">
	import { popIn } from '$lib/transitions/popIn';

	export let animationDuration = 200; // Animation duration for transitions
</script>

<g in:popIn={{ duration: animationDuration, start: 0.85, opacity: 0.2 }}>
	<rect x="425" y="425" width="100" height="100" fill="transparent" />
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
	<text x="50%" y="550" dominant-baseline="middle" text-anchor="middle" font-size="16" fill="#666">
		Initializing...
	</text>
</g>
