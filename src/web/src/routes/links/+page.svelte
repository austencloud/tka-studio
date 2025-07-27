<script>
  import { page } from "$app/stores";
</script>

<svelte:head>
  <title>Links - The Kinetic Alphabet</title>
  <meta
    name="description"
    content="Useful links for The Kinetic Alphabet community and flow arts enthusiasts."
  />
</svelte:head>

<div class="links-container">
  <h1>Useful Links</h1>

  <div class="links-grid">
    <!-- VTG (Vermont Tech Group) -->
    <div class="link-section">
      <h2>Vermont Tech</h2>
      <div class="links">
        <a href="/links/vtg" class="link-card">
          <h3>VTG Resources</h3>
          <p>Vermont Tech Group resources and information</p>
        </a>
      </div>
    </div>

    <!-- Charlie Cushing -->
    <div class="link-section">
      <h2>Charlie Cushing</h2>
      <div class="links">
        <a href="/links/charlie-cushing" class="link-card">
          <h3>Charlie Cushing's Page</h3>
          <p>Information and resources from Charlie Cushing</p>
        </a>
      </div>
    </div>

    <!-- Flow Arts Community -->
    <div class="link-section">
      <h2>Flow Arts Community</h2>
      <div class="links">
        <a
          href="https://flowartsinstitute.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Flow Arts Institute</h3>
          <p>Educational resources and community for flow arts</p>
        </a>

        <a
          href="https://flowtoys.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Flowtoys</h3>
          <p>LED flow props and poi equipment</p>
        </a>

        <a
          href="https://spinfreaks.com"
          target="_blank"
          class="link-card external"
        >
          <h3>SpinFreaks</h3>
          <p>Flow arts community and tutorials</p>
        </a>
      </div>
    </div>

    <!-- Shopping -->
    <div class="link-section">
      <h2>Equipment & Shopping</h2>
      <div class="links">
        <a
          href="https://homeofpoi.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Home of Poi</h3>
          <p>Poi, staff, and flow arts equipment</p>
        </a>

        <a
          href="https://lanternsmith.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Lantern Smith</h3>
          <p>LED and fire performance equipment</p>
        </a>

        <a
          href="https://firetoys.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Firetoys</h3>
          <p>Professional juggling and fire performance equipment</p>
        </a>
      </div>
    </div>

    <!-- Educational Resources -->
    <div class="link-section">
      <h2>Educational Resources</h2>
      <div class="links">
        <a
          href="https://library.drexunlimited.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Drex's Poi Library</h3>
          <p>Comprehensive poi tutorials and theory</p>
        </a>

        <a
          href="https://playpoi.com"
          target="_blank"
          class="link-card external"
        >
          <h3>PlayPoi</h3>
          <p>Interactive poi learning platform</p>
        </a>

        <a
          href="https://contact-staff.com"
          target="_blank"
          class="link-card external"
        >
          <h3>Contact Staff</h3>
          <p>Contact staff tutorials and community</p>
        </a>
      </div>
    </div>

    <!-- Events & Festivals -->
    <div class="link-section">
      <h2>Events & Festivals</h2>
      <div class="links">
        <a
          href="https://burningman.org"
          target="_blank"
          class="link-card external"
        >
          <h3>Burning Man</h3>
          <p>Annual art and community event in Nevada</p>
        </a>

        <a
          href="https://firedrums.org"
          target="_blank"
          class="link-card external"
        >
          <h3>Fire Drums</h3>
          <p>Annual fire arts festival</p>
        </a>

        <a
          href="https://flowfestival.org"
          target="_blank"
          class="link-card external"
        >
          <h3>Flow Festival</h3>
          <p>Flow arts workshops and performances</p>
        </a>
      </div>
    </div>
  </div>
</div>

<style>
  .links-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    text-align: center;
    margin-bottom: 3rem;
    color: var(--color-primary);
  }

  .links-grid {
    display: grid;
    gap: 3rem;
  }

  .link-section h2 {
    color: var(--color-secondary);
    margin-bottom: 1rem;
    border-bottom: 2px solid var(--color-accent);
    padding-bottom: 0.5rem;
  }

  .links {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
  }

  .link-card {
    display: block;
    padding: 1.5rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    position: relative;
  }

  .link-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: var(--color-accent);
  }

  .link-card.external::after {
    content: "↗";
    position: absolute;
    top: 1rem;
    right: 1rem;
    opacity: 0.6;
  }

  .link-card h3 {
    margin: 0 0 0.5rem 0;
    color: var(--color-primary);
  }

  .link-card p {
    margin: 0;
    color: var(--color-text-secondary);
    font-size: 0.9rem;
  }

  @media (max-width: 768px) {
    .links-container {
      padding: 1rem;
    }

    .links {
      grid-template-columns: 1fr;
    }
  }
</style>
