<script lang="ts">
  interface Props {
    /** Title of the resource */
    title: string;
    /** Subtitle/description */
    subtitle: string;
    /** Creator name */
    creator: string;
    /** Creator color for the badge */
    creatorColor: string;
    /** Category of the resource */
    category: string;
    /** Difficulty level */
    level: string;
    /** Hero gradient background */
    heroGradient?: string;
  }

  let {
    title,
    subtitle,
    creator,
    creatorColor,
    category,
    level,
    heroGradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  }: Props = $props();
</script>

<header class="resource-header" style="background: {heroGradient}">
  <div class="header-content">
    <h1 id="modal-title" class="resource-title">{title}</h1>
    <p class="resource-subtitle">{subtitle}</p>
    <div class="resource-meta">
      <span class="creator-badge" style="color: {creatorColor}">{creator}</span>
      <span class="category-badge">{category}</span>
      <span class="level-badge">{level}</span>
    </div>
  </div>
</header>

<style>
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

  @media (max-width: 768px) {
    .resource-header {
      padding: var(--spacing-md);
    }

    .resource-title {
      font-size: 1.5rem;
    }
  }
</style>
