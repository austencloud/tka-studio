<!--
  AuthHeader.svelte - Authentication Sheet Header

  Header with dynamic title/subtitle based on auth mode and close button
-->
<script lang="ts">
  // Props
  let { mode = "signin", onClose } = $props<{
    mode: "signin" | "signup";
    onClose: () => void;
  }>();
</script>

<header class="auth-header">
  <div class="auth-header__content">
    <h2 id="auth-sheet-title" class="auth-header__title">
      {mode === "signin" ? "Welcome to TKA" : "Create Your Account"}
    </h2>
    <p class="auth-header__subtitle">
      {mode === "signin"
        ? "Sign in to access your library and track your progress"
        : "Join TKA to save your progress and access your library"}
    </p>
  </div>
  <button
    class="auth-header__close"
    onclick={onClose}
    aria-label={mode === "signin" ? "Close sign in" : "Close sign up"}
  >
    <i class="fas fa-times"></i>
  </button>
</header>

<style>
  .auth-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .auth-header__content {
    flex: 1;
    min-width: 0;
  }

  .auth-header__title {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0 0 8px 0;
  }

  .auth-header__subtitle {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    line-height: 1.5;
  }

  .auth-header__close {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-left: 16px;
  }

  .auth-header__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .auth-header__close:active {
    transform: scale(0.95);
  }

  .auth-header__close:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     RESPONSIVE DESIGN
     ============================================================================ */
  @media (max-width: 480px) {
    .auth-header {
      padding: 16px;
    }

    .auth-header__title {
      font-size: 20px;
    }

    .auth-header__subtitle {
      font-size: 13px;
    }
  }

  /* iPhone SE 2/3 and similar (667px height) */
  @media (max-height: 700px) {
    .auth-header {
      padding: 8px 16px;
    }

    .auth-header__title {
      font-size: 19px;
      margin-bottom: 4px;
    }

    .auth-header__subtitle {
      font-size: 12.5px;
    }
  }

  /* Small screens */
  @media (max-height: 600px) {
    .auth-header {
      padding: 10px 14px;
    }

    .auth-header__title {
      font-size: 18px;
      margin-bottom: 4px;
    }

    .auth-header__subtitle {
      font-size: 12px;
    }
  }

  /* iPhone SE 1st gen and very small devices (568px height) */
  @media (max-height: 568px) {
    .auth-header {
      padding: 8px 12px;
    }

    .auth-header__title {
      font-size: 17px;
      margin-bottom: 0;
    }

    /* Hide subtitle on very small screens */
    .auth-header__subtitle {
      display: none;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .auth-header__close {
      transition: none;
    }

    .auth-header__close:hover,
    .auth-header__close:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .auth-header {
      border-color: white;
    }
  }
</style>
