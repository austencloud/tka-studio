<script lang="ts">
  import { onMount } from "svelte";
  import type { TableOfContentsItem } from "./types";

  interface Props {
    /** Table of contents items */
    sections: TableOfContentsItem[];
    /** Callback when navigation link is clicked */
    onNavigate?: () => void;
  }

  let { sections, onNavigate }: Props = $props();

  // Track current active section
  let currentSection = $state("");

  // Set up IntersectionObserver to track visible sections
  onMount(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            currentSection = entry.target.id;
          }
        });
      },
      { threshold: 0.6 }
    );

    // Observe all section elements
    sections.forEach((section) => {
      const element = document.getElementById(section.id);
      if (element) {
        observer.observe(element);
      }
    });

    return () => observer.disconnect();
  });
</script>

{#if sections && sections.length > 0}
  <nav class="resource-nav" aria-label="Resource sections">
    <div class="nav-links">
      {#each sections as section}
        <a
          href="#{section.id}"
          class="nav-link"
          class:active={currentSection === section.id}
          onclick={() => onNavigate?.()}
        >
          {section.label}
        </a>
      {/each}
    </div>
  </nav>
{/if}

<style>
  .resource-nav {
    padding: var(--spacing-md) var(--spacing-xl);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
  }

  .nav-links {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .nav-link {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: var(--font-size-sm);
    font-weight: 500;
    transition: all 0.3s ease;
    border: 1px solid transparent;
  }

  .nav-link:hover,
  .nav-link.active {
    color: var(--primary-color);
    background: rgba(168, 28, 237, 0.1);
    border-color: rgba(168, 28, 237, 0.3);
  }

  @media (max-width: 768px) {
    .resource-nav {
      padding: var(--spacing-sm) var(--spacing-md);
    }

    .nav-links {
      justify-content: center;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .nav-link {
      transition: none;
    }
  }
</style>
