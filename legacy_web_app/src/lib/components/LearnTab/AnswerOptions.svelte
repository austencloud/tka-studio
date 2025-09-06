<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import ButtonAnswers from './ButtonAnswers.svelte';
	import PictographAnswers from './PictographAnswers.svelte';
	import type { AnswerFormat } from '$lib/state/stores/learn/lesson_configs';

	export let answerFormat: AnswerFormat = 'button';
	export let options: any[] = [];
	export let disabled: boolean = false;

	const dispatch = createEventDispatcher<{
		select: any;
	}>();

	function handleSelect(option: any) {
		if (!disabled) {
			dispatch('select', option);
		}
	}
</script>

<div class="answer-options">
	{#if answerFormat === 'button'}
		<ButtonAnswers {options} {disabled} on:select={(e) => handleSelect(e.detail)} />
	{:else if answerFormat === 'pictograph'}
		<PictographAnswers pictographs={options} {disabled} on:select={(e) => handleSelect(e.detail)} />
	{/if}
</div>

<style>
	.answer-options {
		width: 100%;
		max-width: 800px;
	}
</style>
