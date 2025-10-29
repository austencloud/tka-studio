<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import type { ModuleId } from "../domain/types";

  // Service resolution - resolve synchronously to avoid timing issues
  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  let {
    currentModule,
    currentModuleName,
    isOpen = false,
    onHover,
    onMouseLeave,
    onClick,
    isDisabled = false,
  } = $props<{
    currentModule: ModuleId;
    currentModuleName: string;
    isOpen?: boolean;
    onHover?: () => void;
    onMouseLeave?: () => void;
    onClick?: () => void;
    isDisabled?: boolean;
  }>();

  // Handle keyboard interaction
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      hapticService?.trigger("navigation");
      onClick?.();
    }
  }

  // Handle click with haptic feedback
  function handleClick() {
    hapticService?.trigger("navigation");
    onClick?.();
  }
</script>

<!-- Hamburger Menu Button with Module Name -->
<button
  class="hamburger-menu-button"
  class:open={isOpen}
  class:disabled={isDisabled}
  onclick={handleClick}
  onmouseenter={onHover}
  onmouseleave={onMouseLeave}
  onkeydown={handleKeydown}
  disabled={isDisabled}
  aria-expanded={isOpen}
  aria-haspopup="menu"
  aria-label="Current module: {currentModuleName}. Select to change modules"
  title="Current module: {currentModuleName}. Click to change modules"
>
  <!-- Hamburger Icon -->
  <div class="hamburger-icon" aria-hidden="true">
    <span class="hamburger-line"></span>
    <span class="hamburger-line"></span>
    <span class="hamburger-line"></span>
  </div>

  <!-- Current Module Name -->
  <span class="module-name">{currentModuleName}</span>

  <!-- Visual Divider -->
</button>

<style>
  .hamburger-menu-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: 0 var(--spacing-md); /* Remove vertical padding for full-height touch target */
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--foreground);
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-sm);
    font-weight: 500;
    height: 100%; /* Fill full navigation bar height */
    user-select: none;
  }

  .hamburger-menu-button:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .hamburger-menu-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  .hamburger-menu-button.open {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.3);
  }

  .hamburger-menu-button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  .hamburger-icon {
    display: flex;
    flex-direction: column;
    gap: 3px;
    width: 18px;
    height: 14px;
    flex-shrink: 0;
  }

  .hamburger-line {
    width: 100%;
    height: 2px;
    background: currentColor;
    border-radius: 1px;
    transition: all var(--transition-fast);
  }

  .hamburger-menu-button.open .hamburger-line:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }

  .hamburger-menu-button.open .hamburger-line:nth-child(2) {
    opacity: 0;
  }

  .hamburger-menu-button.open .hamburger-line:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
  }

  .module-name {
    font-weight: 500;
    color: var(--muted-foreground);
    transition: color var(--transition-fast);
    white-space: nowrap;
  }

  .hamburger-menu-button:hover .module-name {
    color: var(--foreground);
  }

  .hamburger-menu-button.open .module-name {
    color: var(--primary-light);
  }

  /* Mobile responsive - hide module name on mobile, show icon only */
  @media (max-width: 768px) {
    .hamburger-menu-button {
      width: 48px;
      height: 48px;
      padding: var(--spacing-xs);
      justify-content: center;
      min-height: unset;
    }

    .module-name {
      display: none;
    }
  }

  /* Left navigation layout - icon only, no label */
  :global(.layout-left) .hamburger-menu-button {
    width: 48px;
    height: 48px;
    padding: var(--spacing-xs);
    justify-content: center;
    min-height: unset;
  }

  :global(.layout-left) .module-name {
    display: none;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .hamburger-menu-button,
    .hamburger-line,
    .module-name {
      transition: none;
    }

    .hamburger-menu-button:hover {
      transform: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .hamburger-menu-button {
      border: 2px solid rgba(255, 255, 255, 0.5);
    }

    .hamburger-menu-button:hover {
      border-color: white;
    }

    .hamburger-menu-button.open {
      border-color: var(--primary-light, #818cf8);
    }
  }
</style>
