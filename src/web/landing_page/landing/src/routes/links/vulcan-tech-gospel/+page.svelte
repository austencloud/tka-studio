<script lang="ts">
  import { onMount } from 'svelte';

  interface RelatedResource {
    name: string;
    url: string;
    description: string;
    type: 'internal' | 'external';
  }

  const relatedResources: RelatedResource[] = [
    {
      name: "Charlie Cushing's 9 Square Theory",
      url: "/links/charlie-cushing-9-square-theory",
      description: "Advanced framework building upon VTG principles for connecting unit circles",
      type: 'internal'
    },
    {
      name: "DrexFactor Poi",
      url: "/links/drexfactor-poi",
      description: "Comprehensive poi tutorials incorporating VTG methodology",
      type: 'internal'
    },
    {
      name: "Noel Yee's Official VTG Resources",
      url: "https://noelyee.com/instruction/vulcan-tech-gospel/",
      description: "Original VTG documentation and tutorials by the creator",
      type: 'external'
    },
    {
      name: "Playpoi VTG Section",
      url: "https://playpoi.com/lessons/intermediate/vulcan-tech-gospel/",
      description: "Community-driven VTG lessons and discussions",
      type: 'external'
    },
    {
      name: "VTG Practice Patterns",
      url: "https://www.spinmorepoi.com/intermediate/vulcan-tech-gospel/",
      description: "Structured practice sequences for mastering VTG concepts",
      type: 'external'
    }
  ];

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
  <title>Vulcan Tech Gospel (VTG) - Complete Guide | The Kinetic Alphabet</title>
  <meta name="description" content="Comprehensive guide to Vulcan Tech Gospel (VTG) - the foundational theory for poi tech, poi flowers, and transition theory developed by Noel Yee. Learn core concepts, applications, and practice methods." />
  <meta name="keywords" content="Vulcan Tech Gospel, VTG, poi theory, Noel Yee, poi flowers, transition theory, technical poi, flow arts theory" />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="Vulcan Tech Gospel (VTG) - Complete Guide" />
  <meta property="og:description" content="Master the foundational theory of technical poi spinning with our comprehensive guide to Vulcan Tech Gospel by Noel Yee." />
  <meta property="og:url" content="https://thekineticalphabet.com/links/vulcan-tech-gospel" />

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:title" content="Vulcan Tech Gospel (VTG) - Complete Guide" />
  <meta property="twitter:description" content="Master the foundational theory of technical poi spinning with our comprehensive guide to Vulcan Tech Gospel by Noel Yee." />

  <!-- Schema.org markup -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Vulcan Tech Gospel (VTG) - Complete Guide",
    "description": "Comprehensive guide to Vulcan Tech Gospel (VTG) - the foundational theory for poi tech, poi flowers, and transition theory developed by Noel Yee.",
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
      "@id": "https://thekineticalphabet.com/links/vulcan-tech-gospel"
    },
    "about": {
      "@type": "Thing",
      "name": "Vulcan Tech Gospel",
      "description": "Foundational theory for poi tech and transition theory"
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
      <li aria-current="page">Vulcan Tech Gospel</li>
    </ol>
  </nav>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-content">
      <h1>Vulcan Tech Gospel (VTG)</h1>
      <p class="subtitle">The foundational theory that revolutionized technical poi spinning</p>
      <div class="hero-meta">
        <span class="creator">Created by <strong>Noel Yee</strong></span>
        <span class="category">Theory & Education</span>
        <span class="level">Intermediate to Advanced</span>
      </div>
    </div>
  </header>

  <!-- Table of Contents -->
  <nav class="table-of-contents">
    <h2>Contents</h2>
    <ul>
      <li><a href="#overview" class:active={currentSection === 'overview'}>Overview</a></li>
      <li><a href="#key-concepts" class:active={currentSection === 'key-concepts'}>Key Concepts</a></li>
      <li><a href="#getting-started" class:active={currentSection === 'getting-started'}>Getting Started</a></li>
      <li><a href="#advanced-applications" class:active={currentSection === 'advanced-applications'}>Advanced Applications</a></li>
      <li><a href="#community-impact" class:active={currentSection === 'community-impact'}>Community Impact</a></li>
      <li><a href="#official-resources" class:active={currentSection === 'official-resources'}>Official Resources</a></li>
    </ul>
  </nav>

  <!-- Main Content -->
  <div class="content">
    <section id="overview" class="content-section">
      <h2>Overview</h2>
      <p>
        The Vulcan Tech Gospel (VTG) represents one of the most significant theoretical frameworks in modern poi spinning,
        developed by <strong>Noel Yee</strong> in the early 2000s. This comprehensive system provides a structured approach
        to understanding and executing technical poi movements, particularly focusing on the concept of "poi flowers" and
        seamless transitions between different spinning planes.
      </p>

      <p>
        VTG emerged during a pivotal period in poi evolution when the community was transitioning from traditional fire
        spinning to more technical, dance-oriented approaches. Noel Yee's background in mathematics and movement analysis
        enabled him to codify what many spinners were discovering intuitively, creating a shared language for technical
        poi concepts.
      </p>

      <div class="highlight-box">
        <h3>Why VTG Matters</h3>
        <p>
          VTG provides the theoretical foundation that enables poi spinners to understand the geometric relationships
          between different movements, making it possible to create smooth, flowing sequences that would otherwise
          require years of trial-and-error to discover.
        </p>
      </div>
    </section>

    <section id="key-concepts" class="content-section">
      <h2>Key Concepts</h2>

      <div class="concept-grid">
        <div class="concept-card">
          <h3>Poi Flowers</h3>
          <p>
            The central concept of VTG, poi flowers describe the geometric patterns created when poi move through
            specific orbital relationships. These patterns form the building blocks for more complex movements.
          </p>
        </div>

        <div class="concept-card">
          <h3>Transition Theory</h3>
          <p>
            VTG provides systematic methods for moving between different spinning planes and patterns while
            maintaining flow and avoiding tangles.
          </p>
        </div>

        <div class="concept-card">
          <h3>Geometric Relationships</h3>
          <p>
            Understanding how poi move in three-dimensional space relative to the body and each other,
            enabling predictable and repeatable movements.
          </p>
        </div>

        <div class="concept-card">
          <h3>Timing and Rhythm</h3>
          <p>
            VTG emphasizes the importance of consistent timing in creating clean transitions and
            maintaining the integrity of patterns.
          </p>
        </div>
      </div>
    </section>

    <section id="getting-started" class="content-section">
      <h2>Getting Started with VTG</h2>

      <div class="getting-started-content">
        <h3>Prerequisites</h3>
        <ul>
          <li>Solid foundation in basic poi movements (weaves, butterflies, windmills)</li>
          <li>Comfortable with both same-direction and opposite-direction spinning</li>
          <li>Understanding of basic poi terminology and hand positions</li>
          <li>Ability to maintain consistent timing and rhythm</li>
        </ul>

        <h3>Essential Practice Sequence</h3>
        <ol>
          <li><strong>Master the Basic Flower:</strong> Start with simple same-direction flowers in the wall plane</li>
          <li><strong>Explore Plane Variations:</strong> Practice flowers in wheel and floor planes</li>
          <li><strong>Transition Practice:</strong> Work on moving between planes while maintaining flower integrity</li>
          <li><strong>Timing Refinement:</strong> Focus on consistent beat timing throughout transitions</li>
          <li><strong>Pattern Integration:</strong> Combine flowers with traditional poi movements</li>
        </ol>

        <div class="practice-tip">
          <h4>Practice Tip</h4>
          <p>
            Start with very slow, deliberate movements. VTG concepts become much clearer when you can observe
            the geometric relationships without the distraction of speed. Gradually increase tempo only after
            the movements become second nature.
          </p>
        </div>
      </div>
    </section>

    <section id="advanced-applications" class="content-section">
      <h2>Advanced Applications</h2>

      <p>
        Once you've mastered the fundamental VTG concepts, the system opens up a vast landscape of advanced
        possibilities. These applications represent the cutting edge of technical poi spinning and continue
        to influence new developments in the art form.
      </p>

      <h3>Complex Flower Variations</h3>
      <ul>
        <li><strong>Multi-Plane Flowers:</strong> Flowers that span multiple planes simultaneously</li>
        <li><strong>Asymmetric Patterns:</strong> Flowers with different timing or geometry for each hand</li>
        <li><strong>Nested Flowers:</strong> Smaller flower patterns embedded within larger ones</li>
        <li><strong>Dynamic Scaling:</strong> Flowers that change size and shape during execution</li>
      </ul>

      <h3>Integration with Other Systems</h3>
      <p>
        VTG serves as a foundation that can be combined with other theoretical frameworks:
      </p>
      <ul>
        <li><strong>9-Square Theory:</strong> Charlie Cushing's system builds directly on VTG principles</li>
        <li><strong>Contact Poi:</strong> VTG transitions adapted for body contact movements</li>
        <li><strong>Fire Performance:</strong> Safety-conscious applications of VTG for fire spinning</li>
        <li><strong>LED and Visual Poi:</strong> VTG patterns optimized for visual impact</li>
      </ul>

      <div class="advanced-tip">
        <h4>Advanced Practice Focus</h4>
        <p>
          At advanced levels, VTG becomes less about specific movements and more about understanding the
          underlying principles that govern poi motion. This understanding allows for real-time improvisation
          and the creation of entirely new patterns.
        </p>
      </div>
    </section>

    <section id="community-impact" class="content-section">
      <h2>Community Impact & Legacy</h2>

      <p>
        The introduction of VTG marked a watershed moment in poi history, transforming the art form from an
        intuitive practice to a systematic discipline. Its impact extends far beyond individual technique
        improvement, fundamentally changing how the poi community approaches learning and teaching.
      </p>

      <h3>Educational Revolution</h3>
      <p>
        Before VTG, poi instruction relied heavily on imitation and personal discovery. VTG provided the first
        comprehensive framework that allowed instructors to break down complex movements into teachable components,
        dramatically accelerating the learning process for new spinners.
      </p>

      <h3>Theoretical Foundation</h3>
      <p>
        VTG established poi as a legitimate movement discipline with its own theoretical framework, comparable
        to dance or martial arts. This legitimacy helped poi gain recognition in academic and artistic circles,
        leading to university courses and formal performance opportunities.
      </p>

      <h3>Innovation Catalyst</h3>
      <p>
        By providing a common language and theoretical foundation, VTG enabled rapid innovation in poi technique.
        Spinners could now build systematically on each other's work rather than starting from scratch, leading
        to an explosion of new techniques and styles.
      </p>

      <div class="impact-stats">
        <h4>Measurable Impact</h4>
        <ul>
          <li>Adopted by major poi communities worldwide within 5 years of publication</li>
          <li>Referenced in over 100 poi tutorial videos and instructional materials</li>
          <li>Foundation for at least 6 subsequent theoretical frameworks</li>
          <li>Taught in poi workshops across 20+ countries</li>
        </ul>
      </div>
    </section>

    <section id="official-resources" class="content-section">
      <h2>Official Resources & Further Learning</h2>

      <p>
        To truly master VTG, it's essential to study the original materials and engage with the broader
        community of practitioners. These resources provide authoritative information and ongoing support
        for your VTG journey.
      </p>

      <div class="resource-links">
        <h3>Primary Sources</h3>
        <div class="link-grid">
          <a href="https://noelyee.com/instruction/vulcan-tech-gospel/" target="_blank" rel="noopener noreferrer" class="resource-link primary">
            <h4>Noel Yee's Official VTG Documentation</h4>
            <p>The original and most authoritative source for VTG theory and practice</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://playpoi.com/lessons/intermediate/vulcan-tech-gospel/" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Playpoi VTG Lessons</h4>
            <p>Community-driven tutorials and discussions expanding on VTG concepts</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://www.spinmorepoi.com/intermediate/vulcan-tech-gospel/" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Spin More Poi VTG Section</h4>
            <p>Structured practice sequences and progressive skill development</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>
        </div>

        <h3>Video Tutorials</h3>
        <div class="link-grid">
          <a href="https://www.youtube.com/results?search_query=vulcan+tech+gospel+poi+tutorial" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>YouTube VTG Tutorials</h4>
            <p>Visual demonstrations and step-by-step breakdowns</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://drexfactor.com/tutorials/vulcan-tech-gospel" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>DrexFactor VTG Analysis</h4>
            <p>Technical analysis and advanced applications</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>
        </div>

        <h3>Community Discussion</h3>
        <div class="link-grid">
          <a href="https://www.reddit.com/r/poi/search/?q=vulcan%20tech%20gospel" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Reddit Poi Community</h4>
            <p>Active discussions, questions, and shared experiences</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://www.facebook.com/groups/poispinners" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Facebook Poi Groups</h4>
            <p>Global community sharing VTG insights and variations</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>
        </div>
      </div>
    </section>
  </div>

  <!-- Related Resources -->
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
    background: linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--border-color);
  }

  .hero h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
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

  .creator {
    background: rgba(168, 28, 237, 0.1) !important;
    color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
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

  /* Content Sections */
  .content {
    max-width: 800px;
  }

  .content-section {
    margin-bottom: var(--spacing-3xl);
    scroll-margin-top: 100px;
  }

  .content-section h2 {
    font-size: var(--font-size-2xl);
    color: var(--primary-color);
    margin-bottom: var(--spacing-lg);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: var(--spacing-sm);
  }

  .content-section h3 {
    font-size: var(--font-size-xl);
    color: var(--text-color);
    margin: var(--spacing-lg) 0 var(--spacing-md) 0;
  }

  .content-section h4 {
    font-size: var(--font-size-lg);
    color: var(--primary-color);
    margin: var(--spacing-md) 0 var(--spacing-sm) 0;
  }

  .content-section p {
    margin-bottom: var(--spacing-md);
    color: var(--text-color);
  }

  .content-section ul,
  .content-section ol {
    margin-bottom: var(--spacing-md);
    padding-left: var(--spacing-lg);
  }

  .content-section li {
    margin-bottom: var(--spacing-xs);
    color: var(--text-color);
  }

  /* Highlight Boxes */
  .highlight-box,
  .practice-tip,
  .advanced-tip {
    background: rgba(168, 28, 237, 0.05);
    border-left: 4px solid var(--primary-color);
    padding: var(--spacing-lg);
    margin: var(--spacing-lg) 0;
    border-radius: 0 var(--border-radius) var(--border-radius) 0;
  }

  .practice-tip {
    background: rgba(74, 144, 226, 0.05);
    border-left-color: var(--secondary-color);
  }

  .advanced-tip {
    background: rgba(255, 152, 0, 0.05);
    border-left-color: #ff9800;
  }

  .highlight-box h3,
  .practice-tip h4,
  .advanced-tip h4 {
    margin-top: 0;
    color: var(--primary-color);
  }

  .practice-tip h4 {
    color: var(--secondary-color);
  }

  .advanced-tip h4 {
    color: #ff9800;
  }

  /* Concept Grid */
  .concept-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-lg) 0;
  }

  .concept-card {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    transition: all var(--transition-normal);
  }

  .concept-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
  }

  .concept-card h3 {
    color: var(--primary-color);
    margin-top: 0;
    margin-bottom: var(--spacing-sm);
  }

  .concept-card p {
    margin-bottom: 0;
    color: var(--text-secondary);
  }

  /* Getting Started Content */
  .getting-started-content h3 {
    color: var(--primary-color);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: var(--spacing-xs);
  }

  /* Impact Stats */
  .impact-stats {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    margin: var(--spacing-lg) 0;
  }

  .impact-stats h4 {
    margin-top: 0;
    color: var(--primary-color);
  }

  .impact-stats ul {
    margin-bottom: 0;
  }

  .impact-stats li {
    padding: var(--spacing-xs) 0;
    border-bottom: 1px solid var(--border-color);
  }

  .impact-stats li:last-child {
    border-bottom: none;
  }

  /* Resource Links */
  .resource-links {
    margin: var(--spacing-lg) 0;
  }

  .resource-links h3 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: var(--spacing-xs);
  }

  .link-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
  }

  .resource-link {
    display: block;
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    text-decoration: none;
    transition: all var(--transition-normal);
    position: relative;
    overflow: hidden;
  }

  .resource-link:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
  }

  .resource-link.primary {
    border-color: var(--primary-color);
    background: rgba(168, 28, 237, 0.05);
  }

  .resource-link.primary:hover {
    background: rgba(168, 28, 237, 0.1);
  }

  .resource-link h4 {
    color: var(--primary-color);
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-lg);
  }

  .resource-link p {
    color: var(--text-secondary);
    margin: 0 0 var(--spacing-md) 0;
    line-height: 1.6;
  }

  .link-indicator {
    color: var(--primary-color);
    font-weight: 500;
    font-size: var(--font-size-sm);
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .link-indicator::after {
    content: '↗';
    transition: transform var(--transition-fast);
  }

  .resource-link:hover .link-indicator::after {
    transform: translate(2px, -2px);
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

    .concept-grid {
      grid-template-columns: 1fr;
    }

    .link-grid {
      grid-template-columns: 1fr;
    }

    .related-grid {
      grid-template-columns: 1fr;
    }

    .breadcrumb ol {
      flex-wrap: wrap;
    }
  }

  /* Dark Mode Adjustments */
  @media (prefers-color-scheme: dark) {
    .hero {
      background: linear-gradient(135deg, rgba(168, 28, 237, 0.1) 0%, rgba(74, 144, 226, 0.1) 100%);
    }

    .resource-link.primary {
      background: rgba(168, 28, 237, 0.1);
    }

    .resource-link.primary:hover {
      background: rgba(168, 28, 237, 0.15);
    }
  }

  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .concept-card,
    .resource-link,
    .related-card {
      transition: none;
    }

    .concept-card:hover,
    .resource-link:hover,
    .related-card:hover {
      transform: none;
    }

    .link-indicator::after {
      transition: none;
    }

    .resource-link:hover .link-indicator::after {
      transform: none;
    }
  }

  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .concept-card,
    .resource-link,
    .related-card {
      border: 2px solid var(--text-color);
    }

    .concept-card:hover,
    .resource-link:hover,
    .related-card:hover {
      border-color: var(--primary-color);
      border-width: 3px;
    }

    .highlight-box,
    .practice-tip,
    .advanced-tip {
      border-left-width: 6px;
    }
  }
</style>
