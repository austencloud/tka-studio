<script lang="ts">
  import { onMount } from "svelte";

  let isVisible = $state(false);

  onMount(() => {
    isVisible = true;
  });

  // Resource categories
  const resourceCategories = [
    {
      title: "Educational Resources",
      icon: "📚",
      description: "Learning materials and documentation",
      links: [
        {
          title: "Level 1 PDF Book",
          description:
            "Comprehensive introduction to The Kinetic Alphabet methodology",
          url: "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link",
          type: "pdf",
        },
        {
          title: "Vulcan Tech Gospel",
          description: "Advanced technical concepts and methodologies",
          url: "/links/vulcan-tech-gospel",
          type: "internal",
        },
        {
          title: "Charlie Cushing's 9 Square Theory",
          description: "Foundational movement analysis framework",
          url: "/links/charlie-cushing-9-square-theory",
          type: "internal",
        },
      ],
    },
    {
      title: "Software Tools",
      icon: "🔧",
      description: "Digital tools for sequence creation and analysis",
      links: [
        {
          title: "Desktop Constructor v0.1.2",
          description:
            "Full-featured desktop application for sequence creation",
          url: "https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe",
          type: "download",
        },
        {
          title: "Web Constructor",
          description:
            "Browser-based sequence constructor with advanced features",
          url: "/constructor",
          type: "internal",
        },
        {
          title: "Sequence Animator",
          description: "View and animate existing sequences",
          url: "/animator",
          type: "internal",
        },
      ],
    },
    {
      title: "Community & Social",
      icon: "🤝",
      description: "Connect with the flow arts community",
      links: [
        {
          title: "Contact Us",
          description: "Get in touch with the TKA team",
          url: "/contact",
          type: "internal",
        },
        {
          title: "GitHub Repository",
          description: "Source code and development updates",
          url: "https://github.com/austencloud/tka-sequence-constructor",
          type: "external",
        },
        {
          title: "Email",
          description: "Direct communication with the development team",
          url: "mailto:tkaflowarts@gmail.com",
          type: "email",
        },
      ],
    },
    {
      title: "Flow Arts Resources",
      icon: "🌟",
      description: "External resources for flow artists",
      links: [
        {
          title: "Poi Spinning Community",
          description: "Global community for poi spinners and flow artists",
          url: "https://www.reddit.com/r/poi/",
          type: "external",
        },
        {
          title: "Flow Arts Institute",
          description: "Educational resources and workshops",
          url: "https://flowartsinstitute.com/",
          type: "external",
        },
        {
          title: "Spin More Poi",
          description: "Comprehensive poi spinning tutorials and community",
          url: "https://www.spinmorepoi.com/",
          type: "external",
        },
      ],
    },
  ];

  function getLinkIcon(type: string): string {
    switch (type) {
      case "pdf":
        return "📄";
      case "download":
        return "⬇️";
      case "internal":
        return "🔗";
      case "external":
        return "🌐";
      case "email":
        return "📧";
      default:
        return "🔗";
    }
  }

  function getLinkTarget(type: string): string {
    return type === "external" ||
      type === "download" ||
      type === "pdf" ||
      type === "email"
      ? "_blank"
      : "_self";
  }

  function handleLinkClick(url: string, type: string) {
    // Track link clicks for analytics if needed
    console.log(`🔗 Link clicked: ${url} (${type})`);
  }
</script>

<svelte:head>
  <title>Links & Resources - The Kinetic Alphabet</title>
  <meta
    name="description"
    content="Discover resources, tools, and community links for The Kinetic Alphabet and flow arts education."
  />
</svelte:head>

<main class="links-container">
  <!-- Hero Section -->
  <section class="hero" class:visible={isVisible}>
    <div class="hero-content">
      <h1 class="hero-title">Links & Resources</h1>
      <p class="hero-subtitle">
        Tools, documentation, and community connections
      </p>
    </div>
  </section>

  <!-- Resources Grid -->
  <section class="resources">
    <div class="container">
      {#each resourceCategories as category}
        <div class="resource-category">
          <div class="category-header">
            <div class="category-icon">{category.icon}</div>
            <div class="category-info">
              <h2 class="category-title">{category.title}</h2>
              <p class="category-description">{category.description}</p>
            </div>
          </div>

          <div class="links-grid">
            {#each category.links as link}
              <a
                href={link.url}
                target={getLinkTarget(link.type)}
                rel={link.type === "external" ||
                link.type === "download" ||
                link.type === "pdf"
                  ? "noopener noreferrer"
                  : ""}
                class="link-card"
                onclick={() => handleLinkClick(link.url, link.type)}
              >
                <div class="link-header">
                  <div class="link-icon">{getLinkIcon(link.type)}</div>
                  <h3 class="link-title">{link.title}</h3>
                </div>
                <p class="link-description">{link.description}</p>
                <div class="link-meta">
                  <span class="link-type">{link.type}</span>
                  {#if link.type === "external" || link.type === "download" || link.type === "pdf"}
                    <span class="external-indicator">↗</span>
                  {/if}
                </div>
              </a>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  </section>

  <!-- Quick Access Section -->
  <section class="quick-access">
    <div class="container">
      <h2>Quick Access</h2>
      <div class="quick-grid">
        <a href="/constructor" class="quick-link constructor">
          <div class="quick-icon">🔧</div>
          <div class="quick-content">
            <h3>Start Creating</h3>
            <p>Jump into the constructor</p>
          </div>
        </a>

        <a
          href="https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link"
          target="_blank"
          rel="noopener noreferrer"
          class="quick-link learn"
        >
          <div class="quick-icon">📚</div>
          <div class="quick-content">
            <h3>Learn the Basics</h3>
            <p>Download Level 1 PDF</p>
          </div>
        </a>

        <a href="/contact" class="quick-link connect">
          <div class="quick-icon">💬</div>
          <div class="quick-content">
            <h3>Get in Touch</h3>
            <p>Contact the team</p>
          </div>
        </a>
      </div>
    </div>
  </section>
</main>

<style>
  .links-container {
    min-height: 100vh;
    padding: 0;
  }

  /* Hero Section */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 30vh;
    display: flex;
    align-items: center;

    /* Glassmorphism styling */
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    margin: var(--spacing-lg);
  }

  .hero.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .hero-content {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
  }

  .hero-title {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    font-weight: 300;
  }

  /* Resources Section */
  .resources {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .resource-category {
    margin-bottom: var(--spacing-3xl);
  }

  .category-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .category-icon {
    font-size: 3rem;
    flex-shrink: 0;
  }

  .category-title {
    color: var(--text-color);
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 var(--spacing-sm) 0;
  }

  .category-description {
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    font-size: 1.1rem;
  }

  .links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
  }

  .link-card {
    display: block;
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .link-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-3px);
    box-shadow:
      0 12px 24px rgba(0, 0, 0, 0.15),
      0 4px 8px rgba(102, 126, 234, 0.1);
  }

  .link-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
  }

  .link-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .link-title {
    color: var(--text-color);
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0;
  }

  .link-description {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
    margin: 0 0 var(--spacing-md) 0;
  }

  .link-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: var(--font-size-sm);
  }

  .link-type {
    color: rgba(255, 255, 255, 0.6);
    text-transform: capitalize;
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
  }

  .external-indicator {
    color: #667eea;
    font-weight: bold;
  }

  /* Quick Access Section */
  .quick-access {
    padding: var(--spacing-3xl) 0;
    background: rgba(255, 255, 255, 0.02);
  }

  .quick-access h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
  }

  .quick-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    max-width: 900px;
    margin: 0 auto;
  }

  .quick-link {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
  }

  .quick-link:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }

  .quick-link.constructor:hover {
    border-color: rgba(102, 126, 234, 0.4);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
  }

  .quick-link.learn:hover {
    border-color: rgba(34, 197, 94, 0.4);
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.2);
  }

  .quick-link.connect:hover {
    border-color: rgba(249, 115, 22, 0.4);
    box-shadow: 0 8px 20px rgba(249, 115, 22, 0.2);
  }

  .quick-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .quick-content h3 {
    color: var(--text-color);
    font-weight: 600;
    margin: 0 0 4px 0;
  }

  .quick-content p {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    font-size: var(--font-size-sm);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-xl) 0;
      min-height: 25vh;
      margin: var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .resources,
    .quick-access {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .category-header {
      flex-direction: column;
      text-align: center;
      gap: var(--spacing-md);
    }

    .category-icon {
      font-size: 2.5rem;
    }

    .links-grid {
      grid-template-columns: 1fr;
    }

    .quick-grid {
      grid-template-columns: 1fr;
    }

    .quick-link {
      padding: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .hero {
      transition: none;
      opacity: 1;
      transform: none;
    }

    .link-card,
    .quick-link {
      transition: none;
    }

    .link-card:hover,
    .quick-link:hover {
      transform: none;
    }
  }
</style>
