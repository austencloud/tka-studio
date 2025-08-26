<script lang="ts">
  function handleConstructorClick() {
    window.location.href = "/constructor";
  }
</script>

<!-- Quick Acc  /* Mobile Responsive */
  @media (max-width: 768px) {
    .quick-access {
      padding: var(--spacing-md) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }on -->
<section class="quick-access">
  <div class="container">
    <h2>Quick Access</h2>
    <div class="quick-grid">
      <button onclick={handleConstructorClick} class="quick-link constructor">
        <div class="quick-icon">🔧</div>
        <div class="quick-content">
          <h3>Start Creating</h3>
          <p>Jump into the constructor</p>
        </div>
      </button>

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

      <a
        href="https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe"
        class="quick-link download"
        target="_blank"
        rel="noopener noreferrer"
      >
        <div class="quick-icon">⬇️</div>
        <div class="quick-content">
          <h3>Get Desktop App</h3>
          <p>Download v0.1.2</p>
        </div>
      </a>
    </div>
  </div>
</section>

<style>
  /* Quick Access Section */
  .quick-access {
    padding: var(--spacing-lg) 0;
    background: rgba(255, 255, 255, 0.02);
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .quick-access h2 {
    text-align: center;
    margin-bottom: var(--spacing-lg);
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
    cursor: pointer;
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

  .quick-link.download:hover {
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
    .quick-access {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .quick-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .quick-link {
      padding: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .quick-link {
      transition: none;
    }

    .quick-link:hover {
      transform: none;
    }
  }
</style>
