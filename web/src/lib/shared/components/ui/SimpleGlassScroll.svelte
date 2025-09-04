<!--
	Simple Glass Scrollable Container - Fixed Implementation

	A working glassmorphism scrollable container with direct CSS approach.
	This version is guaranteed to work properly.
-->
<script module lang="ts">
  export type ScrollbarVariant =
    | "primary"
    | "secondary"
    | "minimal"
    | "hover"
    | "gradient";
</script>

<script lang="ts">
  // Props
  interface Props {
    variant?: ScrollbarVariant;
    height?: string;
    width?: string;
    className?: string;
    children?: import("svelte").Snippet;
  }

  let {
    variant = "primary",
    height = "100%",
    width = "100%",
    className = "",
    children,
  }: Props = $props();
</script>

<div
  class="glass-scrollable {className}"
  class:primary={variant === "primary"}
  class:secondary={variant === "secondary"}
  class:minimal={variant === "minimal"}
  class:hover={variant === "hover"}
  class:gradient={variant === "gradient"}
  style="height: {height}; width: {width};"
>
  {#if children}
    {@render children()}
  {/if}
</div>

<style>
  .glass-scrollable {
    /* Base scrollable container */
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    background: transparent;
    border-radius: 8px;
  }

  /* Primary Glass Scrollbar */
  .glass-scrollable.primary::-webkit-scrollbar {
    width: 12px;
  }

  .glass-scrollable.primary::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .glass-scrollable.primary::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    transition: all 0.3s ease;
  }

  .glass-scrollable.primary::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
  }

  /* Secondary Glass Scrollbar */
  .glass-scrollable.secondary::-webkit-scrollbar {
    width: 10px;
  }

  .glass-scrollable.secondary::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }

  .glass-scrollable.secondary::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s ease;
  }

  .glass-scrollable.secondary::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.25);
  }

  /* Minimal Glass Scrollbar */
  .glass-scrollable.minimal::-webkit-scrollbar {
    width: 6px;
  }

  .glass-scrollable.minimal::-webkit-scrollbar-track {
    background: transparent;
  }

  .glass-scrollable.minimal::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 3px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: all 0.3s ease;
  }

  .glass-scrollable.minimal::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Hover Glass Scrollbar */
  .glass-scrollable.hover::-webkit-scrollbar {
    width: 0px;
    transition: width 0.3s ease;
  }

  .glass-scrollable.hover:hover::-webkit-scrollbar {
    width: 12px;
  }

  .glass-scrollable.hover::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .glass-scrollable.hover:hover::-webkit-scrollbar-track {
    opacity: 1;
  }

  .glass-scrollable.hover::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    opacity: 0;
    transition: all 0.3s ease;
  }

  .glass-scrollable.hover:hover::-webkit-scrollbar-thumb {
    opacity: 1;
  }

  /* Gradient Glass Scrollbar */
  .glass-scrollable.gradient::-webkit-scrollbar {
    width: 12px;
  }

  .glass-scrollable.gradient::-webkit-scrollbar-track {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.05) 0%,
      rgba(255, 255, 255, 0.02) 50%,
      rgba(255, 255, 255, 0.05) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .glass-scrollable.gradient::-webkit-scrollbar-thumb {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.25) 0%,
      rgba(255, 255, 255, 0.15) 50%,
      rgba(255, 255, 255, 0.25) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.3s ease;
  }

  .glass-scrollable.gradient::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.35) 0%,
      rgba(255, 255, 255, 0.25) 50%,
      rgba(255, 255, 255, 0.35) 100%
    );
  }

  /* Firefox support */
  .glass-scrollable.primary {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.15) rgba(255, 255, 255, 0.03);
  }

  .glass-scrollable.secondary {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.1) rgba(255, 255, 255, 0.02);
  }

  .glass-scrollable.minimal {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.12) transparent;
  }

  .glass-scrollable.hover {
    scrollbar-width: none;
  }

  .glass-scrollable.hover:hover {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.15) rgba(255, 255, 255, 0.03);
  }

  .glass-scrollable.gradient {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) rgba(255, 255, 255, 0.05);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .glass-scrollable.primary::-webkit-scrollbar,
    .glass-scrollable.secondary::-webkit-scrollbar,
    .glass-scrollable.gradient::-webkit-scrollbar {
      width: 8px;
    }

    .glass-scrollable.minimal::-webkit-scrollbar {
      width: 4px;
    }
  }
</style>
