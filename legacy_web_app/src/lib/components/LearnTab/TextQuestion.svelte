<script lang="ts">
	export let text: string = '';
</script>

<div class="text-question">
	<span class="question-text">{text}</span>
</div>

<style>
	.text-question {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.question-text {
		font-size: 4rem;
		font-weight: bold;
		padding: 1rem;
	}
</style>
