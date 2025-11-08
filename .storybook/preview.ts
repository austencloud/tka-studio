import type { Preview } from "@storybook/svelte-vite";

// Mock import.meta.env for Storybook
if (typeof window !== 'undefined') {
  (window as any).import = {
    meta: {
      env: {
        MODE: 'development',
        DEV: true,
        PROD: false,
        SSR: false,
      }
    }
  };
}

// Mock the DI container's resolve function
const mockServices = {
  IHapticFeedbackService: {
    trigger: (type: string) => console.log('Haptic:', type)
  },
  IDeviceDetector: {
    isMobile: () => false,
    isTablet: () => false,
    isDesktop: () => true,
    isMobilePortrait: () => false,
  }
};

// Create a global mock resolve function
(window as any).__mockResolve = (typeSymbol: symbol) => {
  const serviceName = typeSymbol.toString();
  if (serviceName.includes('IHapticFeedbackService')) {
    return mockServices.IHapticFeedbackService;
  }
  if (serviceName.includes('IDeviceDetector')) {
    return mockServices.IDeviceDetector;
  }
  return {};
};

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },

    a11y: {
      // 'todo' - show a11y violations in the test UI only
      // 'error' - fail CI on a11y violations
      // 'off' - skip a11y checks entirely
      test: "todo",
    },
  },
};

export default preview;
