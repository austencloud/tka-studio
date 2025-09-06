/// <reference types="svelte" />

// Try this format instead
declare namespace svelteHTML {
  interface HTMLAttributes {
    "on:swipemove"?: (e: CustomEvent) => void;
    "on:swipemove|stopPropagation"?: (e: CustomEvent) => void;
    "on:swipeend"?: (e: CustomEvent) => void;
    "on:swipeend|stopPropagation"?: (e: CustomEvent) => void;

    // Add standard event handlers
    "on:click"?: (e: MouseEvent) => void;
    "on:change"?: (e: Event) => void;
    "on:input"?: (e: InputEvent) => void;
    "on:focus"?: (e: FocusEvent) => void;
    "on:blur"?: (e: FocusEvent) => void;
    "on:keydown"?: (e: KeyboardEvent) => void;
    "on:keyup"?: (e: KeyboardEvent) => void;
    "on:mouseenter"?: (e: MouseEvent) => void;
    "on:mouseleave"?: (e: MouseEvent) => void;

    // Custom events for BeatFrame component
    "on:naturalheightchange"?: (e: CustomEvent<{ height: number }>) => void;
    "on:beatselected"?: (e: CustomEvent<{ beatId: string }>) => void;

    // Add class directives
    "class:loading"?: boolean;
  }
}
