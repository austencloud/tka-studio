// src/lib/actions/resizeObserver.ts
export function resizeObserver(
    node: HTMLElement,
    callback: (width: number, height: number) => void
  ) {
    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        callback(width, height);
      }
    });
    ro.observe(node);
  
    return {
      destroy() {
        ro.unobserve(node);
      },
    };
  }
  