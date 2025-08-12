<script lang="ts">
  import { onMount } from 'svelte';
  import { modalState, modalActions, type ResourceModalData } from '$lib/core/shared/stores/modalStore';
  import ResourceModal from '$lib/components/resource-guide/ResourceModal.svelte';
  import VTGContent from '$lib/components/resource-guide/content/VTGContent.svelte';

  let searchTerm = '';
  let selectedCategory = 'all';

  interface Resource {
    name: string;
    description: string;
    url: string;
    category: string;
    level: string;
    value: string;
    hasLandingPage?: boolean;
    landingPageUrl?: string;
  }

  let filteredResources: EnhancedResource[] = [];

  // Modal state
  $: isModalOpen = $modalState.isOpen;
  $: currentResourceName = $modalState.resourceName;

  // Enhanced Resource Interface
  interface EnhancedResource extends Resource {
    status: 'active' | 'historical' | 'vendor';
    lastUpdated?: string;
    foundingYear?: number;
    specialties?: string[];
    companyLocation?: string;
    modalType?: 'educational' | 'vendor' | 'archive';
  }

  const resources: EnhancedResource[] = [
    // ACTIVE LEARNING RESOURCES - Current educational content and theory
    {
      name: "Vulcan Tech Gospel (VTG)",
      description: "Foundational theory for poi tech, poi flowers, and transition theory developed by Noel Yee.",
      url: "https://noelyee.com/instruction/vulcan-tech-gospel/",
      category: "active-learning",
      level: "intermediate",
      value: "Essential theoretical framework that forms the backbone of modern technical poi spinning.",
      status: "active",
      lastUpdated: "2023",
      hasLandingPage: true,
      landingPageUrl: "/links/vulcan-tech-gospel",
      modalType: "educational"
    },
    {
      name: "Charlie Cushing's 9 Square Theory",
      description: "Advanced framework for connecting unit circles in technical poi, developed by former helicopter pilot Charlie Cushing.",
      url: "https://www.spinmorepoi.com/advanced/",
      category: "active-learning",
      level: "advanced",
      value: "Revolutionary approach to understanding poi transitions and spatial relationships.",
      status: "active",
      lastUpdated: "2023",
      hasLandingPage: true,
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

    // ACTIVE COMMUNITY PLATFORMS - Current forums and discussion platforms
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

    // JUGGLING-SPECIFIC RESOURCES - Mathematical notation and pure juggling content
    {
      name: "Siteswap Notation System",
      description: "Mathematical notation system for juggling patterns, applicable to flow arts choreography.",
      url: "https://juggle.fandom.com/wiki/Siteswap",
      category: "juggling-specific",
      level: "all",
      value: "Universal language for describing and sharing complex movement patterns.",
      status: "active",
      lastUpdated: "2023",
      modalType: "educational"
    },
    {
      name: "Juggling Lab",
      description: "Popular siteswap generator and animator for creating and visualizing juggling patterns.",
      url: "https://jugglinglab.org/",
      category: "juggling-specific",
      level: "all",
      value: "Essential tool for pattern creation, analysis, and visualization in juggling and flow arts.",
      status: "active",
      lastUpdated: "2023",
      modalType: "educational"
    },
    {
      name: "Siteswap Calculator",
      description: "Web application for validating siteswap patterns and providing useful pattern information.",
      url: "http://www.siteswap.org/",
      category: "juggling-specific",
      level: "intermediate",
      value: "Quick validation and analysis tool for mathematical pattern verification.",
      status: "active",
      lastUpdated: "2019",
      modalType: "educational"
    },
    {
      name: "The Juggling Edge - Siteswap Animator",
      description: "Online siteswap pattern animator and visualization tool for understanding juggling notation.",
      url: "https://www.jugglingedge.com/help/siteswapanimator.php",
      category: "juggling-specific",
      level: "all",
      value: "Visual learning aid for understanding complex siteswap patterns and transitions.",
      status: "active",
      lastUpdated: "2020",
      modalType: "educational"
    },

    // FLOW ARTS VENDORS & EQUIPMENT - Current manufacturers and retailers
    {
      name: "Ninja Pyrate",
      description: "Premium fire props manufacturer specializing in staffs, doubles, and professional fire equipment.",
      url: "https://ninjapyrate.com/",
      category: "vendors",
      level: "all",
      value: "Industry leader in fire safety and professional-grade fire props for performers.",
      status: "vendor",
      foundingYear: 2010,
      companyLocation: "USA",
      specialties: ["Fire Staffs", "Double Staffs", "Fire Safety", "Professional Props"],
      lastUpdated: "2024",
      modalType: "vendor"
    },
    {
      name: "Dark Monk",
      description: "Artisan fire prop manufacturer known for high-quality staffs, swords, and custom fire equipment.",
      url: "https://www.darkmonk.com/",
      category: "vendors",
      level: "all",
      value: "Handcrafted fire props with exceptional build quality and artistic design.",
      status: "vendor",
      foundingYear: 2008,
      companyLocation: "USA",
      specialties: ["Fire Staffs", "Fire Swords", "Custom Props", "Artistic Design"],
      lastUpdated: "2024",
      modalType: "vendor"
    },
    {
      name: "Flowtoys",
      description: "LED and visual poi manufacturer creating innovative programmable and interactive flow props.",
      url: "https://Flowtoys.com/",
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
      name: "Flow On Fire",
      description: "Comprehensive flow arts retailer offering poi, staffs, fans, and fire safety equipment.",
      url: "https://flowonfire.com/",
      category: "vendors",
      level: "all",
      value: "One-stop shop for all flow arts equipment with focus on safety and quality.",
      status: "vendor",
      foundingYear: 2012,
      companyLocation: "USA",
      specialties: ["Poi", "Fire Safety", "Flow Props", "Retail"],
      lastUpdated: "2024",
      modalType: "vendor"
    },
    {
      name: "Home of Poi",
      description: "Long-standing retailer and community hub offering equipment, tutorials, and fire safety resources.",
      url: "https://www.homeofpoi.com/us/",
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

    // HISTORICAL ARCHIVES - Legacy resources with historical significance
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
    { value: 'juggling-specific', label: 'Juggling-Specific Resources' },
    { value: 'vendors', label: 'Flow Arts Vendors & Equipment' },
    { value: 'historical-archives', label: 'Historical Archives' }
  ];

  const levels = [
    { value: 'all', label: 'All Levels' },
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' }
  ];

  function filterResources() {
    filteredResources = resources.filter(resource => {
      const matchesSearch = resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           resource.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }

  onMount(() => {
    filterResources();
  });

  $: {
    searchTerm, selectedCategory;
    filterResources();
  }

  // Modal functions
  function handleLearnMoreClick(event: Event, resource: EnhancedResource) {
    event.preventDefault();
    if (resource.hasLandingPage && resource.landingPageUrl) {
      const resourceName = resource.landingPageUrl.split('/').pop();
      if (resourceName) {
        openResourceModal(resourceName, resource);
      }
    }
  }

  function openResourceModal(resourceName: string, resource: EnhancedResource) {
    modalActions.openModal(resourceName);

    // Set modal data based on resource
    const modalData: ResourceModalData = getModalDataForResource(resourceName, resource);
    modalActions.setModalData(modalData);
  }

  function getModalDataForResource(resourceName: string, resource: EnhancedResource): ResourceModalData {
    // Base data from resource
    const baseData = {
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

    return baseData;
  }

  function getCreatorForResource(resourceName: string, resource: EnhancedResource): string {
    // For vendors, show founding year and location
    if (resource.status === 'vendor') {
      return `Founded ${resource.foundingYear} • ${resource.companyLocation}`;
    }

    // For historical resources, show last updated
    if (resource.status === 'historical') {
      return `Last Updated: ${resource.lastUpdated}`;
    }

    // For educational resources, show specific creators
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
      'juggling-specific': 'Juggling-Specific Resources',
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
            url: "/links/charlie-cushing-9-square-theory",
            description: "Advanced framework building upon VTG principles for connecting unit circles",
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
          }
        ];
      case 'charlie-cushing-9-square-theory':
        return [
          {
            name: "Vulcan Tech Gospel (VTG)",
            url: "/links/vulcan-tech-gospel",
            description: "The foundational theory that 9-square theory builds upon",
            type: 'internal'
          },
          {
            name: "Spin More Poi Advanced Section",
            url: "https://www.spinmorepoi.com/advanced/",
            description: "Charlie Cushing's original 9-square theory documentation",
            type: 'external'
          },
          {
            name: "LanternSmith Poi Resources",
            url: "https://www.lanternsmith.com/poi-resources/",
            description: "Charlie Cushing's equipment and additional learning materials",
            type: 'external'
          }
        ];
      default:
        return [];
    }
  }

  function getHeroGradientForResource(resourceName: string, resource: EnhancedResource): string {
    // Category-based gradients
    switch (resource.category) {
      case 'vendors':
        return 'linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(139, 195, 74, 0.05) 100%)';
      case 'historical-archives':
        return 'linear-gradient(135deg, rgba(158, 158, 158, 0.05) 0%, rgba(117, 117, 117, 0.05) 100%)';
      case 'juggling-specific':
        return 'linear-gradient(135deg, rgba(255, 193, 7, 0.05) 0%, rgba(255, 152, 0, 0.05) 100%)';
      case 'active-community':
        return 'linear-gradient(135deg, rgba(233, 30, 99, 0.05) 0%, rgba(156, 39, 176, 0.05) 100%)';
      default:
        // Specific resource gradients for educational content
        switch (resourceName) {
          case 'vulcan-tech-gospel':
            return 'linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)';
          case 'charlie-cushing-9-square-theory':
            return 'linear-gradient(135deg, rgba(255, 152, 0, 0.05) 0%, rgba(168, 28, 237, 0.05) 100%)';
          default:
            return 'linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)';
        }
    }
  }

  function getCreatorColorForResource(resourceName: string, resource: EnhancedResource): string {
    // Category-based colors
    switch (resource.category) {
      case 'vendors':
        return '#4caf50';
      case 'historical-archives':
        return '#757575';
      case 'juggling-specific':
        return '#ff9800';
      case 'active-community':
        return '#e91e63';
      default:
        // Specific resource colors for educational content
        switch (resourceName) {
          case 'vulcan-tech-gospel':
            return 'var(--primary-color)';
          case 'charlie-cushing-9-square-theory':
            return '#ff9800';
          default:
            return 'var(--primary-color)';
        }
    }
  }

  // Tab navigation functions
  function handleCategoryChange(categoryValue: string) {
    selectedCategory = categoryValue;
  }

  function getResourceCountForCategory(categoryValue: string): number {
    if (categoryValue === 'all') {
      return resources.length;
    }
    return resources.filter(resource => resource.category === categoryValue).length;
  }

  function getTabIndicatorPosition(): number {
    if (typeof document === 'undefined') return 0;

    const activeTab = document.querySelector(`[data-category="${selectedCategory}"]`) as HTMLElement;
    if (!activeTab) return 0;

    const tabsContainer = activeTab.parentElement;
    if (!tabsContainer) return 0;

    return activeTab.offsetLeft;
  }

  function getTabIndicatorWidth(): number {
    if (typeof document === 'undefined') return 0;

    const activeTab = document.querySelector(`[data-category="${selectedCategory}"]`) as HTMLElement;
    if (!activeTab) return 0;

    return activeTab.offsetWidth;
  }
</script>

<svelte:head>
  <title>Flow Arts Historian - The Kinetic Alphabet</title>
  <meta name="description" content="Comprehensive flow arts historian page featuring active learning resources, community platforms, vendor directory, juggling tools, and historical archives preserving flow arts heritage." />
</svelte:head>

<section class="links-section">
  <div class="header">
    <h1>Flow Arts Historian</h1>
    <p class="subtitle">
      Your comprehensive guide to flow arts resources, from cutting-edge learning platforms and active communities
      to essential vendors and historical archives preserving our art form's rich heritage.
    </p>
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

  <!-- Modern Category Navigation -->
  <!-- svelte-ignore a11y-no-noninteractive-element-to-interactive-role -->
  <nav class="category-tabs" role="tablist" aria-label="Resource categories">
    <div class="tab-indicator" style="transform: translateX({getTabIndicatorPosition()}px); width: {getTabIndicatorWidth()}px;"></div>
    {#each categories as category}
      <button
        class="category-tab"
        class:active={selectedCategory === category.value}
        on:click={() => handleCategoryChange(category.value)}
        role="tab"
        aria-selected={selectedCategory === category.value}
        aria-controls="resources-grid"
        tabindex={selectedCategory === category.value ? 0 : -1}
        data-category={category.value}
      >
        <span class="tab-label">{category.label}</span>
        <span class="tab-count">({getResourceCountForCategory(category.value)})</span>
      </button>
    {/each}
  </nav>

  <div class="resources-grid" id="resources-grid">
    {#each filteredResources as resource}
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
            <span class="level-badge level-{resource.level}">
              {levels.find(l => l.value === resource.level)?.label || resource.level}
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
              on:click={(event) => handleLearnMoreClick(event, resource)}
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

  {#if filteredResources.length === 0}
    <div class="no-results">
      <h3>No resources found</h3>
      <p>Try adjusting your search terms or category filter.</p>
    </div>
  {/if}
</section>

<!-- Resource Modal -->
<ResourceModal
  isOpen={isModalOpen}
  onClose={() => modalActions.closeModal()}
>
  {#if currentResourceName === 'vulcan-tech-gospel'}
    <VTGContent />
  {:else if currentResourceName === 'charlie-cushing-9-square-theory'}
    <!-- 9 Square Theory content will be added here -->
    <div class="placeholder-content">
      <p>9 Square Theory content coming soon...</p>
    </div>
  {/if}
</ResourceModal>

<style>
  .links-section {
    width: 100%;
    margin: 0 auto;
    padding: var(--container-padding);
  }

  .header {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
  }

  .header h1 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
  }

  .subtitle {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
  }

  .search-section {
    margin-bottom: var(--spacing-xl);
  }

  .search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto;
  }

  /* Responsive search container */
  @media (min-width: 1200px) {
    .search-container {
      max-width: 600px;
    }
  }

  @media (min-width: 1600px) {
    .search-container {
      max-width: 700px;
    }
  }

  .search-input {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-lg);
    padding-right: 50px;
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    font-size: var(--font-size-base);
    font-weight: 500;

    /* Advanced glassmorphism */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--text-color);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: border-color, box-shadow, background, transform;
  }

  .search-input:focus {
    outline: none;
    border: 2px solid var(--primary-color);
    background: var(--surface-hover);
    box-shadow:
      var(--shadow-glass-hover),
      0 0 0 3px rgba(99, 102, 241, 0.1);
    transform: translateY(-2px) scale(1.01);
  }

  .search-input::placeholder {
    color: var(--text-muted);
    font-weight: 400;
  }

  .search-icon {
    position: absolute;
    right: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    pointer-events: none;
  }

  /* Advanced Glassmorphism Category Tabs */
  .category-tabs {
    position: relative;
    display: flex;

    /* Advanced glassmorphism */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);

    padding: var(--spacing-xs);
    margin-bottom: var(--spacing-2xl);
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;

    /* Enhanced shadows and effects */
    box-shadow: var(--shadow-glass);
    max-width: var(--container-max-width-ultra);
    margin-left: auto;
    margin-right: auto;

    /* Subtle animation */
    animation: fadeInScale 0.8s ease-out;
  }

  /* Full-width tabs for desktop */
  @media (min-width: 1200px) {
    .category-tabs {
      justify-content: space-between;
      overflow-x: visible;
    }

    .category-tab {
      flex: 1;
      max-width: none;
    }
  }

  .category-tabs::-webkit-scrollbar {
    display: none;
  }

  .tab-indicator {
    position: absolute;
    top: var(--spacing-xs);
    bottom: var(--spacing-xs);
    background: var(--gradient-primary);
    border-radius: var(--border-radius);
    box-shadow:
      0 4px 12px var(--shadow-colored),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
    opacity: 0.95;

    /* Cosmic glow effect */
    filter: drop-shadow(0 0 8px rgba(118, 75, 162, 0.4));
  }

  .category-tab {
    position: relative;
    z-index: 2;
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

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, color;
  }

  .category-tab:hover {
    color: var(--text-color);
    transform: translateY(-1px) scale(1.02);
    text-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
  }

  .category-tab.active {
    color: var(--text-inverse);
    font-weight: 600;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }

  .category-tab:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
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

  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--spacing-xl);
    max-width: var(--container-max-width-ultra);
    margin: 0 auto;
  }

  /* Responsive grid columns for optimal desktop utilization */
  @media (min-width: 1200px) and (max-width: 1599px) {
    .resources-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: var(--spacing-xl);
    }
  }

  @media (min-width: 1600px) and (max-width: 1999px) {
    .resources-grid {
      grid-template-columns: repeat(4, 1fr);
      gap: var(--spacing-xl);
    }
  }

  @media (min-width: 2000px) {
    .resources-grid {
      grid-template-columns: repeat(5, 1fr);
      gap: var(--spacing-2xl);
    }
  }

  .resource-card {
    /* Advanced glassmorphism styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
    position: relative;
    overflow: hidden;

    /* Enhanced shadows and transitions */
    box-shadow: var(--shadow-glass);
    transition: all var(--transition-normal);
    will-change: transform, box-shadow, background;

    /* Entrance animation */
    animation: fadeInScale 0.6s ease-out;
  }

  .resource-card:hover {
    transform: translateY(-6px) scale(1.02);
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    box-shadow: var(--shadow-glass-hover);
  }

  /* Cosmic glassmorphism overlay effect */
  .resource-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-cosmic);
    opacity: 0;
    transition: opacity var(--transition-normal);
    pointer-events: none;
    border-radius: var(--border-radius-lg);
  }

  .resource-card:hover::before {
    opacity: 0.03;
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

  .status-indicator {
    font-size: var(--font-size-lg);
    margin-left: var(--spacing-sm);
    opacity: 0.8;
  }

  .status-indicator.status-vendor {
    filter: hue-rotate(120deg);
  }

  .status-indicator.status-historical {
    filter: grayscale(0.3);
  }

  .resource-title a {
    color: var(--text-color);
    text-decoration: none;
    transition: color var(--transition-fast);
  }

  .resource-title a:hover {
    color: var(--primary-color);
  }

  .resource-meta {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .category-badge {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    order: 1; /* Position before level badge */
  }

  .level-badge {
    padding: 2px 6px;
    border-radius: var(--border-radius-sm);
    font-size: 0.65rem;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    opacity: 0.75;
    order: 2; /* Position after category badge */
  }

  .category-active-learning { background: var(--badge-active-learning-bg); color: var(--badge-active-learning-text); }
  .category-active-community { background: var(--badge-community-bg); color: var(--badge-community-text); }
  .category-juggling-specific { background: var(--badge-juggling-bg); color: var(--badge-juggling-text); }
  .category-vendors { background: var(--badge-vendors-bg); color: var(--badge-vendors-text); }
  .category-historical-archives { background: var(--badge-historical-bg); color: var(--badge-historical-text); }

  .level-beginner { background: var(--badge-beginner-bg); color: var(--badge-beginner-text); }
  .level-intermediate { background: var(--badge-intermediate-bg); color: var(--badge-intermediate-text); }
  .level-advanced { background: var(--badge-advanced-bg); color: var(--badge-advanced-text); }
  .level-all { background: var(--badge-all-bg); color: var(--badge-all-text); }

  .founding-badge,
  .last-updated-indicator {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: rgba(158, 158, 158, 0.1);
    color: var(--text-secondary);
    border: 1px solid rgba(158, 158, 158, 0.2);
    opacity: 0.8;
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
    background: var(--badge-vendors-bg);
    color: var(--badge-vendors-text);
    border: 1px solid rgba(76, 175, 80, 0.2);
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 500;
  }

  .resource-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-md);
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

  .learn-more-link {
    display: inline-flex;
    align-items: center;
    padding: var(--spacing-sm) var(--spacing-md);
    position: relative;
    overflow: hidden;

    /* Glassmorphism styling */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--primary-color);
    text-decoration: none;
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    font-weight: 600;
    font-size: var(--font-size-sm);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    cursor: pointer;
    font-family: inherit;
    will-change: transform, background, box-shadow;
  }

  .learn-more-link:hover {
    background: var(--surface-hover);
    border: 2px solid var(--primary-color);
    transform: translateY(-2px) scale(1.02);
    box-shadow: var(--shadow-glass-colored);
    color: var(--primary-light);
  }

  .learn-more-link:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  .visit-link {
    display: inline-flex;
    align-items: center;
    padding: var(--spacing-sm) var(--spacing-md);
    position: relative;
    overflow: hidden;

    /* Primary gradient button */
    background: var(--gradient-primary);
    color: var(--text-inverse);
    text-decoration: none;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-lg);
    font-weight: 600;
    font-size: var(--font-size-sm);
    box-shadow: var(--shadow-glass-colored);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, box-shadow;
  }

  .visit-link:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow:
      0 15px 35px var(--shadow-colored),
      0 5px 15px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    color: var(--text-inverse);
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

  /* Dark mode adjustments are now handled automatically by CSS variables */

  /* Tablet responsive design */
  @media (min-width: 769px) and (max-width: 1199px) {
    .resources-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: var(--spacing-lg);
    }
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .links-section {
      padding: var(--container-padding);
    }

    .search-container {
      max-width: none;
    }

    .category-tabs {
      padding: 4px;
      margin-bottom: var(--spacing-xl);
      justify-content: flex-start;
      overflow-x: auto;
    }

    .category-tab {
      min-width: 100px;
      padding: var(--spacing-xs) var(--spacing-sm);
      flex: none;
    }

    .tab-label {
      font-size: var(--font-size-xs);
    }

    .tab-count {
      font-size: 0.6rem;
    }

    .resources-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-md);
    }

    .resource-card {
      padding: var(--spacing-md);
    }

    .resource-meta {
      justify-content: flex-start;
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
    .category-tab,
    .tab-indicator {
      transition: none;
    }

    .resource-card:hover,
    .visit-link:hover,
    .category-tab:hover,
    .search-input:focus {
      transform: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .resource-card {
      border: 2px solid var(--text-color);
    }

    .resource-card:hover {
      border-color: var(--primary-color);
      border-width: 3px;
    }

    .category-badge,
    .level-badge {
      border: 1px solid currentColor;
    }
  }
</style>
