<!--
Resource Modal Component

Detailed modal view for resources with landing page content and additional information.
-->
<script lang="ts">
  import type { Resource } from './resourcesData';
  import { categories, levels } from './resourcesData';

  // Props
  const {
    resource,
    isOpen = false,
    onClose = () => {}
  } = $props<{
    resource: Resource | null;
    isOpen?: boolean;
    onClose?: () => void;
  }>();

  function handleOverlayClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      onClose();
    }
  }

  function getCategoryLabel(categoryValue: string): string {
    return categories.find(c => c.value === categoryValue)?.label || categoryValue;
  }

  function getLevelLabel(levelValue: string): string {
    return levels.find(l => l.value === levelValue)?.label || levelValue;
  }

  function getStatusIcon(status: string): string {
    switch (status) {
      case 'vendor': return '🏪';
      case 'historical': return '📚';
      default: return '✨';
    }
  }
</script>

{#if isOpen && resource}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div 
    class="modal-overlay" 
    onclick={handleOverlayClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    tabindex="-1"
  >
    <div class="modal-content">
      <header class="modal-header">
        <div class="modal-title-row">
          <h2 id="modal-title" class="modal-title">
            {resource.name}
            <span class="status-icon">{getStatusIcon(resource.status)}</span>
          </h2>
          <button 
            type="button" 
            class="close-btn" 
            onclick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        </div>
        
        <div class="modal-meta">
          <span class="category-badge category-{resource.category}">
            {getCategoryLabel(resource.category)}
          </span>
          <span class="level-badge level-{resource.level}">
            {getLevelLabel(resource.level)}
          </span>
          {#if resource.status === 'vendor' && resource.foundingYear}
            <span class="founding-badge">Est. {resource.foundingYear}</span>
          {/if}
        </div>
      </header>

      <div class="modal-body">
        <section class="description-section">
          <h3>Description</h3>
          <p>{resource.description}</p>
        </section>

        <section class="value-section">
          <h3>{resource.status === 'vendor' ? 'Why Shop Here' : 'Why It\'s Essential'}</h3>
          <p>{resource.value}</p>
        </section>

        {#if resource.status === 'vendor' && resource.specialties}
          <section class="specialties-section">
            <h3>Specialties</h3>
            <div class="specialty-tags">
              {#each resource.specialties as specialty}
                <span class="specialty-tag">{specialty}</span>
              {/each}
            </div>
          </section>
        {/if}

        {#if resource.hasLandingPage && resource.landingPageContent}
          <section class="landing-page-section">
            <h3>Detailed Information</h3>
            <div class="landing-page-content">
              {@html resource.landingPageContent}
            </div>
          </section>
        {/if}

        {#if resource.lastUpdated}
          <section class="metadata-section">
            <h3>Last Updated</h3>
            <p>{resource.lastUpdated}</p>
          </section>
        {/if}
      </div>

      <footer class="modal-footer">
        <a 
          href={resource.url} 
          target="_blank" 
          rel="noopener noreferrer"
          class="visit-btn primary"
        >
          Visit {resource.status === 'vendor' ? 'Store' : resource.status === 'historical' ? 'Archive' : 'Site'}
        </a>
        <button type="button" class="close-modal-btn" onclick={onClose}>
          Close
        </button>
      </footer>
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-content {
    background: var(--color-bg-primary);
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    max-width: 700px;
    max-height: 90vh;
    width: 100%;
    overflow: hidden;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from { 
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .modal-header {
    padding: var(--spacing-lg);
    border-bottom: 2px solid var(--color-border);
    background: var(--color-bg-secondary);
  }

  .modal-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: var(--spacing-md);
  }

  .modal-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    flex: 1;
  }

  .status-icon {
    font-size: var(--font-size-lg);
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 32px;
    cursor: pointer;
    color: var(--color-text-secondary);
    transition: color 0.2s ease;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-btn:hover {
    color: var(--color-text-primary);
  }

  .modal-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    align-items: center;
  }

  .category-badge,
  .level-badge {
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .category-badge {
    background: var(--color-accent-alpha);
    color: var(--color-accent);
  }

  .level-badge {
    background: var(--color-info-alpha);
    color: var(--color-info);
  }

  .founding-badge {
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
  }

  .modal-body {
    padding: var(--spacing-lg);
    max-height: 60vh;
    overflow-y: auto;
  }

  .modal-body section {
    margin-bottom: var(--spacing-lg);
  }

  .modal-body section:last-child {
    margin-bottom: 0;
  }

  .modal-body h3 {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-md);
    font-weight: 600;
    color: var(--color-text-primary);
  }

  .modal-body p {
    margin: 0;
    line-height: 1.6;
    color: var(--color-text-secondary);
  }

  .specialty-tags {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
  }

  .specialty-tag {
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    padding: 4px 8px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
  }

  .landing-page-content {
    background: var(--color-bg-secondary);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--color-accent);
  }

  .modal-footer {
    padding: var(--spacing-lg);
    border-top: 2px solid var(--color-border);
    background: var(--color-bg-secondary);
    display: flex;
    gap: var(--spacing-md);
    justify-content: flex-end;
  }

  .visit-btn,
  .close-modal-btn {
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--radius-md);
    font-weight: 600;
    text-decoration: none;
    text-align: center;
    transition: all 0.2s ease;
    font-size: var(--font-size-sm);
    cursor: pointer;
  }

  .visit-btn {
    background: var(--color-accent);
    color: white;
    border: 2px solid var(--color-accent);
  }

  .visit-btn:hover {
    background: var(--color-accent-dark);
    border-color: var(--color-accent-dark);
    transform: translateY(-1px);
  }

  .close-modal-btn {
    background: transparent;
    color: var(--color-text-secondary);
    border: 2px solid var(--color-border);
  }

  .close-modal-btn:hover {
    color: var(--color-text-primary);
    border-color: var(--color-text-secondary);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .modal-overlay {
      padding: var(--spacing-md);
    }

    .modal-content {
      max-height: 95vh;
    }

    .modal-header,
    .modal-body,
    .modal-footer {
      padding: var(--spacing-md);
    }

    .modal-title {
      font-size: var(--font-size-lg);
    }

    .modal-footer {
      flex-direction: column-reverse;
    }

    .visit-btn,
    .close-modal-btn {
      width: 100%;
    }
  }
</style>
