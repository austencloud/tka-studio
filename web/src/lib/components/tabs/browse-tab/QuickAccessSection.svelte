<script lang="ts">
  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const { onQuickAccess = () => {} } = $props<{
    onQuickAccess?: (data: { type: string; value: string }) => void;
  }>();

  // Quick access filter options matching desktop app
  const quickFilters = [
    {
      label: "⭐ My Favorites",
      type: "favorites",
      value: "favorites",
      color: "#FFD700",
      description: "Your starred sequences",
    },
    {
      label: "🔥 Recently Added",
      type: "recent",
      value: "recent",
      color: "#FF6B6B",
      description: "Recently added sequences",
    },
    {
      label: "📊 All Sequences",
      type: "all_sequences",
      value: "all",
      color: "#4ECDC4",
      description: "Browse all sequences",
    },
  ];

  function handleQuickAccess(filter: { type: string; value: string }) {
    onQuickAccess({
      type: filter.type,
      value: filter.value,
    });
  }
</script>

<div class="quick-access-section">
  {#each quickFilters as filter}
    <button
      class="quick-button"
      style="--accent-color: {filter.color}"
      onclick={() => handleQuickAccess(filter)}
      title={filter.description}
      type="button"
    >
      {filter.label}
    </button>
  {/each}
</div>

<style>
  .quick-access-section {
    display: flex;
    gap: 12px;
  }

  .quick-button {
    min-height: 60px;
    min-width: 180px;
    max-width: 400px;

    background: rgba(255, 255, 255, 0.12);
    border: 2px solid rgba(255, 255, 255, 0.4);
    border-radius: 14px;
    color: white;
    font-weight: bold;
    font-size: 16px;
    padding: 18px 32px;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-fast);
    font-family: inherit;
  }

  .quick-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.5);
  }

  .quick-button:active {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .quick-access-section {
      gap: 8px;
    }

    .quick-button {
      min-width: 140px;
      padding: 12px 20px;
      font-size: 14px;
    }
  }

  @media (max-width: 480px) {
    .quick-button {
      min-width: 100px;
      padding: 8px 12px;
      font-size: 12px;
    }
  }
</style>
