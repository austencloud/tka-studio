<script lang="ts">
  let {
    href,
    icon,
    title,
    description,
    highlight = false,
    onclick = () => {},
  }: {
    href: string;
    icon: string;
    title: string;
    description: string;
    highlight?: boolean;
    onclick?: () => void;
  } = $props();
</script>

<a
  class="dev-card"
  class:discord-highlight={highlight}
  {href}
  target="_blank"
  rel="noopener noreferrer"
  {onclick}
>
  <i class={icon}></i>
  <div>
    <h3>{title}</h3>
    <p>{description}</p>
  </div>
</a>

<style>
  .dev-card {
    display: flex;
    align-items: center;
    gap: clamp(0.5rem, 1.5cqh, 0.625rem);
    padding: clamp(0.5rem, 1.5cqh, 0.625rem) clamp(0.625rem, 1.75cqh, 0.75rem);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(0.375rem, 1.25cqh, 0.5rem);
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    cursor: pointer;
    width: 50%;
    text-align: left;
  }

  /* Hover only on devices that support it (desktop) */
  @media (hover: hover) and (pointer: fine) {
    .dev-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(34, 197, 94, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .discord-highlight:hover {
      border-color: rgba(88, 101, 242, 0.6);
      box-shadow:
        0 8px 16px rgba(0, 0, 0, 0.2),
        0 0 20px rgba(88, 101, 242, 0.3);
    }
  }

  /* Discord highlight styling */
  .discord-highlight {
    background: rgba(88, 101, 242, 0.08);
    border-color: rgba(88, 101, 242, 0.3);
  }

  .discord-highlight i {
    color: rgba(88, 101, 242, 0.9) !important;
  }

  /* Active state - brief feedback that auto-reverts */
  .dev-card:active {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-1px) scale(0.98);
    transition-duration: 0.05s;
  }

  .dev-card:focus-visible {
    outline: 2px solid rgba(34, 197, 94, 0.7);
    outline-offset: 2px;
  }

  .dev-card i {
    font-size: clamp(1.25rem, 3.5cqh, 1.75rem);
    color: rgba(34, 197, 94, 0.9);
    flex-shrink: 0;
  }

  .dev-card div {
    flex: 1;
    min-width: 0;
  }

  .dev-card h3 {
    font-size: clamp(0.6875rem, 1.75cqh, 0.8125rem);
    font-weight: 600;
    color: white;
    margin: 0 0 0.125rem 0;
    line-height: 1.2;
  }

  .dev-card p {
    font-size: clamp(0.625rem, 1.5cqh, 0.75rem);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.25;
  }

  @media (prefers-reduced-motion: reduce) {
    .dev-card:hover,
    .dev-card:active {
      transform: none;
    }
  }
</style>
