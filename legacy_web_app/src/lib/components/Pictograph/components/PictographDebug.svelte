<script lang="ts">
	export let state: string;
	export let componentsLoaded: number;
	export let totalComponents: number;
	export let renderCount: number;
</script>

<g class="debug-overlay">
	<rect x="10" y="10" width="200" height="80" fill="rgba(0,0,0,0.7)" rx="5" />
	<text x="20" y="30" font-size="12" fill="white">State: {state}</text>
	<text x="20" y="50" font-size="12" fill="white">Loaded: {componentsLoaded}/{totalComponents}</text>
	<text x="20" y="70" font-size="12" fill="white">Renders: {renderCount}</text>
</g>

<style>
	.debug-overlay {
		opacity: 0.9;
		pointer-events: none;
	}
</style>