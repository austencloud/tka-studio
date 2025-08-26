<script lang="ts">
  import type { ResourceModalData } from "$lib/components/resource-guide/types";
  import { createModalState } from "$lib/state/modal-state.svelte";
  import ResourceModal from "$lib/components/resource-guide/ResourceModal.svelte";
  import VTGContent from "$lib/components/resource-guide/content/VTGContent.svelte";

  // Import new sub-components
  import ResourceFilters from "./resources/ResourceFilters.svelte";
  import ResourceGrid from "./resources/ResourceGrid.svelte";
  import {
    resources,
    categories,
    type Resource,
    getCategoryDisplayName,
    getLevelDisplayName,
  } from "./resources/resourcesData";

  // State
  let searchTerm = $state("");
  let selectedCategory = $state("all");
  let selectedLevel = $state("all");

  // Modal state
  const modalState = createModalState();

  // Computed filtered resources
  let filteredResources = $derived.by(() => {
    return resources.filter((resource) => {
      const matchesSearch =
        searchTerm === "" ||
        resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        resource.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (resource.specialties &&
          resource.specialties.some((s) =>
            s.toLowerCase().includes(searchTerm.toLowerCase())
          ));
      const matchesCategory =
        selectedCategory === "all" || resource.category === selectedCategory;
      const matchesLevel =
        selectedLevel === "all" || resource.level === selectedLevel;
      return matchesSearch && matchesCategory && matchesLevel;
    });
  });

  // Modal handlers
  function handleOpenModal(resource: Resource) {
    if (resource.hasLandingPage && resource.landingPageUrl) {
      const resourceName = resource.landingPageUrl.split("/").pop();
      if (resourceName) {
        openResourceModal(resourceName, resource);
      }
    }
  }

  function openResourceModal(resourceName: string, resource: Resource) {
    modalState.openModal(resourceName);

    const modalData: ResourceModalData = getModalDataForResource(
      resourceName,
      resource
    );
    modalState.setModalData(modalData);
  }

  function getModalDataForResource(
    resourceName: string,
    resource: Resource
  ): ResourceModalData {
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
      creatorColor: getCreatorColorForResource(resourceName, resource),
    };
  }

  function getCreatorForResource(
    resourceName: string,
    resource: Resource
  ): string {
    if (resource.status === "vendor") {
      return `Founded ${resource.foundingYear} • ${resource.companyLocation}`;
    }
    if (resource.status === "historical") {
      return `Last Updated: ${resource.lastUpdated}`;
    }
    switch (resourceName) {
      case "vulcan-tech-gospel":
        return "Noel Yee";
      case "charlie-cushing-9-square-theory":
        return "Charlie Cushing";
      default:
        return "Community Resource";
    }
  }

  function getKeywordsForResource(resourceName: string): string {
    switch (resourceName) {
      case "vulcan-tech-gospel":
        return "Vulcan Tech Gospel, VTG, poi theory, Noel Yee, poi flowers, transition theory, technical poi, flow arts theory";
      case "charlie-cushing-9-square-theory":
        return "9 square theory, Charlie Cushing, poi theory, unit circles, technical poi, helicopter pilot, LanternSmith, advanced poi, spatial relationships";
      default:
        return "flow arts, poi, theory, tutorial";
    }
  }

  function getTableOfContentsForResource(
    resourceName: string
  ): Array<{ id: string; label: string }> {
    switch (resourceName) {
      case "vulcan-tech-gospel":
        return [
          { id: "overview", label: "Overview" },
          { id: "key-concepts", label: "Key Concepts" },
          { id: "getting-started", label: "Getting Started" },
          { id: "advanced-applications", label: "Advanced Applications" },
          { id: "community-impact", label: "Community Impact" },
          { id: "official-resources", label: "Official Resources" },
        ];
      case "charlie-cushing-9-square-theory":
        return [
          { id: "overview", label: "Overview" },
          { id: "creator-background", label: "Creator Background" },
          { id: "key-concepts", label: "Key Concepts" },
          { id: "getting-started", label: "Getting Started" },
          { id: "advanced-applications", label: "Advanced Applications" },
          { id: "official-resources", label: "Official Resources" },
        ];
      default:
        return [];
    }
  }

  function getRelatedResourcesForResource(resourceName: string): Array<{
    name: string;
    url: string;
    description: string;
    type: "internal" | "external";
  }> {
    switch (resourceName) {
      case "vulcan-tech-gospel":
        return [
          {
            name: "Charlie Cushing's 9 Square Theory",
            url: "/about#charlie-cushing-9-square-theory",
            description:
              "Advanced framework building upon VTG principles for connecting unit circles",
            type: "internal",
          },
          {
            name: "Noel Yee's Official VTG Resources",
            url: "https://noelyee.com/instruction/vulcan-tech-gospel/",
            description:
              "Original VTG documentation and tutorials by the creator",
            type: "external",
          },
        ];
      default:
        return [];
    }
  }

  function getHeroGradientForResource(
    resourceName: string,
    resource: Resource
  ): string {
    switch (resource.category) {
      case "vendors":
        return "linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(139, 195, 74, 0.05) 100%)";
      case "historical-archives":
        return "linear-gradient(135deg, rgba(158, 158, 158, 0.05) 0%, rgba(117, 117, 117, 0.05) 100%)";
      default:
        return "linear-gradient(135deg, rgba(168, 28, 237, 0.05) 0%, rgba(74, 144, 226, 0.05) 100%)";
    }
  }

  function getCreatorColorForResource(
    resourceName: string,
    resource: Resource
  ): string {
    switch (resource.category) {
      case "vendors":
        return "#4caf50";
      case "historical-archives":
        return "#757575";
      default:
        return "var(--primary-color)";
    }
  }
</script>

<!-- Resources & Links Section -->
<section class="resources-links">
  <div class="container">
    <h2>Flow Arts Historian</h2>
    <p class="subtitle">
      Your comprehensive guide to flow arts resources, from cutting-edge
      learning platforms and active communities to essential vendors and
      historical archives preserving our art form's rich heritage.
    </p>

    <ResourceFilters bind:searchTerm bind:selectedCategory bind:selectedLevel />

    <ResourceGrid resources={filteredResources} onOpenModal={handleOpenModal} />
  </div>
</section>

<!-- Resource Modal -->
<ResourceModal
  isOpen={modalState.isOpen}
  modalData={modalState.modalData}
  onClose={() => modalState.closeModal()}
>
  {#if modalState.resourceName === "vulcan-tech-gospel"}
    <VTGContent />
  {:else if modalState.resourceName === "charlie-cushing-9-square-theory"}
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

  .placeholder-content {
    padding: var(--spacing-xl);
    text-align: center;
    color: var(--color-text-secondary);
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
  }
</style>
