<script lang="ts">
  import { onMount } from "svelte";
  import type { ResourceModalData } from "./types";

  interface Props {
    isOpen?: boolean;
    onClose?: () => void;
    modalData?: ResourceModalData | null;
    children?: any;
  }

  let {
    isOpen = false,
    onClose = () => {},
    modalData = null,
    children,
  }: Props = $props();

  // DOM element references - used in reactive contexts so need $state
  let modalContainer: HTMLElement | undefined = $state();
  let modalContent: HTMLElement | undefined = $state();
  let closeButton: HTMLElement | undefined = $state();

  // Reactive state
  let previouslyFocusedElement: HTMLElement | null = null;
  let currentSection = $state("");

  // Derived data from props
  const data = $derived(modalData);
  const loading = $derived(false); // No loading state needed for now

  // Handle body scroll lock
  function lockBodyScroll() {
    if (typeof document !== "undefined") {
      document.body.style.overflow = "hidden";
      document.body.style.paddingRight = getScrollbarWidth() + "px";
    }
  }

  function unlockBodyScroll() {
    if (typeof document !== "undefined") {
      document.body.style.overflow = "";
      document.body.style.paddingRight = "";
    }
  }

  function getScrollbarWidth(): number {
    if (typeof window === "undefined") return 0;
    return window.innerWidth - document.documentElement.clientWidth;
  }

  // Handle close
  function handleClose() {
    onClose();
  }

  // Handle backdrop click
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === modalContainer) {
      handleClose();
    }
  }

  // Handle escape key and focus trap
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      handleClose();
    } else if (event.key === "Tab") {
      // Focus trap implementation
      if (!modalContent) return;

      const focusableElements = modalContent.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (!focusableElements?.length) return;

      const firstElement = focusableElements[0] as HTMLElement;
      const lastElement = focusableElements[
        focusableElements.length - 1
      ] as HTMLElement;

      if (event.shiftKey) {
        if (document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    }
  }

  // Handle modal state changes with $effect
  $effect(() => {
    if (isOpen) {
      lockBodyScroll();
      if (typeof document !== "undefined") {
        previouslyFocusedElement = document.activeElement as HTMLElement;
        // Focus the close button after a brief delay
        setTimeout(() => {
          if (closeButton) {
            closeButton.focus();
          }
        }, 100);
      }
    } else {
      unlockBodyScroll();
      if (previouslyFocusedElement) {
        previouslyFocusedElement.focus();
      }
    }

    // Cleanup function
    return () => {
      if (!isOpen) {
        unlockBodyScroll();
      }
    };
  });

  // Intersection observer for table of contents
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

    return () => observer.disconnect();
  });
</script>

{#if isOpen}
  <!-- Modal Overlay -->
  <div
    class="modal-overlay"
    bind:this={modalContainer}
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    aria-describedby="modal-description"
    tabindex="-1"
  >
    <!-- Modal Container -->
    <div class="modal-container" bind:this={modalContent}>
      <!-- Close Button -->
      <button
        class="modal-close"
        bind:this={closeButton}
        onclick={handleClose}
        aria-label="Close modal"
        type="button"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M18 6L6 18M6 6L18 18"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>

      {#if loading}
        <!-- Loading State -->
        <div class="modal-loading">
          <div class="loading-spinner"></div>
          <p>Loading resource...</p>
        </div>
      {:else if data}
        <!-- Resource Content -->
        <div class="resource-content">
          <!-- Header -->
          <header
            class="resource-header"
            style="background: {data.heroGradient}"
          >
            <div class="header-content">
              <h1 id="modal-title" class="resource-title">{data.title}</h1>
              <p class="resource-subtitle">{data.subtitle}</p>
              <div class="resource-meta">
                <span class="creator-badge" style="color: {data.creatorColor}"
                  >{data.creator}</span
                >
                <span class="category-badge">{data.category}</span>
                <span class="level-badge">{data.level}</span>
              </div>
            </div>
          </header>

          <!-- Navigation -->
          {#if data.tableOfContents && data.tableOfContents.length > 0}
            <nav class="resource-nav" aria-label="Resource sections">
              <div class="nav-links">
                {#each data.tableOfContents as section}
                  <a
                    href="#{section.id}"
                    class="nav-link"
                    class:active={currentSection === section.id}
                  >
                    {section.label}
                  </a>
                {/each}
              </div>
            </nav>
          {/if}

          <!-- Main Content -->
          <main class="resource-main" id="modal-description">
            <!-- Content will be provided by children slot -->
            {@render children?.()}
          </main>

          <!-- Related Resources -->
          {#if data.relatedResources && data.relatedResources.length > 0}
            <aside class="related-resources">
              <h3>Related Resources</h3>
              <div class="related-links">
                {#each data.relatedResources as related}
                  <a
                    href={related.url}
                    class="related-link"
                    class:internal={related.type === "internal"}
                    target={related.type === "external" ? "_blank" : "_self"}
                    rel={related.type === "external"
                      ? "noopener noreferrer"
                      : ""}
                  >
                    <span class="related-name">{related.name}</span>
                    <span class="related-description"
                      >{related.description}</span
                    >
                  </a>
                {/each}
              </div>
            </aside>
          {/if}

          <!-- Footer -->
          <footer class="resource-footer">
            <a
              href={data.url}
              target="_blank"
              rel="noopener noreferrer"
              class="visit-original"
            >
              Visit Original Resource →
            </a>
          </footer>
        </div>
      {:else}
        <!-- No Data State -->
        <div class="modal-error">
          <h2>Resource Not Found</h2>
          <p>The requested resource could not be loaded.</p>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Modal Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: var(--spacing-lg);
    animation: fadeIn 0.3s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Modal Container */
  .modal-container {
    background: var(--surface-color);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    max-width: 900px;
    max-height: 90vh;
    width: 100%;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.3s ease-out;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-50px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  /* Close Button */
  .modal-close {
    position: absolute;
    top: var(--spacing-md);
    right: var(--spacing-md);
    z-index: 10;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: scale(1.1);
  }

  /* Loading State */
  .modal-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-3xl);
    gap: var(--spacing-lg);
    color: var(--text-color);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Resource Content */
  .resource-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-height: 90vh;
  }

  /* Header */
  .resource-header {
    padding: var(--spacing-xl);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .header-content {
    max-width: 800px;
  }

  .resource-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-sm);
    line-height: 1.2;
  }

  .resource-subtitle {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-md);
    line-height: 1.4;
  }

  .resource-meta {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .creator-badge,
  .category-badge,
  .level-badge {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .creator-badge {
    background: rgba(168, 28, 237, 0.2);
    border: 1px solid rgba(168, 28, 237, 0.3);
  }

  .category-badge {
    background: rgba(74, 144, 226, 0.2);
    color: #4a90e2;
    border: 1px solid rgba(74, 144, 226, 0.3);
  }

  .level-badge {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  /* Navigation */
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

  /* Main Content */
  .resource-main {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-xl);
  }

  /* Related Resources */
  .related-resources {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-xl);
    background: rgba(255, 255, 255, 0.02);
  }

  .related-resources h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  .related-links {
    display: grid;
    gap: var(--spacing-sm);
  }

  .related-link {
    display: flex;
    flex-direction: column;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    text-decoration: none;
    transition: all 0.3s ease;
  }

  .related-link:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--primary-color);
    transform: translateY(-2px);
  }

  .related-name {
    color: var(--primary-color);
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
  }

  .related-description {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    line-height: 1.4;
  }

  /* Footer */
  .resource-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-lg) var(--spacing-xl);
    display: flex;
    justify-content: center;
  }

  .visit-original {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: var(--border-radius-lg);
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .visit-original:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  /* Error State */
  .modal-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-3xl);
    text-align: center;
    color: var(--text-color);
  }

  .modal-error h2 {
    margin-bottom: var(--spacing-md);
    color: var(--text-color);
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .modal-overlay {
      padding: var(--spacing-md);
    }

    .modal-container {
      max-height: 95vh;
    }

    .resource-header,
    .resource-main,
    .related-resources,
    .resource-footer {
      padding: var(--spacing-md);
    }

    .resource-nav {
      padding: var(--spacing-sm) var(--spacing-md);
    }

    .resource-title {
      font-size: 1.5rem;
    }

    .nav-links {
      justify-content: center;
    }

    .related-links {
      grid-template-columns: 1fr;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .modal-overlay,
    .modal-container,
    .nav-link,
    .related-link,
    .visit-original,
    .modal-close {
      animation: none;
      transition: none;
    }

    .related-link:hover,
    .visit-original:hover,
    .modal-close:hover {
      transform: none;
    }

    .loading-spinner {
      animation: none;
    }
  }
</style>
