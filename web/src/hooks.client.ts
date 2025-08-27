/**
 * SvelteKit Client Hooks
 *
 * This file handles client-side initialization.
 * The InversifyJS container is self-initializing when imported.
 */

import "reflect-metadata";

/**
 * Initialize the application on the client side
 */
async function initializeClient() {
  try {
    console.log("🚀 Initializing TKA client application...");

    // The InversifyJS container is self-initializing when imported by the layout
    // No need to explicitly initialize it here to avoid circular dependencies

    console.log("✅ TKA client application initialized successfully");
  } catch (error) {
    console.error("❌ Failed to initialize TKA client application:", error);
    throw error;
  }
}

// Initialize when the module loads
initializeClient().catch((error) => {
  console.error("❌ Critical error during client initialization:", error);
});

// Export for potential use in other parts of the application
export { initializeClient };
