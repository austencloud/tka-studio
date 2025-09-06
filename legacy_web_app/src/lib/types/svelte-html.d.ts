/**
 * Type definitions for Svelte HTML attributes
 * This file provides TypeScript support for Svelte-specific HTML attributes
 */

declare namespace svelteHTML {
	/**
	 * Svelte event handler attributes
	 */
	interface HTMLAttributes<T> {
		// Svelte event handlers with proper DOM event types
		'on:click'?: (event: MouseEvent) => any;
		'on:change'?: (event: Event) => any;
		'on:input'?: (event: InputEvent) => any;
		'on:focus'?: (event: FocusEvent) => any;
		'on:blur'?: (event: FocusEvent) => any;
		'on:keydown'?: (event: KeyboardEvent) => any;
		'on:keyup'?: (event: KeyboardEvent) => any;
		'on:mouseenter'?: (event: MouseEvent) => any;
		'on:mouseleave'?: (event: MouseEvent) => any;
		'on:mouseover'?: (event: MouseEvent) => any;
		'on:mouseout'?: (event: MouseEvent) => any;
		'on:mousedown'?: (event: MouseEvent) => any;
		'on:mouseup'?: (event: MouseEvent) => any;
		'on:mousemove'?: (event: MouseEvent) => any;
		'on:load'?: (event: Event) => any;

		// Window events
		'on:resize'?: (event: UIEvent) => any;
		'on:scroll'?: (event: Event) => any;

		// Custom events for TKAGlyph components
		'on:letterLoaded'?: (event: CustomEvent<any>) => any;

		// Custom events for BeatFrame component
		'on:naturalheightchange'?: (event: CustomEvent<{ height: number }>) => any;
		'on:beatselected'?: (event: CustomEvent<{ beatId: string }>) => any;

		// Custom events for Grid component
		'on:error'?: (event: CustomEvent<{ message: string }>) => any;
		onError?: (message: string) => any;

		// Custom events for Prop and Arrow components
		'on:loaded'?: (event: CustomEvent<any>) => any;

		// Svelte class directives
		'class:active'?: boolean;
		'class:selected'?: boolean;
		'class:disabled'?: boolean;
		'class:visible'?: boolean;
		'class:hidden'?: boolean;
		'class:dragging'?: boolean;

		// Svelte binding directives
		'bind:this'?: any;
		'bind:value'?: any;
		'bind:checked'?: boolean;
		'bind:group'?: any;
		'bind:clientWidth'?: number;
		'bind:clientHeight'?: number;
		'bind:offsetWidth'?: number;
		'bind:offsetHeight'?: number;

		// Svelte transition directives
		'in:fade'?: any;
		'out:fade'?: any;
		'transition:fade'?: any;
		'in:fly'?: any;
		'out:fly'?: any;
		'transition:fly'?: any;
		'in:slide'?: any;
		'out:slide'?: any;
		'transition:slide'?: any;
		'transition:scale'?: any;

		// Svelte action directives
		'use:action'?: any;

		// Svelte slot directives
		slot?: string;

		// Other Svelte directives
		'let:item'?: any;
		'let:index'?: number;

		// Event modifiers
		'on:click|self'?: (event: MouseEvent) => any;
		'on:click|stopPropagation'?: (event: MouseEvent) => any;
		'on:click|preventDefault'?: (event: MouseEvent) => any;
		'on:click|capture'?: (event: MouseEvent) => any;
		'on:click|once'?: (event: MouseEvent) => any;
		'on:click|passive'?: (event: MouseEvent) => any;
	}
}
