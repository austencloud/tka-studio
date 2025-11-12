<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import type { InfoDevContent } from "../domain";
  import DevCard from "./DevCard.svelte";

  let {
    panelId,
    labelledBy,
    copy,
    githubUrl,
    discordUrl,
    contactEmail,
  }: {
    panelId: string;
    labelledBy: string;
    copy: InfoDevContent;
    githubUrl: string;
    discordUrl: string;
    contactEmail: string;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleLinkClick() {
    hapticService?.trigger("selection");
  }
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div class="tab-panel" role="tabpanel" aria-labelledby={labelledBy}>
    <h2 class="panel-title">{copy.subtitle}</h2>
    <p class="dev-message">{copy.message}</p>
    <div class="dev-links">
      <DevCard
        href={discordUrl}
        icon="fab fa-discord"
        title="Join Our Discord Community"
        description="Get help, share feedback, and chat directly with the developer"
        highlight={true}
        onclick={handleLinkClick}
      />

      <DevCard
        href={githubUrl}
        icon="fab fa-github"
        title="View on GitHub"
        description="Explore the source code and contribute"
        onclick={handleLinkClick}
      />

      <DevCard
        href={`${githubUrl}/issues/new`}
        icon="fas fa-bug"
        title="Report Bug or Request Feature"
        description="Help improve TKA with your feedback"
        onclick={handleLinkClick}
      />
    </div>
  </div>
</div>

<style>
  .carousel-panel {
    display: flex;
    flex-direction: column;
  }

  .tab-panel {
    display: flex;
    flex-direction: column;
    padding: clamp(0.5rem, 1vh, 0.75rem);
  }

  @media (min-width: 1024px) {
    .tab-panel {
      padding: 0;
    }
  }

  .panel-title {
    font-size: clamp(0.75rem, 2cqh, 0.875rem);
    margin-bottom: clamp(0.25rem, 1cqh, 0.375rem);
  }

  @media (min-width: 1024px) {
    .panel-title {
      display: none;
    }
  }

  .dev-message {
    font-size: clamp(0.625rem, 1.5cqh, 0.75rem);
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: clamp(0.25rem, 1cqh, 0.375rem);
    line-height: 1.25;
    text-align: center;
    flex-shrink: 0;
  }

  .dev-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(0.625rem, 2cqh, 1rem);
    width: 100%;
    flex: 1;
    justify-content: center;
  }

  @media (min-width: 1024px) {
    .dev-links {
      flex: 1;
      justify-content: center;
    }
  }

</style>
