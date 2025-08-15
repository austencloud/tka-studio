<!-- Features Section -->
<section class="features">
  <div class="container">
    <h2>The Kinetic Alphabet Features</h2>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">📚</div>
        <h3>Systematic Learning</h3>
        <p>
          Complex movements are broken down into understandable components
          through a structured notation system.
        </p>
      </div>

      <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Precision Training</h3>
        <p>
          The system supports muscle memory development and technical precision
          through methodical movement approaches.
        </p>
      </div>

      <div class="feature-card">
        <div class="feature-icon">🔧</div>
        <h3>Digital Tools</h3>
        <p>
          The Kinetic Constructor enables visualization, creation, and sharing
          of choreographic sequences.
        </p>
      </div>

      <div class="feature-card">
        <div class="feature-icon">🌟</div>
        <h3>Creative Framework</h3>
        <p>
          The system provides foundational knowledge that enables exploration of
          infinite sequence possibilities.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  /* Features Section */
  .features {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .features h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .features-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
    align-items: stretch;
  }

  .feature-card {
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow:
      0 20px 40px rgba(118, 75, 162, 0.2),
      0 8px 20px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    display: inline-block;
    transition: all 0.3s ease;
  }

  .feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
  }

  .feature-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-weight: 700;
    font-size: 1.25rem;
  }

  .feature-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .features {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .features h2 {
      font-size: 2rem;
    }

    .features-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, auto);
      gap: var(--spacing-lg);
    }

    .feature-card {
      padding: var(--spacing-lg);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .feature-card,
    .feature-icon {
      transition: none;
    }

    .feature-card:hover,
    .feature-card:hover .feature-icon {
      transform: none;
    }
  }
</style>
