<script>
  import { onMount } from 'svelte';
</script>

<svelte:head>
  <title>About - The Kinetic Alphabet</title>
  <meta name="description" content="Learn about The Kinetic Alphabet - a revolutionary flow arts choreography toolbox for poi, staff, and other flow arts." />
</svelte:head>

<section class="about-section">
  <h1>About The Kinetic Alphabet</h1>
  
  <div class="content-grid">
    <div class="main-content">
      <h2>Our Mission</h2>
      <p>
        The Kinetic Alphabet is a revolutionary approach to flow arts choreography, 
        providing practitioners with a systematic framework for creating, learning, 
        and sharing movement sequences.
      </p>
      
      <h2>What We Offer</h2>
      <ul>
        <li>Comprehensive choreography notation system</li>
        <li>Digital tools for sequence construction</li>
        <li>Educational resources and tutorials</li>
        <li>Community platform for flow artists</li>
      </ul>
      
      <h2>For Flow Artists</h2>
      <p>
        Whether you're a beginner learning your first moves or an advanced practitioner 
        developing complex choreographies, The Kinetic Alphabet provides the tools and 
        framework to enhance your flow arts journey.
      </p>
    </div>
    
    <aside class="sidebar">
      <h3>Flow Arts Supported</h3>
      <ul>
        <li>Poi</li>
        <li>Staff</li>
        <li>Fans</li>
        <li>Hoops</li>
        <li>And more...</li>
      </ul>
    </aside>
  </div>
</section>

<style>
  .about-section {
    width: 100%;
    max-width: var(--container-max-width-wide);
    margin: 0 auto;
    padding: var(--container-padding);
  }
  
  .content-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .main-content h2 {
    color: var(--primary-color);
    margin-top: 2rem;
  }
  
  .main-content ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  .main-content li {
    padding: 0.5rem 0;
    border-left: 3px solid var(--primary-color);
    padding-left: 1rem;
    margin: 0.5rem 0;
  }
  
  .sidebar {
    background: var(--background-color);
    padding: 1.5rem;
    border-radius: 8px;
    height: fit-content;
  }
  
  .sidebar h3 {
    color: var(--primary-color);
    margin-top: 0;
  }
  
  /* Desktop optimization */
  @media (min-width: 1200px) {
    .content-grid {
      gap: var(--spacing-2xl);
    }
  }

  @media (max-width: 768px) {
    .content-grid {
      grid-template-columns: 1fr;
    }

    .about-section {
      padding: var(--container-padding);
    }
  }
</style>
