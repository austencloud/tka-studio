<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { modalState, modalData, modalActions, type ResourceModalData } from '$lib/stores/modalStore';
  import { focusTrap } from '$lib/utils/focusTrap';

  // Props that extend ResourceGuideLayout props
  export let isOpen = false;
  export let onClose: () => void = () => {};

  // Modal-specific props
  let modalContainer: HTMLElement;
  let modalContent: HTMLElement;
  let closeButton: HTMLElement;
  let previouslyFocusedElement: HTMLElement | null = null;
  let currentSection = '';

  // Reactive data from store
  $: data = $modalData;
  $: loading = $modalState.isLoading;

  // Handle body scroll lock
  function lockBodyScroll() {
    if (typeof document !== 'undefined') {
      document.body.style.overflow = 'hidden';
      document.body.style.paddingRight = getScrollbarWidth() + 'px';
    }
  }

  function unlockBodyScroll() {
    if (typeof document !== 'undefined') {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }
  }

  function getScrollbarWidth(): number {
    if (typeof window === 'undefined') return 0;
    return window.innerWidth - document.documentElement.clientWidth;
  }

  // Handle backdrop click
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === modalContainer) {
      handleClose();
    }
  }

  // Handle close
  function handleClose() {
    onClose();
    modalActions.closeModal();
  }

  // Handle escape key
  function handleEscape(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      handleClose();
    }
  }

  // Intersection observer for table of contents
  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          currentSection = entry.target.id;
        }
      });
    }, { threshold: 0.6 });

    return () => observer.disconnect();
  });

  // Watch for modal state changes
  $: if (isOpen) {
    lockBodyScroll();
    if (typeof document !== 'undefined') {
      previouslyFocusedElement = document.activeElement as HTMLElement;
    }
  } else {
    unlockBodyScroll();
  }

  onDestroy(() => {
    unlockBodyScroll();
  });
</script>

{#if isOpen}
  <!-- Modal Overlay -->
  <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
  <div
    class="modal-overlay"
    bind:this={modalContainer}
    on:click={handleBackdropClick}
    on:keydown={handleEscape}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    aria-describedby="modal-description"
    use:focusTrap={{
      initialFocus: closeButton,
      returnFocus: previouslyFocusedElement,
      escapeCallback: handleClose
    }}
  >
    <!-- Modal Container -->
    <div class="modal-container" bind:this={modalContent}>
      <!-- Close Button -->
      <button
        class="modal-close"
        bind:this={closeButton}
        on:click={handleClose}
        aria-label="Close modal"
        type="button"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      {#if loading}
        <!-- Loading State -->
        <div class="modal-loading">
          <div class="loading-spinner"></div>
          <p>Loading resource...</p>
        </div>
      {:else if data}
        <!-- Modal Content -->
        <article class="modal-resource-guide">
          <!-- Hero Section -->
          <header class="modal-hero" style="background: {data.heroGradient || 'linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)'};">
            <div class="hero-content">
              <h1 id="modal-title">{data.title}</h1>
              <p class="subtitle" id="modal-description">{data.subtitle}</p>
              <div class="hero-meta">
                <span class="creator" style="background: {data.creatorColor || 'var(--primary-color)'}1a; color: {data.creatorColor || 'var(--primary-color)'}; border-color: {data.creatorColor || 'var(--primary-color)'};">
                  Created by <strong>{data.creator}</strong>
                </span>
                <span class="category">{data.category}</span>
                <span class="level">{data.level}</span>
              </div>
            </div>
          </header>

          <!-- Table of Contents -->
          {#if data.tableOfContents && data.tableOfContents.length > 0}
            <nav class="modal-table-of-contents">
              <h2>Contents</h2>
              <ul>
                {#each data.tableOfContents as item}
                  <li>
                    <a href="#{item.id}" class:active={currentSection === item.id}>
                      {item.label}
                    </a>
                  </li>
                {/each}
              </ul>
            </nav>
          {/if}

          <!-- Main Content Slot -->
          <div class="modal-content">
            <slot />
          </div>

          <!-- Related Resources -->
          {#if data.relatedResources && data.relatedResources.length > 0}
            <aside class="modal-related-resources">
              <h2>Related Resources</h2>
              <div class="related-grid">
                {#each data.relatedResources as resource}
                  <a
                    href={resource.url}
                    class="related-card"
                    class:external={resource.type === 'external'}
                    target={resource.type === 'external' ? '_blank' : '_self'}
                    rel={resource.type === 'external' ? 'noopener noreferrer' : ''}
                  >
                    <h3>{resource.name}</h3>
                    <p>{resource.description}</p>
                    <span class="link-type">{resource.type === 'external' ? 'External Resource' : 'TKA Guide'}</span>
                  </a>
                {/each}
              </div>
            </aside>
          {/if}

          <!-- View Full Page Link -->
          <div class="modal-full-page-link">
            <a href="/links/{data.resourceName}" class="full-page-button">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              View Full Page
            </a>
          </div>
        </article>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Advanced Modal Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: var(--glass-backdrop-strong);
    -webkit-backdrop-filter: var(--glass-backdrop-strong);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    animation: modalFadeIn 300ms cubic-bezier(0.4, 0, 0.2, 1);

    /* Subtle cosmic gradient overlay */
    background-image: radial-gradient(
      circle at center,
      rgba(118, 75, 162, 0.1) 0%,
      rgba(0, 0, 0, 0.7) 70%
    );
  }

  @keyframes modalFadeIn {
    from {
      opacity: 0;
      backdrop-filter: blur(0px);
    }
    to {
      opacity: 1;
      backdrop-filter: blur(8px);
    }
  }

  /* Advanced Modal Container */
  .modal-container {
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    max-width: var(--container-max-width);
    max-height: 90vh;
    width: 100%;
    overflow-y: auto;
    position: relative;
    animation: modalSlideIn 300ms cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-glass-hover);

    /* Subtle cosmic gradient overlay */
    background-image: linear-gradient(135deg,
      rgba(30, 60, 114, 0.02) 0%,
      rgba(102, 126, 234, 0.02) 50%,
      rgba(240, 147, 251, 0.02) 100%);
  }

  /* Ultra-wide modal optimization */
  @media (min-width: 1600px) {
    .modal-container {
      max-width: var(--container-max-width-wide);
    }
  }

  @keyframes modalSlideIn {
    from {
      transform: translateY(20px) scale(0.95);
      opacity: 0;
    }
    to {
      transform: translateY(0) scale(1);
      opacity: 1;
    }
  }

  /* Advanced Close Button */
  .modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 10;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all var(--transition-normal);
    color: var(--text-secondary);
    box-shadow: var(--shadow-glass);
  }

  .modal-close:hover {
    background: var(--gradient-primary);
    color: var(--text-inverse);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transform: scale(1.1) rotate(90deg);
    box-shadow: var(--shadow-glass-colored);
  }

  .modal-close:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  /* Loading State */
  .modal-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-3xl);
    text-align: center;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-lg);
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Modal Resource Guide */
  .modal-resource-guide {
    padding: var(--spacing-lg);
    line-height: 1.7;
  }

  /* Modal Hero */
  .modal-hero {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    padding: var(--spacing-xl) var(--spacing-lg);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--border-color);
    margin-top: var(--spacing-xl); /* Account for close button */
  }

  .modal-hero h1 {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    margin-bottom: var(--spacing-md);
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
  }

  .hero-meta {
    display: flex;
    justify-content: center;
    gap: var(--spacing-md);
    flex-wrap: wrap;
    font-size: var(--font-size-sm);
  }

  .hero-meta span {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    color: var(--text-secondary);
  }

  /* Modal Table of Contents */
  .modal-table-of-contents {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
  }

  .modal-table-of-contents h2 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-lg);
    color: var(--primary-color);
  }

  .modal-table-of-contents ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--spacing-sm);
  }

  .modal-table-of-contents a {
    display: block;
    padding: var(--spacing-sm);
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: var(--border-radius);
    transition: all var(--transition-fast);
    border: 1px solid transparent;
  }

  .modal-table-of-contents a:hover,
  .modal-table-of-contents a.active {
    background: rgba(168, 28, 237, 0.1);
    color: var(--primary-color);
    border-color: var(--primary-color);
  }

  /* Modal Content */
  .modal-content {
    max-width: 700px;
    margin: 0 auto;
  }

  /* Ultra-wide modal content optimization */
  @media (min-width: 1600px) {
    .modal-content {
      max-width: 900px;
    }
  }

  /* Modal Related Resources */
  .modal-related-resources {
    margin-top: var(--spacing-2xl);
    padding-top: var(--spacing-xl);
    border-top: 2px solid var(--border-color);
  }

  .modal-related-resources h2 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-lg);
    text-align: center;
  }

  .related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-md);
  }

  .related-card {
    display: block;
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-md);
    text-decoration: none;
    transition: all var(--transition-normal);
    position: relative;
  }

  .related-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-color);
  }

  .related-card.external::after {
    content: '↗';
    position: absolute;
    top: var(--spacing-sm);
    right: var(--spacing-sm);
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
  }

  .related-card h3 {
    color: var(--primary-color);
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-md);
  }

  .related-card p {
    color: var(--text-secondary);
    margin: 0 0 var(--spacing-xs) 0;
    line-height: 1.5;
    font-size: var(--font-size-sm);
  }

  .link-type {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  /* Full Page Link */
  .modal-full-page-link {
    margin-top: var(--spacing-xl);
    padding-top: var(--spacing-lg);
    border-top: 1px solid var(--border-color);
    text-align: center;
  }

  .full-page-button {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: var(--surface-color);
    color: var(--primary-color);
    text-decoration: none;
    border: 2px solid var(--primary-color);
    border-radius: var(--border-radius);
    font-weight: 500;
    transition: all var(--transition-fast);
  }

  .full-page-button:hover {
    background: var(--primary-color);
    color: white;
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .modal-overlay {
      padding: 0;
      align-items: stretch;
    }

    .modal-container {
      max-height: 100vh;
      border-radius: 0;
      border: none;
    }

    .modal-resource-guide {
      padding: var(--spacing-md);
    }

    .modal-hero {
      margin-top: var(--spacing-2xl);
      padding: var(--spacing-lg) var(--spacing-md);
    }

    .hero-meta {
      flex-direction: column;
      align-items: center;
      gap: var(--spacing-sm);
    }

    .modal-table-of-contents ul {
      grid-template-columns: 1fr;
    }

    .related-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .modal-overlay,
    .modal-container,
    .modal-close,
    .related-card,
    .full-page-button {
      animation: none;
      transition: none;
    }

    .related-card:hover,
    .full-page-button:hover {
      transform: none;
    }
  }

  /* High Contrast Mode */
  @media (prefers-contrast: high) {
    .modal-container {
      border: 3px solid var(--text-color);
    }

    .modal-close {
      border: 2px solid var(--text-color);
    }

    .related-card {
      border: 2px solid var(--text-color);
    }

    .full-page-button {
      border-width: 3px;
    }
  }
</style>
