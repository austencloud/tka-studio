<script lang="ts">
  /**
   * User Menu Component
   *
   * Displays user avatar and provides logout functionality
   */

  import { user, authStore } from "../stores/authStore";

  let {
    class: className = "",
  }: {
    class?: string;
  } = $props();

  let showMenu = $state(false);
  let loading = $state(false);

  async function handleLogout() {
    loading = true;
    try {
      await authStore.signOut();
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      loading = false;
      showMenu = false;
    }
  }

  function toggleMenu() {
    showMenu = !showMenu;
  }

  function closeMenu() {
    showMenu = false;
  }

  // Get user initials for avatar
  const userInitials = $derived(() => {
    if (!$user) return "?";
    const name = $user.displayName || $user.email || "User";
    return name
      .split(" ")
      .map((n: string) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  });

  // Get user display name
  const displayName = $derived($user?.displayName || $user?.email || "User");

  // Get user avatar URL
  const avatarUrl = $derived($user?.photoURL);
</script>

<div class="user-menu {className}">
  <button
    onclick={toggleMenu}
    class="avatar-button"
    aria-label="User menu"
    aria-expanded={showMenu}
  >
    {#if avatarUrl}
      <img src={avatarUrl} alt={displayName} class="avatar-image" />
    {:else}
      <div class="avatar-fallback">
        {userInitials()}
      </div>
    {/if}
  </button>

  {#if showMenu}
    <div class="menu-backdrop" onclick={closeMenu}></div>
    <div class="menu-dropdown">
      <div class="menu-header">
        <p class="user-name">{displayName}</p>
        <p class="user-email">{$user?.email || ""}</p>
      </div>

      <div class="menu-divider"></div>

      <button onclick={handleLogout} disabled={loading} class="logout-button">
        {#if loading}
          <span class="spinner"></span>
        {/if}
        Sign Out
      </button>
    </div>
  {/if}
</div>

<style>
  .user-menu {
    position: relative;
  }

  .avatar-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid transparent;
    padding: 0;
    cursor: pointer;
    transition: all 0.2s ease;
    background: transparent;
  }

  .avatar-button:hover {
    border-color: var(--accent-color, #3b82f6);
    transform: scale(1.05);
  }

  .avatar-image {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }

  .avatar-fallback {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
  }

  .menu-backdrop {
    position: fixed;
    inset: 0;
    z-index: 40;
  }

  .menu-dropdown {
    position: absolute;
    right: 0;
    top: calc(100% + 0.5rem);
    min-width: 200px;
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    z-index: 50;
    overflow: hidden;
    animation: slideIn 0.2s ease;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .menu-header {
    padding: 1rem;
  }

  .user-name {
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 0.25rem 0;
    font-size: 0.875rem;
  }

  .user-email {
    color: #6b7280;
    margin: 0;
    font-size: 0.75rem;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .menu-divider {
    height: 1px;
    background: #e5e7eb;
  }

  .logout-button {
    width: 100%;
    padding: 0.75rem 1rem;
    text-align: left;
    background: transparent;
    border: none;
    color: #ef4444;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
  }

  .logout-button:hover {
    background: #fef2f2;
  }

  .logout-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .spinner {
    display: inline-block;
    width: 0.875rem;
    height: 0.875rem;
    border: 2px solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .menu-dropdown {
      background: #1f2937;
    }

    .user-name {
      color: #f9fafb;
    }

    .user-email {
      color: #9ca3af;
    }

    .menu-divider {
      background: #374151;
    }

    .logout-button:hover {
      background: #374151;
    }
  }
</style>
