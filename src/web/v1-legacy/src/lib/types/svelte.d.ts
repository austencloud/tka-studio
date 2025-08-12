/**
 * Type definitions for Svelte
 */

declare module "svelte" {
  // Define the Svelte module to avoid TypeScript errors
}

/**
 * Type definitions for Svelte HTML attributes
 */
declare namespace svelteHTML {
  interface HTMLAttributes<T> {
    // DOM events
    onblur?: (event: FocusEvent) => any;
    onchange?: (event: Event) => any;
    onclick?: (event: MouseEvent) => any;
    ondblclick?: (event: MouseEvent) => any;
    onfocus?: (event: FocusEvent) => any;
    oninput?: (event: InputEvent) => any;
    onkeydown?: (event: KeyboardEvent) => any;
    onkeypress?: (event: KeyboardEvent) => any;
    onkeyup?: (event: KeyboardEvent) => any;
    onload?: (event: Event) => any;
    onmousedown?: (event: MouseEvent) => any;
    onmousemove?: (event: MouseEvent) => any;
    onmouseout?: (event: MouseEvent) => any;
    onmouseover?: (event: MouseEvent) => any;
    onmouseup?: (event: MouseEvent) => any;
    onresize?: (event: UIEvent) => any;
    onsubmit?: (event: SubmitEvent) => any;
    
    // Svelte event directives
    "on:blur"?: (event: FocusEvent) => any;
    "on:change"?: (event: Event) => any;
    "on:click"?: (event: MouseEvent) => any;
    "on:dblclick"?: (event: MouseEvent) => any;
    "on:focus"?: (event: FocusEvent) => any;
    "on:input"?: (event: InputEvent) => any;
    "on:keydown"?: (event: KeyboardEvent) => any;
    "on:keypress"?: (event: KeyboardEvent) => any;
    "on:keyup"?: (event: KeyboardEvent) => any;
    "on:load"?: (event: Event) => any;
    "on:mousedown"?: (event: MouseEvent) => any;
    "on:mousemove"?: (event: MouseEvent) => any;
    "on:mouseout"?: (event: MouseEvent) => any;
    "on:mouseover"?: (event: MouseEvent) => any;
    "on:mouseup"?: (event: MouseEvent) => any;
    "on:resize"?: (event: UIEvent) => any;
    "on:submit"?: (event: SubmitEvent) => any;
    
    // Svelte event modifiers
    "on:click|capture"?: (event: MouseEvent) => any;
    "on:click|once"?: (event: MouseEvent) => any;
    "on:click|passive"?: (event: MouseEvent) => any;
    "on:click|preventDefault"?: (event: MouseEvent) => any;
    "on:click|self"?: (event: MouseEvent) => any;
    "on:click|stopPropagation"?: (event: MouseEvent) => any;
    "on:keydown|capture"?: (event: KeyboardEvent) => any;
    "on:keydown|once"?: (event: KeyboardEvent) => any;
    "on:keydown|passive"?: (event: KeyboardEvent) => any;
    "on:keydown|preventDefault"?: (event: KeyboardEvent) => any;
    "on:keydown|self"?: (event: KeyboardEvent) => any;
    "on:keydown|stopPropagation"?: (event: KeyboardEvent) => any;
    
    // Svelte binding directives
    "bind:checked"?: boolean;
    "bind:clientHeight"?: number;
    "bind:clientWidth"?: number;
    "bind:group"?: any;
    "bind:offsetHeight"?: number;
    "bind:offsetWidth"?: number;
    "bind:this"?: any;
    "bind:value"?: any;
    
    // Svelte class directives
    "class:active"?: boolean;
    "class:disabled"?: boolean;
    "class:dragging"?: boolean;
    "class:hidden"?: boolean;
    "class:selected"?: boolean;
    "class:visible"?: boolean;
    
    // Svelte transition directives
    "in:fade"?: any;
    "in:fly"?: any;
    "in:slide"?: any;
    "out:fade"?: any;
    "out:fly"?: any;
    "out:slide"?: any;
    "transition:fade"?: any;
    "transition:fly"?: any;
    "transition:scale"?: any;
    "transition:slide"?: any;
    
    // Svelte action directives
    "use:action"?: any;
    
    // Svelte slot directives
    slot?: string;
    
    // Other Svelte directives
    "let:index"?: number;
    "let:item"?: any;
    
    // Custom events
    "on:letterLoaded"?: (event: CustomEvent<any>) => any;
  }
}
