<script lang="ts">
  import { onMount } from 'svelte';

  export let title: string;
  export let subtitle: string;
  export let creator: string;
  export let category: string;
  export let level: string;
  export let description: string;
  export let keywords: string;
  export let url: string;
  export let resourceName: string;
  export let tableOfContents: Array<{id: string, label: string}> = [];
  export let relatedResources: Array<{name: string, url: string, description: string, type: 'internal' | 'external'}> = [];
  export let heroGradient: string = 'linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)';
  export let creatorColor: string = 'var(--primary-color)';

  let currentSection = '';

  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          currentSection = entry.target.id;
        }
      });
    }, { threshold: 0.6 });

    document.querySelectorAll('section[id]').forEach((section) => {
      observer.observe(section);
    });

    return () => observer.disconnect();
  });
</script>

<svelte:head>
  <title>{title} | The Kinetic Alphabet</title>
  <meta name="description" content={description} />
  <meta name="keywords" content={keywords} />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content="https://thekineticalphabet.com/links/{resourceName}" />

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:title" content={title} />
  <meta property="twitter:description" content={description} />

  <!-- Schema.org markup -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{description}",
    "author": {
      "@type": "Organization",
      "name": "The Kinetic Alphabet"
    },
    "publisher": {
      "@type": "Organization",
      "name": "The Kinetic Alphabet"
    },
    "datePublished": "2024-01-01",
    "dateModified": "2024-01-01",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": "https://thekineticalphabet.com/links/{resourceName}"
    },
    "about": {
      "@type": "Thing",
      "name": "{title}",
      "description": "{subtitle}"
    }
  }
  </script>
</svelte:head>

<article class="resource-guide">
  <!-- Breadcrumb Navigation -->
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/links">Links</a></li>
      <li aria-current="page">{title}</li>
    </ol>
  </nav>

  <!-- Hero Section -->
  <header class="hero" style="background: {heroGradient};">
    <div class="hero-content">
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <div class="hero-meta">
        <span class="creator" style="background: {creatorColor}1a; color: {creatorColor}; border-color: {creatorColor};">
          Created by <strong>{creator}</strong>
        </span>
        <span class="category">{category}</span>
        <span class="level">{level}</span>
      </div>
    </div>
  </header>

  <!-- Table of Contents -->
  {#if tableOfContents.length > 0}
    <nav class="table-of-contents">
      <h2>Contents</h2>
      <ul>
        {#each tableOfContents as item}
          <li>
            <a href="#{item.id}" class:active={currentSection === item.id}>
              {item.label}
            </a>
          </li>
        {/each}
      </ul>
    </nav>
  {/if}

  <!-- Main Content -->
  <div class="content">
    <slot />
  </div>

  <!-- Related Resources -->
  {#if relatedResources.length > 0}
    <aside class="related-resources">
      <h2>Related Resources</h2>
      <div class="related-grid">
        {#each relatedResources as resource}
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
</article>

<style>
  .resource-guide {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: var(--spacing-lg);
    line-height: 1.7;
  }

  /* Breadcrumb Navigation */
  .breadcrumb {
    margin-bottom: var(--spacing-xl);
  }

  .breadcrumb ol {
    display: flex;
    list-style: none;
    padding: 0;
    margin: 0;
    gap: var(--spacing-sm);
    align-items: center;
  }

  .breadcrumb li {
    display: flex;
    align-items: center;
  }

  .breadcrumb li:not(:last-child)::after {
    content: '→';
    margin-left: var(--spacing-sm);
    color: var(--text-secondary);
  }

  .breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color var(--transition-fast);
  }

  .breadcrumb a:hover {
    color: var(--secondary-color);
  }

  .breadcrumb li[aria-current="page"] {
    color: var(--text-secondary);
    font-weight: 500;
  }

  /* Hero Section */
  .hero {
    text-align: center;
    margin-bottom: var(--spacing-3xl);
    padding: var(--spacing-2xl) 0;
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--border-color);
  }

  .hero h1 {
    font-size: clamp(1.8rem, 4vw, 3rem);
    margin-bottom: var(--spacing-md);
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: var(--font-size-xl);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .hero-meta {
    display: flex;
    justify-content: center;
    gap: var(--spacing-lg);
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

  /* Table of Contents */
  .table-of-contents {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-2xl);
    position: sticky;
    top: var(--spacing-lg);
    z-index: 10;
  }

  .table-of-contents h2 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-lg);
    color: var(--primary-color);
  }

  .table-of-contents ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-sm);
  }

  .table-of-contents a {
    display: block;
    padding: var(--spacing-sm);
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: var(--border-radius);
    transition: all var(--transition-fast);
    border: 1px solid transparent;
  }

  .table-of-contents a:hover,
  .table-of-contents a.active {
    background: rgba(168, 28, 237, 0.1);
    color: var(--primary-color);
    border-color: var(--primary-color);
  }

  /* Content */
  .content {
    max-width: 800px;
  }

  /* Related Resources */
  .related-resources {
    margin-top: var(--spacing-3xl);
    padding-top: var(--spacing-2xl);
    border-top: 2px solid var(--border-color);
  }

  .related-resources h2 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-lg);
    text-align: center;
  }

  .related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-lg);
  }

  .related-card {
    display: block;
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    text-decoration: none;
    transition: all var(--transition-normal);
    position: relative;
  }

  .related-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
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
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-lg);
  }

  .related-card p {
    color: var(--text-secondary);
    margin: 0 0 var(--spacing-sm) 0;
    line-height: 1.6;
  }

  .link-type {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  /* Mobile Responsive Design */
  @media (max-width: 768px) {
    .resource-guide {
      padding: var(--spacing-md);
    }

    .hero {
      padding: var(--spacing-lg) var(--spacing-md);
    }

    .hero-meta {
      flex-direction: column;
      align-items: center;
      gap: var(--spacing-sm);
    }

    .table-of-contents {
      position: static;
      margin-bottom: var(--spacing-lg);
    }

    .table-of-contents ul {
      grid-template-columns: 1fr;
    }

    .related-grid {
      grid-template-columns: 1fr;
    }

    .breadcrumb ol {
      flex-wrap: wrap;
    }
  }

  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .related-card {
      transition: none;
    }

    .related-card:hover {
      transform: none;
    }
  }

  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .related-card {
      border: 2px solid var(--text-color);
    }

    .related-card:hover {
      border-color: var(--primary-color);
      border-width: 3px;
    }
  }
</style>
