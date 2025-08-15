<!-- Project Overview -->
<section class="project-overview">
  <div class="container">
    <h2>The Project</h2>
    <div class="overview-grid">
      <div class="overview-card">
        <h3>🎯 Mission</h3>
        <p>
          To provide systematic tools and methodologies that enhance technical
          precision and creative expression in flow arts through structured
          learning approaches.
        </p>
      </div>

      <div class="overview-card">
        <h3>🔬 Methodology</h3>
        <p>
          The system breaks down complex movements into understandable
          components, creating a notation system that enables precise
          communication and analysis.
        </p>
      </div>

      <div class="overview-card">
        <h3>🌟 Vision</h3>
        <p>
          A global community of flow artists connected through shared language
          and collaborative tools for sequence creation and knowledge sharing.
        </p>
      </div>

      <div class="overview-card">
        <h3>🛠️ Tools</h3>
        <p>
          Digital applications that support visualization, creation, and sharing
          of choreographic sequences across multiple flow art disciplines.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  /* Project Overview */
  .project-overview {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-xl);
  }

  .overview-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
  }

  .overview-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .overview-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: 1.25rem;
    font-weight: 600;
  }

  .overview-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .project-overview {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 2rem;
    }

    .overview-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .overview-card {
      transition: none;
    }

    .overview-card:hover {
      transform: none;
    }
  }
</style>
