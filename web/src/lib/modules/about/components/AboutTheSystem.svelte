<!-- About The System - Honest, consolidated overview -->
<section class="about-system">
  <div class="container">
    <h2>What is TKA?</h2>
    <div class="intro">
      <div class="quick-summary">
        <h3>TKA in 30 seconds:</h3>
        <ul class="summary-list">
          <li>
            <strong>What:</strong> A way to write down flow art movements (like sheet
            music for dance)
          </li>
          <li>
            <strong>Why:</strong> Learn patterns instead of just copying moves
          </li>
          <li>
            <strong>How:</strong> Web app + learning materials + notation system
          </li>
          <li>
            <strong>Who:</strong> Flow artists who want to level up their practice
          </li>
        </ul>
      </div>
    </div>

    <div class="system-grid">
      <div class="system-card">
        <div class="card-icon">📝</div>
        <h3>Movement Notation</h3>
        <p>Like sheet music for dance - write down any flow art movement</p>
        <div class="card-example">Example: "Start → Spin → Cross → End"</div>
      </div>

      <div class="system-card">
        <div class="card-icon">🔧</div>
        <h3>Sequence Constructor</h3>
        <p>Build and visualize movement sequences in your browser</p>
        <div class="card-example">Try it: Click "Start Creating" above</div>
      </div>

      <div class="system-card">
        <div class="card-icon">📖</div>
        <h3>Learning Materials</h3>
        <p>Step-by-step guides from basic concepts to advanced techniques</p>
        <div class="card-example">Start with: Level 1 PDF (free download)</div>
      </div>

      <div class="system-card">
        <div class="card-icon">🎯</div>
        <h3>Structured Practice</h3>
        <p>Learn patterns, not just moves - create your own variations</p>
        <div class="card-example">Result: Endless creative possibilities</div>
      </div>
    </div>
  </div>
</section>

<style>
  .about-system {
    padding: var(--spacing-lg) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  h2 {
    text-align: center;
    margin-bottom: var(--spacing-md);
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
  }

  .intro {
    text-align: center;
    margin-bottom: var(--spacing-lg);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }

  .quick-summary {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    padding: var(--spacing-lg);
    text-align: left;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .quick-summary h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: 1.25rem;
    text-align: center;
  }

  .summary-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: var(--spacing-sm);
  }

  .summary-list li {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    line-height: 1.5;
    padding: var(--spacing-xs) 0;
  }

  .summary-list strong {
    color: var(--primary-color);
    font-weight: 600;
  }

  .system-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-xl);
  }

  .system-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-lg);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    text-align: center;
  }

  .system-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .card-icon {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-md);
    display: block;
  }

  .system-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: 1.25rem;
    font-weight: 600;
  }

  .system-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
    margin-bottom: var(--spacing-sm);
  }

  .card-example {
    background: rgba(255, 255, 255, 0.1);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.5rem;
    font-size: 0.9rem;
    color: var(--primary-color);
    font-weight: 500;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .about-system {
      padding: var(--spacing-md) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 1.75rem;
    }

    .system-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-md);
    }

    .system-card {
      padding: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .system-card {
      transition: none;
    }

    .system-card:hover {
      transform: none;
    }
  }
</style>
