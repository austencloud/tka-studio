import { createStore } from "../core/index.js";

// Resize observer composable
export function useResizeObserver() {
  // Create a reactive store for size
  const sizeStore = createStore({
    width: 0,
    height: 0,
  });

  // Svelte action for resize observer
  function resizeObserver(element) {
    if (typeof ResizeObserver !== "undefined") {
      const observer = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          sizeStore.update(() => ({ width, height }));
        }
      });

      observer.observe(element);

      return {
        destroy() {
          observer.disconnect();
        },
      };
    }

    return {
      destroy() {},
    };
  }

  return {
    size: sizeStore,
    resizeObserver,
    // Legacy observe method for backward compatibility
    observe: (element, callback) => {
      if (typeof ResizeObserver !== "undefined") {
        const observer = new ResizeObserver(callback);
        observer.observe(element);
        return () => observer.disconnect();
      }
      return () => {};
    },
  };
}
