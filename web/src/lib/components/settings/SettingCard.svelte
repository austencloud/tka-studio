<!-- SettingCard.svelte - Improved contrast card container -->
<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    title?: string;
    description?: string;
    children: Snippet;
  }

  let { title, description, children }: Props = $props();
</script>

<div class="setting-section">
  {#if title}
    <h3 class="section-title">{title}</h3>
  {/if}
  {#if description}
    <p class="section-description">{description}</p>
  {/if}

  <div class="setting-cards">
    {@render children()}
  </div>
</div>

<style>
  .setting-section {
    margin-bottom: clamp(16px, 2vw, 32px);
    container-type: inline-size;
  }

  .section-title {
    margin: 0 0 clamp(8px, 1vw, 16px) 0;
    font-size: clamp(16px, 1.6vw, 20px);
    font-weight: 600;
    color: #ffffff;
  }

  .section-description {
    margin: 0 0 clamp(12px, 1.5vw, 24px) 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: clamp(12px, 1.2vw, 16px);
    line-height: 1.4;
  }

  .setting-cards {
    display: flex;
    flex-direction: column;
    gap: clamp(8px, 1vw, 16px);
  }

  /* Container queries for setting cards layout */
  @container (min-width: 600px) {
    .setting-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: clamp(12px, 1.5vw, 24px);
    }
  }
</style>
