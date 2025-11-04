<!--
SearchExplorePanel.svelte

AI-powered search panel for the Explore module.
Allows natural language queries to find sequences, users, and collections.
-->
<script lang="ts">
  import { onMount } from "svelte";

  interface SearchResult {
    id: string;
    type: "sequence" | "user" | "collection";
    title: string;
    description: string;
    metadata?: any;
    relevance: number;
  }

  let searchQuery = $state("");
  let isSearching = $state(false);
  let searchResults = $state<SearchResult[]>([]);
  let hasSearched = $state(false);
  let searchFilter = $state<"all" | "sequences" | "users" | "collections">(
    "all"
  );

  // Suggested searches for inspiration
  const suggestedSearches = [
    "beginner-friendly sequences",
    "complex transitions",
    "alpha position starts",
    "sequences by FlowMaster",
    "popular collections",
    "3-beat sequences",
  ];

  // Filtered results based on type filter
  const filteredResults = $derived(() => {
    if (searchFilter === "all") return searchResults;
    // Map plural filter names to singular types
    const typeMap: Record<string, SearchResult["type"]> = {
      sequences: "sequence",
      users: "user",
      collections: "collection",
    };
    const targetType = typeMap[searchFilter] || searchFilter;
    return searchResults.filter((result) => result.type === targetType);
  });

  async function handleSearch() {
    if (!searchQuery.trim()) return;

    isSearching = true;
    hasSearched = true;

    // TODO: Implement actual AI-powered search
    // This would integrate with a backend search service or AI model
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Mock search results
    searchResults = [
      {
        id: "1",
        type: "sequence",
        title: "Basic Flow Sequence",
        description: "A simple sequence perfect for beginners",
        relevance: 0.95,
      },
      {
        id: "2",
        type: "user",
        title: "FlowMaster",
        description: "Expert flow artist with 42 sequences",
        relevance: 0.87,
      },
      {
        id: "3",
        type: "collection",
        title: "Beginner Fundamentals",
        description: "Essential sequences for learning the basics",
        relevance: 0.82,
      },
    ];

    isSearching = false;
  }

  function handleSuggestedSearch(suggestion: string) {
    searchQuery = suggestion;
    handleSearch();
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      handleSearch();
    }
  }

  function handleResultClick(result: SearchResult) {
    console.log("Navigate to result:", result);
    // TODO: Navigate to appropriate detail view based on result type
  }

  function getResultIcon(type: SearchResult["type"]): string {
    switch (type) {
      case "sequence":
        return "fa-list";
      case "user":
        return "fa-user";
      case "collection":
        return "fa-folder";
    }
  }

  function getResultTypeLabel(type: SearchResult["type"]): string {
    return type.charAt(0).toUpperCase() + type.slice(1);
  }
</script>

<div class="search-explore-panel">
  <!-- Search header -->
  <div class="search-header">
    <h2 class="search-title">
      <i class="fas fa-search"></i>
      Intelligent Search
    </h2>
    <p class="search-subtitle">
      Use natural language to find sequences, users, and collections
    </p>
  </div>

  <!-- Search input -->
  <div class="search-input-container">
    <i class="fas fa-search search-icon"></i>
    <input
      type="text"
      class="search-input"
      placeholder="Try 'beginner sequences' or 'sequences with alpha start'..."
      bind:value={searchQuery}
      onkeydown={handleKeydown}
    />
    <button
      class="search-button"
      onclick={handleSearch}
      disabled={!searchQuery.trim() || isSearching}
    >
      {#if isSearching}
        <i class="fas fa-spinner fa-spin"></i>
      {:else}
        <i class="fas fa-arrow-right"></i>
      {/if}
    </button>
  </div>

  <!-- Filter tabs -->
  {#if hasSearched}
    <div class="result-filters">
      <button
        class="filter-tab"
        class:active={searchFilter === "all"}
        onclick={() => (searchFilter = "all")}
      >
        All ({searchResults.length})
      </button>
      <button
        class="filter-tab"
        class:active={searchFilter === "sequences"}
        onclick={() => (searchFilter = "sequences")}
      >
        Sequences ({searchResults.filter((r) => r.type === "sequence").length})
      </button>
      <button
        class="filter-tab"
        class:active={searchFilter === "users"}
        onclick={() => (searchFilter = "users")}
      >
        Users ({searchResults.filter((r) => r.type === "user").length})
      </button>
      <button
        class="filter-tab"
        class:active={searchFilter === "collections"}
        onclick={() => (searchFilter = "collections")}
      >
        Collections ({searchResults.filter((r) => r.type === "collection")
          .length})
      </button>
    </div>
  {/if}

  <!-- Content area -->
  <div class="search-content">
    {#if !hasSearched}
      <!-- Suggested searches -->
      <div class="suggestions-container">
        <h3 class="suggestions-title">Try searching for:</h3>
        <div class="suggestions-grid">
          {#each suggestedSearches as suggestion}
            <button
              class="suggestion-chip"
              onclick={() => handleSuggestedSearch(suggestion)}
            >
              <i class="fas fa-lightbulb"></i>
              {suggestion}
            </button>
          {/each}
        </div>

        <!-- AI feature callout -->
        <div class="ai-callout">
          <i class="fas fa-brain"></i>
          <div class="callout-content">
            <strong>Powered by AI</strong>
            <p>
              Our intelligent search understands natural language and context to
              help you find exactly what you're looking for.
            </p>
          </div>
        </div>
      </div>
    {:else if isSearching}
      <!-- Loading state -->
      <div class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Searching...</p>
      </div>
    {:else if filteredResults().length === 0}
      <!-- No results -->
      <div class="empty-state">
        <i class="fas fa-search"></i>
        <h3>No results found</h3>
        <p>
          Try adjusting your search query or browse suggested searches above
        </p>
      </div>
    {:else}
      <!-- Search results -->
      <div class="results-list">
        {#each filteredResults() as result (result.id)}
          <button class="result-item" onclick={() => handleResultClick(result)}>
            <div class="result-icon">
              <i class="fas {getResultIcon(result.type)}"></i>
            </div>
            <div class="result-content">
              <div class="result-header">
                <h4 class="result-title">{result.title}</h4>
                <span class="result-type"
                  >{getResultTypeLabel(result.type)}</span
                >
              </div>
              <p class="result-description">{result.description}</p>
              <div class="result-relevance">
                <div class="relevance-bar">
                  <div
                    class="relevance-fill"
                    style="width: {result.relevance * 100}%"
                  ></div>
                </div>
                <span class="relevance-text"
                  >{Math.round(result.relevance * 100)}% match</span
                >
              </div>
            </div>
            <i class="fas fa-chevron-right result-arrow"></i>
          </button>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .search-explore-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding: 20px;
    gap: 20px;
  }

  /* Header */
  .search-header {
    text-align: center;
  }

  .search-title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }

  .search-subtitle {
    margin: 8px 0 0 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* Search input */
  .search-input-container {
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }

  .search-icon {
    position: absolute;
    left: 16px;
    color: rgba(255, 255, 255, 0.4);
    pointer-events: none;
  }

  .search-input {
    flex: 1;
    padding: 14px 16px 14px 48px;
    background: var(--input-bg-current);
    border: 2px solid var(--input-border-current);
    border-radius: 12px;
    color: var(--text-primary-current);
    font-size: 15px;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    background: var(--input-focus-current);
    border-color: rgba(0, 123, 255, 0.5);
    box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.1);
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  .search-button {
    padding: 14px 20px;
    background: rgba(0, 123, 255, 0.2);
    border: 2px solid rgba(0, 123, 255, 0.4);
    border-radius: 12px;
    color: #4da3ff;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .search-button:hover:not(:disabled) {
    background: rgba(0, 123, 255, 0.3);
    border-color: rgba(0, 123, 255, 0.6);
    transform: translateX(2px);
  }

  .search-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Result filters */
  .result-filters {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    scrollbar-width: none;
    padding: 4px 0;
  }

  .result-filters::-webkit-scrollbar {
    display: none;
  }

  .filter-tab {
    padding: 8px 16px;
    background: var(--panel-bg-current);
    border: var(--panel-border-current);
    border-radius: 20px;
    color: var(--text-secondary-current);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .filter-tab:hover {
    background: var(--panel-hover-current);
    color: var(--text-primary-current);
  }

  .filter-tab.active {
    background: rgba(0, 123, 255, 0.2);
    border-color: rgba(0, 123, 255, 0.4);
    color: white;
  }

  /* Content area */
  .search-content {
    flex: 1;
    overflow-y: auto;
    padding: 4px;
  }

  /* Suggestions */
  .suggestions-container {
    max-width: 800px;
    margin: 0 auto;
  }

  .suggestions-title {
    margin: 0 0 16px 0;
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
  }

  .suggestions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 32px;
  }

  .suggestion-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: var(--card-bg-current);
    border: var(--card-border-current);
    border-radius: 10px;
    color: var(--text-secondary-current);
    font-size: 14px;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .suggestion-chip:hover {
    background: var(--card-hover-current);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .suggestion-chip i {
    color: rgba(255, 193, 7, 0.8);
  }

  /* AI callout */
  .ai-callout {
    display: flex;
    gap: 16px;
    padding: 20px;
    background: linear-gradient(
      135deg,
      rgba(123, 31, 162, 0.15),
      rgba(0, 123, 255, 0.15)
    );
    border: 1px solid rgba(123, 31, 162, 0.3);
    border-radius: 12px;
  }

  .ai-callout i {
    font-size: 32px;
    color: rgba(186, 104, 200, 0.8);
  }

  .callout-content strong {
    display: block;
    margin-bottom: 4px;
    font-size: 16px;
    color: white;
  }

  .callout-content p {
    margin: 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
  }

  /* Loading and empty states */
  .loading-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 60px 20px;
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-state i,
  .empty-state i {
    font-size: 48px;
  }

  .empty-state h3 {
    margin: 0;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.7);
  }

  .empty-state p {
    margin: 0;
    font-size: 14px;
    text-align: center;
  }

  /* Results list */
  .results-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .result-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: var(--card-bg-current);
    border: var(--card-border-current);
    border-radius: 12px;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .result-item:hover {
    background: var(--card-hover-current);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateX(4px);
  }

  .result-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.6);
    flex-shrink: 0;
  }

  .result-content {
    flex: 1;
    min-width: 0;
  }

  .result-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 6px;
  }

  .result-title {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
  }

  .result-type {
    padding: 3px 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
  }

  .result-description {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
  }

  .result-relevance {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .relevance-bar {
    flex: 1;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
  }

  .relevance-fill {
    height: 100%;
    background: linear-gradient(90deg, #00c853, #4da3ff);
    transition: width 0.3s ease;
  }

  .relevance-text {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
    white-space: nowrap;
  }

  .result-arrow {
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
    flex-shrink: 0;
  }

  /* Responsive design */
  @media (max-width: 480px) {
    .search-explore-panel {
      padding: 16px;
      gap: 16px;
    }

    .search-title {
      font-size: 20px;
    }

    .search-subtitle {
      font-size: 13px;
    }

    .search-input {
      font-size: 14px;
      padding: 12px 12px 12px 44px;
    }

    .search-button {
      padding: 12px 16px;
    }

    .suggestions-grid {
      grid-template-columns: 1fr;
    }

    .result-item {
      padding: 12px;
      gap: 12px;
    }

    .result-icon {
      width: 40px;
      height: 40px;
      font-size: 18px;
    }
  }
</style>
