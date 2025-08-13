<script lang="ts">
  import { modalManager, type ResourceModalData } from '$lib/stores/modalStore.svelte';
  import ResourceModal from '$lib/components/resource-guide/ResourceModal.svelte';
  import VTGContent from '$lib/components/resource-guide/content/VTGContent.svelte';
  
  // Import new sub-components
  import ResourceFilters from './resources/ResourceFilters.svelte';
  import ResourceGrid from './resources/ResourceGrid.svelte';
  import { 
    resources, 
    categories, 
    type Resource,
    getCategoryDisplayName,
    getLevelDisplayName 
  } from './resources/resourcesData';

  // State
  let searchTerm = $state('');
  let selectedCategory = $state('all');
  let selectedLevel = $state('all');

  // Computed filtered resources
  let filteredResources = $derived(() => {
    return resources.filter(resource => {
      const matchesSearch = searchTerm === '' || 
                          resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          resource.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (resource.specialties && resource.specialties.some(s => 
                            s.toLowerCase().includes(searchTerm.toLowerCase())
                          ));
      const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory;
      const matchesLevel = selectedLevel === 'all' || resource.level === selectedLevel;
      return matchesSearch && matchesCategory && matchesLevel;
    });
  });

  // Modal handlers
  function handleOpenModal(resource: Resource) {
    if (resource.hasLandingPage && resource.landingPageUrl) {
      const resourceName = resource.landingPageUrl.split('/').pop();
      if (resourceName) {
        openResourceModal(resourceName, resource);
      }
    }
  }
      landingPageUrl: "/links/charlie-cushing-9-square-theory",
      modalType: "educational"
    },
    {
      name: "Flow Arts Institute",
      description: "Educational platform exploring the phenomena of flow arts and providing comprehensive learning resources.",
      url: "https://flowartsinstitute.com/",
      category: "active-learning",
      level: "all",
      value: "Academic approach to understanding flow state and movement theory in flow arts.",
      status: "active",
      lastUpdated: "2024",
      modalType: "educational"
    },
    {
      name: "Playpoi",
      description: "Community-driven platform with extensive tutorials, courses, and educational content for poi spinning.",
      url: "https://playpoi.com/",
      category: "active-learning",
      level: "all",
      value: "Long-standing pillar of the poi community with comprehensive learning materials.",
      status: "active",
      lastUpdated: "2024",
      modalType: "educational"
    },
    {
      name: "The Kinetic Alphabet",
      description: "Revolutionary choreography notation system providing a systematic framework for flow arts movement documentation and sharing.",
      url: "/",
      category: "active-learning",
      level: "all",
      value: "Innovative approach to documenting and sharing flow arts choreography with structured notation - the core offering of this website.",
      status: "active",
      lastUpdated: "2024",
      modalType: "educational"
    },

    // ACTIVE COMMUNITY PLATFORMS
    {
      name: "Reddit Flow Arts Community", 
      description: "Active discussion platform covering poi, staff, fans, hoops, and all flow arts disciplines.",
      url: "https://www.reddit.com/r/flowarts/",
      category: "active-community",
      level: "all",
      value: "Vibrant community for sharing videos, asking questions, and connecting with flow artists worldwide.",
      status: "active",
      lastUpdated: "2024",
      modalType: "educational"
    },
    {
      name: "Reddit Poi Community",
      description: "Dedicated subreddit for poi spinning discussion, tutorials, and community support.",
      url: "https://www.reddit.com/r/poi/",
      category: "active-community",
      level: "all", 
      value: "Focused community for poi-specific discussions, technique sharing, and beginner support.",
      status: "active",
      lastUpdated: "2024",
      modalType: "educational"
    },

    // FLOW ARTS VENDORS & EQUIPMENT
    {
      name: "Fire & Flow",
      description: "Professional fire and LED flow arts equipment, poi, staff, and more",
      url: "https://fireandflow.com/",
      category: "vendors",
      level: "all",
      value: "Industry leader in fire safety and professional-grade fire props for performers.",
      status: "vendor",
      foundingYear: 2010,
      companyLocation: "USA",
      specialties: ["Fire Props", "LED Equipment", "Safety Gear", "Professional Tools"],
      lastUpdated: "2024",
      modalType: "vendor"
    },
    {
      name: "Flowtoys",
      description: "High-quality LED flow props, poi, staff, clubs, and accessories",
      url: "https://flowtoys.com/",
      category: "vendors",
      level: "all",
      value: "Cutting-edge LED technology for visual flow arts and performance.",
      status: "vendor",
      foundingYear: 2015,
      companyLocation: "International",
      specialties: ["LED Poi", "Visual Props", "Programmable LEDs", "Interactive Technology"],
      lastUpdated: "2024",
      modalType: "vendor"
    },
    {
      name: "Home of Poi",
      description: "Traditional and modern poi equipment, including practice and performance poi",
      url: "https://homeofpoi.com/",
      category: "vendors",
      level: "all",
      value: "Established community business combining retail with educational resources.",
      status: "vendor", 
      foundingYear: 1998,
      companyLocation: "UK/USA",
      specialties: ["Poi", "Fire Props", "Tutorials", "Community"],
      lastUpdated: "2024",
      modalType: "vendor"
    },

    // HISTORICAL ARCHIVES
    {
      name: "Spin More Poi",
      description: "Well-organized and curated reference for learning and sharing poi tricks, developed by Willow Solow.",
      url: "https://www.spinmorepoi.com/",
      category: "historical-archives",
      level: "all",
      value: "Systematic approach to poi learning with clear progression and community sharing.",
      status: "historical",
      lastUpdated: "2018",
      modalType: "archive"
    },
    {
      name: "DrexFactor Poi",
      description: "Comprehensive poi tutorials focusing on tech spinning, flow exploration, and advanced techniques.",
      url: "https://drexfactor.com/",
      category: "historical-archives",
      level: "all",
      value: "Premier resource for technical poi education with detailed explanations and progressive learning.",
      status: "historical",
      lastUpdated: "2016",
      modalType: "archive"
    }
  ];

  const categories = [
    { value: 'all', label: 'All Categories' },
    { value: 'active-learning', label: 'Active Learning Resources' },
    { value: 'active-community', label: 'Active Community Platforms' },
    { value: 'vendors', label: 'Flow Arts Vendors & Equipment' },
    { value: 'historical-archives', label: 'Historical Archives' }
  ];

  let filteredResources = $derived(() => {
    const filtered = resources.filter(resource => {
      const matchesSearch = searchTerm === '' || 
                          resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          resource.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
    
    return filtered;
  });

  function handleLearnMoreClick(event: Event, resource: Resource) {
    event.preventDefault();
    if (resource.hasLandingPage && resource.landingPageUrl) {
      const resourceName = resource.landingPageUrl.split('/').pop();
      if (resourceName) {
        openResourceModal(resourceName, resource);
      }
    }
  }

  function openResourceModal(resourceName: string, resource: Resource) {
    modalManager.openModal(resourceName);
    
    const modalData: ResourceModalData = getModalDataForResource(resourceName, resource);
    modalManager.setModalData(modalData);
  }

  function getModalDataForResource(resourceName: string, resource: Resource): ResourceModalData {
    return {
      title: resource.name,
      subtitle: resource.description,
      creator: getCreatorForResource(resourceName, resource),
      category: getCategoryDisplayName(resource.category),
      level: getLevelDisplayName(resource.level),
      description: resource.value,
      keywords: getKeywordsForResource(resourceName),
      url: resource.url,
      resourceName: resourceName,
      tableOfContents: getTableOfContentsForResource(resourceName),
      relatedResources: getRelatedResourcesForResource(resourceName),
      heroGradient: getHeroGradientForResource(resourceName, resource),
      creatorColor: getCreatorColorForResource(resourceName, resource)
    };
  }

  function getCreatorForResource(resourceName: string, resource: Resource): string {
    if (resource.status === 'vendor') {
      return `Founded ${resource.foundingYear} • ${resource.companyLocation}`;
    }
    if (resource.status === 'historical') {
      return `Last Updated: ${resource.lastUpdated}`;
    }
    switch (resourceName) {
      case 'vulcan-tech-gospel':
        return 'Noel Yee';
      case 'charlie-cushing-9-square-theory':
        return 'Charlie Cushing';
      default:
        return 'Community Resource';
    }
  }

  function getCategoryDisplayName(category: string): string {
    const categoryMap: Record<string, string> = {
      'active-learning': 'Active Learning Resources',
      'active-community': 'Active Community Platforms', 
      'vendors': 'Flow Arts Vendors & Equipment',
      'historical-archives': 'Historical Archives'
    };
    return categoryMap[category] || category;
  }

  function getLevelDisplayName(level: string): string {
    const levelMap: Record<string, string> = {
      'beginner': 'Beginner',
      'intermediate': 'Intermediate to Advanced',
      'advanced': 'Advanced',
      'all': 'All Levels'
    };
    return levelMap[level] || level;
  }

  function getKeywordsForResource(resourceName: string): string {
    switch (resourceName) {
      case 'vulcan-tech-gospel':
        return 'Vulcan Tech Gospel, VTG, poi theory, Noel Yee, poi flowers, transition theory, technical poi, flow arts theory';
      case 'charlie-cushing-9-square-theory':
        return '9 square theory, Charlie Cushing, poi theory, unit circles, technical poi, helicopter pilot, LanternSmith, advanced poi, spatial relationships';
      default:
        return 'flow arts, poi, theory, tutorial';
    }
  }

  function getTableOfContentsForResource(resourceName: string): Array<{id: string, label: string}> {
    switch (resourceName) {
      case 'vulcan-tech-gospel':
        return [
          { id: 'overview', label: 'Overview' },
          { id: 'key-concepts', label: 'Key Concepts' },
          { id: 'getting-started', label: 'Getting Started' },
          { id: 'advanced-applications', label: 'Advanced Applications' },
          { id: 'community-impact', label: 'Community Impact' },
          { id: 'official-resources', label: 'Official Resources' }
        ];
      case 'charlie-cushing-9-square-theory':
        return [
          { id: 'overview', label: 'Overview' },
          { id: 'creator-background', label: 'Creator Background' },
          { id: 'key-concepts', label: 'Key Concepts' },
          { id: 'getting-started', label: 'Getting Started' },
          { id: 'advanced-applications', label: 'Advanced Applications' },
          { id: 'official-resources', label: 'Official Resources' }
        ];
      default:
        return [];
    }
  }

  function getRelatedResourcesForResource(resourceName: string): Array<{name: string, url: string, description: string, type: 'internal' | 'external'}> {
    switch (resourceName) {
      case 'vulcan-tech-gospel':
        return [
          {
            name: "Charlie Cushing's 9 Square Theory",
            url: "/about#charlie-cushing-9-square-theory",
            description: "Advanced framework building upon VTG principles for connecting unit circles",
            type: 'internal'
          },
          {
            name: "Noel Yee's Official VTG Resources",
            url: "https://noelyee.com/instruction/vulcan-tech-gospel/",
            description: "Original VTG documentation and tutorials by the creator",
            type: 'external'
          }
        ];
      default:
        return [];
    }
  }

  function getHeroGradientForResource(resourceName: string, resource: Resource): string {
    switch (resource.category) {
      case 'vendors':
        return 'linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(139, 195, 74, 0.05) 100%)';
      case 'historical-archives':
        return 'linear-gradient(135deg, rgba(158, 158, 158, 0.05) 0%, rgba(117, 117, 117, 0.05) 100%)';
      default:
        return 'linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)';
    }
  }

  function getCreatorColorForResource(resourceName: string, resource: Resource): string {
    switch (resource.category) {
      case 'vendors':
        return '#4caf50';
      case 'historical-archives':
        return '#757575';
      default:
        return 'var(--primary-color)';
    }
  }

  function getResourceCountForCategory(categoryValue: string): number {
    if (categoryValue === 'all') {
      return resources.length;
    }
    return resources.filter(resource => resource.category === categoryValue).length;
  }
</script>

<!-- Resources & Links Section -->
<section class="resources-links">
  <div class="container">
    <h2>Flow Arts Historian</h2>
    <p class="subtitle">
      Your comprehensive guide to flow arts resources, from cutting-edge learning platforms and active communities
      to essential vendors and historical archives preserving our art form's rich heritage.
    </p>
    
    <!-- Debug info -->
    <div class="debug-info" style="background: rgba(255,255,255,0.1); padding: 10px; margin: 10px 0; border-radius: 8px; font-size: 12px;">
      <strong>Debug:</strong> Total resources: {resources.length} | Filtered: {filteredResources.length} | Category: {selectedCategory} | Search: "{searchTerm}"
    </div>
    
    <div class="search-section">
      <div class="search-container">
        <input
          type="text"
          placeholder="Search resources..."
          bind:value={searchTerm}
          class="search-input"
          aria-label="Search flow arts resources"
        />
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
          <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>
    </div>

    <!-- Category Navigation -->
    <nav class="category-tabs" aria-label="Resource categories">
      {#each categories as category}
        <button
          class="category-tab"
          class:active={selectedCategory === category.value}
          onclick={() => selectedCategory = category.value}
          aria-pressed={selectedCategory === category.value}
        >
          <span class="tab-label">{category.label}</span>
          <span class="tab-count">({getResourceCountForCategory(category.value)})</span>
        </button>
      {/each}
    </nav>
    
    <div class="resources-grid">
      {#each filteredResources() as resource}
        <article class="resource-card">
          <div class="resource-header">
            <div class="resource-title-row">
              <h3 class="resource-title">
                <a href={resource.url} target="_blank" rel="noopener noreferrer">
                  {resource.name}
                </a>
              </h3>
              <span class="status-indicator status-{resource.status}">
                {resource.status === 'vendor' ? '🏪' : resource.status === 'historical' ? '📚' : '✨'}
              </span>
            </div>
            <div class="resource-meta">
              <span class="category-badge category-{resource.category}">
                {categories.find(c => c.value === resource.category)?.label || resource.category}
              </span>
              {#if resource.status === 'vendor' && resource.foundingYear}
                <span class="founding-badge">Est. {resource.foundingYear}</span>
              {/if}
              {#if resource.lastUpdated}
                <span class="last-updated-indicator">Updated {resource.lastUpdated}</span>
              {/if}
            </div>
          </div>
          
          <p class="resource-description">{resource.description}</p>
          
          {#if resource.status === 'vendor' && resource.specialties}
            <div class="vendor-specialties">
              <strong>Specialties:</strong>
              <div class="specialty-tags">
                {#each resource.specialties as specialty}
                  <span class="specialty-tag">{specialty}</span>
                {/each}
              </div>
            </div>
          {/if}

          <div class="resource-value">
            <strong>{resource.status === 'vendor' ? 'Why shop here:' : 'Why it\'s essential:'}</strong> {resource.value}
          </div>

          <div class="resource-actions">
            {#if resource.hasLandingPage}
              <button
                class="learn-more-link"
                onclick={(event) => handleLearnMoreClick(event, resource)}
                type="button"
              >
                {resource.status === 'vendor' ? 'Company Profile' : 'Learn More'}
              </button>
            {/if}
            <a href={resource.url} target="_blank" rel="noopener noreferrer" class="visit-link">
              {resource.status === 'vendor' ? 'Shop Now →' : 'Visit Resource →'}
            </a>
          </div>
        </article>
      {/each}
    </div>
    
    {#if filteredResources().length === 0}
      <div class="no-results">
        <h3>No resources found</h3>
        <p>Try adjusting your search terms or category filter.</p>
      </div>
    {/if}
  </div>
</section>

<!-- Resource Modal -->
<ResourceModal
  isOpen={modalManager.isOpen}
  onClose={() => modalManager.closeModal()}
>
  {#if modalManager.resourceName === 'vulcan-tech-gospel'}
    <VTGContent />
  {:else if modalManager.resourceName === 'charlie-cushing-9-square-theory'}
    <div class="placeholder-content">
      <p>9 Square Theory content coming soon...</p>
    </div>
  {/if}
</ResourceModal>

<style>
  /* Resources Section */
  .resources-links {
    padding: var(--spacing-3xl) 0;
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
    font-size: 2.5rem;
    font-weight: 700;
  }

  .subtitle {
    text-align: center;
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto var(--spacing-2xl) auto;
    line-height: 1.6;
  }

  /* Search Section */
  .search-section {
    margin-bottom: var(--spacing-xl);
  }

  .search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto;
  }

  .search-input {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-lg);
    padding-right: 50px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    font-size: var(--font-size-base);
    font-weight: 500;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    color: var(--text-color);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }

  .search-input:focus {
    outline: none;
    border: 2px solid var(--primary-color);
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  .search-icon {
    position: absolute;
    right: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    pointer-events: none;
  }

  /* Category Tabs */
  .category-tabs {
    display: flex;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xs);
    margin-bottom: var(--spacing-2xl);
    overflow-x: auto;
    gap: var(--spacing-xs);
  }

  .category-tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-family: inherit;
    font-size: var(--font-size-sm);
    font-weight: 500;
    border-radius: var(--border-radius);
    cursor: pointer;
    white-space: nowrap;
    min-width: 120px;
    transition: all 0.3s ease;
  }

  .category-tab:hover {
    color: var(--text-color);
    background: rgba(255, 255, 255, 0.05);
  }

  .category-tab.active {
    background: var(--primary-color);
    color: white;
    font-weight: 600;
  }

  .tab-label {
    font-size: var(--font-size-sm);
    line-height: 1.2;
  }

  .tab-count {
    font-size: var(--font-size-xs);
    opacity: 0.8;
    font-weight: 400;
  }

  /* Resources Grid */
  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--spacing-xl);
  }

  .resource-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
    transition: all 0.3s ease;
  }

  .resource-card:hover {
    transform: translateY(-6px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .resource-header {
    margin-bottom: var(--spacing-md);
  }

  .resource-title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-sm);
  }

  .resource-title {
    margin: 0;
    font-size: var(--font-size-xl);
    flex: 1;
  }

  .resource-title a {
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .resource-title a:hover {
    color: var(--primary-color);
  }

  .status-indicator {
    font-size: var(--font-size-lg);
    margin-left: var(--spacing-sm);
    opacity: 0.8;
  }

  .resource-meta {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .category-badge,
  .founding-badge,
  .last-updated-indicator {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .category-active-learning { background: rgba(168, 28, 237, 0.2); color: #a81ced; }
  .category-active-community { background: rgba(233, 30, 99, 0.2); color: #e91e63; }
  .category-vendors { background: rgba(76, 175, 80, 0.2); color: #4caf50; }
  .category-historical-archives { background: rgba(158, 158, 158, 0.2); color: #9e9e9e; }

  .founding-badge,
  .last-updated-indicator {
    background: rgba(158, 158, 158, 0.1);
    color: var(--text-secondary);
    border: 1px solid rgba(158, 158, 158, 0.2);
    opacity: 0.8;
  }

  .resource-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-md);
  }

  /* Vendor Specialties */
  .vendor-specialties {
    margin-bottom: var(--spacing-md);
  }

  .vendor-specialties strong {
    color: var(--text-color);
    font-size: var(--font-size-sm);
    display: block;
    margin-bottom: var(--spacing-xs);
  }

  .specialty-tags {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
  }

  .specialty-tag {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.2);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 500;
  }

  .resource-value {
    background: rgba(168, 28, 237, 0.05);
    border-left: 3px solid var(--primary-color);
    padding: var(--spacing-sm) var(--spacing-md);
    margin-bottom: var(--spacing-md);
    border-radius: 0 var(--border-radius-sm) var(--border-radius-sm) 0;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .resource-value strong {
    color: var(--primary-color);
  }

  .resource-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .learn-more-link,
  .visit-link {
    display: inline-flex;
    align-items: center;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-lg);
    font-weight: 600;
    font-size: var(--font-size-sm);
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
  }

  .learn-more-link {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    color: var(--primary-color);
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-family: inherit;
  }

  .learn-more-link:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary-color);
    transform: translateY(-2px);
  }

  .visit-link {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .visit-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    color: white;
  }

  .no-results {
    text-align: center;
    padding: var(--spacing-3xl);
    color: var(--text-secondary);
  }

  .no-results h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-sm);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .resources-links {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 2rem;
    }

    .search-container {
      max-width: none;
    }

    .category-tabs {
      justify-content: flex-start;
      overflow-x: auto;
    }

    .category-tab {
      min-width: 100px;
      padding: var(--spacing-xs) var(--spacing-sm);
      flex: none;
    }

    .resources-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-md);
    }

    .resource-card {
      padding: var(--spacing-md);
    }

    .resource-actions {
      justify-content: center;
      margin-top: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .resource-card,
    .visit-link,
    .search-input,
    .category-tab {
      transition: none;
    }

    .resource-card:hover,
    .visit-link:hover,
    .search-input:focus {
      transform: none;
    }
  }
</style>
