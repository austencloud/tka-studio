<script lang="ts">
  import { FontAwesomeIcon } from "$shared";
  
  // Icon candidates for "Generate New" button
  const iconCandidates = [
    { name: "wand-magic-sparkles", label: "Magic Wand Sparkles", description: "Classic generation/creation icon" },
    { name: "bolt", label: "Lightning Bolt", description: "Speed, energy, instant action" },
    { name: "bolt-lightning", label: "Lightning", description: "Power, generation" },
    { name: "sparkles", label: "Sparkles", description: "Magic, creation, new" },
    { name: "star", label: "Star", description: "New, special, featured" },
    { name: "stars", label: "Stars", description: "Multiple stars, magic" },
    { name: "circle-plus", label: "Circle Plus", description: "Add new, create" },
    { name: "plus", label: "Plus", description: "Simple add/create" },
    { name: "arrows-rotate", label: "Rotate Arrows", description: "Generate, refresh, new" },
    { name: "rotate", label: "Rotate", description: "Regenerate, refresh" },
    { name: "shuffle", label: "Shuffle", description: "Random generation" },
    { name: "dice", label: "Dice", description: "Random, generate" },
    { name: "wand-magic", label: "Magic Wand", description: "Simple magic wand" },
    { name: "fire", label: "Fire", description: "Energy, creation" },
    { name: "rocket", label: "Rocket", description: "Launch, go, action" },
    { name: "play", label: "Play", description: "Start, go, action" },
    { name: "forward", label: "Forward", description: "Go, proceed, action" },
    { name: "arrow-right", label: "Arrow Right", description: "Go, proceed" },
    { name: "circle-arrow-right", label: "Circle Arrow Right", description: "Go, action" },
    { name: "angles-right", label: "Double Angles Right", description: "Fast forward, go" }
  ];
</script>

<div class="icon-preview-page">
  <h1>Generate New Button - Icon Candidates</h1>
  <p class="description">
    Click on any icon to see it larger. These are all Font Awesome icons that could work for "Generate New".
  </p>
  
  <div class="icon-grid">
    {#each iconCandidates as icon}
      <div class="icon-card">
        <div class="icon-display">
          <FontAwesomeIcon icon={icon.name} size="3x" />
        </div>
        <div class="icon-info">
          <h3>{icon.label}</h3>
          <p class="icon-name">{icon.name}</p>
          <p class="icon-description">{icon.description}</p>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .icon-preview-page {
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
    background: #1a1a2e;
    min-height: 100vh;
    color: white;
  }
  
  h1 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #10b981 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .description {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 40px;
    color: rgba(255, 255, 255, 0.7);
  }
  
  .icon-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 24px;
  }
  
  .icon-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    transition: all 0.3s ease;
    cursor: pointer;
  }
  
  .icon-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(16, 185, 129, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
  }
  
  .icon-display {
    width: 100%;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #10b981;
  }
  
  .icon-info {
    text-align: center;
    width: 100%;
  }
  
  .icon-info h3 {
    font-size: 1.2rem;
    margin-bottom: 8px;
    color: white;
  }
  
  .icon-name {
    font-family: monospace;
    font-size: 0.9rem;
    color: rgba(16, 185, 129, 0.8);
    margin-bottom: 8px;
  }
  
  .icon-description {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
  }
  
  @media (max-width: 768px) {
    .icon-preview-page {
      padding: 20px;
    }
    
    h1 {
      font-size: 2rem;
    }
    
    .icon-grid {
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 16px;
    }
  }
</style>

