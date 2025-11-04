<!--
CollectionsExplorePanel.svelte

Collections browser for the Explore module.
Displays user-created collections/playlists of sequences.
-->
<script lang="ts">
  import { onMount } from "svelte";

  // Mock collection data structure (to be replaced with real data)
  interface Collection {
    id: string;
    name: string;
    description: string;
    creator: string;
    creatorId: string;
    sequenceCount: number;
    thumbnail?: string;
    tags: string[];
    isPublic: boolean;
    likeCount: number;
    createdDate: string;
    isLiked?: boolean;
  }

  let collections = $state<Collection[]>([]);
  let isLoading = $state(true);
  let searchQuery = $state("");
  let filterType = $state<"all" | "popular" | "recent">("all");

  // Filtered collections based on search and filter
  const filteredCollections = $derived(() => {
    let filtered = collections;

    // Apply search
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (col) =>
          col.name.toLowerCase().includes(query) ||
          col.description.toLowerCase().includes(query) ||
          col.tags.some((tag) => tag.toLowerCase().includes(query))
      );
    }

    // Apply sorting based on filter type
    if (filterType === "popular") {
      filtered = [...filtered].sort((a, b) => b.likeCount - a.likeCount);
    } else if (filterType === "recent") {
      filtered = [...filtered].sort(
        (a, b) =>
          new Date(b.createdDate).getTime() - new Date(a.createdDate).getTime()
      );
    }

    return filtered;
  });

  onMount(() => {
    // TODO: Replace with actual data fetching
    setTimeout(() => {
      collections = [
        {
          id: "1",
          name: "Beginner Flow Fundamentals",
          description: "Essential sequences for learning the basics",
          creator: "Flow Master",
          creatorId: "1",
          sequenceCount: 12,
          tags: ["beginner", "fundamentals", "basics"],
          isPublic: true,
          likeCount: 245,
          createdDate: "2024-01-15",
        },
        {
          id: "2",
          name: "Advanced Transitions",
          description: "Complex transition sequences for experienced practitioners",
          creator: "Kinetic Artist",
          creatorId: "2",
          sequenceCount: 8,
          tags: ["advanced", "transitions", "technical"],
          isPublic: true,
          likeCount: 187,
          createdDate: "2024-02-20",
        },
        // Add more mock collections
      ];
      isLoading = false;
    }, 500);
  });

  function handleCollectionClick(collection: Collection) {
    console.log("Open collection:", collection.id);
    // TODO: Navigate to collection detail view
  }

  function handleLikeToggle(collection: Collection) {
    console.log("Toggle like for collection:", collection.id);
    // TODO: Implement like/unlike functionality
  }

  function handleFilterChange(newFilter: typeof filterType) {
    filterType = newFilter;
  }
</script>

<div class="collections-explore-panel">
  <!-- Controls bar -->
  <div class="controls-bar">
    <!-- Search -->
    <div class="search-container">
      <i class="fas fa-search search-icon"></i>
      <input
        type="text"
        class="search-input"
        placeholder="Search collections..."
        bind:value={searchQuery}
      />
    </div>

    <!-- Filter buttons -->
    <div class="filter-buttons">
      <button
        class="filter-button"
        class:active={filterType === "all"}
        onclick={() => handleFilterChange("all")}
      >
        All
      </button>
      <button
        class="filter-button"
        class:active={filterType === "popular"}
        onclick={() => handleFilterChange("popular")}
      >
        <i class="fas fa-fire"></i>
        Popular
      </button>
      <button
        class="filter-button"
        class:active={filterType === "recent"}
        onclick={() => handleFilterChange("recent")}
      >
        <i class="fas fa-clock"></i>
        Recent
      </button>
    </div>
  </div>

  <!-- Collections grid -->
  {#if isLoading}
    <div class="loading-state">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading collections...</p>
    </div>
  {:else if filteredCollections().length === 0}
    <div class="empty-state">
      <i class="fas fa-folder-open"></i>
      <p>No collections found</p>
    </div>
  {:else}
    <div class="collections-grid">
      {#each filteredCollections() as collection (collection.id)}
        <div class="collection-card">
          <!-- Thumbnail -->
          <div class="collection-thumbnail">
            {#if collection.thumbnail}
              <img src={collection.thumbnail} alt={collection.name} />
            {:else}
              <div class="thumbnail-placeholder">
                <i class="fas fa-folder"></i>
                <span class="sequence-count">{collection.sequenceCount}</span>
              </div>
            {/if}
          </div>

          <!-- Content -->
          <div class="collection-content">
            <h3 class="collection-name">{collection.name}</h3>
            <p class="collection-description">{collection.description}</p>

            <!-- Creator -->
            <div class="collection-creator">
              <i class="fas fa-user"></i>
              <span>{collection.creator}</span>
            </div>

            <!-- Tags -->
            {#if collection.tags.length > 0}
              <div class="collection-tags">
                {#each collection.tags.slice(0, 3) as tag}
                  <span class="tag">#{tag}</span>
                {/each}
              </div>
            {/if}

            <!-- Stats and actions -->
            <div class="collection-footer">
              <div class="collection-stats">
                <span class="stat">
                  <i class="fas fa-list"></i>
                  {collection.sequenceCount}
                </span>
                <span class="stat">
                  <i class="fas fa-heart"></i>
                  {collection.likeCount}
                </span>
              </div>

              <div class="collection-actions">
                <button
                  class="like-button"
                  class:liked={collection.isLiked}
                  onclick={(e) => {
                    e.stopPropagation();
                    handleLikeToggle(collection);
                  }}
                  aria-label="Like collection"
                >
                  <i class="fas fa-heart"></i>
                </button>
                <button
                  class="view-button"
                  onclick={() => handleCollectionClick(collection)}
                >
                  View
                </button>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .collections-explore-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding: 16px;
    gap: 16px;
  }

  /* Controls bar */
  .controls-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }

  .search-container {
    position: relative;
    flex: 1;
    min-width: 200px;
  }

  .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.5);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: 10px 12px 10px 40px;
    background: var(--input-bg-current);
    border: var(--input-border-current);
    border-radius: 8px;
    color: var(--text-primary-current);
    font-size: 14px;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    background: var(--input-focus-current);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  /* Filter buttons */
  .filter-buttons {
    display: flex;
    gap: 6px;
  }

  .filter-button {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 14px;
    background: var(--panel-bg-current);
    border: var(--panel-border-current);
    border-radius: 8px;
    color: var(--text-secondary-current);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .filter-button:hover {
    background: var(--panel-hover-current);
    border-color: rgba(255, 255, 255, 0.2);
    color: var(--text-primary-current);
  }

  .filter-button.active {
    background: var(--button-active-current);
    border-color: rgba(255, 255, 255, 0.3);
    color: var(--text-primary-current);
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.1);
  }

  /* Loading and empty states */
  .loading-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .loading-state i,
  .empty-state i {
    font-size: 48px;
  }

  /* Collections grid */
  .collections-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    overflow-y: auto;
    padding: 4px;
  }

  /* Collection card */
  .collection-card {
    display: flex;
    flex-direction: column;
    background: var(--card-bg-current);
    border: var(--card-border-current);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: pointer;
  }

  .collection-card:hover {
    background: var(--card-hover-current);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  /* Thumbnail */
  .collection-thumbnail {
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
  }

  .collection-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .thumbnail-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: rgba(255, 255, 255, 0.3);
  }

  .thumbnail-placeholder i {
    font-size: 48px;
  }

  .sequence-count {
    font-size: 14px;
    font-weight: 600;
  }

  /* Content */
  .collection-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 16px;
  }

  .collection-name {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
    line-height: 1.3;
  }

  .collection-description {
    margin: 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .collection-creator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .collection-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .tag {
    padding: 3px 8px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* Footer */
  .collection-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
  }

  .collection-stats {
    display: flex;
    gap: 12px;
  }

  .stat {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .stat i {
    font-size: 11px;
  }

  .collection-actions {
    display: flex;
    gap: 6px;
  }

  .like-button,
  .view-button {
    padding: 6px 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .like-button {
    background: transparent;
    color: rgba(255, 255, 255, 0.5);
  }

  .like-button:hover {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.8);
  }

  .like-button.liked {
    background: rgba(255, 0, 100, 0.15);
    border-color: rgba(255, 0, 100, 0.3);
    color: #ff0064;
  }

  .view-button {
    background: rgba(0, 123, 255, 0.15);
    border-color: rgba(0, 123, 255, 0.3);
    color: #4da3ff;
  }

  .view-button:hover {
    background: rgba(0, 123, 255, 0.25);
    border-color: rgba(0, 123, 255, 0.5);
  }

  /* Responsive design */
  @media (max-width: 480px) {
    .collections-explore-panel {
      padding: 12px;
    }

    .collections-grid {
      grid-template-columns: 1fr;
      gap: 12px;
    }

    .controls-bar {
      flex-direction: column;
    }

    .filter-buttons {
      width: 100%;
      overflow-x: auto;
      scrollbar-width: none;
    }

    .filter-buttons::-webkit-scrollbar {
      display: none;
    }
  }
</style>
