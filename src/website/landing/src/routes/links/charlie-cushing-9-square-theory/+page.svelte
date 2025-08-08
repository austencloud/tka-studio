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
      name: "Vulcan Tech Gospel (VTG)",
      url: "/links/vulcan-tech-gospel",
      description: "The foundational theory that 9-square theory builds upon",
      type: 'internal'
    },
    {
      name: "DrexFactor Poi",
      url: "/links/drexfactor-poi",
      description: "Advanced poi tutorials incorporating 9-square methodology",
      type: 'internal'
    },
    {
      name: "Spin More Poi Advanced Section",
      url: "https://www.spinmorepoi.com/advanced/",
      description: "Charlie Cushing's original 9-square theory documentation",
      type: 'external'
    },
    {
      name: "Playpoi Advanced Techniques",
      url: "https://playpoi.com/lessons/advanced/",
      description: "Community discussions and applications of 9-square theory",
      type: 'external'
    },
    {
      name: "LanternSmith Poi Resources",
      url: "https://www.lanternsmith.com/poi-resources/",
      description: "Charlie Cushing's equipment and additional learning materials",
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
  <title>Charlie Cushing's 9 Square Theory - Complete Guide | The Kinetic Alphabet</title>
  <meta name="description" content="Master Charlie Cushing's revolutionary 9 Square Theory for poi spinning. Learn advanced unit circle connections, spatial relationships, and technical poi applications from the former helicopter pilot's systematic approach." />
  <meta name="keywords" content="9 square theory, Charlie Cushing, poi theory, unit circles, technical poi, helicopter pilot, LanternSmith, advanced poi, spatial relationships" />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="Charlie Cushing's 9 Square Theory - Complete Guide" />
  <meta property="og:description" content="Master the advanced framework for connecting unit circles in technical poi spinning with Charlie Cushing's revolutionary 9 Square Theory." />
  <meta property="og:url" content="https://thekineticalphabet.com/links/charlie-cushing-9-square-theory" />

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:title" content="Charlie Cushing's 9 Square Theory - Complete Guide" />
  <meta property="twitter:description" content="Master the advanced framework for connecting unit circles in technical poi spinning with Charlie Cushing's revolutionary 9 Square Theory." />

  <!-- Schema.org markup -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Charlie Cushing's 9 Square Theory - Complete Guide",
    "description": "Master Charlie Cushing's revolutionary 9 Square Theory for poi spinning. Learn advanced unit circle connections, spatial relationships, and technical poi applications.",
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
      "@id": "https://thekineticalphabet.com/links/charlie-cushing-9-square-theory"
    },
    "about": {
      "@type": "Thing",
      "name": "9 Square Theory",
      "description": "Advanced framework for connecting unit circles in technical poi"
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
      <li aria-current="page">Charlie Cushing's 9 Square Theory</li>
    </ol>
  </nav>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-content">
      <h1>Charlie Cushing's 9 Square Theory</h1>
      <p class="subtitle">Revolutionary framework for connecting unit circles in technical poi</p>
      <div class="hero-meta">
        <span class="creator">Created by <strong>Charlie Cushing</strong></span>
        <span class="category">Advanced Theory</span>
        <span class="level">Advanced</span>
      </div>
    </div>
  </header>

  <!-- Table of Contents -->
  <nav class="table-of-contents">
    <h2>Contents</h2>
    <ul>
      <li><a href="#overview" class:active={currentSection === 'overview'}>Overview</a></li>
      <li><a href="#creator-background" class:active={currentSection === 'creator-background'}>Creator Background</a></li>
      <li><a href="#key-concepts" class:active={currentSection === 'key-concepts'}>Key Concepts</a></li>
      <li><a href="#getting-started" class:active={currentSection === 'getting-started'}>Getting Started</a></li>
      <li><a href="#advanced-applications" class:active={currentSection === 'advanced-applications'}>Advanced Applications</a></li>
      <li><a href="#official-resources" class:active={currentSection === 'official-resources'}>Official Resources</a></li>
    </ul>
  </nav>

  <!-- Main Content -->
  <div class="content">
    <section id="overview" class="content-section">
      <h2>Overview</h2>
      <p>
        Charlie Cushing's 9 Square Theory represents one of the most sophisticated and mathematically rigorous
        approaches to technical poi spinning ever developed. Building upon the foundational concepts of Vulcan
        Tech Gospel (VTG), this advanced framework provides a systematic method for understanding and executing
        complex transitions between unit circles in three-dimensional space.
      </p>

      <p>
        The theory emerged from Cushing's unique background as a former helicopter pilot, bringing principles
        of spatial navigation and three-dimensional thinking to poi spinning. His analytical approach to movement
        has created a framework that allows advanced spinners to navigate complex technical sequences with
        precision and intentionality.
      </p>

      <div class="highlight-box">
        <h3>Why 9 Square Theory Matters</h3>
        <p>
          9 Square Theory provides the missing link between basic poi movements and truly advanced technical
          spinning. It offers a systematic approach to understanding spatial relationships that would otherwise
          require years of intuitive development to master.
        </p>
      </div>
    </section>

    <section id="creator-background" class="content-section">
      <h2>Creator Background: Charlie Cushing</h2>

      <p>
        Charlie Cushing brought a unique perspective to poi theory development through his background as a
        helicopter pilot and founder of LanternSmith, a respected poi equipment manufacturer. His aviation
        experience provided him with an intuitive understanding of three-dimensional navigation and spatial
        relationships that directly translated to poi movement analysis.
      </p>

      <h3>Professional Background</h3>
      <ul>
        <li><strong>Aviation Career:</strong> Former helicopter pilot with extensive experience in 3D navigation</li>
        <li><strong>LanternSmith Founder:</strong> Created high-quality poi equipment used by professionals worldwide</li>
        <li><strong>Community Educator:</strong> Developed teaching methods that made advanced concepts accessible</li>
        <li><strong>Innovation Pioneer:</strong> Bridged the gap between VTG theory and practical application</li>
      </ul>

      <h3>Theoretical Contributions</h3>
      <p>
        Cushing's approach to poi theory was revolutionary in its systematic nature. Rather than relying on
        intuitive understanding, he created a framework that could be taught, learned, and applied consistently.
        His work represents the evolution of poi from an art form to a technical discipline with its own
        mathematical foundations.
      </p>

      <div class="creator-insight">
        <h4>Aviation Influence</h4>
        <p>
          Cushing's helicopter piloting experience directly influenced his approach to poi theory. The same
          spatial awareness and three-dimensional thinking required for aviation translated perfectly to
          understanding poi movement in space, leading to insights that purely ground-based practitioners
          might never develop.
        </p>
      </div>
    </section>

    <section id="key-concepts" class="content-section">
      <h2>Key Concepts</h2>

      <div class="concept-grid">
        <div class="concept-card">
          <h3>The 9 Square Grid</h3>
          <p>
            A three-dimensional conceptual framework that maps all possible poi positions relative to the
            spinner's body, providing a systematic way to understand and navigate spatial relationships.
          </p>
        </div>

        <div class="concept-card">
          <h3>Unit Circle Connections</h3>
          <p>
            Methods for transitioning between different circular patterns while maintaining flow and avoiding
            tangles, building upon VTG flower concepts with greater precision.
          </p>
        </div>

        <div class="concept-card">
          <h3>Spatial Navigation</h3>
          <p>
            Systematic approaches to moving poi through three-dimensional space with intentionality and
            precision, drawing from aviation navigation principles.
          </p>
        </div>

        <div class="concept-card">
          <h3>Advanced Timing Systems</h3>
          <p>
            Complex timing relationships that allow for sophisticated pattern combinations and seamless
            transitions between different movement vocabularies.
          </p>
        </div>
      </div>

      <h3>The Mathematical Foundation</h3>
      <p>
        Unlike earlier poi theories that relied heavily on intuitive understanding, 9 Square Theory provides
        a mathematical framework for understanding poi movement. This systematic approach allows practitioners
        to predict outcomes, plan sequences, and troubleshoot problems with unprecedented precision.
      </p>

      <h3>Integration with VTG</h3>
      <p>
        9 Square Theory doesn't replace VTG but rather builds upon it, providing advanced tools for practitioners
        who have mastered the foundational concepts. The theory assumes familiarity with poi flowers and basic
        transition theory, then extends these concepts into more complex spatial relationships.
      </p>
    </section>

    <section id="getting-started" class="content-section">
      <h2>Getting Started with 9 Square Theory</h2>

      <div class="getting-started-content">
        <h3>Prerequisites</h3>
        <ul>
          <li>Mastery of VTG concepts including poi flowers and basic transitions</li>
          <li>Comfortable with advanced poi movements (isolations, antispin, contact)</li>
          <li>Strong spatial awareness and ability to visualize 3D relationships</li>
          <li>Experience with complex timing patterns and polyrhythms</li>
          <li>Solid foundation in both same-direction and split-time spinning</li>
        </ul>

        <h3>Learning Progression</h3>
        <ol>
          <li><strong>Conceptual Understanding:</strong> Study the 9-square grid and spatial relationships</li>
          <li><strong>Basic Navigation:</strong> Practice moving between adjacent squares</li>
          <li><strong>Unit Circle Mapping:</strong> Apply the framework to existing VTG patterns</li>
          <li><strong>Transition Development:</strong> Create new pathways between patterns</li>
          <li><strong>Advanced Integration:</strong> Combine multiple concepts into flowing sequences</li>
        </ol>

        <div class="practice-tip">
          <h4>Essential Practice Approach</h4>
          <p>
            9 Square Theory requires a methodical approach to learning. Unlike more intuitive poi concepts,
            this framework demands intellectual understanding before physical execution. Spend significant
            time studying the theory before attempting complex applications.
          </p>
        </div>
      </div>
    </section>

    <section id="advanced-applications" class="content-section">
      <h2>Advanced Applications</h2>

      <p>
        The true power of 9 Square Theory becomes apparent in its advanced applications, where the systematic
        framework enables possibilities that would be nearly impossible to discover through intuitive exploration alone.
      </p>

      <h3>Complex Sequence Design</h3>
      <ul>
        <li><strong>Multi-Plane Choreography:</strong> Sequences that utilize all nine spatial positions</li>
        <li><strong>Predictive Transitions:</strong> Using the framework to plan complex movement pathways</li>
        <li><strong>Error Recovery:</strong> Systematic approaches to recovering from mistakes mid-sequence</li>
        <li><strong>Improvisation Structure:</strong> Framework for real-time sequence creation</li>
      </ul>

      <h3>Integration with Other Disciplines</h3>
      <p>
        9 Square Theory's systematic approach makes it particularly valuable for integration with other movement disciplines:
      </p>
      <ul>
        <li><strong>Dance Integration:</strong> Mapping poi movements to choreographic structures</li>
        <li><strong>Fire Performance:</strong> Safety-conscious applications for fire spinning</li>
        <li><strong>LED and Visual Arts:</strong> Creating visually striking patterns with intentional design</li>
        <li><strong>Teaching and Instruction:</strong> Systematic methods for advanced poi education</li>
      </ul>

      <div class="advanced-tip">
        <h4>Professional Application</h4>
        <p>
          Many professional poi performers use 9 Square Theory as the foundation for their choreographic work.
          The framework's predictability and systematic nature make it invaluable for creating reliable,
          repeatable performances that can be adapted for different venues and contexts.
        </p>
      </div>
    </section>

    <section id="official-resources" class="content-section">
      <h2>Official Resources & Further Learning</h2>

      <p>
        Charlie Cushing's 9 Square Theory is primarily documented through his work with LanternSmith and
        contributions to the broader poi community. These resources provide the most authoritative information
        for serious students of the theory.
      </p>

      <div class="resource-links">
        <h3>Primary Sources</h3>
        <div class="link-grid">
          <a href="https://www.spinmorepoi.com/advanced/" target="_blank" rel="noopener noreferrer" class="resource-link primary">
            <h4>Spin More Poi Advanced Section</h4>
            <p>Charlie Cushing's original documentation and explanations of 9 Square Theory</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://www.lanternsmith.com/poi-resources/" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>LanternSmith Resources</h4>
            <p>Equipment and additional learning materials from Charlie Cushing's company</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://playpoi.com/lessons/advanced/" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Playpoi Advanced Lessons</h4>
            <p>Community discussions and applications of 9 Square Theory concepts</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>
        </div>

        <h3>Video Tutorials</h3>
        <div class="link-grid">
          <a href="https://www.youtube.com/results?search_query=charlie+cushing+9+square+theory+poi" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>YouTube 9 Square Theory Tutorials</h4>
            <p>Visual demonstrations and explanations of key concepts</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://drexfactor.com/advanced/9-square-theory" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>DrexFactor Advanced Analysis</h4>
            <p>Technical breakdowns and practical applications</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>
        </div>

        <h3>Community Discussion</h3>
        <div class="link-grid">
          <a href="https://www.reddit.com/r/poi/search/?q=9%20square%20theory" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Reddit Poi Community</h4>
            <p>Active discussions about 9 Square Theory applications and questions</p>
            <span class="link-indicator">Visit Resource →</span>
          </a>

          <a href="https://www.facebook.com/groups/advancedpoispinners" target="_blank" rel="noopener noreferrer" class="resource-link">
            <h4>Advanced Poi Spinners Groups</h4>
            <p>Specialized communities focused on advanced theoretical concepts</p>
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
  /* Import the same styles from VTG page with minor modifications */
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

  /* Hero Section - Modified for 9 Square Theory */
  .hero {
    text-align: center;
    margin-bottom: var(--spacing-3xl);
    padding: var(--spacing-2xl) 0;
    background: linear-gradient(135deg, rgba(255, 152, 0, 0.05) 0%, rgba(168, 28, 237, 0.05) 100%);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--border-color);
  }

  .hero h1 {
    font-size: clamp(1.8rem, 4vw, 3rem);
    margin-bottom: var(--spacing-md);
    background: linear-gradient(135deg, #ff9800, var(--primary-color));
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
    background: rgba(255, 152, 0, 0.1) !important;
    color: #ff9800 !important;
    border-color: #ff9800 !important;
  }

  /* Creator Insight Box */
  .creator-insight {
    background: rgba(255, 152, 0, 0.05);
    border-left: 4px solid #ff9800;
    padding: var(--spacing-lg);
    margin: var(--spacing-lg) 0;
    border-radius: 0 var(--border-radius) var(--border-radius) 0;
  }

  .creator-insight h4 {
    margin-top: 0;
    color: #ff9800;
  }

  /* All other styles inherited from VTG page */
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
    border-color: #ff9800;
    background: rgba(255, 152, 0, 0.05);
  }

  .resource-link.primary:hover {
    background: rgba(255, 152, 0, 0.1);
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
      background: linear-gradient(135deg, rgba(255, 152, 0, 0.1) 0%, rgba(168, 28, 237, 0.1) 100%);
    }

    .resource-link.primary {
      background: rgba(255, 152, 0, 0.1);
    }

    .resource-link.primary:hover {
      background: rgba(255, 152, 0, 0.15);
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
    .advanced-tip,
    .creator-insight {
      border-left-width: 6px;
    }
  }
</style>
